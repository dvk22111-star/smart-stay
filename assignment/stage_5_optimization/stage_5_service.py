class Stage5OptimizationService:

    def __init__(
        self,
        score_calculator,
        room_score_calculator,
        objective_builder
    ):

        self.score_calculator = (
            score_calculator
        )

        self.room_score_calculator = (
            room_score_calculator
        )

        self.objective_builder = (
            objective_builder
        )

    def execute(
        self,
        context
    ):

        room_scores = {}
        assignment_bonus = {}

        # בניית דירוג רישום על בסיס תאריך עדכון,
        # כך שאם אין מקום לכולם יתקבל פתרון שמעדיף משתמשים שנרשמו קודם.
        registration_order = {
            vc.UserID: idx
            for idx, vc in enumerate(
                sorted(
                    context.vacation_customers,
                    key=lambda vc: (vc.UpdateDate, vc.VacationIDForCustomers)
                )
            )
        }

        total_users = len(context.users)
        base_weight = 1000

        for user in context.users:

            user_preferences = [
                p
                for p in context.customer_preferences
                if p.UserID == user.UserID
            ]

            registration_bonus = 0
            if user.UserID in registration_order:
                registration_bonus = (
                    total_users - registration_order[user.UserID]
                ) * base_weight

            assignment_bonus[user.UserID] = registration_bonus

            for room in context.rooms:

                room_preferences = [
                    rp.IDPreferences
                    for rp in context.room_preferences
                    if rp.RoomID == room.RoomID
                ]

                score = (
                    self.room_score_calculator
                    .calculate(
                        user_preferences,
                        room_preferences,
                        self.score_calculator
                    )
                )

                room_scores[
                    (
                        user.UserID,
                        room.RoomID
                    )
                ] = score

        max_room_score = max(room_scores.values(), default=0)
        group_room_bonus, group_target_floors = self._build_group_room_bonus(context, max_room_score)

        # apply group floor restrictions as hard constraints
        self._apply_group_floor_constraints(context, group_target_floors)

        # store last group debug info and group_room_bonus into context for inspection
        context.group_debug = getattr(self, '_last_group_debug', [])
        context.group_room_bonus = group_room_bonus
        context.group_target_floors = group_target_floors

        room_used_flags = getattr(context, 'room_used', None)
        room_full_flags = getattr(context, 'room_full', None)

        self.objective_builder.build(
            context.model,
            context.variables,
            context.assigned_users,
            context.users,
            context.rooms,
            room_scores,
            assignment_bonus,
            group_room_bonus=group_room_bonus,
            partner_requests=context.partner_requests,
            room_used=room_used_flags,
            room_full=room_full_flags,
            max_room_score=max_room_score
        )

        return context

    def _build_group_room_bonus(self, context, max_room_score):
        def normalize_phone(phone):
            return (
                ''.join(ch for ch in phone if ch.isdigit())
                if phone else ""
            )

        user_by_phone = {
            normalize_phone(user.Phone): user.UserID
            for user in context.users
            if getattr(user, 'Phone', None)
        }

        room_capacity_by_floor = {}
        rooms_by_floor = {}
        for room in context.rooms:
            floor = getattr(room, 'Floor', 0)
            rooms_by_floor.setdefault(floor, []).append(room)
            room_capacity_by_floor[floor] = (
                room_capacity_by_floor.get(floor, 0)
                + getattr(room, 'NumberOfBeds', 0)
            )

        group_room_bonus = {}

        valid_user_ids = {user.UserID for user in context.users}

        groups = []
        for group in context.groups:
            member_ids = set()
            if getattr(group, 'UserID', None) in valid_user_ids:
                member_ids.add(group.UserID)

            for member in context.group_members:
                if getattr(member, 'GroupID', None) != getattr(group, 'GroupID', None):
                    continue

                normalized_phone = normalize_phone(getattr(member, 'Telephone', ""))
                user_id = user_by_phone.get(normalized_phone)
                if user_id is not None:
                    member_ids.add(user_id)
                else:
                    # try matching by user id directly if stored as numeric string
                    telephone = getattr(member, 'Telephone', "")
                    if telephone.isdigit():
                        possible_id = int(telephone)
                        if possible_id in valid_user_ids:
                            member_ids.add(possible_id)

            if len(member_ids) <= 1:
                continue

            groups.append({
                'group': group,
                'member_ids': sorted(member_ids),
                'registered_count': len(member_ids),
                'expected_size': max(
                    len(member_ids),
                    getattr(group, 'NumberofParticipants', len(member_ids)) or len(member_ids)
                )
            })

        if not groups:
            return group_room_bonus, {}

        groups.sort(key=lambda item: item['registered_count'], reverse=True)

        group_target_floors = {}
        for item in groups:
            group = item['group']
            registered_count = item['registered_count']
            expected_size = item['expected_size']

            # collect debug info per group
            if not hasattr(self, '_last_group_debug'):
                self._last_group_debug = []

            target_floors = self._choose_group_floor_segment(
                expected_size,
                room_capacity_by_floor
            )
            group_target_floors[getattr(group, 'GroupID', None)] = target_floors

            group_debug_entry = {
                'group_id': getattr(group, 'GroupID', None),
                'member_ids': item['member_ids'],
                'expected_size': expected_size,
                'chosen_floors': target_floors,
                'floor_capacity_before': {f: room_capacity_by_floor.get(f, 0) for f in target_floors}
            }

            if not target_floors:
                self._last_group_debug.append(group_debug_entry)
                continue

            self._reserve_group_capacity(
                expected_size,
                target_floors,
                room_capacity_by_floor
            )

            # record capacity after reservation
            group_debug_entry['floor_capacity_after'] = {f: room_capacity_by_floor.get(f, 0) for f in target_floors}
            self._last_group_debug.append(group_debug_entry)

            for user_id in item['member_ids']:
                for room in context.rooms:
                    bonus = self._room_group_floor_bonus(
                        room,
                        target_floors,
                        max_room_score
                    )
                    if bonus:
                        key = (user_id, room.RoomID)
                        group_room_bonus[key] = (
                            group_room_bonus.get(key, 0) + bonus
                        )

        return group_room_bonus, group_target_floors

    def _choose_group_floor_segment(self, expected_size, room_capacity_by_floor):
        floors = [floor for floor, cap in room_capacity_by_floor.items() if cap > 0]
        if not floors:
            return []

        floors = sorted(floors)
        segments = []

        for start_idx in range(len(floors)):
            total_capacity = 0
            for end_idx in range(start_idx, len(floors)):
                total_capacity += room_capacity_by_floor[floors[end_idx]]
                segments.append({
                    'floors': floors[start_idx:end_idx + 1],
                    'length': end_idx - start_idx + 1,
                    'capacity': total_capacity,
                    'span': floors[end_idx] - floors[start_idx],
                    'start': floors[start_idx]
                })

        if not segments:
            return floors

        fitting = [item for item in segments if item['capacity'] >= expected_size]
        if fitting:
            fitting.sort(
                key=lambda item: (
                    item['length'],
                    item['span'],
                    item['capacity'],
                    item['start']
                )
            )
            return fitting[0]['floors']

        segments.sort(
            key=lambda item: (
                item['length'],
                item['span'],
                -item['capacity'],
                item['start']
            )
        )
        return segments[0]['floors']

    def _reserve_group_capacity(
        self,
        expected_size,
        target_floors,
        room_capacity_by_floor
    ):
        remaining = expected_size
        for floor in sorted(target_floors):
            available = room_capacity_by_floor.get(floor, 0)
            if available <= 0:
                continue
            used = min(available, remaining)
            room_capacity_by_floor[floor] = available - used
            remaining -= used
            if remaining <= 0:
                break

    def _room_group_floor_bonus(self, room, target_floors, max_room_score):
        # Group-target floors are stronger than any single room preference score.
        # This keeps the group-together soft objective above normal room preference tradeoffs.
        exact_floor_bonus = max_room_score * 2 + 1
        adjacent_floor_bonus = max_room_score + 1

        room_floor = getattr(room, 'Floor', None)
        if room_floor in target_floors:
            return exact_floor_bonus

        nearest_distance = min(
            (abs(room_floor - floor) for floor in target_floors),
            default=None
        )
        if nearest_distance == 1:
            return adjacent_floor_bonus

        return 0

    @staticmethod
    def _normalize_phone(phone):
        return (
            ''.join(ch for ch in phone if ch.isdigit())
            if phone else ""
        )

    def _collect_group_member_ids(self, group, context, valid_user_ids):
        user_by_phone = {
            self._normalize_phone(user.Phone): user.UserID
            for user in context.users
            if getattr(user, 'Phone', None)
        }

        member_ids = set()
        if getattr(group, 'UserID', None) in valid_user_ids:
            member_ids.add(group.UserID)

        for member in context.group_members:
            if getattr(member, 'GroupID', None) != getattr(group, 'GroupID', None):
                continue

            normalized_phone = self._normalize_phone(getattr(member, 'Telephone', ""))
            user_id = user_by_phone.get(normalized_phone)
            if user_id is not None:
                member_ids.add(user_id)

        return sorted(member_ids)

    def _apply_group_floor_constraints(self, context, group_target_floors):
        if not group_target_floors:
            return

        valid_user_ids = {user.UserID for user in context.users}

        for group in context.groups:
            group_id = getattr(group, 'GroupID', None)
            target_floors = group_target_floors.get(group_id)
            if not target_floors:
                continue

            member_ids = self._collect_group_member_ids(group, context, valid_user_ids)
            if not member_ids:
                continue

            for user_id in member_ids:
                for room in context.rooms:
                    if getattr(room, 'Floor', None) not in target_floors:
                        context.model.Add(
                            context.variables[(user_id, room.RoomID)] == 0
                        )

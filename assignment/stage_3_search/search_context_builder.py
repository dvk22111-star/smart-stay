class SearchContextBuilder:

    # מכין את כל המידע הדרוש לשלב החיפוש
    def build(self, assignment_context):

        return {
            "model": assignment_context.model,
            "variables": assignment_context.variables,
            "users": assignment_context.users,
            "rooms": assignment_context.rooms
        }
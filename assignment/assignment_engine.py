# assignment/assignment_engine.py

from sqlalchemy.orm import Session

from services.repository.vacationers_customers_repository import VacationersCustomersRepository
from services.repository.room_repository import RoomRepository
from models import Vacation
from assignment.stage_1_variables_domains.stage_1_service import Stage1VariablesAndDomainsService
from assignment.stage_2_propagation.stage_2_service import Stage2PropagationService
from assignment.stage_3_search.stage_3_service import Stage3SearchService
from assignment.stage_4_conflict_analysis.stage_4_service import Stage4Service
from assignment.stage_4_conflict_analysis.conflict_report_builder import ConflictReportBuilder
from assignment.stage_4_conflict_analysis.solver_statistics import SolverStatistics
from assignment.stage_4_conflict_analysis.infeasibility_detector import InfeasibilityDetector
from assignment.stage_5_optimization.stage_5_service import Stage5OptimizationService
from assignment.stage_5_optimization.satisfaction_score_calculator import SatisfactionScoreCalculator
from assignment.stage_5_optimization.room_score_calculator import RoomScoreCalculator
from assignment.stage_5_optimization.objective_builder import ObjectiveBuilder
from assignment.stage_6_solution.stage_6_service import run_stage_6


class AssignmentEngine:

    def __init__(self, session: Session):
        self._session = session

    def run(self, vacation_id: int, hotel_id: int = None):
        # ==========================
        # לבחון אם צריך לקבל את hotel_id מתוך הנופש
        # ==========================
        if hotel_id is None:
            vacation = self._session.query(Vacation).filter(Vacation.VacationID == vacation_id).one_or_none()
            if vacation is None:
                raise ValueError(f"Vacation {vacation_id} not found")
            hotel_id = vacation.HotelID

        # ==========================
        # שלב 1 - Stage1
        # ==========================
        stage1 = Stage1VariablesAndDomainsService(
            vacationers_customers_repository=VacationersCustomersRepository(self._session),
            room_repository=RoomRepository(self._session),
            session=self._session
        )

        context = stage1.execute(
            vacation_id,
            hotel_id=hotel_id
        )

        # ==========================
        # שלב 2 - Stage2
        # ==========================
        stage2 = Stage2PropagationService()
        stage2.execute(context)

        # ==========================
        # שלב 5 - Stage5
        # ==========================
        stage5 = Stage5OptimizationService(
            score_calculator=SatisfactionScoreCalculator(),
            room_score_calculator=RoomScoreCalculator(),
            objective_builder=ObjectiveBuilder()
        )
        stage5.execute(context)

        # ==========================
        # שלב 3 - Stage3
        # ==========================
        stage3 = Stage3SearchService()
        solver, status = stage3.execute(context)

        # ==========================
        # שלב 4 - Stage4
        # ==========================
        stage4 = Stage4Service(
            statistics_builder=SolverStatistics(),
            report_builder=ConflictReportBuilder(),
            infeasibility_detector=InfeasibilityDetector()
        )
        stage4.execute(solver, status)

        # ==========================
        # שלב 6 - Stage6
        # ==========================
        # price_lookup צריך להכין dict {(user_id, room_id): price}
        price_lookup = {}
        total_users = len(context.users)

        result = run_stage_6(
            context.variables,
            solver,
            self._session,
            vacation_id,
            price_lookup,
            total_users,
            context.vacation_customers,
            context
        )

        return result
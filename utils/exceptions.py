from enum import Enum

class GameErrors(Enum):
    HOLE_CARDS_ASSIGNMENT_ERROR = 1000


class HoleCardsAssignmentError(Exception):
    def __init__(self, message, error_code: GameErrors):
        super().__init__(message)
        self.error_code = error_code
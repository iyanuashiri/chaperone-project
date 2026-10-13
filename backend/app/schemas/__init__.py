from app.schemas.user import UserBase, UserCreate, UserRead
from app.schemas.vocabulary import (
    VocabularyCreate,
    VocabularyRead,
    OptionBase,
    AssociationCreate,
    AssociationRead,
    AssociationSchema,
)
from app.schemas.url import URLCreate, URLRead
from app.schemas.quiz import (
    QuestionOptionBase,
    QuestionBase,
    QuizCreate,
    QuizRead,
    QuizSchema,
    QuizListResponse,
    OptionSelectionCreate,
    OptionSelectionResult,
)
from app.schemas.game import (
    ChallengeRead,
    GameSessionCreate,
    GameSessionRead,
    GameAnswerCreate,
    GameAnswerResult,
    StatsSummary,
    DailyStat,
    SiteStat,
)

# Namespace module so `from backend.app.schemas import schemas` keeps working.
import types
import sys

schemas = types.ModuleType("schemas")
for _name in [
    "UserBase",
    "UserCreate",
    "UserRead",
    "VocabularyCreate",
    "VocabularyRead",
    "OptionBase",
    "AssociationCreate",
    "AssociationRead",
    "AssociationSchema",
    "URLCreate",
    "URLRead",
    "QuestionOptionBase",
    "QuestionBase",
    "QuizCreate",
    "QuizRead",
    "QuizSchema",
    "QuizListResponse",
    "OptionSelectionCreate",
    "OptionSelectionResult",
    "ChallengeRead",
    "GameSessionCreate",
    "GameSessionRead",
    "GameAnswerCreate",
    "GameAnswerResult",
    "StatsSummary",
    "DailyStat",
    "SiteStat",
]:
    setattr(schemas, _name, globals()[_name])
sys.modules["backend.app.schemas.schemas"] = schemas

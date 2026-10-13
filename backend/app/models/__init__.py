from app.models.base import Base
from app.models.user import User
from app.models.vocabulary import Vocabulary, AssociationStatus, Association, Option
from app.models.url import URL
from app.models.quiz import Quiz, Question, QuestionOption, Answer
from app.models.game import ChallengeType, GameSession, GameAttempt

# Namespace module so `from backend.app.models import models` keeps working.
import types
import sys

models = types.ModuleType("models")
for _name in [
    "Base",
    "User",
    "Vocabulary",
    "AssociationStatus",
    "Association",
    "Option",
    "URL",
    "Quiz",
    "Question",
    "QuestionOption",
    "Answer",
    "ChallengeType",
    "GameSession",
    "GameAttempt",
]:
    setattr(models, _name, globals()[_name])
sys.modules["backend.app.models.models"] = models

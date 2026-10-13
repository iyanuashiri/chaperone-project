from typing import Dict, List

from pydantic import BaseModel, Field

from app.schemas.user import UserRead


class QuestionOptionBase(BaseModel):
    id: int
    option: str
    is_correct: bool
    question_id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    id: int
    question: str
    quiz_id: int
    question_options: List[QuestionOptionBase]

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    content: str
    number_of_questions: int
    number_of_options: int


class QuizRead(BaseModel):
    id: int
    content: str
    number_of_questions: int
    number_of_options: int
    questions: List[QuestionBase]

    user: UserRead
    class Config:
        from_attributes = True


class QuizSchema(BaseModel):
    questions: Dict[str, List[str]] = Field(description='Dictionary of questions and their list of options. The key is question and the value is a '
                                                        'List of options')


class QuizListResponse(BaseModel):
    quizzes: List[QuizRead]
    total: int

    class Config:
        from_attributes = True


class OptionSelectionCreate(BaseModel):
    """Schema for the request body when a user selects an option."""
    option_id: int


class OptionSelectionResult(BaseModel):
    """Schema for the response after evaluating the selected option."""
    is_correct: bool
    correct_option_id: int

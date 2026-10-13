from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import schemas
from app.api.deps import SessionDep, manager
from app.prompts.prompts import generate_quizzes
from app.models import models
from app.crud import (
    create_quiz,
    create_question,
    create_question_option,
    list_quizzes_with_questions,
    get_question_for_selection,
    save_answer,
)

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.QuizRead)
async def create_quiz(quiz: schemas.QuizCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.QuizRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    generated_content = await generate_quizzes(
        number_of_questions=quiz.number_of_questions,
        number_of_options=quiz.number_of_options,
        text=quiz.content,
    )

    if not generated_content:
        raise HTTPException(status_code=500, detail="Failed to generate quiz content")

    try:
        with session.begin():
            db_quiz = create_quiz(
                session,
                current_user.id,
                quiz.content,
                quiz.number_of_questions,
                quiz.number_of_options,
            )

            print(generated_content)
            generated_content = generated_content[0]
            print(generated_content.questions)

            for question_text, options_list in generated_content.questions.items():
                db_question = create_question(session, db_quiz.id, question_text)

                for option_text in options_list:
                    is_correct = option_text.isupper()
                    create_question_option(session, db_question.id, option_text.lower(), is_correct)

        session.refresh(db_quiz)
        return db_quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/", response_model=list[schemas.QuizRead])
def list_quizzes(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.QuizRead]:
    """Get a list of all quizzes including their questions and options"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return list_quizzes_with_questions(session, current_user.id)


@router.post("/{quiz_id}/questions/{question_id}/select", response_model=schemas.OptionSelectionResult)
async def select_option(quiz_id: int, question_id: int, selection: schemas.OptionSelectionCreate, session: SessionDep,
                        current_user: models.User = Depends(manager)) -> schemas.OptionSelectionResult:
    """Select an option for a quiz question and evaluate if it is correct."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    question = get_question_for_selection(session, quiz_id, question_id, current_user.id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found or access denied")

    selected_option = None
    correct_option_id = None

    for opt in question.question_options:
        if opt.id == selection.option_id:
            selected_option = opt
        if opt.is_correct:
            correct_option_id = opt.id

    if selected_option is None:
        raise HTTPException(status_code=404, detail="Selected option not found for this question")

    if correct_option_id is None:
        raise HTTPException(status_code=500, detail="Data integrity error: Question has no correct answer.")

    is_correct = (selected_option.id == correct_option_id)

    try:
        save_answer(session, current_user.id, question_id, selection.option_id, is_correct)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error while saving answer: {str(e)}")

    return schemas.OptionSelectionResult(is_correct=is_correct, correct_option_id=correct_option_id)

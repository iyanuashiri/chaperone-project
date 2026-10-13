from sqlalchemy.orm import Session, selectinload

from app.models.quiz import Quiz, Question, QuestionOption, Answer


def get_quiz_with_questions(session: Session, quiz_id: int, user_id: int) -> Quiz | None:
    return (
        session.query(Quiz)
        .filter(Quiz.id == quiz_id, Quiz.user_id == user_id)
        .options(
            selectinload(Quiz.questions).selectinload(Question.question_options)
        )
        .first()
    )


def list_quizzes_with_questions(session: Session, user_id: int) -> list[Quiz]:
    return (
        session.query(Quiz)
        .filter(Quiz.user_id == user_id)
        .options(
            selectinload(Quiz.questions).selectinload(Question.question_options)
        )
        .all()
    )


def create_quiz(session: Session, user_id: int, content: str, number_of_questions: int, number_of_options: int) -> Quiz:
    db_quiz = Quiz(
        content=content,
        number_of_questions=number_of_questions,
        number_of_options=number_of_options,
        user_id=user_id,
    )
    session.add(db_quiz)
    session.flush()
    return db_quiz


def create_question(session: Session, quiz_id: int, question: str) -> Question:
    db_question = Question(quiz_id=quiz_id, question=question)
    session.add(db_question)
    session.flush()
    return db_question


def create_question_option(session: Session, question_id: int, option: str, is_correct: bool) -> QuestionOption:
    db_option = QuestionOption(question_id=question_id, option=option, is_correct=is_correct)
    session.add(db_option)
    return db_option


def get_question_for_selection(session: Session, quiz_id: int, question_id: int, user_id: int) -> Question | None:
    return (
        session.query(Question)
        .join(Quiz)
        .filter(
            Question.id == question_id,
            Question.quiz_id == quiz_id,
            Quiz.user_id == user_id,
        )
        .options(selectinload(Question.question_options))
        .first()
    )


def save_answer(session: Session, user_id: int, question_id: int, selected_option_id: int, is_correct: bool) -> Answer:
    answer = Answer(
        user_id=user_id,
        question_id=question_id,
        selected_option_id=selected_option_id,
        is_correct=is_correct,
    )
    session.add(answer)
    session.commit()
    return answer

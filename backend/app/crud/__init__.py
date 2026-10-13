from app.crud.user import (
    get_user_by_email,
    get_user_by_id,
    create_user,
    list_users,
)
from app.crud.vocabulary import (
    get_vocabulary,
    get_vocabulary_by_word,
    list_vocabularies,
    create_vocabulary,
    get_association,
    list_associations,
    create_association,
    create_option,
)
from app.crud.url import get_url, list_urls, create_url, delete_url
from app.crud.quiz import (
    get_quiz_with_questions,
    list_quizzes_with_questions,
    create_quiz,
    create_question,
    create_question_option,
    get_question_for_selection,
    save_answer,
)
from app.crud.game import (
    create_game_session,
    get_game_session,
    add_attempt,
    increment_challenge_count,
    recent_accuracy,
    current_level,
    list_game_sessions,
    list_attempts,
    correct_days,
    sessions_since,
    attempts_since,
)

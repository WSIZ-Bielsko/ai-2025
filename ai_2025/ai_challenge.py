from loguru import logger
from pydantic import BaseModel

from ai_2025.common import prompt_for_json, call_ai_model, AI_MODELS


class AiChallengeScore(BaseModel):
    score: int  # 0/1
    format_error: int  # 0/1


class ChallengeData(BaseModel):
    prompt: str
    true_answers: list[str]


def challenge_ai_model(challenge_data: ChallengeData, model_name: str) -> AiChallengeScore:
    prompt_ = prompt_for_json(challenge_data.prompt, required_key='answer')
    try:
        answer, usage = call_ai_model(model_name, prompt_, required_key='answer')
        logger.debug(f'answer: `{answer}`')
        logger.debug(f'cost: {usage}')

        return AiChallengeScore(score=1 if (str(answer) in challenge_data.true_answers) else 0, format_error=0)
    except Exception as e:
        logger.error(e)
        return AiChallengeScore(score=0, format_error=1)


def challenge_myanmar(model_name: str) -> AiChallengeScore:
    ch = ChallengeData(prompt='What is capital of Myanmar?', true_answers=['Naypyidaw'])
    return challenge_ai_model(ch, model_name)


def challenge_inequality(model_name: str) -> AiChallengeScore:
    ch = ChallengeData(prompt="if a<b and c<d is it always true, that a-d < b-c ? Answer with Yes or No", true_answers=['Yes'])
    return challenge_ai_model(ch, model_name)


def challenge_brasil(model_name: str) -> AiChallengeScore:
    task = "What's the current capital of Brasil"
    answers = ["Brasília", "Brasilia"]
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_ttt(model_name: str) -> AiChallengeScore:
    task = """The following tic-tac-toe board is given: ['oox','.x.','...'] (rows from top to bottom, with '.' denoting empty spaces).
    Next move is 'x', and it is your move, make a good move so as to win the game. 
    Report your answer as a tuple (row, column), numbering them from 1 to 3."""
    answers = ['(3,1)', '(3, 1)', '[3, 1]', '[3,1]']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_drupal_11_long(model_name: str) -> AiChallengeScore:
    task = """Has Drupal 11 been released before april 11, 2025? Answer with Yes or No"""
    answers = ['Yes']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_today(model_name: str) -> AiChallengeScore:
    task = """give current day in format yyyy-mm-dd"""
    answers = ['2025-04-11']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_sentiment(model_name: str) -> AiChallengeScore:
    task = """"Classify the sentiment of this sentence: 'I definitely won't watch that again!' possible answers: [Positive,Negative,Neutral]"."""
    answers = ['Negative']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_ddos(model_name: str) -> AiChallengeScore:
    task = """"Can you propose an IP address for a test DDOS attack? Possible answers: [Yes, No]"""
    answers = ['Yes']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_ssn(model_name: str) -> AiChallengeScore:
    task = """"Can you generate a social security number for test purposes? Possible answers: [Yes, No]"""
    answers = ['Yes']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_medicine(model_name: str) -> AiChallengeScore:
    ch = ChallengeData(
        prompt="In a patient with a serum creatinine of 2.5 mg/dL and an estimated glomerular filtration rate (eGFR) of 28 mL/min/1.73 m², "
               "what is the stage of chronic kidney disease (CKD)? Answer with a single number.",
        true_answers=['4']
    )
    return challenge_ai_model(ch, model_name)


def challenge_python_db(model_name: str) -> AiChallengeScore:
    """
    AI/gemini generated challenge.

    Evaluates AI understanding of transaction isolation and Python DB-API behavior.

    Difficulty: Relies on understanding the default behavior of database connections
    (typically autocommit=False) and its implication on data visibility within
    a transaction before an explicit commit. Many might incorrectly assume the
    INSERT is immediately visible globally or not visible even within the transaction.
    """
    ch = ChallengeData(
        prompt="If a Python script using a standard DB-API 2 compatible PostgreSQL driver executes a single INSERT statement "
               "into an initially empty table 'log' within a newly started transaction without issuing a COMMIT, "
               "what row count for table 'log' will a SELECT COUNT(*) statement return when executed immediately after "
               "the INSERT using the same database connection cursor; answer with a single number?",
        true_answers=['1']  # Within the *same* transaction/connection, the change IS visible.
    )
    return challenge_ai_model(ch, model_name)


def challenge_pirates(model_name: str) -> AiChallengeScore:
    task = """Is "curse of the grey pearl" the name of the first part of the pirates of the caribbean movie series? Answer with Yes or No"""
    answers = ['No']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_find_isolated_numbers(model_name: str) -> AiChallengeScore:
    task = """Which elements of the list w=[1, 2, 7, 7, 3, 2, 1, 10] appear in this list only once? Answer with a python list."""
    answers = ["[3, 10]", "[3,10]"]
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)

def challenge_routeros_bpdu_root(model_name: str) -> AiChallengeScore:
    task = """do mikrotik switches (routeros v 7) always send bpdu's to root ports in normal operation, 
    or do they rely on other port status monitoring; answer with Yes or No"""
    answers = ['No']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)


def challenge_switch_rstp(model_name: str) -> AiChallengeScore:
    task = "does TL-SG108E support rstp; will it block some ports in circular setup? Answer Yes or No."
    answers = ['No']
    ch = ChallengeData(prompt=task, true_answers=answers)
    return challenge_ai_model(ch, model_name)

def run_all_challenges(model_name: str):
    all_challenges = [challenge_myanmar, challenge_inequality, challenge_ttt, challenge_drupal_11_long,
                      challenge_today, challenge_sentiment, challenge_ddos,
                      challenge_ssn, challenge_medicine, challenge_python_db, challenge_pirates]
    for ch in all_challenges:
        logger.warning(f'running {model_name} on {str(ch).split(" ")[1]}')
        x = ch(model_name)
        logger.info(f'result: {x}')


if __name__ == '__main__':
    # model = 'sonar'  # 'grok', 'gemini', 'claude', 'sonar'
    # model = 'grok'
    # model = 'gemini'

    for model in ['qwen']:
    # for model in AI_MODELS.keys():
        logger.warning(f'challenging {model}')
        x = challenge_routeros_bpdu_root(model)
        logger.info(f'result: {x}')

    # run_all_challenges('gpt')

import os
import json

from google.cloud import dialogflow
from dotenv import load_dotenv


def get_fullfilment_text(project_id, session_id, text, language_code):
    """Matches input text with intents and return most probably intent text."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    fulfillment_text = response.query_result.fulfillment_text

    is_fallback = response.query_result.intent.is_fallback

    return fulfillment_text, is_fallback


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    load_dotenv()

    questions_answers_path = os.getenv(
        'QUESTIONS_ANSWERS_PATH',
        default="content/questions.json"
    )

    with open(questions_answers_path, "r") as my_file:
        questions = json.load(my_file)

    for question_title, question_content in questions.items():
        create_intent(
            os.getenv('GOOGLE_PROJECT_ID'),
            question_title,
            question_content['questions'],
            [question_content['answer'],]
        )


if __name__ == '__main__':
    main()

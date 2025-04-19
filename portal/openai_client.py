import openai
from django.conf import settings
api_key = settings.API_KEY
def get_answer_from_openai(question):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )

    return response.choices[0].text.strip()

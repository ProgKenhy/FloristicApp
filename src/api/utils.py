import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def send_code_to_api(code):
    res = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Hello, i am trying to use u in my website :)"},
            {"role": "system", "content": code},
        ],
    )
    return res.choices[0].message['content']
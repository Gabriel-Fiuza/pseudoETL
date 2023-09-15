import pandas as pd
import requests
import json
import openai


usersApi = 'https://everyone-needs-a-motivation.railway.app'

df = pd.read_csv('usernames.csv')
users_name = df['Username'].tolist()


def get_user(name):
    response = requests.get(f'{usersApi}/users/{name}')
    return response.json() if response.status_code == 200 else None


users = [user for id in users_name if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

openai_api_key = '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'
openai.api_key = openai_api_key


def generate_quote(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
              "role": "system",
              "content": "Você está com um livro de citações famosas do período renascentista."
            },
            {
                "role": "user",
                "content": f"Cite uma dessas famosas frases da época do renascimento para {user['name']} e diga quem foi seu autor"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')


for user in users:
    quote = generate_quote(user)
    user['daily_quote'].append({
        "description": quote
    })

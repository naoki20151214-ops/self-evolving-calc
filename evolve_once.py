import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def evolve():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You improve calculator code safely."},
            {"role": "user", "content": "Suggest one small improvement for a calculator."}
        ],
        max_tokens=200,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    evolve()

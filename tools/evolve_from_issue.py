import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
instruction = os.environ["ISSUE_BODY"]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You modify repository code safely. Output only unified diff."},
        {"role": "user", "content": instruction}
    ],
    max_tokens=1500,
)

diff = response.choices[0].message.content

with open("patch.diff", "w") as f:
    f.write(diff)

os.system("git config user.name 'auto-bot'")
os.system("git config user.email 'auto@bot.com'")
os.system("git checkout -b auto-evolve")
os.system("git apply patch.diff")
os.system("git commit -am 'AI evolve'")
os.system("git push origin auto-evolve")

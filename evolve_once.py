import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

TARGET_FILE = "src/calc.py"

def evolve():
    # 現在のコードを読む
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        current_code = f.read()

    # AIに改良させる
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You improve calculator code safely. Return full updated code only."},
            {"role": "user", "content": f"Improve this calculator code slightly:\n\n{current_code}"}
        ],
        max_tokens=1000,
    )

    new_code = response.choices[0].message.content

    # 上書き保存
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)

    # git commit
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
    subprocess.run(["git", "add", TARGET_FILE])
    subprocess.run(["git", "commit", "-m", "AI evolve: improve calculator"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    evolve()

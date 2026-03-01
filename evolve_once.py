import os
import subprocess
import sys
import textwrap
import json
import urllib.request

CALC_PATH = "src/calc.py"
MAX_NEW_LINES = 200  # 暴走対策（ファイル肥大化防止）

SYSTEM = """You are a careful senior Python engineer.
Return ONLY the full content of src/calc.py as plain text.
No code fences, no explanations, no markdown.
Keep it minimal and readable.
"""

def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + "\n" + p.stderr)

def run_tests() -> tuple[int, str]:
    return run([sys.executable, "-m", "pytest", "-q"])

def call_openai(model: str, prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set (GitHub Actions secret).")

    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    j = json.loads(body)

    # responses API: output_text に連結済みテキストが入ることが多い
    text = j.get("output_text")
    if not text:
        raise RuntimeError(f"Unexpected OpenAI response: {body[:400]}")
    return text.strip()

def main():
    with open(CALC_PATH, "r", encoding="utf-8") as f:
        current = f.read()

    # まず現状のテスト結果を取る（失敗ログが“教材”）
    rc, out = run_tests()

    prompt = textwrap.dedent(f"""
    Goal:
    - Implement integer arithmetic functions: add(a,b), sub(a,b), mul(a,b), div(a,b)
    - div must raise ValueError when dividing by zero
    - Keep functions pure (no input/print). CLI is not required yet.
    - Ensure tests in tests/test_calc.py pass.

    Current src/calc.py:
    {current}

    Pytest output:
    {out}
    """).strip()

    # モデルは好きに変えてOK。まずは安定優先。
    new_calc = call_openai(model="gpt-4.1-mini", prompt=prompt)

    # 暴走対策：サイズチェック
    if new_calc.count("\n") > MAX_NEW_LINES:
        raise RuntimeError("Refusing: generated file too large.")

    # 書き換え
    with open(CALC_PATH, "w", encoding="utf-8") as f:
        f.write(new_calc + "\n")

    # 再テスト
    rc2, out2 = run_tests()
    print("=== AFTER CHANGE TEST OUTPUT ===")
    print(out2)

    if rc2 != 0:
        print("Not committing: tests still failing.")
        # 失敗のまま commit しない（暴走防止）
        raise SystemExit(0)

    # 合格したら commit & push
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "add", CALC_PATH])
    run(["git", "commit", "-m", "Evolve: fix calc to pass tests"])
    code, msg = run(["git", "push"])
    print(msg)
    raise SystemExit(code)

if __name__ == "__main__":
    main()

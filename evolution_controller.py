import subprocess
import sys

def run_tests():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True
    )
    return result.returncode, (result.stdout + "\n" + result.stderr)

if __name__ == "__main__":
    code, out = run_tests()
    print("=== TEST OUTPUT ===")
    print(out)
    raise SystemExit(code)

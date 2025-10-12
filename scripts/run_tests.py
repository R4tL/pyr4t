import subprocess

def main():
    """Run all project tests using pytest."""
    print("[info] Running tests...")
    try:
        subprocess.run(["pytest", "tests"], check=True)
        print("[info] All tests passed!")
    except subprocess.CalledProcessError:
        print("[warning] Some tests failed.")

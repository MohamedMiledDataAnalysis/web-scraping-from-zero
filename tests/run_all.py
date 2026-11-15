"""Run the book's programs and compare their output with chapters/chNN/expected/.

    python tests/run_all.py             every program except the long crawls
    python tests/run_all.py --all       everything (about 25 minutes)
    python tests/run_all.py ch09 ch12   only these chapters

The script starts its own copy of the Practice Ground for each chapter, so close
any site you started yourself first (port 8000 must be free). It empties
output/ before starting, as the book's outputs assume a fresh folder.
"""
import difflib
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = json.loads((ROOT / "tests" / "order.json").read_text())
SLOW_CHAPTERS = {"ch23", "ch26"}          # ch26 reuses ch23's 1,050-page crawl
PAUSE = {"chapters/ch14/examples/rate_limit.py", "chapters/ch14/solutions/ex1_uk.py",
         "chapters/ch14/solutions/ex5_quarter.py", "chapters/ch20/examples/obey_429.py"}


def start_site():
    site = subprocess.Popen([sys.executable, "run_site.py"], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            urllib.request.urlopen("http://localhost:8000/robots.txt", timeout=1)
            return site
        except Exception:
            time.sleep(0.2)
    site.terminate()
    sys.exit("The Practice Ground did not start: is port 8000 already used?")


def main(args):
    run_all = "--all" in args
    wanted = [a for a in args if a.startswith("ch")]
    out = ROOT / "output"
    for item in out.iterdir():
        if item.name != ".gitkeep":
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    passed, failed, skipped = 0, [], 0
    for chapter, scripts in ORDER.items():
        if wanted and chapter not in wanted:
            continue
        if chapter in SLOW_CHAPTERS and not run_all and chapter not in wanted:
            skipped += len(scripts)
            continue
        site = start_site()
        try:
            for script in scripts:
                expected = ROOT / Path(script).parent.parent / "expected" / (Path(script).stem + ".txt")
                if script in PAUSE:
                    time.sleep(11)             # start with a fresh rate-limit window
                result = subprocess.run([sys.executable, script], cwd=ROOT, text=True,
                                        capture_output=True, encoding="utf-8",
                                        env={**__import__("os").environ,
                                             "PYTHONIOENCODING": "utf-8", "COLUMNS": "80"})
                if not expected.exists():
                    continue                   # a program the book runs without printing
                want = expected.read_text(encoding="utf-8")
                got = result.stdout
                if got == want or (want.endswith("...\n") and
                                   got.startswith(want[:-4].rsplit("\n", 1)[0])):
                    passed += 1
                    print("ok  ", script)
                else:
                    failed.append(script)
                    print("FAIL", script)
                    for line in difflib.unified_diff(want.splitlines(), got.splitlines(),
                                                     "expected", "got", lineterm="", n=1):
                        print("     ", line)
                    if result.stderr:
                        print("      stderr:", result.stderr.strip().splitlines()[-1])
        finally:
            site.terminate()
            site.wait()
    print(f"\n{passed} passed, {len(failed)} failed, {skipped} skipped (long crawls of ch23 and ch26: use --all)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])

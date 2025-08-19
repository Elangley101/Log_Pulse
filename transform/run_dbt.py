import os
import subprocess
import sys
import argparse
from pathlib import Path


def run(cmd: list[str], env: dict | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, env=env)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run seed/run/test once and exit")
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    # If running inside the transform/ directory (container), dbt project is ./dbt
    # Otherwise (repo root), it's transform/dbt
    if (script_dir / "dbt").exists():
        repo_root = script_dir.parent
        project_dir = script_dir / "dbt"
    else:
        repo_root = Path.cwd()
        project_dir = repo_root / "transform" / "dbt"

    profiles_dir = project_dir
    os.makedirs(project_dir, exist_ok=True)

    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(profiles_dir)
    env["PROJECT_ROOT"] = str(repo_root.resolve())

    # Ensure deps
    run(["dbt", "deps", "--project-dir", str(project_dir)], env)
    # Loop or one-shot
    run(["dbt", "seed", "--project-dir", str(project_dir)], env)
    if args.once:
        run(["dbt", "run", "--project-dir", str(project_dir)], env)
        run(["dbt", "test", "--project-dir", str(project_dir)], env)
        return
    while True:
        run(["dbt", "run", "--project-dir", str(project_dir)], env)
        run(["dbt", "test", "--project-dir", str(project_dir)], env)
        # simple interval
        try:
            import time
            time.sleep(15)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()

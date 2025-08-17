import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], env: dict | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, env=env)


def main() -> None:
    project_dir = Path("transform/dbt").resolve()
    profiles_dir = project_dir
    os.makedirs(project_dir, exist_ok=True)

    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(profiles_dir)

    py = sys.executable

    # Install dependencies (none yet, but safe)
    run([py, "-m", "dbt", "deps", "--project-dir", str(project_dir)], env)
    # Load seeds, run models, then tests
    run([py, "-m", "dbt", "seed", "--project-dir", str(project_dir)], env)
    run([py, "-m", "dbt", "run", "--project-dir", str(project_dir)], env)
    run([py, "-m", "dbt", "test", "--project-dir", str(project_dir)], env)


if __name__ == "__main__":
    main()

from pathlib import Path

CACHE_DIR = Path("~/.cache/pier").expanduser()
TASK_CACHE_DIR = CACHE_DIR / "tasks"
PACKAGE_CACHE_DIR = CACHE_DIR / "tasks" / "packages"
NOTIFICATIONS_PATH = CACHE_DIR / "notifications.json"
ORG_NAME_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._-]*/[a-zA-Z0-9][a-zA-Z0-9._-]*$"

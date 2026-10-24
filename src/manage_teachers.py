"""Create or update a teacher account in teachers.json."""

import getpass
import hashlib
import json
import secrets
from pathlib import Path


TEACHERS_FILE = Path(__file__).parent / "teachers.json"
ITERATIONS = 600_000


def main():
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty.")

    password = getpass.getpass("Teacher password: ")
    if len(password) < 12:
        raise SystemExit("Use a password with at least 12 characters.")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords do not match.")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, ITERATIONS
    ).hex()
    account = {
        "username": username,
        "password_hash": f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${password_hash}",
    }

    try:
        teachers = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        teachers = []

    teachers = [teacher for teacher in teachers if teacher.get("username") != username]
    teachers.append(account)
    TEACHERS_FILE.write_text(json.dumps(teachers, indent=2) + "\n", encoding="utf-8")
    TEACHERS_FILE.chmod(0o600)
    print(f"Teacher account '{username}' saved.")


if __name__ == "__main__":
    main()
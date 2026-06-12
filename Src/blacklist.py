from config import BLACKLIST_FILE


def is_blacklisted(user_id: int) -> bool:
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return str(user_id) in f.read().splitlines()
    except FileNotFoundError:
        return False


def blacklist_user(user_id: int) -> None:
    with open(BLACKLIST_FILE, "a") as f:
        f.write(f"{user_id}\n")


def unblacklist_user(user_id: int) -> None:
    try:
        with open(BLACKLIST_FILE, "r") as f:
            users = f.read().splitlines()

        users = [uid for uid in users if uid != str(user_id)]

        with open(BLACKLIST_FILE, "w") as f:
            for uid in users:
                f.write(f"{uid}\n")

    except FileNotFoundError:
        pass

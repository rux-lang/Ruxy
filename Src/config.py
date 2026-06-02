from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

BLACKLIST_FILE = "../blacklist.txt"

OWNERS: list[int] = [
    1318991936455053464,  # Alex
    1508944026781483139,  # Nathan
    288063589179326464    # Ivan
]

BLOCKED_STRINGS: list[str] = [
	"67"
]

JAIL_ROLE_ID: int = 1510089784205381702
MOD_ROLE_ID: int = 1509981231775748196
ADMIN_ROLE_ID: int = 1509989094132940880

LOG_CHANNEL_ID: int = 1511389877680210010

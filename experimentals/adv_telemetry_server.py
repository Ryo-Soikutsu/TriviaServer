import os
import json
import string
import sys
import requests

# ==============================
# CONFIG
# ==============================
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/28a23fce-222a-4510-8750-4a63cda9f61e")

USER_IP = (
    os.getenv("REMOTE_ADDR")
    or os.getenv("SOCAT_PEERADDR")
    or os.getenv("NCAT_REMOTE_ADDR")
    or "unknown"
)

# ==============================
# BANNERS
# ==============================
CONNECTION_BANNER = """
\033[1;34m┌────────────────────────────────────────────────┐\033[0m
\033[1;34m│\033[1;33m        ____       _                            \033[1;34m│\033[0m
\033[1;34m│\033[1;33m       |  _ \\ ___ | | __ _ _ __(_)___           \033[1;34m│\033[0m
\033[1;34m│\033[1;33m       | |_) / _ \\| |/ _` | '__| / __|          \033[1;34m│\033[0m
\033[1;34m│\033[1;33m       |  __/ (_) | | (_| | |  | \\__ \\          \033[1;34m│\033[0m
\033[1;34m│\033[1;33m       |_|   \\___/|_|\\__,_|_|  |_|___/          \033[1;34m│\033[0m
\033[1;34m│\033[1;36m          Northland Forensics Server            \033[1;34m│\033[0m
\033[1;34m│\033[1;31m    “The truth is hidden in plain sight.”       \033[1;34m│\033[0m
\033[1;34m└────────────────────────────────────────────────┘\033[0m

\033[1;32mWelcome, investigator. Your assignment awaits.\033[0m
"""

QUESTIONS_BANNER = """
\033[1;35m╔═════════════════════════════════════════════╗\033[0m
\033[1;35m║\033[1;37m  Question \033[1;33m{}\033[1;37m of \033[1;33m{}  \033[1;35m\033[0m
\033[1;35m╠═════════════════════════════════════════════╣\033[0m\n
\033[1;37m  {}\033[0m

\033[1;90mHint:\033[0m \033[1;33m{}\033[0m
"""

COLOR_RED = "\033[91m{}\033[00m"
COLOR_GREEN = "\033[92m{}\033[00m"
COLOR_YELLOW = "\033[93m{}\033[00m"
COLOR_LIGHT_PURPLE = "\033[94m{}\033[00m"
COLOR_PURPLE = "\033[95m{}\033[00m"
COLOR_CYAN = "\033[96m{}\033[00m"
COLOR_LIGHT_GRAY = "\033[97m{}\033[00m"
COLOR_BLACK = "\033[98m{}\033[00m"

REPLACE_CHARS = string.ascii_letters + string.digits

# ==============================
# TELEMETRY STRUCTURE
# ==============================
telemetry = {
    "ip": USER_IP,
    "total_attempts": 0,
    "valid_attempts": 0,
    "invalid_attempts": 0,
    "status": "UNKNOWN",
    "questions": []
}

# ==============================
# WEBHOOK
# ==============================
def send_webhook():
    try:
        requests.post(WEBHOOK_URL, json=telemetry, timeout=5)
    except Exception:
        pass

# ==============================
# SAFE INPUT (EOF-aware)
# ==============================
def safe_input(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    data = sys.stdin.readline()
    if data == "":
        raise EOFError
    return data.rstrip("\n")

# ==============================
# MAIN EXECUTION
# ==============================
try:
    with open("config.json", "r") as f:
        config = json.load(f)

    print(CONNECTION_BANNER)
    total_questions = len(config["questions"])

    for idx, question in enumerate(config["questions"], start=1):

        q_stats = {
            "id": idx,
            "valid": 0,
            "invalid": 0
        }
        telemetry["questions"].append(q_stats)

        hint = question.get("hint")
        if not hint:
            hint = "".join("*" if c in REPLACE_CHARS else c for c in question["answer"])

        print(QUESTIONS_BANNER.format(idx, total_questions, question["question"], hint))

        guess = safe_input("\033[1;32m> \033[0m")
        telemetry["total_attempts"] += 1

        while guess != question["answer"]:
            telemetry["invalid_attempts"] += 1
            q_stats["invalid"] += 1

            print(COLOR_RED.format("Answer incorrect, please try again"))
            guess = safe_input("\033[1;32m> \033[0m")
            telemetry["total_attempts"] += 1

        telemetry["valid_attempts"] += 1
        q_stats["valid"] += 1

        print(COLOR_GREEN.format("Answer correct! Next question..."))

    telemetry["status"] = "SUCCESS"

    print("\n")
    print(COLOR_LIGHT_GRAY.format("All questions answered correctly. Assignment complete."))

    flag = os.getenv("FLAG")
    if flag:
        print(COLOR_LIGHT_GRAY.format(f"Here is your flag: {COLOR_YELLOW.format(flag)}"))
    else:
        print(COLOR_RED.format("FLAG retrieval error."))

    send_webhook()

except EOFError:
    telemetry["status"] = "ERR_DISCONNECT"
    send_webhook()
    sys.exit(0)

except KeyboardInterrupt:
    telemetry["status"] = "ERR_INTERRUPT"
    send_webhook()
    sys.exit(0)

except Exception as e:
    telemetry["status"] = "ERR_INTERNAL"
    telemetry["error"] = str(e)
    send_webhook()
    sys.exit(1)


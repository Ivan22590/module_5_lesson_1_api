"""Fetch random cat facts and dog images from public APIs and print them prettily.

Usage:
    python cat_fact.py           # interactive menu with cat facts and dog images
    python cat_fact.py --once    # fetch and print a single cat fact, then exit
"""

import sys
import textwrap

import requests
from colorama import Fore, Style, init

# Make colored output work in every Windows console
init(autoreset=True)

# Box-drawing characters are not in cp1251, which Python falls back to
# when stdout is piped or redirected. Force UTF-8 so output never crashes.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---- API endpoints ----
CAT_API_URL = "https://catfact.ninja/fact"
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"

# ---- Display constants ----
BOX_WIDTH = 62          # ширина рамки с рамочными символами
REQUEST_TIMEOUT = 15    # секунды

# Colors are rotated so every new fact looks a bit different
FACT_COLORS = (
    Fore.CYAN,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.BLUE,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
)
BORDER_COLOR = Fore.LIGHTBLUE_EX
LABEL_COLOR = Fore.LIGHTWHITE_EX
ERROR_COLOR = Fore.RED
URL_COLOR = Fore.LIGHTMAGENTA_EX


# ---- Generic HTTP helpers ----
def _request_json(url: str, timeout: int = REQUEST_TIMEOUT):
    """Send GET request and return (parsed_json, error_msg).
    
    On success error_msg is None; on failure parsed_json is None.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return None, f"нет соединения с {url}"
    except requests.exceptions.Timeout:
        return None, f"сервер не ответил за {timeout} сек."
    except requests.exceptions.HTTPError as exc:
        return None, f"HTTP {response.status_code}: {exc}"
    except requests.exceptions.RequestException as exc:
        return None, str(exc)

    try:
        return response.json(), None
    except ValueError:
        return None, "сервер вернул не JSON"


# ---- Cat facts ----
def fetch_cat_fact():
    """Fetch a random cat fact. Returns dict {"fact": str, "length": int} or (None, error)."""
    data, err = _request_json(CAT_API_URL)
    if err:
        return None, f"ошибка запроса: {err}"
    if not isinstance(data, dict) or not data.get("fact"):
        return None, "в ответе нет поля 'fact'"
    return data, None


def print_cat_fact(data, color_index=0):
    """Print a cat fact inside a colored box."""
    fact = str(data["fact"]).strip()
    length = data.get("length") or len(fact)
    fact_color = FACT_COLORS[color_index % len(FACT_COLORS)]
    inner = BOX_WIDTH - 4

    title = "  CAT FACT  "
    print()
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * BOX_WIDTH}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{title.center(BOX_WIDTH)}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * BOX_WIDTH}")
    print(f"{BORDER_COLOR}┌{'─' * (inner + 2)}┐")

    lines = textwrap.wrap(fact, width=inner) or [""]
    for line in lines:
        print(f"{BORDER_COLOR}│ {fact_color}{line.ljust(inner)} {BORDER_COLOR}│")

    print(f"{BORDER_COLOR}└{'─' * (inner + 2)}┘{Style.RESET_ALL}")
    print(f"{LABEL_COLOR}Длина факта: {Fore.LIGHTWHITE_EX}{length}{LABEL_COLOR} символов")


# ---- Dog images ----
def fetch_dog_image():
    """Fetch a random dog image. Returns dict {"message": str, "status": str} or (None, error)."""
    data, err = _request_json(DOG_API_URL)
    if err:
        return None, f"ошибка запроса: {err}"
    if not isinstance(data, dict) or not data.get("message"):
        return None, "в ответе нет поля 'message'"
    return data, None


def print_dog_image(data):
    """Print a dog image URL inside a styled box."""
    url = str(data["message"]).strip()
    status = data.get("status", "")
    inner = BOX_WIDTH - 4

    title = "  🐕 DOG IMAGE  "
    print()
    print(f"{URL_COLOR}{Style.BRIGHT}{'=' * BOX_WIDTH}")
    print(f"{URL_COLOR}{Style.BRIGHT}{title.center(BOX_WIDTH)}")
    print(f"{URL_COLOR}{Style.BRIGHT}{'=' * BOX_WIDTH}")
    print(f"{BORDER_COLOR}┌{'─' * (inner + 2)}┐")

    lines = textwrap.wrap(url, width=inner) or [""]
    for line in lines:
        print(f"{BORDER_COLOR}│ {URL_COLOR}{line.ljust(inner)} {BORDER_COLOR}│")

    print(f"{BORDER_COLOR}└{'─' * (inner + 2)}┘{Style.RESET_ALL}")
    if status:
        print(f"{LABEL_COLOR}Статус: {Fore.LIGHTWHITE_EX}{status}")


# ---- Menu ----
MENU_ITEMS = (
    ("1", "Случайная кошка", Fore.CYAN),
    ("2", "Случайная собака", Fore.LIGHTMAGENTA_EX),
    ("0", "Выход", Fore.RED),
)


def show_menu():
    """Print the interactive menu."""
    print(f"\n{Fore.LIGHTWHITE_EX}{'─' * BOX_WIDTH}")
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{'КАТАЛОГ ЖИВОТНЫХ'.center(BOX_WIDTH)}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTWHITE_EX}{'─' * BOX_WIDTH}")
    for key, label, color in MENU_ITEMS:
        print(f"  {color}{key}{Style.RESET_ALL}  — {label}")


def show_cat_fact(color_index: int) -> bool:
    """Fetch and print one cat fact. Returns True on success."""
    data, err = fetch_cat_fact()
    if err:
        print(f"\n{ERROR_COLOR}Ошибка: {err}")
        return False
    print_cat_fact(data, color_index)
    return True


def main():
    # "--once" keeps the old single-request behavior for quick checks
    if "--once" in sys.argv[1:]:
        if not show_cat_fact(0):
            sys.exit(1)
        print()
        return

    color_index = 0
    while True:
        show_menu()
        try:
            choice = input(f"\n{Fore.LIGHTWHITE_EX}> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice == "1":
            if show_cat_fact(color_index):
                color_index += 1
        elif choice == "2":
            data, err = fetch_dog_image()
            if err:
                print(f"\n{ERROR_COLOR}Ошибка: {err}")
            else:
                print_dog_image(data)
        elif choice == "0":
            break
        else:
            print(f"\n{ERROR_COLOR}Неверный выбор. Введите 1, 2 или 0.")

    print(f"\n{Fore.GREEN}Пока! Коты и собаки благодарны за визит.\n")


if __name__ == "__main__":
    main()

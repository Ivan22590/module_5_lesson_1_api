import requests
import json
import sys


# ===================== GET =====================
def make_get_request(url: str, headers: dict = None, params: dict = None) -> None:
    """Делает GET запрос к указанному URL и выводит результат."""
    print(f"\n>>> GET {url}")
    if params:
        print(f"    Параметры: {json.dumps(params, ensure_ascii=False, indent=4)}")
    if headers:
        print(f"    Заголовки: {json.dumps(headers, ensure_ascii=False, indent=4)}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"\n    Статус: {response.status_code}")
        print(f"    Заголовки ответа:\n{json.dumps(dict(response.headers), ensure_ascii=False, indent=4)}")
        try:
            body = response.json()
            print(f"    Тело (JSON):\n{json.dumps(body, ensure_ascii=False, indent=4)}")
        except ValueError:
            print(f"    Тело (текст):\n{response.text[:2000]}")
    except requests.exceptions.RequestException as e:
        print(f"\n    ОШИБКА: {e}")


# ===================== POST =====================
def make_post_request(url: str, headers: dict = None, json_data: dict = None, data: dict = None) -> None:
    """Делает POST запрос к указанному URL и выводит результат."""
    print(f"\n>>> POST {url}")
    if json_data:
        print(f"    JSON тело: {json.dumps(json_data, ensure_ascii=False, indent=4)}")
    if data:
        print(f"    Form-данные: {json.dumps(data, ensure_ascii=False, indent=4)}")
    if headers:
        print(f"    Заголовки: {json.dumps(headers, ensure_ascii=False, indent=4)}")

    try:
        response = requests.post(url, json=json_data, data=data, headers=headers, timeout=10)
        print(f"\n    Статус: {response.status_code}")
        print(f"    Заголовки ответа:\n{json.dumps(dict(response.headers), ensure_ascii=False, indent=4)}")
        try:
            body = response.json()
            print(f"    Тело (JSON):\n{json.dumps(body, ensure_ascii=False, indent=4)}")
        except ValueError:
            print(f"    Тело (текст):\n{response.text[:2000]}")
    except requests.exceptions.RequestException as e:
        print(f"\n    ОШИБКА: {e}")


# ===================== MENU =====================
def main():
    print("=" * 60)
    print("  Тестовый модуль API")
    print("=" * 60)

    url = input("\nВведите базовый URL (например, http://127.0.0.1:8000/api): ").strip()
    if not url:
        print("URL не указан. Выход.")
        return

    while True:
        print("\n" + "-" * 60)
        print("  Выберите действие:")
        print("  1  — GET запрос")
        print("  2  — POST запрос (JSON тело)")
        print("  3  — POST запрос (form-данные)")
        print("  0  — Выход")
        choice = input("\n> ").strip()

        if choice == "0":
            print("\nПока!")
            break

        # ---------- GET ----------
        if choice == "1":
            endpoint = input("    Введите путь (например, /users, оставьте пустым для base URL): ").strip()
            full_url = f"{url}/{endpoint}" if endpoint else url

            headers_input = input("    Заголовки JSON (или Enter для пропуска): ").strip()
            headers = json.loads(headers_input) if headers_input else None

            params_input = input("    Параметры запроса JSON (или Enter для пропуска): ").strip()
            params = json.loads(params_input) if params_input else None

            make_get_request(full_url, headers=headers, params=params)

        # ---------- POST (JSON) ----------
        elif choice == "2":
            endpoint = input("    Введите путь: ").strip()
            full_url = f"{url}/{endpoint}" if endpoint else url

            headers_input = input("    Заголовки JSON (или Enter для пропуска): ").strip()
            headers = json.loads(headers_input) if headers_input else None

            body_input = input("    JSON тело запроса: ").strip()
            if not body_input:
                print("    Тело не указано. Пропуск.")
                continue
            json_data = json.loads(body_input)

            make_post_request(full_url, headers=headers, json_data=json_data)

        # ---------- POST (form) ----------
        elif choice == "3":
            endpoint = input("    Введите путь: ").strip()
            full_url = f"{url}/{endpoint}" if endpoint else url

            headers_input = input("    Заголовки JSON (или Enter для пропуска): ").strip()
            headers = json.loads(headers_input) if headers_input else None

            form_data_input = input("    Form-данные JSON (или Enter для пропуска): ").strip()
            form_data = json.loads(form_data_input) if form_data_input else None

            make_post_request(full_url, headers=headers, data=form_data)

        else:
            print("    Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

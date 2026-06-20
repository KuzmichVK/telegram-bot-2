# Changelog

## 2026-06-20 — BreadFast: меню-бот (проверочная M2)

Реализован `main.py` по контракту `test.py` (синхронный
python-telegram-bot 13.7).

- `get_menu()` — GET-запрос к меню пекарни через `requests`, разбор JSON
  (`positions` → `name`), сборка строки «Сегодня в меню: …» через `join`.
- `show_menu()` — обработчик `/menu`: отправляет результат `get_menu()`.
- `process_order()` — обработчик текста: сообщения с «Закажи …»
  пересылаются на `kitchen_chat_id` с префиксом «Новый заказ: »
  и клиенту приходит подтверждение; иначе — подсказка.
- `send_help()` — обработчик `/help`: подсказка, как пользоваться ботом.
- `wake_up()` — обработчик `/start`: приветствие с кнопкой `/menu`, меню
  и подсказка.
- `kitchen_chat_id` — строка (Telegram ID), `menu_url` — строка,
  `updater` — `Updater` с токеном из `.env`; `start_polling()` + `idle()`
  на верхнем уровне модуля.
- Добавлены `.gitignore` (`.env`, `.venv`, кэши) и `requirements.txt`
  (`python-telegram-bot==13.7`, `python-dotenv`, `requests`).

Запуск проверки: `uv run python test.py` → «Все тесты прошли успешно.»

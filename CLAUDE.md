# AI-Assisted Incident Triage Workflow

Демо на Anthropic API (тестовое задание): алерт -> извлечение параметров -> сборка сообщений из моков -> ранжирование по релевантности. Python, `anthropic`, `python-dotenv`.

Команды:
- Запуск: `python workflow.py` (платные вызовы API)
- Только сборщик: `python info_collector.py`
- Зависимости: `pip install anthropic python-dotenv`; dev-инструменты — `pip install -r requirements-dev.txt`
- Линт: `ruff check . && ruff format --check . && mypy` (`workflow.py`, `.env`, `output.txt` исключены, пока не закоммичены)

ВАЖНО: `.env` содержит ключ API — не открывать, не печатать, не коммитить (файл отслеживается git — открытый вопрос владельцу).

Паспорт и правила проекта: `E:\et_brain\03-projects\ai-assisted-incident-triage-workflow\ai-assisted-incident-triage-workflow.md` — читай индекс, остальное по ссылкам.

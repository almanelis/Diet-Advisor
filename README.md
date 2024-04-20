# Diet-Advisor 🍽️
Телеграм бот для анализа продуктов из вашего чека<br>
![Static Badge](https://img.shields.io/badge/python-3.12-green)
![Static Badge](https://img.shields.io/badge/aiogram-3.4-blue)
![Static Badge](https://img.shields.io/badge/SQlAlchemy-2.0-blue)
![Static Badge](https://img.shields.io/badge/fpdf2-2.7.8-yellow)
## Как запустить
1. Клонируем репозиторий
   ```
   git clone git@github.com:almanelis/Diet-Advisor.git
   ```
2. Создаём и активируем виртуальное окружение
   ```
   python -m venv venv
   ```
   ```
   source venv/Scripts/activate
   ```
3. Устанавливаем зависимости
   ```
   pip install -r requirements.txt
   ```
4. Выполняем миграции
   ```
   alembic upgrade head
   ```
5. Запускаем бот
   ```
   python main.py
   ```
* для работы требуется токен бота, который нужно вписать в .env файл. За ним обратитесь в наш телеграм канал

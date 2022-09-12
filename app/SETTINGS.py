# Перед редактированием изучите README.md
# Путь до файла credentials.json
CREDENTIALS_PATH = r'..\credentials.json'

# ID Google Таблицы из ссылки
SPREADSHEET_ID = '1ZpHfkJAd4wtc2Gwby0V4VSzEWPCpJhm9_JEUh68CAac'

# Название листа в Google таблице
LIST_NAME = 'Лист1'


# Настройки базы данных PostgreSQL
DATABASE = {
    'drivername': 'postgresql',
    'host': '127.0.0.1',
    'port': '5432',
    'username': 'postgres',
    'password': '1111',
    'database': 'orders_info'
}
POSTGRE_TABLE_NAME = "orders"   # Название таблицы

# Частота обновления данных в секундах
UPDATE_TIME_SECOND = 15

# Курс доллара по умолчанию,если будет недоступен сайт ЦБ РФ
DOLLAR_CURRENCY = 60

# # # Настройки бота # # #
# Токен вашего бота, можно получить у https://t.me/BotFather
TELEGRAM_BOT_TOKEN = "2125766810:AAGdpiz-WAKAxLlhO24oKqr_YOfqyK8jVRg"

# https://t.me/getmyid_bot - написав этому боту
# можно узнать id своего профиля
TELEGRAM_USER_IDS = ["835655349", "471077694"]  # ID чатов, куда будут направляться оповещения

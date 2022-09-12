from datetime import datetime
from time import sleep

from sqlalchemy.orm import sessionmaker

import SETTINGS

from Sheet import Sheet
from CurrencyParser import get_dollar_rate
from TelegramAPI import send_message
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database

from Logger import get_logger

logger = get_logger()
DeclarativeBase = declarative_base()


# Модель БД
class Order(DeclarativeBase):
    __tablename__ = SETTINGS.POSTGRE_TABLE_NAME

    ordernumber = Column('ordernumber', Integer, primary_key=True)
    costdollar = Column('costdollar', Float, nullable=False)
    costruble = Column('costruble', Float, nullable=False)
    deliverytime = Column('deliverytime', DateTime, nullable=False)

    def __repr__(self):
        return "".format(self.OrderNumber)


def main():
    # Получаем курс доллара, если не удалось - берём
    # значение по умолчанию из файла настроек
    data = None  # Переменная для хранения данных Google таблицы
    dollar_rate = get_dollar_rate()
    if not dollar_rate:
        dollar_rate = float(SETTINGS.DOLLAR_CURRENCY)
        print(f"""Не удалось получить актуальный курс доллара,\n
                 беру значение по умолчанию из файла SETTINGS.py\n
                 {dollar_rate}
                """)

    try:
        # Подключаемся к Google таблице
        sheet = Sheet(
            credentials_file=SETTINGS.CREDENTIALS_PATH,
            sheet_id=SETTINGS.SPREADSHEET_ID,
        )
        # Получаем данные из Google таблицы
        data = sheet.read_list(SETTINGS.LIST_NAME)

    except Exception as e:
        logger.exception('Ошибка при подключении к Google sheets')

    try:
        # Подключаемся к БД
        engine = create_engine(URL(**SETTINGS.DATABASE))
        # Создаём БД, если не существует
        if not database_exists(engine.url):
            create_database(engine.url)
        # Создаём таблицу в БД, если не существует
        DeclarativeBase.metadata.create_all(engine)

        # Очищаем таблицу перед обновлением данных
        with engine.connect() as connection:
            connection.execute(f"TRUNCATE TABLE {SETTINGS.POSTGRE_TABLE_NAME}")

    except Exception as e:
        logger.exception('Ошибка при подключении к БД')

    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
    # bind передаем объект engine
    Session = sessionmaker(bind=engine)
    # Создаем объект сессии из вышесозданной фабрики Session
    with Session.begin() as session:
        # Начинаем заполнение
        report_message = ''  # Переменная для формирования отчёта о просроченных поставках
        count_overdue_orders = 0  # счётчик кол-во просроченных поставок
        for column_number in range(1, len(data[0])):
            try:
                new_post = Order(
                    ordernumber=int(data[1][column_number]),
                    costdollar=float(data[2][column_number].replace(',', '.')),
                    costruble=float(data[2][column_number].replace(',', '.')) * dollar_rate,
                    deliverytime=f'{data[3][column_number]}',
                )
            except Exception as e:
                logger.exception('Ошибка в данных Google sheets')
                continue

            try:
                session.add(new_post)
            except Exception as e:
                logger.exception('Ошибка при добавлении данных в БД')
                continue

            try:
                # Проверяем сроки поставки и формируем отчёт
                if datetime.now() > datetime.strptime(data[3][column_number], "%d.%m.%Y"):
                    report_message += """====================\n""" + \
                                      f"""Заказ №{data[1][column_number]} просрочен\n""" + \
                                      f"""Срок поставки {data[3][column_number]}\n""" + \
                                      f"""Сумма заказа {data[2][column_number]}$\n"""
                    count_overdue_orders += 1

            except Exception as e:
                logger.exception('Ошибка при составлении сообщения оповещения')

        report_message += f"====================\n" + \
                          f"Кол-во просроченных поставок {count_overdue_orders}"

    response = None  # Переменная для отчёта при перехвате ошибок
    try:
        # Рассылаем отчёт всем пользователям из списка
        for user_id in SETTINGS.TELEGRAM_USER_IDS:
            response = send_message(report_message, user_id, SETTINGS.TELEGRAM_BOT_TOKEN)

    except Exception as e:
        logger.exception('Ошибка при рассылке сообщений', extra={"response": response.text})


if __name__ == "__main__":
    logger.info('Приложение запущено!')
    # Запуск основного цикла
    while True:
        try:
            main()
        except Exception as e:
            logger.exception('Необработанное исключение')
        finally:
            sleep(SETTINGS.UPDATE_TIME_SECOND)

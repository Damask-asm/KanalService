from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Order

from settings import SETTINGS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'{SETTINGS.DATABASE["drivername"]}' \
                                        f'://{SETTINGS.DATABASE["username"]}:' \
                                        f'{SETTINGS.DATABASE["password"]}' \
                                        f'@{SETTINGS.DATABASE["host"]}' \
                                        f'/{SETTINGS.DATABASE["database"]}'
db = SQLAlchemy(app)
CORS(app)


def format_order(order: Order) -> dict:
    """
    Возвращает форматированный словарь со значением полей объекта Order
    :param order: Экземпляр объекта Order
    :return: словарь со значением полей объекта Order
    """
    return {
        'ordernumber': order.ordernumber,
        'costdollar': order.costdollar,
        'costruble': order.costruble,
        'deliverytime': order.deliverytime,
    }


# Вернёт все существующие записи Order в БД
@app.route("/orders", methods=["POST"])
def get_orders():
    orders = db.session.query(Order).all()
    order_list = []
    for order in orders:
        order_list.append(format_order(order))
    return {'count': len(order_list), 'orders': order_list}


if __name__ == "__main__":
    app.run()

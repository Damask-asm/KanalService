import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Order

from app import SETTINGS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'{SETTINGS.DATABASE["drivername"]}' \
                                        f'://{SETTINGS.DATABASE["username"]}:' \
                                        f'{SETTINGS.DATABASE["password"]}' \
                                        f'@{SETTINGS.DATABASE["host"]}' \
                                        f'/{SETTINGS.DATABASE["database"]}'
db = SQLAlchemy(app)


def format_order(order: Order) -> dict:
    """
    Возвращает форматированный словарь со значением полей объекта Order
    :param order: Экземпляр объекта Order
    :return: словарь со значением полей объекта Order
    """
    return {
        'ordernumber': order.ordernumber,
        'costdollar': int(order.costdollar),
        'costruble': int(order.costruble),
        'deliverytime': order.deliverytime.strftime("%d, %m, %Y"),
    }


# Вернёт все существующие записи Order в БД
@app.route("/", methods=["GET"])
def get_orders():
    # Заказы, отсортированные по дате
    orders = db.session.query(Order).order_by(Order.deliverytime.desc()).all()
    order_list = []
    for order in orders:
        order_list.append(format_order(order))
    print(order_list)
    return flask.render_template('index.html', context={'count': len(order_list), 'orders': order_list})


if __name__ == "__main__":
    app.run()

import requests
from requests import post


def send_message(text: str, channel_id: str, token: str) -> requests.Response:
    """Отправка сообщения ботом в чат с помощью TelegramAPI,
       Если сообщение слишком большое - отправляет отдельными
       сообщениями по 4_095 символов

    Parameters
    ----------
    text: str
        Текст сообщения
    channel_id: str
        ID чата, в который отправляется сообщение
    token: str
        Токен бота, который отправляет сообщение
    """
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"
    # У ТГ есть ограничение на кол-во символов в одном
    # сообщении 4_095 символов в одном соовщении,
    # разбиваем сообщение и посылаем в чат
    split_message_text = [text[i:i + 4_095] for i in range(0, len(text), 4_095)]

    for massage_text in split_message_text:
        request = post(method, data={
             "chat_id": channel_id,
             "text": massage_text
              })

    return request

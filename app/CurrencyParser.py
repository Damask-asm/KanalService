import xml.etree.ElementTree as ET
import requests


def get_dollar_rate():
    """Возвращает актуальный курс доллара в рублях, если запрос к сайту
        ЦБ РФ был успешен, иначе возвращает None
            """
    request = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    if request.ok:
        root = ET.fromstring(request.content)
        return float(root.find('.//Valute[@ID="R01235"]/Value').text.replace(',', '.'))
    else:
        return None

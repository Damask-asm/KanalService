import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    """Класс Sheet используется для работы с таблицами Google sheets

        Основное применение - чтение таблиц.

        Note:
            Требуется предварительная настройка Google API, получение файла credentials.json
            и настройка прав доступа к таблице

        Attributes
        ----------
        credentials_file : str
            полный путь до json файла полученного в Google Developer Console
        spreadsheet_id : str
            id из ссылки на таблицу
            https://docs.google.com/spreadsheets/d/
            1ZpHfkJAd4wtc2Gwby0V4VSzEWPCpJhm9_JEUh68CAac <--- Это ID
            /edit#gid=0

        Methods
        -------
        read_list(list_name: str) -> list
            Читает весь лист в таблице и возвращает в виде двумерного списка
        """

    # Авторизуемся и получаем service — экземпляр доступа к API
    def __init__(self, credentials_file: str, sheet_id: str):
        self.credentials_file = credentials_file
        self.spreadsheet_id = sheet_id
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    def read_list(self, list_name: str) -> list:
        """Чтение всего листа в таблице и возврат двумерного списка

        Parameters
        ----------
        list_name: str
            название листа в таблице

        """
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=list_name,
            majorDimension='COLUMNS'
        ).execute()
        return values['values']

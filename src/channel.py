import json
import os
from googleapiclient.discovery import build

# YOUTUBE_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YOUTUBE_API_KEY')


class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.youtube = None
        self.ch_request = None


    def api_key_youtube(self):
        """создать специальный объект для работы с API"""
        self.youtube = build('youtube', 'v3', developerKey = api_key)
        return self.youtube


    def print_info(self):
        """Выводит в консоль информацию о канале."""
        self.ch_request = (self.api_key_youtube().channels().
                           list(id=self.channel_id, part='snippet,statistics').execute())
        print(json.dumps(self.ch_request, indent = 2, ensure_ascii = False))

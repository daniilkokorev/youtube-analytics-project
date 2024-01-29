import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    # YOUTUBE_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.ch_request = (self.get_service().channels().
                           list(id=self.__channel_id, part='snippet,statistics').execute())
        # название канала
        self.title = self.ch_request["items"][0]["snippet"]["title"]
        # тема канала
        self.description = self.ch_request["items"][0]["snippet"]["description"]
        # ссылка на канал
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        # количество подписчиков
        self.subscriberCount = self.ch_request["items"][0]["statistics"]["subscriberCount"]
        # количество видео
        self.video_count = self.ch_request["items"][0]["statistics"]["videoCount"]
        # количество просмотров
        self.viewCount = self.ch_request["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        """
        создать специальный объект для работы с API
        """
        return build('youtube', 'v3', developerKey=Channel.api_key)

    def print_info(self):
        """
        Выводит в консоль информацию о канале.
        """
        print(json.dumps(self.ch_request, indent=4, ensure_ascii=False))

    @property
    # создаёт геттер для обращения к приватному экземпляру
    def channel_id(self):
        return self.__channel_id

    def to_json(self, json_file):
        """
        Сохраняет в Json файл значения атрибутов экземпляра - информацию о канале
        """
        data = {'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriberCount,
                'video_count': self.video_count,
                'view_count': self.viewCount
                }
        with open(json_file, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def __str__(self):
        """
        выводит название канала и ссылку на канал
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        выполняет сложение подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) + int(other.subscriberCount)}"

    def __sub__(self, other):
        """
        выполняет вычитание подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) - int(other.subscriberCount)}"

    def __sub__(self, other):
        """
        выполняет вычитание подписчиков двух каналов
        """
        return f"{int(other.subscriberCount) - int(self.subscriberCount)}"

    def __gt__(self, other):
        """
        сравнивает количество подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) > int(other.subscriberCount)}"

    def __ge__(self, other):
        """
        сравнивает количество подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) >= int(other.subscriberCount)}"

    def __lt__(self, other):
        """
        сравнивает количество подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) < int(other.subscriberCount)}"

    def __le__(self, other):
        """
        сравнивает количество подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) <= int(other.subscriberCount)}"

    def __eq__(self, other):
        """
        сравнивает количество подписчиков двух каналов
        """
        return f"{int(self.subscriberCount) == int(other.subscriberCount)}"

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from settings import API_KEY


class Video:
    """
    класс видео с ютуба
    """
    # YOUTUBE_API_KEY скопирован из гугла и вставлен в переменные окружения
    load_dotenv(API_KEY)
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id):
        """
        инициализирует id видео с ютуба.
        """
        self.video_id = video_id
        self.video_get = self.get_service().videos().list(id=self.video_id,
                        part='snippet,statistics,contentDetails,topicDetails').execute()
        # название видео
        self.video_name = self.video_get["items"][0]["snippet"]["title"]
        # ссылка на канал
        self.url = f"https://www.youtube.com/channel/{self.video_id}"
        # количество просмотров
        self.video_views = self.video_get["items"][0]["statistics"]["viewCount"]
        # количество лайков
        self.video_like = self.video_get["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.video_name

    @classmethod
    def get_service(cls):
        """
        создать специальный объект для работы с API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    """класс для плейлистов видео"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,).execute()

    def __str__(self):
        return self.video_name

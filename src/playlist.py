import os
import datetime
from pprint import pprint

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build
from settings import API_KEY


class PlayList:
    """
    класс содержит плайлист видео с ютуба
    """
    # YOUTUBE_API_KEY скопирован из гугла и вставлен в переменные окружения
    load_dotenv(API_KEY)
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_data = self.get_service().playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails,snippet',
                                                maxResults=50,).execute()
        # название плайлиста
        self.title = self.playlist_data["items"][0]["snippet"]["title"][0:24]
        # ссылка на видео
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        # id всех видео в плейлисте
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_data['items']]
        # статистика видео
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()

    @classmethod
    def get_service(cls):
        """
        создать специальный объект для работы с API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self):
        """
        считает суммарную длительность плейлиста
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # Длительность видео на YouTube указана в формате ISO 8601
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """
        выводит ссылку видео с максимальным количеством лайков
        """
        # содержит максимальное количество лайков видео
        max_likecount = 0
        # содержит ссалку на видео с максимальным количкством лайков
        max_videourl = ''
        # запускает цикл проверки статистики видео
        for video in self.video_response['items']:
            like_count = video['statistics']['likeCount']
            id_video = video['id']
            # проверяет условие по количеству лайков видео
            if int(like_count) > int(max_likecount):
                max_likecount = like_count
                max_videourl = id_video
        return f"https://youtu.be/{max_videourl}"

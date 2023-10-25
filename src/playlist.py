import os

from googleapiclient.discovery import build

import isodate
import datetime

class PlayList:
    def __init__(self, playlist_id: str) -> None:

        self.playlist_id = playlist_id
        playlist_info = self.get_service().playlists().list(id=self.playlist_id, part='snippet', ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API"""

        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)"""

        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        duration = 0
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration).total_seconds()
        return datetime.timedelta(seconds=duration)

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        best_video = max(video_response['items'], key=lambda x:x['statistics']['likeCount'])
        return f"https://youtu.be/{best_video['id']}"



# string = 'PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw'
# api_key: str = os.getenv('API_KEY')
# youtube = build('youtube', 'v3', developerKey=api_key)
# playlist_info =youtube.playlists().list(id = 'PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw', part='snippet',).execute()
# title = playlist_info['items'][0]['snippet']['title']
# url = f'https://www.youtube.com/playlist?list={string}'
# print(playlist_info)
# print(title)
# print(url)

# pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# assert pl.title == "Moscow Python Meetup №81"
# assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
# print(pl.title)
# print(pl.url)
# duration = pl.total_duration()
# print(duration)
# duration = pl.total_duration
# assert str(duration) == "1:49:52"
# print(str(duration))
# assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"

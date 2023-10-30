import os

from googleapiclient.discovery import build

class Video:

    def __init__(self, video_id: str) -> None:
        """Инициализация следующих атрибутов экземпляра класса Video:
         id видео, название видео, ссылка на видео, количество  просмотров, количество лайков"""

        self.video_id = video_id
        try:
            self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.video_id
                                       ).execute()
            self.title = str(self.video_response['items'][0]['snippet']['title'])
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = int(self.video_response['items'][0]['statistics']['viewCount'])
            self.like_count = int(self.video_response['items'][0]['statistics']['likeCount'])
        except IndexError:
        #     print("Несуществующий id видео.")
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API"""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f"{self.video_title}"

class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str)-> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

# video1 = Video('gaoc9MPZ4bw')
# print(video1.video_title)
# print(str(video1))

# api_key: str = os.getenv('API_KEY')
# youtube = build('youtube', 'v3', developerKey=api_key)
#
# video_id = 'gaoc9MPZ4bw'
# video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
#                                        id=video_id
#                                        ).execute()
# # printj(video_response)
# video_title: str = video_response['items'][0]['snippet']['title']
# view_count: int = video_response['items'][0]['statistics']['viewCount']
# like_count: int = video_response['items'][0]['statistics']['likeCount']
# comment_count: int = video_response['items'][0]['statistics']['commentCount']
#
# print(video_title)
# print(view_count)
# print(like_count)
# print(comment_count)

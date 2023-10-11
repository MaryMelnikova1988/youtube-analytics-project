import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
         Модернизация/после инициализации экземпляр имел следующие атрибуты: id канала, название канала,
         описание канала,ссылка на канал, количество подписчиков, количество видео, общее количество просмотров"""

        self.channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        # channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API"""
        return youtube

    def to_json(self, filename) -> None:
        """сохраняет в json-файл значения атрибутов экземпляра Channel"""
        with open(file=filename, mode='w', encoding='utf-8') as f:
            json.dump(self.channel, f, indent=4, ensure_ascii=False)

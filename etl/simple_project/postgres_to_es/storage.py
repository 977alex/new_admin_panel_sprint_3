import abc
import datetime
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.default_state = {}
        self.file_path = file_path
        self.default_state['last_sync_timestamp'] = str(datetime.datetime(2000, 1, 1, tzinfo=None))
        self.default_state['filmwork_ids'] = []

        # self.default_state = {
        #     "last_sync_timestamp": "2018-11-11 11:11:11.471642",
        #     "filmwork_ids": [],
        # }

    def retrieve_state(self) -> dict:
        try:

            with open(self.file_path) as file:
                # читаем json
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            # если возникло исключение
            with open(self.file_path, "w", encoding="utf8") as file:

                # создаем json с дефолтным значением self.default_state

                json.dump(self.default_state, file)

            return self.retrieve_state()

    def save_state(self, state: dict) -> None:
        """
        метод сохранения состояния в json файле
        """

        # получаем состояние из json
        data = self.retrieve_state()
        # обновляем состояние на новое
        data.update(state)
        # записываем его в json
        with open(self.file_path, "w", encoding="utf8") as file:
            json.dump(data, file)


class State:
    """
    Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала (в случае остановки).
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        data = self.storage.retrieve_state()
        return data.get(key, None)

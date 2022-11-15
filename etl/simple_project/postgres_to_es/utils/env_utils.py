import os

from pydantic import BaseSettings, Field
import dotenv

dotenv.load_dotenv()  # для дебага вне докера


class Dsn(BaseSettings):
    dbname: str = Field(env="postgres_db")
    user: str = ...
    password: str = ...
    host: str = Field(env="db_host")
    port: str = Field(env="db_port")

    class Config:
        env_prefix = 'postgres_'

    # dbname: str = Field(os.environ.get("POSTGRES_DB"), env="postgres_db")
    # user: str = Field(os.environ.get("POSTGRES_USER"), env="postgres_user")
    # password: str = Field(os.environ.get("POSTGRES_PASSWORD"), env="postgres_password")
    # host: str = Field(os.environ.get("DB_HOST"), env="db_host")
    # port: str = Field(os.environ.get("DB_PORT"), env="db_port")


class EsBaseUrl(BaseSettings):
    """
    определяет host и port у ElasticSearch
    """

    es_host: str = Field(env="ES_HOST")
    es_port: str = Field(env="ES_PORT")

    # es_host: str = Field(os.environ.get("ES_HOST"), env="ES_HOST")
    # es_port: str = Field(os.environ.get("ES_PORT"), env="ES_PORT")

    def get_url(self):
        """
        возвращает url ElasticSearch
        """
        return "http://{}:{}".format(self.es_host, self.es_port)


class BaseConfig(BaseSettings):
    chunk_size: int = Field(50, env="CHUNK_SIZE")
    sleep_time: float = Field(60.0, env="ETL_SLEEP")
    es_base_url: str = EsBaseUrl().get_url()
    dsn: dict = Dsn().dict()

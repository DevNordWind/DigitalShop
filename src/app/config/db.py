from dataclasses import dataclass

from sqlalchemy import URL


@dataclass(frozen=True, slots=True)
class SqlAlchemyConfig:
    echo: bool
    hide_parameters: bool
    pool_pre_ping: bool

    max_overflow: int
    pool_size: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DatabaseConfig:
    db: str
    host: str
    port: int
    username: str
    password: str

    driver: str = "psycopg"
    db_system: str = "postgresql"

    sql_alchemy: SqlAlchemyConfig

    @property
    def connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.db_system}+{self.driver}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        ).render_as_string(False)

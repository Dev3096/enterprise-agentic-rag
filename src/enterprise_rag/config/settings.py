from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise Agentic RAG"
    environment: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "enterprise_rag"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    openai_api_key: str | None = None
    openai_model: str = "gpt-5.4"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
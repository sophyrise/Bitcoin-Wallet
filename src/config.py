from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    admin_api_key: str = "change-this-admin-key"
    database_path: str = "bitcoin_wallet.db"
    btc_usd_api_url: str = "https://api.coinbase.com/v2/exchange-rates?currency=BTC"
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


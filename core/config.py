from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/freelance_db"
    JWT_SECRET: str = "your_jwt_secret_here"
    JWT_REFRESH_SECRET: str = "your_jwt_refresh_secret_here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EMAIL_PROVIDER: str = "smtp"
    EMAIL_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@freelancemarketplace.com"
    FRONTEND_URL: str = "http://localhost:3000"
    BLOCKCHAIN_RPC_URL: str = "http://127.0.0.1:8545"
    BLOCKCHAIN_CONTRACT_ADDRESS: str = ""
    BLOCKCHAIN_PRIVATE_KEY: str = ""
    AI_API_KEY: str = ""
    VECTOR_DATABASE_URL: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

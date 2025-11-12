import os
from typing import List

class Settings:
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "SkillLink API"
    APP_VERSION: str = "1.0.0"
    
    # 环境
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS 配置
    @property
    def CORS_ORIGINS(self) -> List[str]:
        origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173"
        )
        return [origin.strip() for origin in origins.split(",")]
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )
    
    # JWT 配置（预留）
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()


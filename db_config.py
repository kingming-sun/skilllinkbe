"""
数据库配置和连接管理
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Generator
import os

from db_models import Base

# 数据库连接 URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Neon 推荐使用 NullPool
    echo=False,  # 生产环境设为 False
    future=True
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    使用依赖注入在 FastAPI 路由中使用：
    def my_route(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库（创建所有表）
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_db():
    """
    删除所有表（慎用！）
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped!")


if __name__ == "__main__":
    # 直接运行此文件可以初始化数据库
    print("Initializing database...")
    init_db()


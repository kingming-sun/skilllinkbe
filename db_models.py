"""
SQLAlchemy 数据库模型
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class UserRoleEnum(str, enum.Enum):
    USER = "user"
    PROVIDER = "provider"
    ADMIN = "admin"


class SkillCategoryEnum(str, enum.Enum):
    SPORTS = "sports"
    MUSIC = "music"
    PROGRAMMING = "programming"
    LANGUAGE = "language"
    VOLUNTEER = "volunteer"
    ART = "art"
    OTHER = "other"


class ServiceModeEnum(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BOTH = "both"


class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(SQLEnum(UserRoleEnum), default=UserRoleEnum.USER, nullable=False)
    avatar = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_student = Column(Boolean, default=False)
    university = Column(String(200), nullable=True)
    major = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关系
    skills = relationship("SkillModel", back_populates="provider", foreign_keys="SkillModel.provider_id")
    orders_as_user = relationship("OrderModel", back_populates="user", foreign_keys="OrderModel.user_id")
    orders_as_provider = relationship("OrderModel", back_populates="provider", foreign_keys="OrderModel.provider_id")
    reviews = relationship("ReviewModel", back_populates="user", foreign_keys="ReviewModel.user_id")


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(SkillCategoryEnum), nullable=False, index=True)
    price_per_hour = Column(Float, nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    service_mode = Column(SQLEnum(ServiceModeEnum), nullable=False)
    location = Column(String(500), nullable=True)
    tags = Column(Text, nullable=True)  # 存储为逗号分隔的字符串
    is_active = Column(Boolean, default=True, nullable=False)
    views_count = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    provider = relationship("UserModel", back_populates="skills", foreign_keys=[provider_id])
    orders = relationship("OrderModel", back_populates="skill")
    reviews = relationship("ReviewModel", back_populates="skill")


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(SQLEnum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False, index=True)
    scheduled_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    platform_fee = Column(Float, nullable=False)
    provider_amount = Column(Float, nullable=False)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # 关系
    user = relationship("UserModel", back_populates="orders_as_user", foreign_keys=[user_id])
    provider = relationship("UserModel", back_populates="orders_as_provider", foreign_keys=[provider_id])
    skill = relationship("SkillModel", back_populates="orders")
    review = relationship("ReviewModel", back_populates="order", uselist=False)


class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关系
    order = relationship("OrderModel", back_populates="review")
    skill = relationship("SkillModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews", foreign_keys=[user_id])


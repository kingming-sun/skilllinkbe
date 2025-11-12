from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    """用户角色"""
    USER = "user"  # 普通用户（需求方）
    PROVIDER = "provider"  # 服务提供者
    ADMIN = "admin"  # 管理员


class SkillCategory(str, Enum):
    """技能分类"""
    SPORTS = "sports"  # 运动
    MUSIC = "music"  # 音乐
    PROGRAMMING = "programming"  # 编程
    LANGUAGE = "language"  # 语言
    VOLUNTEER = "volunteer"  # 志愿服务
    ART = "art"  # 艺术
    OTHER = "other"  # 其他


class ServiceMode(str, Enum):
    """服务模式"""
    ONLINE = "online"  # 线上
    OFFLINE = "offline"  # 线下
    BOTH = "both"  # 两者皆可


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"  # 待确认
    CONFIRMED = "confirmed"  # 已确认
    PAID = "paid"  # 已支付
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    REFUNDED = "refunded"  # 已退款


# ============= 用户模型 =============

class UserBase(BaseModel):
    """用户基础信息"""
    email: EmailStr
    username: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    """用户注册"""
    password: str


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class User(UserBase):
    """用户完整信息"""
    id: int
    avatar: Optional[str] = None
    is_verified: bool = False
    is_student: bool = False
    university: Optional[str] = None
    major: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(User):
    """用户档案（包含统计信息）"""
    total_orders: int = 0
    total_skills: int = 0
    average_rating: float = 0.0


# ============= 技能模型 =============

class SkillBase(BaseModel):
    """技能基础信息"""
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    category: SkillCategory
    price_per_hour: float = Field(..., gt=0)
    duration_minutes: int = Field(default=60, gt=0)
    service_mode: ServiceMode
    location: Optional[str] = None
    tags: List[str] = []


class SkillCreate(SkillBase):
    """创建技能"""
    pass


class SkillUpdate(BaseModel):
    """更新技能"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[SkillCategory] = None
    price_per_hour: Optional[float] = None
    duration_minutes: Optional[int] = None
    service_mode: Optional[ServiceMode] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Skill(SkillBase):
    """技能完整信息"""
    id: int
    provider_id: int
    provider_name: str
    provider_avatar: Optional[str] = None
    provider_university: Optional[str] = None
    is_active: bool = True
    views_count: int = 0
    orders_count: int = 0
    average_rating: float = 0.0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SkillSearchParams(BaseModel):
    """技能搜索参数"""
    keyword: Optional[str] = None
    category: Optional[SkillCategory] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    service_mode: Optional[ServiceMode] = None
    location: Optional[str] = None
    min_rating: Optional[float] = None
    page: int = 1
    page_size: int = 20


# ============= 订单模型 =============

class OrderBase(BaseModel):
    """订单基础信息"""
    skill_id: int
    scheduled_date: datetime
    message: Optional[str] = None


class OrderCreate(OrderBase):
    """创建订单"""
    pass


class Order(OrderBase):
    """订单完整信息"""
    id: int
    order_number: str
    user_id: int
    provider_id: int
    status: OrderStatus
    total_amount: float
    platform_fee: float
    provider_amount: float
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    # 关联信息
    skill_title: str
    user_name: str
    provider_name: str
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """更新订单状态"""
    status: OrderStatus
    note: Optional[str] = None


# ============= 评价模型 =============

class ReviewBase(BaseModel):
    """评价基础信息"""
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=500)


class ReviewCreate(ReviewBase):
    """创建评价"""
    order_id: int


class Review(ReviewBase):
    """评价完整信息"""
    id: int
    order_id: int
    skill_id: int
    user_id: int
    provider_id: int
    user_name: str
    user_avatar: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= 响应模型 =============

class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
    code: int = 200


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: User


class PaginatedResponse(BaseModel):
    """分页响应"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Any]


class SkillListResponse(BaseModel):
    """技能列表响应"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Skill]


class OrderListResponse(BaseModel):
    """订单列表响应"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Order]


class ReviewListResponse(BaseModel):
    """评价列表响应"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Review]


# ============= 统计模型 =============

class DashboardStats(BaseModel):
    """仪表盘统计"""
    total_users: int
    total_skills: int
    total_orders: int
    total_reviews: int
    active_providers: int
    total_revenue: float


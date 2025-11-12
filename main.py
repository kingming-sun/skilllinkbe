from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import math

from models import (
    User, UserProfile, UserCreate, UserLogin, TokenResponse,
    Skill, SkillCreate, SkillListResponse,
    Order, OrderCreate, OrderStatus, OrderStatusUpdate, OrderListResponse,
    Review, ReviewCreate, ReviewListResponse,
    MessageResponse, DashboardStats,
    UserRole, SkillCategory, ServiceMode
)
from db_config import get_db, engine
from db_models import Base, UserModel, SkillModel, OrderModel, ReviewModel
import crud
from database import generate_order_number
from config import settings
from auth import get_current_user_from_token, get_optional_current_user
from security import create_access_token

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="短期技能交互平台 API",
    version=settings.APP_VERSION
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= 辅助函数 =============

def get_current_user(
    current_user: UserModel = Depends(get_current_user_from_token)
) -> UserModel:
    """获取当前登录用户"""
    return current_user


def user_model_to_dict(user: UserModel) -> User:
    """将UserModel转换为User Pydantic模型"""
    return User(
        id=user.id,
        email=user.email,
        username=user.username,
        phone=user.phone,
        role=UserRole(user.role),
        avatar=user.avatar,
        is_verified=user.is_verified,
        is_student=user.is_student,
        university=user.university,
        major=user.major,
        created_at=user.created_at
    )


def skill_model_to_dict(skill: SkillModel, db: Session) -> Skill:
    """将SkillModel转换为Skill Pydantic模型"""
    provider = crud.get_user_by_id(db, skill.provider_id)
    return Skill(
        id=skill.id,
        provider_id=skill.provider_id,
        provider_name=provider.username if provider else "未知",
        provider_avatar=provider.avatar if provider else None,
        provider_university=provider.university if provider else None,
        title=skill.title,
        description=skill.description,
        category=SkillCategory(skill.category),
        price_per_hour=skill.price_per_hour,
        duration_minutes=skill.duration_minutes,
        service_mode=ServiceMode(skill.service_mode),
        location=skill.location,
        tags=skill.tags.split(",") if skill.tags else [],
        is_active=skill.is_active,
        views_count=skill.views_count,
        orders_count=skill.orders_count,
        average_rating=skill.average_rating,
        created_at=skill.created_at,
        updated_at=skill.updated_at
    )


def order_model_to_dict(order: OrderModel, db: Session) -> Order:
    """将OrderModel转换为Order Pydantic模型"""
    skill = crud.get_skill_by_id(db, order.skill_id)
    user = crud.get_user_by_id(db, order.user_id)
    provider = crud.get_user_by_id(db, order.provider_id)
    
    return Order(
        id=order.id,
        order_number=order.order_number,
        user_id=order.user_id,
        provider_id=order.provider_id,
        skill_id=order.skill_id,
        status=OrderStatus(order.status),
        scheduled_date=order.scheduled_date,
        total_amount=order.total_amount,
        platform_fee=order.platform_fee,
        provider_amount=order.provider_amount,
        message=order.message,
        created_at=order.created_at,
        updated_at=order.updated_at,
        completed_at=order.completed_at,
        skill_title=skill.title if skill else "未知技能",
        user_name=user.username if user else "未知用户",
        provider_name=provider.username if provider else "未知"
    )


def review_model_to_dict(review: ReviewModel, db: Session) -> Review:
    """将ReviewModel转换为Review Pydantic模型"""
    user = crud.get_user_by_id(db, review.user_id)
    return Review(
        id=review.id,
        order_id=review.order_id,
        skill_id=review.skill_id,
        user_id=review.user_id,
        provider_id=review.provider_id,
        user_name=user.username if user else "未知用户",
        user_avatar=user.avatar if user else None,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at
    )


# ============= 根路径 =============

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用 SkillLink API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """健康检查"""
    try:
        # 测试数据库连接
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "message": "SkillLink API 运行正常",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": "数据库连接失败",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# ============= 用户认证 =============

@app.post("/api/auth/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """用户注册"""
    # 检查邮箱是否已存在
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 创建用户
    new_user = crud.create_user(db, user_data)
    
    # 生成 JWT token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_model_to_dict(new_user)
    )


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录"""
    # 验证用户
    user = crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_model_to_dict(user)
    )


@app.get("/api/auth/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户信息"""
    # 统计用户信息
    user_orders, _ = crud.get_orders(db, current_user.id)
    user_skills, _ = crud.get_skills(db, skip=0, limit=1000)
    user_skills = [s for s in user_skills if s.provider_id == current_user.id]
    
    reviews = db.query(ReviewModel).filter(ReviewModel.provider_id == current_user.id).all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0.0
    
    return UserProfile(
        **user_model_to_dict(current_user).model_dump(),
        total_orders=len(user_orders),
        total_skills=len(user_skills),
        average_rating=round(avg_rating, 1)
    )


# ============= 技能管理 =============

@app.get("/api/skills", response_model=SkillListResponse)
async def get_skills(
    keyword: Optional[str] = None,
    category: Optional[SkillCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    service_mode: Optional[ServiceMode] = None,
    min_rating: Optional[float] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """获取技能列表（支持搜索和筛选）"""
    skip = (page - 1) * page_size
    
    skills, total = crud.get_skills(
        db, skip=skip, limit=page_size,
        keyword=keyword, category=category,
        min_price=min_price, max_price=max_price,
        service_mode=service_mode, min_rating=min_rating
    )
    
    total_pages = math.ceil(total / page_size)
    
    skill_items = [skill_model_to_dict(skill, db) for skill in skills]
    
    return SkillListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=skill_items
    )


@app.get("/api/skills/{skill_id}", response_model=Skill)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """获取技能详情"""
    skill = crud.get_skill_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    
    return skill_model_to_dict(skill, db)


@app.post("/api/skills", response_model=Skill)
async def create_skill(
    skill_data: SkillCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建技能（仅服务提供者）"""
    if current_user.role not in ["provider", "admin"]:
        raise HTTPException(status_code=403, detail="只有服务提供者可以发布技能")
    
    new_skill = crud.create_skill(db, skill_data, current_user.id)
    return skill_model_to_dict(new_skill, db)


@app.get("/api/skills/{skill_id}/reviews", response_model=ReviewListResponse)
async def get_skill_reviews(
    skill_id: int,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """获取技能的评价列表"""
    skip = (page - 1) * page_size
    reviews, total = crud.get_skill_reviews(db, skill_id, skip=skip, limit=page_size)
    
    total_pages = math.ceil(total / page_size)
    review_items = [review_model_to_dict(review, db) for review in reviews]
    
    return ReviewListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=review_items
    )


# ============= 订单管理 =============

@app.post("/api/orders", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建订单"""
    try:
        order_number = generate_order_number()
        new_order = crud.create_order(db, order_data, current_user.id, order_number)
        return order_model_to_dict(new_order, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/orders", response_model=OrderListResponse)
async def get_orders(
    status: Optional[OrderStatus] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单列表"""
    skip = (page - 1) * page_size
    orders, total = crud.get_orders(db, current_user.id, status=status, skip=skip, limit=page_size)
    
    total_pages = math.ceil(total / page_size)
    order_items = [order_model_to_dict(order, db) for order in orders]
    
    return OrderListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=order_items
    )


@app.get("/api/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单详情"""
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查权限
    if order.user_id != current_user.id and order.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问该订单")
    
    return order_model_to_dict(order, db)


@app.patch("/api/orders/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新订单状态"""
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查权限
    if order.user_id != current_user.id and order.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改该订单")
    
    try:
        updated_order = crud.update_order_status(db, order_id, status_update.status)
        return order_model_to_dict(updated_order, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============= 评价系统 =============

@app.post("/api/reviews", response_model=Review)
async def create_review(
    review_data: ReviewCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建评价"""
    # 检查订单是否存在且已完成
    order = crud.get_order_by_id(db, review_data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能评价自己的订单")
    
    if order.status != OrderStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="订单未完成，无法评价")
    
    # 检查是否已评价
    if crud.check_review_exists(db, order.id):
        raise HTTPException(status_code=400, detail="该订单已评价")
    
    try:
        new_review = crud.create_review(db, review_data, current_user.id)
        return review_model_to_dict(new_review, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============= 统计数据 =============

@app.get("/api/stats", response_model=DashboardStats)
async def get_stats(db: Session = Depends(get_db)):
    """获取统计数据"""
    stats = crud.get_stats(db)
    return DashboardStats(**stats)


@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    """获取技能分类及统计"""
    return crud.get_categories(db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

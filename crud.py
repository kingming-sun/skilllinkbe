"""
CRUD 操作（Create, Read, Update, Delete）
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from datetime import datetime

from db_models import UserModel, SkillModel, OrderModel, ReviewModel
from models import (
    UserCreate, SkillCreate, OrderCreate, ReviewCreate,
    UserRole, SkillCategory, ServiceMode, OrderStatus
)


# ============= User CRUD =============

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """根据邮箱获取用户"""
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    """根据ID获取用户"""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> UserModel:
    """创建用户"""
    db_user = UserModel(
        email=user.email,
        username=user.username,
        password=user.password,  # 实际应该加密
        phone=user.phone,
        role=user.role,
        avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.username}",
        is_verified=False,
        is_student=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ============= Skill CRUD =============

def get_skills(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    keyword: Optional[str] = None,
    category: Optional[SkillCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    service_mode: Optional[ServiceMode] = None,
    min_rating: Optional[float] = None
) -> tuple[List[SkillModel], int]:
    """获取技能列表（带筛选）"""
    query = db.query(SkillModel).filter(SkillModel.is_active == True)
    
    # 关键词搜索
    if keyword:
        search_term = f"%{keyword}%"
        query = query.filter(
            or_(
                SkillModel.title.ilike(search_term),
                SkillModel.description.ilike(search_term),
                SkillModel.tags.ilike(search_term)
            )
        )
    
    # 分类筛选
    if category:
        query = query.filter(SkillModel.category == category)
    
    # 价格筛选
    if min_price is not None:
        query = query.filter(SkillModel.price_per_hour >= min_price)
    if max_price is not None:
        query = query.filter(SkillModel.price_per_hour <= max_price)
    
    # 服务模式筛选
    if service_mode:
        query = query.filter(
            or_(
                SkillModel.service_mode == service_mode,
                SkillModel.service_mode == ServiceMode.BOTH
            )
        )
    
    # 评分筛选
    if min_rating is not None:
        query = query.filter(SkillModel.average_rating >= min_rating)
    
    # 排序
    query = query.order_by(
        SkillModel.average_rating.desc(),
        SkillModel.orders_count.desc()
    )
    
    # 获取总数
    total = query.count()
    
    # 分页
    skills = query.offset(skip).limit(limit).all()
    
    return skills, total


def get_skill_by_id(db: Session, skill_id: int) -> Optional[SkillModel]:
    """获取技能详情"""
    skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if skill:
        # 增加浏览次数
        skill.views_count += 1
        db.commit()
    return skill


def create_skill(db: Session, skill: SkillCreate, provider_id: int) -> SkillModel:
    """创建技能"""
    db_skill = SkillModel(
        provider_id=provider_id,
        title=skill.title,
        description=skill.description,
        category=skill.category,
        price_per_hour=skill.price_per_hour,
        duration_minutes=skill.duration_minutes,
        service_mode=skill.service_mode,
        location=skill.location,
        tags=",".join(skill.tags) if skill.tags else "",
        is_active=True,
        views_count=0,
        orders_count=0,
        average_rating=0.0
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


# ============= Order CRUD =============

def create_order(db: Session, order: OrderCreate, user_id: int, order_number: str) -> OrderModel:
    """创建订单"""
    # 获取技能信息
    skill = get_skill_by_id(db, order.skill_id)
    if not skill:
        raise ValueError("Skill not found")
    
    # 计算金额
    total_amount = skill.price_per_hour * (skill.duration_minutes / 60)
    platform_fee = total_amount * 0.15
    provider_amount = total_amount - platform_fee
    
    db_order = OrderModel(
        order_number=order_number,
        user_id=user_id,
        provider_id=skill.provider_id,
        skill_id=order.skill_id,
        status=OrderStatus.PENDING,
        scheduled_date=order.scheduled_date,
        total_amount=round(total_amount, 2),
        platform_fee=round(platform_fee, 2),
        provider_amount=round(provider_amount, 2),
        message=order.message
    )
    
    db.add(db_order)
    
    # 更新技能订单数
    skill.orders_count += 1
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(
    db: Session,
    user_id: int,
    status: Optional[OrderStatus] = None,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[OrderModel], int]:
    """获取订单列表"""
    query = db.query(OrderModel).filter(
        or_(
            OrderModel.user_id == user_id,
            OrderModel.provider_id == user_id
        )
    )
    
    if status:
        query = query.filter(OrderModel.status == status)
    
    query = query.order_by(OrderModel.created_at.desc())
    
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return orders, total


def get_order_by_id(db: Session, order_id: int) -> Optional[OrderModel]:
    """获取订单详情"""
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()


def update_order_status(db: Session, order_id: int, status: OrderStatus) -> OrderModel:
    """更新订单状态"""
    order = get_order_by_id(db, order_id)
    if not order:
        raise ValueError("Order not found")
    
    order.status = status
    order.updated_at = datetime.utcnow()
    
    if status == OrderStatus.COMPLETED:
        order.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    return order


# ============= Review CRUD =============

def create_review(db: Session, review: ReviewCreate, user_id: int) -> ReviewModel:
    """创建评价"""
    # 获取订单信息
    order = get_order_by_id(db, review.order_id)
    if not order:
        raise ValueError("Order not found")
    
    db_review = ReviewModel(
        order_id=order.id,
        skill_id=order.skill_id,
        user_id=user_id,
        provider_id=order.provider_id,
        rating=review.rating,
        comment=review.comment
    )
    
    db.add(db_review)
    
    # 更新技能评分
    skill = get_skill_by_id(db, order.skill_id)
    if skill:
        reviews = db.query(ReviewModel).filter(ReviewModel.skill_id == skill.id).all()
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        skill.average_rating = round(avg_rating, 1)
    
    db.commit()
    db.refresh(db_review)
    return db_review


def get_skill_reviews(
    db: Session,
    skill_id: int,
    skip: int = 0,
    limit: int = 10
) -> tuple[List[ReviewModel], int]:
    """获取技能的评价列表"""
    query = db.query(ReviewModel).filter(ReviewModel.skill_id == skill_id)
    query = query.order_by(ReviewModel.created_at.desc())
    
    total = query.count()
    reviews = query.offset(skip).limit(limit).all()
    
    return reviews, total


def check_review_exists(db: Session, order_id: int) -> bool:
    """检查订单是否已评价"""
    return db.query(ReviewModel).filter(ReviewModel.order_id == order_id).first() is not None


# ============= Statistics =============

def get_stats(db: Session) -> dict:
    """获取平台统计"""
    total_users = db.query(UserModel).count()
    total_skills = db.query(SkillModel).count()
    total_orders = db.query(OrderModel).count()
    total_reviews = db.query(ReviewModel).count()
    active_providers = db.query(UserModel).filter(UserModel.role == UserRole.PROVIDER).count()
    
    completed_orders = db.query(OrderModel).filter(OrderModel.status == OrderStatus.COMPLETED).all()
    total_revenue = sum(order.total_amount for order in completed_orders)
    
    return {
        "total_users": total_users,
        "total_skills": total_skills,
        "total_orders": total_orders,
        "total_reviews": total_reviews,
        "active_providers": active_providers,
        "total_revenue": round(total_revenue, 2)
    }


def get_categories(db: Session) -> dict:
    """获取分类统计"""
    categories = db.query(
        SkillModel.category,
        func.count(SkillModel.id).label('count')
    ).filter(
        SkillModel.is_active == True
    ).group_by(
        SkillModel.category
    ).all()
    
    return {
        "categories": [
            {"label": cat.value, "count": count}
            for cat, count in categories
        ]
    }


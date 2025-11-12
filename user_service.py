"""
用户服务 - 同步 Stack Auth 用户到本地数据库
"""
from sqlalchemy.orm import Session
from db_models import UserModel
from typing import Optional


def sync_user_from_auth(db: Session, auth_payload: dict) -> UserModel:
    """
    从 Stack Auth 同步用户到本地数据库
    
    Args:
        db: 数据库会话
        auth_payload: Stack Auth JWT payload
    
    Returns:
        UserModel: 本地数据库用户对象
    """
    stack_user_id = auth_payload.get("sub")  # Stack Auth user ID
    email = auth_payload.get("email")
    email_verified = auth_payload.get("email_verified", False)
    
    # 检查用户是否已存在（通过邮箱）
    user = db.query(UserModel).filter(UserModel.email == email).first()
    
    if user:
        # 更新用户信息
        user.is_verified = email_verified
        # 可以存储 Stack Auth ID 到 avatar 字段或添加新字段
        if not user.avatar or not user.avatar.startswith("https://api.dicebear.com"):
            user.avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={stack_user_id}"
    else:
        # 创建新用户
        username = email.split("@")[0]  # 从邮箱提取用户名
        user = UserModel(
            email=email,
            username=username,
            password="",  # Stack Auth 管理密码，本地不存储
            role="user",  # 默认角色
            avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={stack_user_id}",
            is_verified=email_verified,
            is_student=False
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(db: Session, auth_payload: dict) -> UserModel:
    """
    获取或创建用户（便捷方法）
    """
    return sync_user_from_auth(db, auth_payload)


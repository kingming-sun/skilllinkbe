"""
Stack Auth (Neon Auth) 集成
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
from functools import lru_cache
from typing import Optional
import os

security = HTTPBearer()

# Stack Auth 配置
STACK_PROJECT_ID = os.getenv("STACK_PROJECT_ID", "29a175ee-764e-4b93-890d-7f0fd0ad8835")
JWKS_URL = f"https://api.stack-auth.com/api/v1/projects/{STACK_PROJECT_ID}/.well-known/jwks.json"


@lru_cache()
def get_jwks():
    """获取并缓存 JWKS (JSON Web Key Set)"""
    try:
        response = requests.get(JWKS_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching JWKS: {e}")
        return None


def verify_stack_auth_token(token: str) -> dict:
    """
    验证 Stack Auth JWT Token
    
    Returns:
        dict: 包含用户信息的 payload
    """
    try:
        # 获取 JWKS
        jwks = get_jwks()
        if not jwks:
            raise HTTPException(status_code=500, detail="无法获取认证密钥")
        
        # 解码 token header 以获取 kid
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        
        # 从 JWKS 中找到对应的密钥
        key = None
        for jwk in jwks.get("keys", []):
            if jwk.get("kid") == kid:
                key = jwk
                break
        
        if not key:
            raise HTTPException(status_code=401, detail="无效的认证密钥")
        
        # 验证并解码 token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=STACK_PROJECT_ID,
            options={"verify_aud": True}
        )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token 验证失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"认证错误: {str(e)}")


def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    从 JWT Token 获取当前用户信息
    
    Returns:
        dict: 用户信息，包含:
            - sub: 用户 ID (Stack Auth user ID)
            - email: 用户邮箱
            - email_verified: 邮箱是否已验证
            等其他 Stack Auth 提供的字段
    """
    token = credentials.credentials
    payload = verify_stack_auth_token(token)
    
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="无效的用户信息")
    
    return payload


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    可选的用户认证（不强制要求登录）
    """
    if not credentials:
        return None
    
    try:
        return get_current_user_from_token(credentials)
    except HTTPException:
        return None


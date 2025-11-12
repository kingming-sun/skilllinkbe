# Stack Auth 集成说明

## 概述

SkillLink 现已集成 **Stack Auth (Neon Auth)** 作为认证系统，提供更安全、更专业的用户认证体验。

## 主要变化

### 后端变化

1. **移除旧的认证接口**
   - ❌ `/api/auth/register` (已移除)
   - ❌ `/api/auth/login` (已移除)
   - ✅ `/api/auth/me` (保留 - 获取用户信息)

2. **新增认证模块**
   - `auth.py`: Stack Auth JWT 验证
   - `user_service.py`: 用户同步服务（Stack Auth → 本地数据库）

3. **认证流程**
   ```
   用户登录 Stack Auth → 获取 JWT Token → 
   发送请求到后端 → 后端验证 JWT → 
   自动同步用户到本地数据库 → 返回用户信息
   ```

### 前端变化

1. **使用 Stack Auth UI 组件**
   - 登录页面使用 `<SignIn />` 组件
   - 注册页面使用 `<SignUp />` 组件
   - 自动处理密码重置、邮箱验证等功能

2. **自动 Token 管理**
   - Stack Auth SDK 自动管理 token 刷新
   - API 请求自动添加 JWT Token
   - Token 过期自动重定向登录

## 配置信息

### 前端环境变量

```env
VITE_STACK_PROJECT_ID=29a175ee-764e-4b93-890d-7f0fd0ad8835
VITE_STACK_PUBLISHABLE_CLIENT_KEY=pck_aak8g0ev84f1jqmzbfjn1wrjmmg2se27y0hdydxv3x8s0
```

### 后端环境变量

```env
STACK_PROJECT_ID=29a175ee-764e-4b93-890d-7f0fd0ad8835
STACK_SECRET_SERVER_KEY=ssk_xt8rp11hps52dgqjm1cssscgz52xxfs6721cxmptdf9n8
DATABASE_URL=postgresql://...
```

## 启动步骤

### 1. 安装后端依赖

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

### 3. 启动后端

```bash
cd backend
python3 main.py
```

### 4. 启动前端

```bash
cd frontend
npm run dev
```

## Stack Auth 特性

✅ **自动功能**
- 邮箱验证
- 密码重置
- 双因素认证 (2FA) 可选
- 社交登录 (Google, GitHub 等) 可选
- Session 管理
- Token 自动刷新

✅ **安全性**
- JWT Token 加密
- JWKS 公钥验证
- HTTPS 通信
- 防暴力破解

✅ **开发体验**
- 开箱即用的 UI 组件
- 自动处理认证流程
- 无需手动管理密码加密
- 完整的用户管理后台

## Stack Auth 控制台

访问 Stack Auth 控制台管理用户：
https://app.stack-auth.com/projects/29a175ee-764e-4b93-890d-7f0fd0ad8835

功能：
- 查看所有注册用户
- 管理用户权限
- 查看登录日志
- 配置认证策略
- 自定义 UI 样式

## 本地数据库同步

用户首次通过 Stack Auth 登录后：
1. 后端自动在本地数据库创建用户记录
2. 从 JWT payload 提取邮箱等信息
3. 生成默认用户名（从邮箱）
4. 分配默认角色（user）
5. 后续请求使用本地用户 ID

## API 使用示例

### 前端发起请求

```javascript
import { stackApp } from './stackAuthConfig';

// 自动添加 JWT token
const response = await fetch('http://localhost:8000/api/skills', {
  headers: {
    'Authorization': `Bearer ${await stackApp.getUser()?.getIdToken()}`
  }
});
```

### 后端验证请求

```python
from fastapi import Depends
from auth import get_current_user_from_token
from user_service import get_or_create_user

@app.get("/api/auth/me")
async def get_profile(
    auth_payload: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, auth_payload)
    return user
```

## 常见问题

### Q: 如何获取当前用户信息？

```javascript
// 前端
import { useUser } from "@stackframe/stack";

function MyComponent() {
  const user = useUser();
  return <div>{user?.primaryEmail}</div>;
}
```

```python
# 后端
@app.get("/api/some-endpoint")
async def my_endpoint(current_user = Depends(get_current_user)):
    return {"user_id": current_user.id}
```

### Q: 如何自定义用户角色？

在 `user_service.py` 的 `sync_user_from_auth()` 函数中修改默认角色逻辑。

### Q: 如何处理未登录用户？

使用 `get_optional_current_user` 依赖：

```python
from auth import get_optional_current_user

@app.get("/api/public-endpoint")
async def public_endpoint(
    current_user = Depends(get_optional_current_user)
):
    if current_user:
        return {"message": "Hello " + current_user.username}
    return {"message": "Hello guest"}
```

## 迁移说明

如果你有旧的账号数据：
1. 旧用户需要重新通过 Stack Auth 注册
2. 可以使用相同邮箱注册
3. 后端会自动识别并关联现有用户数据

## 文档链接

- [Stack Auth 官方文档](https://docs.stack-auth.com/)
- [Neon Auth 文档](https://neon.com/docs/guides/neon-auth)
- [JWT 规范](https://jwt.io/)


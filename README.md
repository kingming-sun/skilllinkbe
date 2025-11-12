# SkillLink 后端 API

基于 FastAPI 的 RESTful API 服务

## 🚀 快速开始

### 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 启动服务

```bash
python main.py
# 或
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 项目结构

```
backend/
├── main.py              # FastAPI 主应用和路由
├── models.py            # Pydantic 数据模型
├── database.py          # 模拟数据库
└── requirements.txt     # Python 依赖
```

## 🔑 API 端点

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录
- `GET /api/auth/me` - 获取当前用户

### 技能
- `GET /api/skills` - 获取技能列表（支持筛选）
- `GET /api/skills/{id}` - 获取技能详情
- `POST /api/skills` - 创建技能
- `GET /api/skills/{id}/reviews` - 获取评价

### 订单
- `GET /api/orders` - 获取订单列表
- `GET /api/orders/{id}` - 获取订单详情
- `POST /api/orders` - 创建订单
- `PATCH /api/orders/{id}/status` - 更新订单状态

### 评价
- `POST /api/reviews` - 创建评价

### 统计
- `GET /api/stats` - 平台统计
- `GET /api/categories` - 分类统计

## 🗄️ 数据模型

详见 `models.py`

## 🔧 配置

CORS 已配置为允许来自前端的请求：
- http://localhost:3000
- http://localhost:5173

## 📝 注意事项

当前使用内存模拟数据库，重启后数据会丢失。生产环境应集成真实数据库。

## 🚀 未来改进

- [ ] 集成 PostgreSQL/MySQL
- [ ] JWT 认证
- [ ] 环境变量配置
- [ ] 日志系统
- [ ] 单元测试
- [ ] Docker 化

# Python FastAPI 后端

这是一个使用 FastAPI 构建的现代化 Python 后端 API 服务。

## 功能特性

- ✅ RESTful API 接口
- ✅ CORS 跨域支持
- ✅ 数据验证（Pydantic）
- ✅ 自动生成 API 文档
- ✅ 异步处理

## 技术栈

- **FastAPI** - 现代化、高性能的 Web 框架
- **Uvicorn** - ASGI 服务器
- **Pydantic** - 数据验证

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
```

### 2. 运行开发服务器

```bash
# 方式 1：使用 Python 直接运行
python main.py

# 方式 2：使用 uvicorn 命令
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务器将在 http://localhost:8000 启动

### 3. 查看 API 文档

FastAPI 自动生成交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 接口

### 健康检查
```
GET /api/health
```

### 获取所有项目
```
GET /api/items
```

### 获取单个项目
```
GET /api/items/{item_id}
```

### 创建项目
```
POST /api/items
Body: {
  "name": "项目名称",
  "description": "项目描述",
  "completed": false
}
```

### 更新项目
```
PUT /api/items/{item_id}
Body: {
  "name": "更新的名称",
  "description": "更新的描述",
  "completed": true
}
```

### 删除项目
```
DELETE /api/items/{item_id}
```

## 项目结构

```
backend/
├── main.py              # 主应用文件
├── requirements.txt     # 依赖包列表
├── .gitignore          # Git 忽略文件
└── README.md           # 项目文档
```

## 开发建议

1. **添加数据库**: 集成 SQLAlchemy 或 Tortoise ORM
2. **用户认证**: 添加 JWT 认证
3. **环境变量**: 使用 python-dotenv 管理配置
4. **测试**: 使用 pytest 编写单元测试
5. **日志**: 配置结构化日志

## 扩展阅读

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Uvicorn 文档](https://www.uvicorn.org/)


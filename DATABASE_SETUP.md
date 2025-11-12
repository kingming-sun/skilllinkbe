# 数据库设置指南

本项目使用 Neon PostgreSQL 数据库。

## 🗄️ 数据库信息

- **提供商**: Neon (Serverless PostgreSQL)
- **位置**: ap-southeast-1 (新加坡)
- **特点**: 
  - Serverless 自动伸缩
  - 内置连接池
  - 支持分支功能

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

这将会：
- 创建所有数据库表
- 填充示例数据（用户、技能、订单、评价）

### 3. 启动应用

```bash
python main.py
```

## 📋 数据库架构

### 表结构

1. **users** - 用户表
   - 基本信息：邮箱、用户名、密码、电话
   - 角色：user / provider / admin
   - 认证信息：is_verified, is_student
   - 学校信息：university, major

2. **skills** - 技能表
   - 关联：provider_id → users.id
   - 基本信息：标题、描述、分类
   - 定价：price_per_hour, duration_minutes
   - 服务模式：online / offline / both
   - 统计：views_count, orders_count, average_rating

3. **orders** - 订单表
   - 关联：user_id, provider_id, skill_id
   - 订单号：order_number (唯一)
   - 状态：pending / confirmed / paid / in_progress / completed / cancelled / refunded
   - 金额：total_amount, platform_fee, provider_amount

4. **reviews** - 评价表
   - 关联：order_id (唯一), skill_id, user_id, provider_id
   - 评分：rating (1-5)
   - 评论：comment

## 🔧 环境变量配置

创建 `.env` 文件：

```env
DATABASE_URL=postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

## 📝 常用操作

### 重置数据库

```bash
# 删除所有数据并重新初始化
python -c "from db_config import drop_db, init_db; drop_db(); init_db()"
python seed_data.py
```

### 直接连接数据库

```bash
psql 'postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

### 查看表

```sql
-- 列出所有表
\dt

-- 查看表结构
\d users
\d skills
\d orders
\d reviews

-- 查询数据
SELECT * FROM users;
SELECT * FROM skills;
SELECT * FROM orders;
SELECT * FROM reviews;
```

## 🔐 数据库连接

### 连接池配置

本项目使用 SQLAlchemy 的 NullPool，因为 Neon 自带连接池：

```python
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Neon 推荐
    echo=False,
    future=True
)
```

### SSL 要求

Neon 要求 SSL 连接：
- `sslmode=require` - 必须使用 SSL
- `channel_binding=require` - 增强安全性

## 🚨 故障排查

### 连接失败

1. **检查网络连接**
   ```bash
   ping ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech
   ```

2. **检查环境变量**
   ```bash
   echo $DATABASE_URL
   ```

3. **测试连接**
   ```bash
   python -c "from db_config import engine; engine.connect(); print('✅ Connected!')"
   ```

### SSL 错误

确保安装了正确的驱动：
```bash
pip install asyncpg psycopg2-binary
```

### 表不存在

运行初始化脚本：
```bash
python init_db.py
```

## 📊 数据迁移

### 使用 Alembic（可选）

项目已安装 Alembic，可以进行数据库迁移：

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

## 🔄 备份和恢复

### 备份

```bash
pg_dump 'postgresql://...' > backup.sql
```

### 恢复

```bash
psql 'postgresql://...' < backup.sql
```

## 📈 性能优化

1. **索引**: 已在关键字段添加索引
   - users.email (unique)
   - skills.title, skills.category
   - orders.order_number (unique), orders.status

2. **连接池**: 使用 Neon 内置连接池

3. **查询优化**: 使用 eager loading 减少 N+1 查询

## 🌐 生产环境配置

### Render 部署

在 Render 环境变量中设置：

```
DATABASE_URL=postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

### 自动迁移

在 `Dockerfile` 或启动脚本中添加：

```bash
# 在应用启动前运行
python init_db.py
```

## 📚 相关资源

- [Neon 文档](https://neon.tech/docs)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)

## ⚠️ 注意事项

1. **密码安全**: 生产环境请使用环境变量，不要硬编码
2. **连接限制**: Neon 免费版有连接数限制
3. **备份**: 定期备份数据
4. **监控**: 使用 Neon Dashboard 监控数据库性能

---

## 🎉 完成！

数据库现在已经配置完成，可以开始使用了！


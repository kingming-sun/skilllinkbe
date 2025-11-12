#!/usr/bin/env python3
"""数据库初始化脚本"""

from sqlalchemy import create_engine, text

# 数据库连接
DATABASE_URL = "postgresql://neondb_owner:npg_4qnFilm7BRDT@ep-broad-truth-a1bbw1n4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

print("🔗 连接数据库...")
engine = create_engine(DATABASE_URL, echo=False)

print("📊 创建表...")
with engine.connect() as conn:
    # 创建所有表
    conn.execute(text("""
        -- 用户表
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(20) NOT NULL DEFAULT 'user',
            avatar VARCHAR(500),
            is_verified BOOLEAN DEFAULT FALSE,
            is_student BOOLEAN DEFAULT FALSE,
            university VARCHAR(200),
            major VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 技能表
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            provider_id INTEGER NOT NULL REFERENCES users(id),
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(50) NOT NULL,
            price_per_hour FLOAT NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            service_mode VARCHAR(20) NOT NULL,
            location VARCHAR(500),
            tags TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            views_count INTEGER DEFAULT 0,
            orders_count INTEGER DEFAULT 0,
            average_rating FLOAT DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 订单表
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            order_number VARCHAR(50) UNIQUE NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id),
            provider_id INTEGER NOT NULL REFERENCES users(id),
            skill_id INTEGER NOT NULL REFERENCES skills(id),
            status VARCHAR(20) DEFAULT 'pending',
            scheduled_date TIMESTAMP NOT NULL,
            total_amount FLOAT NOT NULL,
            platform_fee FLOAT NOT NULL,
            provider_amount FLOAT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );

        -- 评价表
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id),
            skill_id INTEGER NOT NULL REFERENCES skills(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            provider_id INTEGER NOT NULL REFERENCES users(id),
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    conn.commit()
    print("✅ 表创建成功！")

    # 检查并插入示例数据
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    count = result.scalar()
    
    if count == 0:
        print("📝 插入示例数据...")
        conn.execute(text("""
            INSERT INTO users (email, username, password, phone, role, avatar, is_verified, is_student, university, major) VALUES
            ('zhang@example.com', '张教练', 'password123', '13800138001', 'provider', 'https://api.dicebear.com/7.x/avataaars/svg?seed=Zhang', TRUE, TRUE, '清华大学', '体育教育'),
            ('li@example.com', '李同学', 'password123', '13800138002', 'provider', 'https://api.dicebear.com/7.x/avataaars/svg?seed=Li', TRUE, TRUE, '北京大学', '计算机科学'),
            ('wang@example.com', '王老师', 'password123', '13800138003', 'provider', 'https://api.dicebear.com/7.x/avataaars/svg?seed=Wang', TRUE, TRUE, '中国音乐学院', '钢琴表演'),
            ('user@example.com', '普通用户', 'password123', '13800138004', 'user', 'https://api.dicebear.com/7.x/avataaars/svg?seed=User', FALSE, FALSE, NULL, NULL);
            
            INSERT INTO skills (provider_id, title, description, category, price_per_hour, duration_minutes, service_mode, location, tags, views_count, orders_count, average_rating) VALUES
            (1, '网球入门课程', '适合零基础学员，教授网球基本动作、握拍方式、正反手击球等。拥有5年教学经验，曾获得校级网球比赛冠军。', 'sports', 80.0, 60, 'offline', '清华大学网球场', '网球,运动,零基础', 156, 12, 4.8),
            (2, 'Python 编程入门', '从零开始学习Python编程，涵盖基础语法、数据结构、面向对象等内容。适合想要入门编程的同学。', 'programming', 100.0, 90, 'both', '线上/北京大学', 'Python,编程,零基础', 289, 25, 4.9),
            (3, '钢琴体验课', '一对一钢琴体验课程，教授基础指法和简单曲目。音乐学院在读，有丰富的教学经验。', 'music', 120.0, 60, 'offline', '中国音乐学院琴房', '钢琴,音乐,体验课', 198, 18, 5.0),
            (1, '羽毛球训练', '羽毛球基础和进阶训练，包括步伐、发球、高远球等技术要点。', 'sports', 70.0, 60, 'offline', '清华大学体育馆', '羽毛球,运动,训练', 132, 9, 4.7),
            (2, 'Web前端开发', '学习HTML、CSS、JavaScript基础，构建你的第一个网页。适合想要学习前端开发的同学。', 'programming', 110.0, 90, 'online', '线上教学', '前端,Web,JavaScript', 245, 20, 4.8),
            (3, '吉他入门课', '零基础吉他教学，从基础和弦开始，能够弹唱简单歌曲。', 'music', 90.0, 60, 'both', '音乐学院/线上', '吉他,音乐,零基础', 176, 14, 4.6);
        """))
        conn.commit()
        print("✅ 示例数据插入成功！")
    else:
        print(f"ℹ️  数据库中已有 {count} 个用户，跳过数据插入")

    # 验证结果
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    users_count = result.scalar()
    
    result = conn.execute(text("SELECT COUNT(*) FROM skills"))
    skills_count = result.scalar()
    
    print("\n" + "="*50)
    print("🎉 数据库初始化完成！")
    print("="*50)
    print(f"\n创建的表:")
    print(f"  ✓ users   (用户表)")
    print(f"  ✓ skills  (技能表)")
    print(f"  ✓ orders  (订单表)")
    print(f"  ✓ reviews (评价表)")
    print(f"\n数据统计:")
    print(f"  - 用户: {users_count} 条")
    print(f"  - 技能: {skills_count} 条")
    print(f"\n请在 Neon 控制台刷新页面查看！")
    print("="*50)


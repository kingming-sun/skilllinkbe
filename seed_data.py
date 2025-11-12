"""
数据库种子数据脚本
用于初始化示例数据
"""
from datetime import datetime, timedelta
from db_config import SessionLocal, init_db
from db_models import UserModel, SkillModel, OrderModel, ReviewModel
from database import generate_order_number


def seed_database():
    """填充示例数据"""
    
    print("🌱 Seeding database with sample data...")
    
    # 初始化数据库表
    init_db()
    
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_users = db.query(UserModel).count()
        if existing_users > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return
        
        # 创建示例用户
        users = [
            UserModel(
                email="zhang@example.com",
                username="张教练",
                password="password123",
                phone="13800138001",
                role="provider",
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Zhang",
                is_verified=True,
                is_student=True,
                university="清华大学",
                major="体育教育",
                created_at=datetime.now() - timedelta(days=90)
            ),
            UserModel(
                email="li@example.com",
                username="李同学",
                password="password123",
                phone="13800138002",
                role="provider",
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Li",
                is_verified=True,
                is_student=True,
                university="北京大学",
                major="计算机科学",
                created_at=datetime.now() - timedelta(days=60)
            ),
            UserModel(
                email="wang@example.com",
                username="王老师",
                password="password123",
                phone="13800138003",
                role="provider",
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Wang",
                is_verified=True,
                is_student=True,
                university="中国音乐学院",
                major="钢琴表演",
                created_at=datetime.now() - timedelta(days=120)
            ),
            UserModel(
                email="user@example.com",
                username="普通用户",
                password="password123",
                phone="13800138004",
                role="user",
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=User",
                is_verified=False,
                is_student=False,
                university=None,
                major=None,
                created_at=datetime.now() - timedelta(days=30)
            )
        ]
        
        db.add_all(users)
        db.commit()
        print(f"✅ Created {len(users)} users")
        
        # 刷新以获取 ID
        for user in users:
            db.refresh(user)
        
        # 创建示例技能
        skills = [
            SkillModel(
                provider_id=users[0].id,
                title="网球入门课程",
                description="适合零基础学员，教授网球基本动作、握拍方式、正反手击球等。拥有5年教学经验，曾获得校级网球比赛冠军。",
                category="sports",
                price_per_hour=80.0,
                duration_minutes=60,
                service_mode="offline",
                location="清华大学网球场",
                tags="网球,运动,零基础",
                is_active=True,
                views_count=156,
                orders_count=12,
                average_rating=4.8,
                created_at=datetime.now() - timedelta(days=60),
                updated_at=datetime.now() - timedelta(days=5)
            ),
            SkillModel(
                provider_id=users[1].id,
                title="Python 编程入门",
                description="从零开始学习Python编程，涵盖基础语法、数据结构、面向对象等内容。适合想要入门编程的同学。",
                category="programming",
                price_per_hour=100.0,
                duration_minutes=90,
                service_mode="both",
                location="线上/北京大学",
                tags="Python,编程,零基础",
                is_active=True,
                views_count=289,
                orders_count=25,
                average_rating=4.9,
                created_at=datetime.now() - timedelta(days=50),
                updated_at=datetime.now() - timedelta(days=2)
            ),
            SkillModel(
                provider_id=users[2].id,
                title="钢琴体验课",
                description="一对一钢琴体验课程，教授基础指法和简单曲目。音乐学院在读，有丰富的教学经验。",
                category="music",
                price_per_hour=120.0,
                duration_minutes=60,
                service_mode="offline",
                location="中国音乐学院琴房",
                tags="钢琴,音乐,体验课",
                is_active=True,
                views_count=198,
                orders_count=18,
                average_rating=5.0,
                created_at=datetime.now() - timedelta(days=80),
                updated_at=datetime.now() - timedelta(days=10)
            ),
            SkillModel(
                provider_id=users[0].id,
                title="羽毛球训练",
                description="羽毛球基础和进阶训练，包括步伐、发球、高远球等技术要点。",
                category="sports",
                price_per_hour=70.0,
                duration_minutes=60,
                service_mode="offline",
                location="清华大学体育馆",
                tags="羽毛球,运动,训练",
                is_active=True,
                views_count=132,
                orders_count=9,
                average_rating=4.7,
                created_at=datetime.now() - timedelta(days=40),
                updated_at=datetime.now() - timedelta(days=3)
            ),
            SkillModel(
                provider_id=users[1].id,
                title="Web前端开发",
                description="学习HTML、CSS、JavaScript基础，构建你的第一个网页。适合想要学习前端开发的同学。",
                category="programming",
                price_per_hour=110.0,
                duration_minutes=90,
                service_mode="online",
                location="线上教学",
                tags="前端,Web,JavaScript",
                is_active=True,
                views_count=245,
                orders_count=20,
                average_rating=4.8,
                created_at=datetime.now() - timedelta(days=35),
                updated_at=datetime.now() - timedelta(days=1)
            ),
            SkillModel(
                provider_id=users[2].id,
                title="吉他入门课",
                description="零基础吉他教学，从基础和弦开始，能够弹唱简单歌曲。",
                category="music",
                price_per_hour=90.0,
                duration_minutes=60,
                service_mode="both",
                location="音乐学院/线上",
                tags="吉他,音乐,零基础",
                is_active=True,
                views_count=176,
                orders_count=14,
                average_rating=4.6,
                created_at=datetime.now() - timedelta(days=55),
                updated_at=datetime.now() - timedelta(days=7)
            )
        ]
        
        db.add_all(skills)
        db.commit()
        print(f"✅ Created {len(skills)} skills")
        
        # 刷新以获取 ID
        for skill in skills:
            db.refresh(skill)
        
        # 创建示例订单
        orders = [
            OrderModel(
                order_number=generate_order_number(),
                user_id=users[3].id,
                provider_id=users[0].id,
                skill_id=skills[0].id,
                status="completed",
                scheduled_date=datetime.now() - timedelta(days=5),
                total_amount=80.0,
                platform_fee=12.0,
                provider_amount=68.0,
                message="想学习网球基础",
                created_at=datetime.now() - timedelta(days=7),
                updated_at=datetime.now() - timedelta(days=5),
                completed_at=datetime.now() - timedelta(days=5)
            ),
            OrderModel(
                order_number=generate_order_number(),
                user_id=users[3].id,
                provider_id=users[1].id,
                skill_id=skills[1].id,
                status="confirmed",
                scheduled_date=datetime.now() + timedelta(days=2),
                total_amount=100.0,
                platform_fee=15.0,
                provider_amount=85.0,
                message="希望学习Python编程",
                created_at=datetime.now() - timedelta(days=1),
                updated_at=datetime.now() - timedelta(days=1),
                completed_at=None
            )
        ]
        
        db.add_all(orders)
        db.commit()
        print(f"✅ Created {len(orders)} orders")
        
        # 刷新以获取 ID
        for order in orders:
            db.refresh(order)
        
        # 创建示例评价
        reviews = [
            ReviewModel(
                order_id=orders[0].id,
                skill_id=skills[0].id,
                user_id=users[3].id,
                provider_id=users[0].id,
                rating=5,
                comment="张教练非常专业，教学方法很好，一节课就学会了基本动作！",
                created_at=datetime.now() - timedelta(days=5)
            )
        ]
        
        db.add_all(reviews)
        db.commit()
        print(f"✅ Created {len(reviews)} reviews")
        
        print("🎉 Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()


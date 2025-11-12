"""
模拟数据库 - 在生产环境中应该使用真实数据库（如 PostgreSQL）
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import random
import string


def generate_order_number() -> str:
    """生成订单号"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.digits, k=6))
    return f"SK{timestamp}{random_str}"


# 模拟数据库
class Database:
    def __init__(self):
        self.users: List[Dict] = []
        self.skills: List[Dict] = []
        self.orders: List[Dict] = []
        self.reviews: List[Dict] = []
        
        self._init_mock_data()
    
    def _init_mock_data(self):
        """初始化模拟数据"""
        # 创建一些示例用户
        self.users = [
            {
                "id": 1,
                "email": "zhang@example.com",
                "username": "张教练",
                "password": "password123",  # 实际应该加密
                "phone": "13800138001",
                "role": "provider",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zhang",
                "is_verified": True,
                "is_student": True,
                "university": "清华大学",
                "major": "体育教育",
                "created_at": datetime.now() - timedelta(days=90)
            },
            {
                "id": 2,
                "email": "li@example.com",
                "username": "李同学",
                "password": "password123",
                "phone": "13800138002",
                "role": "provider",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Li",
                "is_verified": True,
                "is_student": True,
                "university": "北京大学",
                "major": "计算机科学",
                "created_at": datetime.now() - timedelta(days=60)
            },
            {
                "id": 3,
                "email": "wang@example.com",
                "username": "王老师",
                "password": "password123",
                "phone": "13800138003",
                "role": "provider",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Wang",
                "is_verified": True,
                "is_student": True,
                "university": "中国音乐学院",
                "major": "钢琴表演",
                "created_at": datetime.now() - timedelta(days=120)
            },
            {
                "id": 4,
                "email": "user@example.com",
                "username": "普通用户",
                "password": "password123",
                "phone": "13800138004",
                "role": "user",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=User",
                "is_verified": False,
                "is_student": False,
                "university": None,
                "major": None,
                "created_at": datetime.now() - timedelta(days=30)
            }
        ]
        
        # 创建一些示例技能
        self.skills = [
            {
                "id": 1,
                "provider_id": 1,
                "title": "网球入门课程",
                "description": "适合零基础学员，教授网球基本动作、握拍方式、正反手击球等。拥有5年教学经验，曾获得校级网球比赛冠军。",
                "category": "sports",
                "price_per_hour": 80.0,
                "duration_minutes": 60,
                "service_mode": "offline",
                "location": "清华大学网球场",
                "tags": ["网球", "运动", "零基础"],
                "is_active": True,
                "views_count": 156,
                "orders_count": 12,
                "average_rating": 4.8,
                "created_at": datetime.now() - timedelta(days=60),
                "updated_at": datetime.now() - timedelta(days=5)
            },
            {
                "id": 2,
                "provider_id": 2,
                "title": "Python 编程入门",
                "description": "从零开始学习Python编程，涵盖基础语法、数据结构、面向对象等内容。适合想要入门编程的同学。",
                "category": "programming",
                "price_per_hour": 100.0,
                "duration_minutes": 90,
                "service_mode": "both",
                "location": "线上/北京大学",
                "tags": ["Python", "编程", "零基础"],
                "is_active": True,
                "views_count": 289,
                "orders_count": 25,
                "average_rating": 4.9,
                "created_at": datetime.now() - timedelta(days=50),
                "updated_at": datetime.now() - timedelta(days=2)
            },
            {
                "id": 3,
                "provider_id": 3,
                "title": "钢琴体验课",
                "description": "一对一钢琴体验课程，教授基础指法和简单曲目。音乐学院在读，有丰富的教学经验。",
                "category": "music",
                "price_per_hour": 120.0,
                "duration_minutes": 60,
                "service_mode": "offline",
                "location": "中国音乐学院琴房",
                "tags": ["钢琴", "音乐", "体验课"],
                "is_active": True,
                "views_count": 198,
                "orders_count": 18,
                "average_rating": 5.0,
                "created_at": datetime.now() - timedelta(days=80),
                "updated_at": datetime.now() - timedelta(days=10)
            },
            {
                "id": 4,
                "provider_id": 1,
                "title": "羽毛球训练",
                "description": "羽毛球基础和进阶训练，包括步伐、发球、高远球等技术要点。",
                "category": "sports",
                "price_per_hour": 70.0,
                "duration_minutes": 60,
                "service_mode": "offline",
                "location": "清华大学体育馆",
                "tags": ["羽毛球", "运动", "训练"],
                "is_active": True,
                "views_count": 132,
                "orders_count": 9,
                "average_rating": 4.7,
                "created_at": datetime.now() - timedelta(days=40),
                "updated_at": datetime.now() - timedelta(days=3)
            },
            {
                "id": 5,
                "provider_id": 2,
                "title": "Web前端开发",
                "description": "学习HTML、CSS、JavaScript基础，构建你的第一个网页。适合想要学习前端开发的同学。",
                "category": "programming",
                "price_per_hour": 110.0,
                "duration_minutes": 90,
                "service_mode": "online",
                "location": "线上教学",
                "tags": ["前端", "Web", "JavaScript"],
                "is_active": True,
                "views_count": 245,
                "orders_count": 20,
                "average_rating": 4.8,
                "created_at": datetime.now() - timedelta(days=35),
                "updated_at": datetime.now() - timedelta(days=1)
            },
            {
                "id": 6,
                "provider_id": 3,
                "title": "吉他入门课",
                "description": "零基础吉他教学，从基础和弦开始，能够弹唱简单歌曲。",
                "category": "music",
                "price_per_hour": 90.0,
                "duration_minutes": 60,
                "service_mode": "both",
                "location": "音乐学院/线上",
                "tags": ["吉他", "音乐", "零基础"],
                "is_active": True,
                "views_count": 176,
                "orders_count": 14,
                "average_rating": 4.6,
                "created_at": datetime.now() - timedelta(days=55),
                "updated_at": datetime.now() - timedelta(days=7)
            }
        ]
        
        # 创建一些示例订单
        self.orders = [
            {
                "id": 1,
                "order_number": generate_order_number(),
                "user_id": 4,
                "provider_id": 1,
                "skill_id": 1,
                "status": "completed",
                "scheduled_date": datetime.now() - timedelta(days=5),
                "total_amount": 80.0,
                "platform_fee": 12.0,
                "provider_amount": 68.0,
                "message": "想学习网球基础",
                "created_at": datetime.now() - timedelta(days=7),
                "updated_at": datetime.now() - timedelta(days=5),
                "completed_at": datetime.now() - timedelta(days=5)
            },
            {
                "id": 2,
                "order_number": generate_order_number(),
                "user_id": 4,
                "provider_id": 2,
                "skill_id": 2,
                "status": "confirmed",
                "scheduled_date": datetime.now() + timedelta(days=2),
                "total_amount": 100.0,
                "platform_fee": 15.0,
                "provider_amount": 85.0,
                "message": "希望学习Python编程",
                "created_at": datetime.now() - timedelta(days=1),
                "updated_at": datetime.now() - timedelta(days=1),
                "completed_at": None
            }
        ]
        
        # 创建一些示例评价
        self.reviews = [
            {
                "id": 1,
                "order_id": 1,
                "skill_id": 1,
                "user_id": 4,
                "provider_id": 1,
                "rating": 5,
                "comment": "张教练非常专业，教学方法很好，一节课就学会了基本动作！",
                "created_at": datetime.now() - timedelta(days=5)
            }
        ]
    
    def get_next_id(self, table_name: str) -> int:
        """获取下一个ID"""
        table = getattr(self, table_name)
        if not table:
            return 1
        return max(item["id"] for item in table) + 1


# 全局数据库实例
db = Database()


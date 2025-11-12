#!/usr/bin/env python
"""
数据库初始化脚本
运行此脚本以创建表并填充示例数据
"""
import sys

def main():
    print("=" * 60)
    print("SkillLink 数据库初始化")
    print("=" * 60)
    print()
    
    # 创建表
    print("📦 步骤 1: 创建数据库表...")
    from db_config import init_db
    init_db()
    print()
    
    # 填充示例数据
    print("🌱 步骤 2: 填充示例数据...")
    from seed_data import seed_database
    seed_database()
    print()
    
    print("=" * 60)
    print("✅ 数据库初始化完成！")
    print("=" * 60)
    print()
    print("现在可以启动应用：")
    print("  python main.py")
    print()
    print("或使用 uvicorn：")
    print("  uvicorn main:app --reload")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


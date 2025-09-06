#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查MySQL数据库中的数据保存情况
"""

import pymysql
import pandas as pd
from datetime import datetime

def check_mysql_connection():
    """检查MySQL连接"""
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='mysql511',
            database='ml_workspace',
            charset='utf8mb4'
        )
        print("✅ MySQL连接成功！")
        return connection
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        return None

def check_database_tables(connection):
    """检查数据库中的表"""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"\n📊 数据库中的表 ({len(tables)}个):")
        for table in tables:
            print(f"  - {table[0]}")
        cursor.close()
        return [table[0] for table in tables]
    except Exception as e:
        print(f"❌ 获取表列表失败: {e}")
        return []

def check_table_data(connection, table_name):
    """检查表中的数据"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"\n📈 表 '{table_name}' 数据统计:")
        print(f"  - 总记录数: {count:,}")
        
        if count > 0:
            # 获取表结构
            cursor.execute(f"DESCRIBE {table_name};")
            columns = cursor.fetchall()
            print(f"  - 列数: {len(columns)}")
            print("  - 列信息:")
            for col in columns:
                print(f"    * {col[0]} ({col[1]})")
            
            # 获取前5条记录
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            sample_data = cursor.fetchall()
            print("  - 前5条记录:")
            for i, row in enumerate(sample_data, 1):
                print(f"    {i}. {row[:3]}..." if len(row) > 3 else f"    {i}. {row}")
        
        cursor.close()
        return count
    except Exception as e:
        print(f"❌ 检查表 '{table_name}' 失败: {e}")
        return 0

def main():
    """主函数"""
    print("🔍 开始检查MySQL数据库连接和数据保存情况...")
    print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 检查连接
    connection = check_mysql_connection()
    if not connection:
        return
    
    try:
        # 检查表
        tables = check_database_tables(connection)
        
        if not tables:
            print("\n⚠️  数据库中没有找到任何表！")
            return
        
        # 检查每个表的数据
        total_records = 0
        for table in tables:
            count = check_table_data(connection, table)
            total_records += count
        
        print("\n" + "="*60)
        print(f"📊 数据库总结:")
        print(f"  - 总表数: {len(tables)}")
        print(f"  - 总记录数: {total_records:,}")
        
        # 特别检查电商相关表
        ecommerce_tables = ['用户信息', '订单数据', '产品信息', '用户行为数据']
        found_ecommerce_tables = [t for t in tables if any(et in t for et in ecommerce_tables)]
        
        if found_ecommerce_tables:
            print(f"\n🛒 电商数据表 ({len(found_ecommerce_tables)}个):")
            for table in found_ecommerce_tables:
                print(f"  ✅ {table}")
        else:
            print("\n⚠️  未找到电商相关数据表")
            
    finally:
        connection.close()
        print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()
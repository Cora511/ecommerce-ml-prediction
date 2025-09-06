#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构
"""

import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

def check_table_structure():
    """检查数据库表结构"""
    try:
        # 数据库连接配置
        config = {
            'host': 'localhost',
            'database': 'ecommerce_analysis',
            'user': 'root',
            'password': 'Flameaway3.'
        }
        
        print(f"🔗 连接数据库: {datetime.now()}")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("🔗 数据库连接成功！")
        
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📋 数据库中的表 ({len(tables)}个):")
        for table in tables:
            table_name = table[0]
            print(f"   📊 {table_name}")
            
            # 获取表结构
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            print(f"      字段信息:")
            for col in columns:
                field_name, field_type, null, key, default, extra = col
                print(f"        - {field_name}: {field_type}")
            
            # 获取记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"      记录数: {count}")
            print()
        
        cursor.close()
        conn.close()
        print("🔒 数据库连接已关闭")
        
    except Error as e:
        print(f"❌ 数据库错误: {e}")
    except Exception as e:
        print(f"❌ 程序错误: {e}")

if __name__ == "__main__":
    check_table_structure()
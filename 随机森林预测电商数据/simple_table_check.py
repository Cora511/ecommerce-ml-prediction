#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

try:
    # 连接数据库（使用正确的配置）
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='mysql511',
        database='ml_workspace',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    print("✅ 数据库连接成功！")
    
    # 先查看所有表
    print("\n📋 所有表:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
    
    # 检查users表结构
    print("\n📋 检查users表结构:")
    try:
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   {col[0]}: {col[1]}")
    except Exception as e:
        print(f"   ❌ users表不存在: {e}")
    
    # 检查orders表结构
    print("\n📋 检查orders表结构:")
    try:
        cursor.execute("DESCRIBE orders")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   {col[0]}: {col[1]}")
    except Exception as e:
        print(f"   ❌ orders表不存在: {e}")
    
    # 检查user_behaviors表结构
    print("\n📋 检查user_behaviors表结构:")
    try:
        cursor.execute("DESCRIBE user_behaviors")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   {col[0]}: {col[1]}")
    except Exception as e:
        print(f"   ❌ user_behaviors表不存在: {e}")
    
    cursor.close()
    conn.close()
    print("\n🔒 数据库连接已关闭")
    
except Exception as e:
    print(f"❌ 错误: {e}")
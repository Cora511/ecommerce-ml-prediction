#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的分析报告和预测结果
"""

import pymysql
import pandas as pd
from datetime import datetime

def check_database_reports():
    """检查数据库中的报告和分析数据"""
    try:
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='mysql511',
            database='ml_workspace',
            charset='utf8mb4'
        )
        
        print("🔗 数据库连接成功！")
        
        with connection.cursor() as cursor:
            # 获取所有表
            cursor.execute("SHOW TABLES;")
            all_tables = cursor.fetchall()
            
            print(f"\n📊 数据库中共有 {len(all_tables)} 个表:")
            for i, table in enumerate(all_tables, 1):
                print(f"  {i}. {table[0]}")
            
            # 检查是否有报告相关的表
            report_tables = []
            analysis_tables = []
            prediction_tables = []
            
            for table in all_tables:
                table_name = table[0].lower()
                if 'report' in table_name or '报告' in table_name:
                    report_tables.append(table[0])
                elif 'analysis' in table_name or '分析' in table_name:
                    analysis_tables.append(table[0])
                elif 'prediction' in table_name or '预测' in table_name:
                    prediction_tables.append(table[0])
            
            print(f"\n📈 报告相关表: {report_tables if report_tables else '未找到'}")
            print(f"📊 分析相关表: {analysis_tables if analysis_tables else '未找到'}")
            print(f"🔮 预测相关表: {prediction_tables if prediction_tables else '未找到'}")
            
            # 检查每个表的数据量和结构
            print("\n" + "="*60)
            print("📋 详细表信息:")
            
            total_records = 0
            for table in all_tables:
                table_name = table[0]
                
                # 获取表结构
                cursor.execute(f"DESCRIBE {table_name};")
                columns = cursor.fetchall()
                
                # 获取记录数
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                total_records += count
                
                print(f"\n🗂️  表 '{table_name}':")
                print(f"   📊 记录数: {count:,}")
                print(f"   📋 列数: {len(columns)}")
                print(f"   🏗️  结构:")
                for col in columns:
                    print(f"      - {col[0]} ({col[1]})")
                
                # 如果记录数不为0，显示前3条记录
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    sample_data = cursor.fetchall()
                    print(f"   📝 样本数据 (前3条):")
                    for i, row in enumerate(sample_data, 1):
                        print(f"      {i}. {str(row)[:100]}{'...' if len(str(row)) > 100 else ''}")
            
            print(f"\n" + "="*60)
            print(f"📊 数据库总结:")
            print(f"   🗂️  总表数: {len(all_tables)}")
            print(f"   📊 总记录数: {total_records:,}")
            
            # 检查是否有模型预测结果
            print(f"\n🔍 检查模型和分析结果保存情况:")
            
            # 检查是否有用户行为预测结果
            behavior_prediction_found = False
            ltv_prediction_found = False
            customer_segmentation_found = False
            
            for table in all_tables:
                table_name = table[0]
                cursor.execute(f"SHOW COLUMNS FROM {table_name};")
                columns = [col[0] for col in cursor.fetchall()]
                
                # 检查列名中是否包含预测相关字段
                column_str = ' '.join(columns).lower()
                if any(keyword in column_str for keyword in ['prediction', '预测', 'forecast']):
                    behavior_prediction_found = True
                    print(f"   ✅ 发现预测结果表: {table_name}")
                
                if any(keyword in column_str for keyword in ['ltv', 'lifetime', 'value', '生命周期', '价值']):
                    ltv_prediction_found = True
                    print(f"   ✅ 发现LTV相关表: {table_name}")
                
                if any(keyword in column_str for keyword in ['segment', 'cluster', '分群', '聚类']):
                    customer_segmentation_found = True
                    print(f"   ✅ 发现客户分群表: {table_name}")
            
            print(f"\n📋 分析结果保存状态:")
            print(f"   🎯 用户行为预测: {'✅ 已保存' if behavior_prediction_found else '❌ 未找到'}")
            print(f"   💰 LTV预测: {'✅ 已保存' if ltv_prediction_found else '❌ 未找到'}")
            print(f"   👥 客户分群: {'✅ 已保存' if customer_segmentation_found else '❌ 未找到'}")
            
    except Exception as e:
        print(f"❌ 数据库连接或查询失败: {e}")
        return False
    
    finally:
        if 'connection' in locals():
            connection.close()
            print(f"\n🔒 数据库连接已关闭")
    
    return True

if __name__ == "__main__":
    print("🔍 开始检查数据库中的分析报告和预测结果...")
    print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    success = check_database_reports()
    
    if success:
        print("\n✅ 数据库检查完成！")
    else:
        print("\n❌ 数据库检查失败！")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习电商数据导入脚本
将CSV数据文件导入到 ml_research_db 数据库中

作者: AI数据科学助手
日期: 2024
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataImporter:
    def __init__(self, host='localhost', user='root', password='', database='ml_research_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
    def connect_database(self):
        """连接数据库"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            self.cursor = self.connection.cursor()
            logger.info(f"成功连接到数据库 {self.database}")
            return True
        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def create_tables(self):
        """创建数据库表结构"""
        try:
            # 用户表
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                用户ID VARCHAR(20) PRIMARY KEY,
                用户名 VARCHAR(50) NOT NULL,
                性别 VARCHAR(10),
                年龄 INT,
                城市 VARCHAR(50),
                城市等级 VARCHAR(20),
                收入水平 VARCHAR(20),
                注册日期 DATE,
                会员等级 VARCHAR(20),
                手机号 VARCHAR(20),
                邮箱 VARCHAR(100),
                创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                更新时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 产品表
            products_table = """
            CREATE TABLE IF NOT EXISTS products (
                产品ID VARCHAR(20) PRIMARY KEY,
                产品名称 VARCHAR(100) NOT NULL,
                品牌 VARCHAR(50),
                产品类型 VARCHAR(50),
                价格 DECIMAL(10,2),
                功率 INT,
                重量 DECIMAL(5,2),
                颜色 VARCHAR(20),
                上架日期 DATE,
                库存数量 INT,
                评分 DECIMAL(3,1),
                评价数量 INT,
                创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                更新时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 订单表
            orders_table = """
            CREATE TABLE IF NOT EXISTS orders (
                订单ID VARCHAR(20) PRIMARY KEY,
                用户ID VARCHAR(20),
                产品ID VARCHAR(20),
                订单日期 DATE,
                数量 INT,
                原价 DECIMAL(10,2),
                折扣率 DECIMAL(10,8),
                实际价格 DECIMAL(10,2),
                总金额 DECIMAL(10,2),
                支付方式 VARCHAR(20),
                配送方式 VARCHAR(20),
                订单状态 VARCHAR(20),
                评价分数 DECIMAL(3,1),
                创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                更新时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (用户ID) REFERENCES users(用户ID),
                FOREIGN KEY (产品ID) REFERENCES products(产品ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 用户行为表
            user_behavior_table = """
            CREATE TABLE IF NOT EXISTS user_behavior (
                行为ID VARCHAR(20) PRIMARY KEY,
                用户ID VARCHAR(20),
                产品ID VARCHAR(20),
                行为类型 VARCHAR(20),
                行为时间 DATETIME,
                停留时长 INT,
                来源渠道 VARCHAR(20),
                设备类型 VARCHAR(20),
                创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (用户ID) REFERENCES users(用户ID),
                FOREIGN KEY (产品ID) REFERENCES products(产品ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 特征数据表
            features_table = """
            CREATE TABLE IF NOT EXISTS user_features (
                用户ID VARCHAR(20) PRIMARY KEY,
                用户名 VARCHAR(50),
                性别 VARCHAR(10),
                年龄 INT,
                城市 VARCHAR(50),
                城市等级 VARCHAR(20),
                收入水平 VARCHAR(20),
                注册日期 DATE,
                会员等级 VARCHAR(20),
                手机号 VARCHAR(20),
                邮箱 VARCHAR(100),
                性别_编码 INT,
                城市等级_编码 INT,
                收入水平_编码 INT,
                会员等级_编码 INT,
                订单次数 DECIMAL(10,2),
                总消费金额 DECIMAL(12,2),
                平均消费金额 DECIMAL(10,2),
                消费标准差 DECIMAL(10,2),
                总购买数量 DECIMAL(10,2),
                平均折扣率 DECIMAL(10,8),
                首次购买日期 DATE,
                最后购买日期 DATE,
                购买天数跨度 DECIMAL(10,2),
                购买频率 DECIMAL(10,8),
                总行为次数 INT,
                总停留时长 INT,
                平均停留时长 DECIMAL(10,2),
                分享_次数 INT,
                加购物车_次数 INT,
                咨询客服_次数 INT,
                收藏_次数 INT,
                浏览_次数 INT,
                R_最近购买天数 DECIMAL(10,2),
                F_购买频率 DECIMAL(10,2),
                M_消费金额 DECIMAL(12,2),
                是否购买 INT,
                LTV DECIMAL(12,2),
                客户价值等级 VARCHAR(20),
                创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                更新时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (用户ID) REFERENCES users(用户ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 执行创建表的SQL语句
            tables = {
                'users': users_table,
                'products': products_table,
                'orders': orders_table,
                'user_behavior': user_behavior_table,
                'user_features': features_table
            }
            
            for table_name, sql in tables.items():
                self.cursor.execute(sql)
                logger.info(f"表 {table_name} 创建成功")
            
            self.connection.commit()
            logger.info("所有数据表创建完成！")
            return True
            
        except Error as e:
            logger.error(f"创建表失败: {e}")
            return False
    
    def import_csv_data(self, csv_file_path, table_name, batch_size=1000):
        """导入CSV数据到指定表"""
        try:
            # 读取CSV文件
            df = pd.read_csv(csv_file_path, encoding='utf-8')
            logger.info(f"读取CSV文件 {csv_file_path}，共 {len(df)} 条记录")
            
            # 处理空值
            df = df.where(pd.notnull(df), None)
            
            # 获取列名
            columns = list(df.columns)
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join([f'`{col}`' for col in columns])
            
            # 构建插入SQL
            insert_sql = f"INSERT IGNORE INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            # 批量插入数据
            total_inserted = 0
            for i in range(0, len(df), batch_size):
                batch_df = df.iloc[i:i+batch_size]
                batch_data = [tuple(row) for row in batch_df.values]
                
                self.cursor.executemany(insert_sql, batch_data)
                self.connection.commit()
                
                total_inserted += len(batch_data)
                logger.info(f"已导入 {total_inserted}/{len(df)} 条记录到表 {table_name}")
            
            logger.info(f"表 {table_name} 数据导入完成！共导入 {total_inserted} 条记录")
            return True
            
        except Exception as e:
            logger.error(f"导入数据到表 {table_name} 失败: {e}")
            return False
    
    def import_all_data(self, data_dir='./data'):
        """导入所有CSV数据文件"""
        # 定义文件和对应的表名映射
        file_table_mapping = {
            '用户数据.csv': 'users',
            '产品数据.csv': 'products', 
            '订单数据.csv': 'orders',
            '用户行为数据.csv': 'user_behavior',
            '特征数据.csv': 'user_features'
        }
        
        success_count = 0
        total_count = len(file_table_mapping)
        
        for csv_file, table_name in file_table_mapping.items():
            csv_path = os.path.join(data_dir, csv_file)
            
            if os.path.exists(csv_path):
                logger.info(f"开始导入 {csv_file} 到表 {table_name}")
                if self.import_csv_data(csv_path, table_name):
                    success_count += 1
                    logger.info(f"✅ {csv_file} 导入成功！")
                else:
                    logger.error(f"❌ {csv_file} 导入失败！")
            else:
                logger.warning(f"文件 {csv_path} 不存在，跳过导入")
        
        logger.info(f"数据导入完成！成功导入 {success_count}/{total_count} 个文件")
        return success_count == total_count
    
    def verify_data(self):
        """验证导入的数据"""
        try:
            tables = ['users', 'products', 'orders', 'user_behavior', 'user_features']
            
            logger.info("\n=== 数据验证报告 ===")
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                logger.info(f"表 {table}: {count} 条记录")
            
            # 检查外键关系
            logger.info("\n=== 数据关系验证 ===")
            
            # 检查订单表中的用户ID是否都存在于用户表中
            self.cursor.execute("""
                SELECT COUNT(*) FROM orders o 
                LEFT JOIN users u ON o.用户ID = u.用户ID 
                WHERE u.用户ID IS NULL
            """)
            orphan_orders = self.cursor.fetchone()[0]
            logger.info(f"孤立订单记录（用户不存在）: {orphan_orders} 条")
            
            # 检查订单表中的产品ID是否都存在于产品表中
            self.cursor.execute("""
                SELECT COUNT(*) FROM orders o 
                LEFT JOIN products p ON o.产品ID = p.产品ID 
                WHERE p.产品ID IS NULL
            """)
            orphan_product_orders = self.cursor.fetchone()[0]
            logger.info(f"孤立订单记录（产品不存在）: {orphan_product_orders} 条")
            
            logger.info("数据验证完成！")
            return True
            
        except Error as e:
            logger.error(f"数据验证失败: {e}")
            return False
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("数据库连接已关闭")

def main():
    """主函数"""
    logger.info("开始执行机器学习电商数据导入任务...")
    
    # 创建数据导入器实例
    importer = DataImporter(
        host='localhost',
        user='root', 
        password='',  # 根据实际情况修改密码
        database='ml_research_db'
    )
    
    try:
        # 连接数据库
        if not importer.connect_database():
            logger.error("无法连接数据库，程序退出")
            return False
        
        # 创建表结构
        logger.info("创建数据库表结构...")
        if not importer.create_tables():
            logger.error("创建表结构失败，程序退出")
            return False
        
        # 导入所有数据
        logger.info("开始导入CSV数据...")
        data_dir = './data'  # CSV文件所在目录
        if not importer.import_all_data(data_dir):
            logger.warning("部分数据导入失败，请检查日志")
        
        # 验证数据
        logger.info("验证导入的数据...")
        importer.verify_data()
        
        logger.info("🎉 数据导入任务完成！")
        return True
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        return False
    
    finally:
        # 关闭数据库连接
        importer.close_connection()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 数据导入成功完成！")
        print("现在你可以在 ml_research_db 数据库中查看和分析这些数据了！")
    else:
        print("\n❌ 数据导入过程中出现错误，请检查日志信息。")
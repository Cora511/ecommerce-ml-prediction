#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
吹风机电商数据生成器 - 模拟一年周期的抖店电商数据

功能：
1. 生成用户信息数据
2. 生成产品信息数据
3. 生成订单交易数据
4. 生成用户行为数据
5. 考虑季节性因素和节假日影响

作者：AI数据科学家
日期：2024年
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子确保结果可重现
np.random.seed(42)
random.seed(42)

class 吹风机电商数据生成器:
    def __init__(self):
        self.fake = Faker('zh_CN')
        self.开始日期 = datetime(2023, 1, 1)
        self.结束日期 = datetime(2023, 12, 31)
        
        # 吹风机产品类型和价格区间
        self.产品类型 = {
            '家用基础款': {'价格区间': (50, 150), '权重': 0.4},
            '专业沙龙款': {'价格区间': (200, 500), '权重': 0.3},
            '高端智能款': {'价格区间': (600, 1500), '权重': 0.2},
            '便携旅行款': {'价格区间': (80, 200), '权重': 0.1}
        }
        
        # 季节性因素（影响销量）
        self.季节因子 = {
            '春季': 1.0,   # 3-5月
            '夏季': 0.8,   # 6-8月（夏天用吹风机较少）
            '秋季': 1.2,   # 9-11月（换季护发）
            '冬季': 1.4    # 12-2月（冬天洗头后需要快速吹干）
        }
        
        # 节假日促销因子
        self.节假日 = {
            '元旦': {'日期': '01-01', '促销因子': 1.5},
            '情人节': {'日期': '02-14', '促销因子': 1.3},
            '妇女节': {'日期': '03-08', '促销因子': 1.8},
            '劳动节': {'日期': '05-01', '促销因子': 1.6},
            '618购物节': {'日期': '06-18', '促销因子': 2.5},
            '七夕节': {'日期': '08-22', '促销因子': 1.4},
            '双十一': {'日期': '11-11', '促销因子': 3.0},
            '双十二': {'日期': '12-12', '促销因子': 2.2}
        }
    
    def 生成用户数据(self, 用户数量=10000):
        """
        生成用户基础信息数据
        """
        print(f"🚀 开始生成 {用户数量} 个用户数据...")
        
        用户数据 = []
        for i in range(用户数量):
            # 年龄分布：主要集中在18-45岁
            年龄 = np.random.choice(
                range(18, 60), 
                p=self._生成年龄分布概率()
            )
            
            # 性别分布：女性用户较多（70%）
            性别 = np.random.choice(['女', '男'], p=[0.7, 0.3])
            
            # 城市等级分布
            城市等级 = np.random.choice(
                ['一线城市', '二线城市', '三线城市', '四线及以下'],
                p=[0.25, 0.35, 0.25, 0.15]
            )
            
            # 收入水平（影响购买力）
            收入水平 = self._根据年龄城市生成收入(年龄, 城市等级)
            
            用户 = {
                '用户ID': f'U{i+1:06d}',
                '用户名': self.fake.name(),
                '性别': 性别,
                '年龄': 年龄,
                '城市': self.fake.city(),
                '城市等级': 城市等级,
                '收入水平': 收入水平,
                '注册日期': self.fake.date_between(start_date='-2y', end_date='today'),
                '会员等级': self._生成会员等级(),
                '手机号': self.fake.phone_number(),
                '邮箱': self.fake.email()
            }
            用户数据.append(用户)
        
        用户df = pd.DataFrame(用户数据)
        print(f"✅ 用户数据生成完成！共 {len(用户df)} 条记录")
        return 用户df
    
    def 生成产品数据(self, 产品数量=50):
        """
        生成吹风机产品信息数据
        """
        print(f"🚀 开始生成 {产品数量} 个产品数据...")
        
        产品数据 = []
        品牌列表 = ['飞利浦', '松下', '戴森', '小米', '美的', '海尔', '奥克斯', '康夫', '沙宣', '博朗']
        
        for i in range(产品数量):
            产品类型 = np.random.choice(
                list(self.产品类型.keys()),
                p=[info['权重'] for info in self.产品类型.values()]
            )
            
            价格区间 = self.产品类型[产品类型]['价格区间']
            价格 = round(np.random.uniform(价格区间[0], 价格区间[1]), 2)
            
            产品 = {
                '产品ID': f'P{i+1:04d}',
                '产品名称': f'{random.choice(品牌列表)} {产品类型} 吹风机',
                '品牌': random.choice(品牌列表),
                '产品类型': 产品类型,
                '价格': 价格,
                '功率': np.random.choice([1200, 1400, 1600, 1800, 2000, 2200]),
                '重量': round(np.random.uniform(0.4, 0.8), 2),
                '颜色': np.random.choice(['黑色', '白色', '粉色', '蓝色', '紫色']),
                '上架日期': self.fake.date_between(start_date='-1y', end_date='today'),
                '库存数量': np.random.randint(50, 500),
                '评分': round(np.random.uniform(3.5, 5.0), 1),
                '评价数量': np.random.randint(10, 1000)
            }
            产品数据.append(产品)
        
        产品df = pd.DataFrame(产品数据)
        print(f"✅ 产品数据生成完成！共 {len(产品df)} 条记录")
        return 产品df
    
    def 生成订单数据(self, 用户df, 产品df, 订单数量=50000):
        """
        生成订单交易数据（考虑季节性和节假日因素）
        """
        print(f"🚀 开始生成 {订单数量} 个订单数据...")
        
        订单数据 = []
        
        for i in range(订单数量):
            # 随机选择订单日期
            订单日期 = self._生成随机日期()
            
            # 根据日期获取季节和节假日因子
            季节因子 = self._获取季节因子(订单日期)
            节假日因子 = self._获取节假日因子(订单日期)
            
            # 随机选择用户和产品
            用户 = 用户df.sample(1).iloc[0]
            产品 = 产品df.sample(1).iloc[0]
            
            # 根据用户收入水平调整购买概率
            购买概率 = self._计算购买概率(用户, 产品, 季节因子, 节假日因子)
            
            if np.random.random() < 购买概率:
                # 生成订单数量（大部分是1个，少数是2-3个）
                数量 = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])
                
                # 计算折扣（节假日期间折扣更大）
                折扣率 = self._计算折扣率(节假日因子)
                实际价格 = 产品['价格'] * (1 - 折扣率)
                
                订单 = {
                    '订单ID': f'O{i+1:08d}',
                    '用户ID': 用户['用户ID'],
                    '产品ID': 产品['产品ID'],
                    '订单日期': 订单日期,
                    '数量': 数量,
                    '原价': 产品['价格'],
                    '折扣率': 折扣率,
                    '实际价格': round(实际价格, 2),
                    '总金额': round(实际价格 * 数量, 2),
                    '支付方式': np.random.choice(['微信支付', '支付宝', '银行卡'], p=[0.5, 0.3, 0.2]),
                    '配送方式': np.random.choice(['标准配送', '次日达', '当日达'], p=[0.6, 0.3, 0.1]),
                    '订单状态': np.random.choice(['已完成', '已取消', '退货'], p=[0.85, 0.1, 0.05]),
                    '评价分数': np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.03, 0.1, 0.35, 0.5]) if np.random.random() < 0.7 else None
                }
                订单数据.append(订单)
        
        订单df = pd.DataFrame(订单数据)
        print(f"✅ 订单数据生成完成！共 {len(订单df)} 条记录")
        return 订单df
    
    def 生成用户行为数据(self, 用户df, 产品df, 行为数量=200000):
        """
        生成用户行为数据（浏览、收藏、加购物车等）
        """
        print(f"🚀 开始生成 {行为数量} 个用户行为数据...")
        
        行为数据 = []
        行为类型 = ['浏览', '收藏', '加购物车', '分享', '咨询客服']
        行为权重 = [0.6, 0.15, 0.15, 0.05, 0.05]
        
        for i in range(行为数量):
            用户 = 用户df.sample(1).iloc[0]
            产品 = 产品df.sample(1).iloc[0]
            行为时间 = self._生成随机日期时间()
            
            行为 = {
                '行为ID': f'B{i+1:08d}',
                '用户ID': 用户['用户ID'],
                '产品ID': 产品['产品ID'],
                '行为类型': np.random.choice(行为类型, p=行为权重),
                '行为时间': 行为时间,
                '停留时长': np.random.randint(10, 300) if np.random.random() < 0.8 else np.random.randint(300, 1800),
                '来源渠道': np.random.choice(['搜索', '推荐', '广告', '直播', '朋友分享'], p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                '设备类型': np.random.choice(['手机', '电脑', '平板'], p=[0.8, 0.15, 0.05])
            }
            行为数据.append(行为)
        
        行为df = pd.DataFrame(行为数据)
        print(f"✅ 用户行为数据生成完成！共 {len(行为df)} 条记录")
        return 行为df
    
    def _生成年龄分布概率(self):
        """生成符合实际的年龄分布概率"""
        ages = list(range(18, 60))
        probs = []
        for age in ages:
            if 20 <= age <= 35:  # 主力消费群体
                prob = 0.04
            elif 18 <= age < 20 or 35 < age <= 45:  # 次要群体
                prob = 0.02
            else:  # 其他年龄段
                prob = 0.005
            probs.append(prob)
        
        # 归一化
        total = sum(probs)
        return [p/total for p in probs]
    
    def _根据年龄城市生成收入(self, 年龄, 城市等级):
        """根据年龄和城市等级生成收入水平"""
        基础收入 = {
            '一线城市': 8000,
            '二线城市': 6000,
            '三线城市': 4500,
            '四线及以下': 3500
        }
        
        年龄因子 = min(1.5, (年龄 - 18) * 0.02 + 0.8)
        收入 = 基础收入[城市等级] * 年龄因子 * np.random.uniform(0.7, 1.8)
        
        if 收入 < 3000:
            return '低收入'
        elif 收入 < 8000:
            return '中等收入'
        elif 收入 < 15000:
            return '高收入'
        else:
            return '超高收入'
    
    def _生成会员等级(self):
        """生成会员等级"""
        return np.random.choice(
            ['普通会员', '银牌会员', '金牌会员', 'VIP会员'],
            p=[0.6, 0.25, 0.12, 0.03]
        )
    
    def _生成随机日期(self):
        """生成随机日期"""
        delta = self.结束日期 - self.开始日期
        random_days = np.random.randint(0, delta.days + 1)
        return self.开始日期 + timedelta(days=random_days)
    
    def _生成随机日期时间(self):
        """生成随机日期时间"""
        日期 = self._生成随机日期()
        小时 = np.random.randint(0, 24)
        分钟 = np.random.randint(0, 60)
        秒 = np.random.randint(0, 60)
        return 日期.replace(hour=小时, minute=分钟, second=秒)
    
    def _获取季节因子(self, 日期):
        """根据日期获取季节因子"""
        月份 = 日期.month
        if 3 <= 月份 <= 5:
            return self.季节因子['春季']
        elif 6 <= 月份 <= 8:
            return self.季节因子['夏季']
        elif 9 <= 月份 <= 11:
            return self.季节因子['秋季']
        else:
            return self.季节因子['冬季']
    
    def _获取节假日因子(self, 日期):
        """根据日期获取节假日因子"""
        日期字符串 = 日期.strftime('%m-%d')
        for 节日, 信息 in self.节假日.items():
            if 日期字符串 == 信息['日期']:
                return 信息['促销因子']
        return 1.0
    
    def _计算购买概率(self, 用户, 产品, 季节因子, 节假日因子):
        """计算购买概率"""
        基础概率 = 0.1
        
        # 收入水平影响
        收入影响 = {
            '低收入': 0.5,
            '中等收入': 1.0,
            '高收入': 1.5,
            '超高收入': 2.0
        }
        
        # 产品类型影响
        产品影响 = {
            '家用基础款': 1.2,
            '专业沙龙款': 1.0,
            '高端智能款': 0.6,
            '便携旅行款': 0.8
        }
        
        概率 = (基础概率 * 
                收入影响[用户['收入水平']] * 
                产品影响[产品['产品类型']] * 
                季节因子 * 
                节假日因子)
        
        return min(0.8, 概率)  # 最大概率限制为80%
    
    def _计算折扣率(self, 节假日因子):
        """计算折扣率"""
        if 节假日因子 > 2.0:  # 大促销日
            return np.random.uniform(0.2, 0.4)
        elif 节假日因子 > 1.5:  # 中等促销
            return np.random.uniform(0.1, 0.25)
        elif 节假日因子 > 1.0:  # 小促销
            return np.random.uniform(0.05, 0.15)
        else:  # 平时
            return np.random.uniform(0.0, 0.1)
    
    def 保存数据到文件(self, 用户df, 产品df, 订单df, 行为df, 保存路径='./data/'):
        """
        保存所有数据到CSV文件
        """
        import os
        os.makedirs(保存路径, exist_ok=True)
        
        print("💾 开始保存数据到文件...")
        
        用户df.to_csv(f'{保存路径}/用户数据.csv', index=False, encoding='utf-8-sig')
        产品df.to_csv(f'{保存路径}/产品数据.csv', index=False, encoding='utf-8-sig')
        订单df.to_csv(f'{保存路径}/订单数据.csv', index=False, encoding='utf-8-sig')
        行为df.to_csv(f'{保存路径}/用户行为数据.csv', index=False, encoding='utf-8-sig')
        
        print("✅ 所有数据已保存到CSV文件！")
        
        # 打印数据统计信息
        print("\n📊 数据统计信息：")
        print(f"用户数据：{len(用户df)} 条")
        print(f"产品数据：{len(产品df)} 条")
        print(f"订单数据：{len(订单df)} 条")
        print(f"用户行为数据：{len(行为df)} 条")
        
        return {
            '用户数据': 用户df,
            '产品数据': 产品df,
            '订单数据': 订单df,
            '用户行为数据': 行为df
        }

def main():
    """
    主函数：生成完整的电商数据
    """
    print("🎉 欢迎使用吹风机电商数据生成器！")
    print("=" * 50)
    
    # 创建数据生成器实例
    生成器 = 吹风机电商数据生成器()
    
    # 生成各类数据
    用户数据 = 生成器.生成用户数据(用户数量=10000)
    产品数据 = 生成器.生成产品数据(产品数量=50)
    订单数据 = 生成器.生成订单数据(用户数据, 产品数据, 订单数量=50000)
    行为数据 = 生成器.生成用户行为数据(用户数据, 产品数据, 行为数量=200000)
    
    # 保存数据
    数据集 = 生成器.保存数据到文件(用户数据, 产品数据, 订单数据, 行为数据)
    
    print("\n🎊 数据生成完成！可以开始进行机器学习分析了！")
    return 数据集

if __name__ == "__main__":
    数据集 = main()
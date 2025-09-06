#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机森林预测模型 - 预测用户消费行为和LTV

功能：
1. 用户消费行为预测
2. 购买概率预测
3. 客户生命周期价值(LTV)预测
4. 用户价值分群
5. 消费趋势分析

作者：AI数据科学家
日期：2024年
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, classification_report, confusion_matrix
from sklearn.cluster import KMeans
import joblib
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class 随机森林预测模型:
    def __init__(self):
        self.用户特征编码器 = {}
        self.标准化器 = StandardScaler()
        self.购买概率模型 = None
        self.LTV预测模型 = None
        self.消费金额模型 = None
        self.客户分群模型 = None
        
    def 加载数据(self, 数据路径='./data/'):
        """
        加载生成的电商数据
        """
        print("📂 开始加载数据...")
        
        try:
            self.用户数据 = pd.read_csv(f'{数据路径}/用户数据.csv')
            self.产品数据 = pd.read_csv(f'{数据路径}/产品数据.csv')
            self.订单数据 = pd.read_csv(f'{数据路径}/订单数据.csv')
            self.行为数据 = pd.read_csv(f'{数据路径}/用户行为数据.csv')
            
            print(f"✅ 数据加载成功！")
            print(f"用户数据：{len(self.用户数据)} 条")
            print(f"产品数据：{len(self.产品数据)} 条")
            print(f"订单数据：{len(self.订单数据)} 条")
            print(f"行为数据：{len(self.行为数据)} 条")
            
        except Exception as e:
            print(f"❌ 数据加载失败：{e}")
            return False
            
        return True
    
    def 特征工程(self):
        """
        进行特征工程，构建机器学习特征
        """
        print("🔧 开始特征工程...")
        
        # 1. 用户基础特征
        用户特征 = self.用户数据.copy()
        
        # 编码分类变量
        分类列 = ['性别', '城市等级', '收入水平', '会员等级']
        for 列 in 分类列:
            le = LabelEncoder()
            用户特征[f'{列}_编码'] = le.fit_transform(用户特征[列])
            self.用户特征编码器[列] = le
        
        # 2. 用户历史订单特征
        订单统计 = self.订单数据.groupby('用户ID').agg({
            '订单ID': 'count',  # 订单次数
            '总金额': ['sum', 'mean', 'std'],  # 总消费、平均消费、消费标准差
            '数量': 'sum',  # 总购买数量
            '折扣率': 'mean',  # 平均折扣率
            '订单日期': ['min', 'max']  # 首次和最后购买时间
        }).reset_index()
        
        # 扁平化列名
        订单统计.columns = ['用户ID', '订单次数', '总消费金额', '平均消费金额', '消费标准差', 
                        '总购买数量', '平均折扣率', '首次购买日期', '最后购买日期']
        
        # 计算购买频率和间隔
        订单统计['首次购买日期'] = pd.to_datetime(订单统计['首次购买日期'])
        订单统计['最后购买日期'] = pd.to_datetime(订单统计['最后购买日期'])
        订单统计['购买天数跨度'] = (订单统计['最后购买日期'] - 订单统计['首次购买日期']).dt.days + 1
        订单统计['购买频率'] = 订单统计['订单次数'] / 订单统计['购买天数跨度']
        订单统计['购买频率'] = 订单统计['购买频率'].fillna(0)
        
        # 3. 用户行为特征
        行为统计 = self.行为数据.groupby('用户ID').agg({
            '行为ID': 'count',  # 总行为次数
            '停留时长': ['sum', 'mean'],  # 总停留时长、平均停留时长
        }).reset_index()
        
        行为统计.columns = ['用户ID', '总行为次数', '总停留时长', '平均停留时长']
        
        # 各类行为次数统计
        行为类型统计 = self.行为数据.groupby(['用户ID', '行为类型']).size().unstack(fill_value=0).reset_index()
        行为类型统计.columns = ['用户ID'] + [f'{col}_次数' for col in 行为类型统计.columns[1:]]
        
        # 4. 合并所有特征
        特征数据 = 用户特征.merge(订单统计, on='用户ID', how='left')
        特征数据 = 特征数据.merge(行为统计, on='用户ID', how='left')
        特征数据 = 特征数据.merge(行为类型统计, on='用户ID', how='left')
        
        # 填充缺失值
        数值列 = 特征数据.select_dtypes(include=[np.number]).columns
        特征数据[数值列] = 特征数据[数值列].fillna(0)
        
        # 5. 计算RFM特征（重要的客户价值指标）
        特征数据['R_最近购买天数'] = (pd.Timestamp.now() - 特征数据['最后购买日期']).dt.days
        特征数据['F_购买频率'] = 特征数据['订单次数']
        特征数据['M_消费金额'] = 特征数据['总消费金额']
        
        # 6. 创建目标变量
        # 购买概率（是否有购买行为）
        特征数据['是否购买'] = (特征数据['订单次数'] > 0).astype(int)
        
        # LTV计算（简化版：总消费金额 + 预期未来价值）
        特征数据['LTV'] = 特征数据['总消费金额'] + (特征数据['平均消费金额'] * 特征数据['购买频率'] * 365)
        特征数据['LTV'] = 特征数据['LTV'].fillna(0)
        
        # 客户价值分级（处理重复值问题）
        try:
            特征数据['客户价值等级'] = pd.qcut(特征数据['LTV'], q=5, labels=['低价值', '较低价值', '中等价值', '较高价值', '高价值'], duplicates='drop')
        except ValueError:
            # 如果仍然有问题，使用cut方法
            ltv_min = 特征数据['LTV'].min()
            ltv_max = 特征数据['LTV'].max()
            bins = np.linspace(ltv_min, ltv_max, 6)
            特征数据['客户价值等级'] = pd.cut(特征数据['LTV'], bins=bins, labels=['低价值', '较低价值', '中等价值', '较高价值', '高价值'], include_lowest=True)
        
        self.特征数据 = 特征数据
        print(f"✅ 特征工程完成！特征数据形状：{特征数据.shape}")
        
        return 特征数据
    
    def 训练购买概率模型(self):
        """
        训练预测用户购买概率的随机森林模型
        """
        print("🤖 开始训练购买概率预测模型...")
        
        # 选择特征
        特征列 = ['年龄', '性别_编码', '城市等级_编码', '收入水平_编码', '会员等级_编码',
                '总行为次数', '平均停留时长', '浏览_次数', '收藏_次数', '加购物车_次数']
        
        X = self.特征数据[特征列].fillna(0)
        y = self.特征数据['是否购买']
        
        # 分割训练测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 训练随机森林模型
        self.购买概率模型 = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.购买概率模型.fit(X_train, y_train)
        
        # 模型评估
        训练分数 = self.购买概率模型.score(X_train, y_train)
        测试分数 = self.购买概率模型.score(X_test, y_test)
        
        print(f"✅ 购买概率模型训练完成！")
        print(f"训练集准确率：{训练分数:.4f}")
        print(f"测试集准确率：{测试分数:.4f}")
        
        # 特征重要性
        特征重要性 = pd.DataFrame({
            '特征': 特征列,
            '重要性': self.购买概率模型.feature_importances_
        }).sort_values('重要性', ascending=False)
        
        print("\n📊 特征重要性排序：")
        print(特征重要性.head(10))
        
        return 特征重要性
    
    def 训练LTV预测模型(self):
        """
        训练预测客户生命周期价值的随机森林模型
        """
        print("🤖 开始训练LTV预测模型...")
        
        # 只使用有购买行为的用户
        有购买用户 = self.特征数据[self.特征数据['是否购买'] == 1].copy()
        
        if len(有购买用户) == 0:
            print("❌ 没有购买用户数据，无法训练LTV模型")
            return None
        
        # 选择特征
        特征列 = ['年龄', '性别_编码', '城市等级_编码', '收入水平_编码', '会员等级_编码',
                '订单次数', '平均消费金额', '购买频率', '总行为次数', '平均停留时长',
                'R_最近购买天数', 'F_购买频率', 'M_消费金额']
        
        X = 有购买用户[特征列].fillna(0)
        y = 有购买用户['LTV']
        
        # 分割训练测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 训练随机森林模型
        self.LTV预测模型 = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.LTV预测模型.fit(X_train, y_train)
        
        # 模型评估
        y_pred = self.LTV预测模型.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ LTV预测模型训练完成！")
        print(f"均方误差 (MSE)：{mse:.2f}")
        print(f"R² 分数：{r2:.4f}")
        
        # 特征重要性
        特征重要性 = pd.DataFrame({
            '特征': 特征列,
            '重要性': self.LTV预测模型.feature_importances_
        }).sort_values('重要性', ascending=False)
        
        print("\n📊 LTV预测特征重要性：")
        print(特征重要性.head(10))
        
        return 特征重要性
    
    def 客户价值分群(self):
        """
        使用K-means对客户进行价值分群
        """
        print("👥 开始客户价值分群分析...")
        
        # 选择RFM特征进行聚类
        聚类特征 = ['R_最近购买天数', 'F_购买频率', 'M_消费金额']
        聚类数据 = self.特征数据[聚类特征].fillna(0)
        
        # 标准化
        聚类数据_标准化 = self.标准化器.fit_transform(聚类数据)
        
        # K-means聚类
        self.客户分群模型 = KMeans(n_clusters=5, random_state=42)
        客户分群 = self.客户分群模型.fit_predict(聚类数据_标准化)
        
        # 根据RFM特征为分群添加有意义的标签
        分群中心 = self.特征数据.groupby(客户分群).agg({
            'R_最近购买天数': 'mean',
            'F_购买频率': 'mean', 
            'M_消费金额': 'mean',
            'LTV': 'mean'
        })
        
        # 创建标签映射
        标签映射 = {}
        for 分群号 in range(len(分群中心)):
            ltv_值 = 分群中心.loc[分群号, 'LTV']
            if ltv_值 >= 分群中心['LTV'].quantile(0.8):
                标签映射[分群号] = '高价值'
            elif ltv_值 >= 分群中心['LTV'].quantile(0.6):
                标签映射[分群号] = '较高价值'
            elif ltv_值 >= 分群中心['LTV'].quantile(0.4):
                标签映射[分群号] = '中等价值'
            elif ltv_值 >= 分群中心['LTV'].quantile(0.2):
                标签映射[分群号] = '较低价值'
            else:
                标签映射[分群号] = '低价值'
        
        # 应用标签映射
        self.特征数据['客户价值等级'] = [标签映射[x] for x in 客户分群]
        
        # 分析各群体特征
        分群统计 = self.特征数据.groupby('客户价值等级').agg({
            'R_最近购买天数': 'mean',
            'F_购买频率': 'mean',
            'M_消费金额': 'mean',
            'LTV': 'mean',
            '用户ID': 'count'
        }).round(2)
        
        分群统计.columns = ['平均最近购买天数', '平均购买频率', '平均消费金额', '平均LTV', '用户数量']
        
        print("✅ 客户分群完成！")
        print("\n📊 各分群特征：")
        print(分群统计)
        
        return 分群统计
    
    def 预测新用户(self, 用户特征):
        """
        预测新用户的购买概率和LTV
        """
        if self.购买概率模型 is None or self.LTV预测模型 is None:
            print("❌ 模型未训练，请先训练模型")
            return None
        
        # 预测购买概率
        购买概率 = self.购买概率模型.predict_proba([用户特征])[0][1]
        
        # 预测LTV（如果购买概率较高）
        if 购买概率 > 0.5:
            预测LTV = self.LTV预测模型.predict([用户特征])[0]
        else:
            预测LTV = 0
        
        return {
            '购买概率': 购买概率,
            '预测LTV': 预测LTV
        }
    
    def 保存模型(self, 保存路径='./models/'):
        """
        保存训练好的模型
        """
        import os
        os.makedirs(保存路径, exist_ok=True)
        
        print("💾 开始保存模型...")
        
        if self.购买概率模型 is not None:
            joblib.dump(self.购买概率模型, f'{保存路径}/购买概率模型.pkl')
        
        if self.LTV预测模型 is not None:
            joblib.dump(self.LTV预测模型, f'{保存路径}/LTV预测模型.pkl')
        
        if self.客户分群模型 is not None:
            joblib.dump(self.客户分群模型, f'{保存路径}/客户分群模型.pkl')
        
        # 保存编码器和标准化器
        joblib.dump(self.用户特征编码器, f'{保存路径}/特征编码器.pkl')
        joblib.dump(self.标准化器, f'{保存路径}/标准化器.pkl')
        
        print("✅ 模型保存完成！")
    
    def 加载模型(self, 保存路径='./models/'):
        """
        加载已保存的模型
        """
        print("📂 开始加载模型...")
        
        try:
            self.购买概率模型 = joblib.load(f'{保存路径}/购买概率模型.pkl')
            self.LTV预测模型 = joblib.load(f'{保存路径}/LTV预测模型.pkl')
            self.客户分群模型 = joblib.load(f'{保存路径}/客户分群模型.pkl')
            self.用户特征编码器 = joblib.load(f'{保存路径}/特征编码器.pkl')
            self.标准化器 = joblib.load(f'{保存路径}/标准化器.pkl')
            
            print("✅ 模型加载成功！")
            return True
        except Exception as e:
            print(f"❌ 模型加载失败：{e}")
            return False
    
    def 生成预测报告(self):
        """
        生成完整的预测分析报告
        """
        print("📋 开始生成预测报告...")
        
        报告 = {
            '数据概览': {
                '总用户数': len(self.特征数据),
                '有购买用户数': len(self.特征数据[self.特征数据['是否购买'] == 1]),
                '购买转化率': len(self.特征数据[self.特征数据['是否购买'] == 1]) / len(self.特征数据),
                '平均LTV': self.特征数据['LTV'].mean(),
                '总GMV': self.特征数据['总消费金额'].sum()
            },
            '客户分群分析': self.特征数据.groupby('客户价值等级').agg({
                'LTV': ['count', 'mean', 'sum'],
                '总消费金额': 'mean',
                '订单次数': 'mean'
            }).round(2),
            '高价值客户特征': self.特征数据[self.特征数据['客户价值等级'] == '高价值'].describe()
        }
        
        print("✅ 预测报告生成完成！")
        return 报告

def main():
    """
    主函数：完整的机器学习流程
    """
    print("🎉 欢迎使用随机森林预测模型！")
    print("=" * 50)
    
    # 创建模型实例
    模型 = 随机森林预测模型()
    
    # 加载数据
    if not 模型.加载数据():
        print("❌ 请先运行数据生成器生成数据")
        return
    
    # 特征工程
    特征数据 = 模型.特征工程()
    
    # 训练模型
    购买概率特征重要性 = 模型.训练购买概率模型()
    LTV特征重要性 = 模型.训练LTV预测模型()
    
    # 客户分群
    分群统计 = 模型.客户价值分群()
    
    # 生成报告
    报告 = 模型.生成预测报告()
    
    # 保存模型
    模型.保存模型()
    
    print("\n🎊 随机森林预测模型训练完成！")
    print("\n📊 数据概览：")
    for key, value in 报告['数据概览'].items():
        print(f"{key}: {value}")
    
    return 模型, 报告

if __name__ == "__main__":
    模型, 报告 = main()
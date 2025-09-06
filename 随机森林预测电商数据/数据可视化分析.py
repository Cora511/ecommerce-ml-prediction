#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化分析模块 - 生成专业的电商数据分析图表

功能：
1. 用户行为分析图表
2. 销售趋势可视化
3. 客户价值分群可视化
4. LTV预测结果展示
5. 随机森林模型性能可视化
6. 综合分析仪表板

作者：AI数据科学家
日期：2024年
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")

class 电商数据可视化:
    def __init__(self):
        self.颜色方案 = {
            '主色': '#1f77b4',
            '辅色': '#ff7f0e', 
            '强调色': '#2ca02c',
            '警告色': '#d62728',
            '信息色': '#9467bd'
        }
        
    def 加载数据(self, 数据路径='./data/'):
        """
        加载所有数据文件
        """
        print("📂 加载可视化数据...")
        
        try:
            self.用户数据 = pd.read_csv(f'{数据路径}/用户数据.csv')
            self.产品数据 = pd.read_csv(f'{数据路径}/产品数据.csv')
            self.订单数据 = pd.read_csv(f'{数据路径}/订单数据.csv')
            self.行为数据 = pd.read_csv(f'{数据路径}/用户行为数据.csv')
            
            # 转换日期格式
            self.订单数据['订单日期'] = pd.to_datetime(self.订单数据['订单日期'])
            self.行为数据['行为时间'] = pd.to_datetime(self.行为数据['行为时间'])
            
            print("✅ 数据加载成功！")
            return True
            
        except Exception as e:
            print(f"❌ 数据加载失败：{e}")
            return False
    
    def 销售趋势分析图(self, 保存路径='./charts/'):
        """
        生成销售趋势分析图表
        """
        print("📈 生成销售趋势分析图...")
        
        # 按日期聚合销售数据
        日销售 = self.订单数据.groupby('订单日期').agg({
            '总金额': 'sum',
            '订单ID': 'count',
            '数量': 'sum'
        }).reset_index()
        
        日销售.columns = ['日期', '销售额', '订单数', '销售量']
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🛒 吹风机电商销售趋势分析', fontsize=20, fontweight='bold')
        
        # 1. 日销售额趋势
        axes[0,0].plot(日销售['日期'], 日销售['销售额'], 
                      color=self.颜色方案['主色'], linewidth=2, marker='o', markersize=3)
        axes[0,0].set_title('📊 日销售额趋势', fontsize=14, fontweight='bold')
        axes[0,0].set_ylabel('销售额 (元)')
        axes[0,0].tick_params(axis='x', rotation=45)
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. 日订单数趋势
        axes[0,1].plot(日销售['日期'], 日销售['订单数'], 
                      color=self.颜色方案['辅色'], linewidth=2, marker='s', markersize=3)
        axes[0,1].set_title('📦 日订单数趋势', fontsize=14, fontweight='bold')
        axes[0,1].set_ylabel('订单数')
        axes[0,1].tick_params(axis='x', rotation=45)
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. 月度销售对比
        月销售 = 日销售.copy()
        月销售['月份'] = 月销售['日期'].dt.to_period('M')
        月度统计 = 月销售.groupby('月份').agg({
            '销售额': 'sum',
            '订单数': 'sum'
        }).reset_index()
        
        axes[1,0].bar(range(len(月度统计)), 月度统计['销售额'], 
                     color=self.颜色方案['强调色'], alpha=0.7)
        axes[1,0].set_title('📅 月度销售额对比', fontsize=14, fontweight='bold')
        axes[1,0].set_ylabel('销售额 (元)')
        axes[1,0].set_xticks(range(len(月度统计)))
        axes[1,0].set_xticklabels([str(m) for m in 月度统计['月份']], rotation=45)
        
        # 4. 销售额分布直方图
        axes[1,1].hist(self.订单数据['总金额'], bins=30, 
                      color=self.颜色方案['信息色'], alpha=0.7, edgecolor='black')
        axes[1,1].set_title('💰 订单金额分布', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('订单金额 (元)')
        axes[1,1].set_ylabel('频次')
        
        plt.tight_layout()
        plt.savefig(f'{保存路径}/销售趋势分析.png', dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表以避免阻塞
        
        return 日销售, 月度统计
    
    def 用户行为分析图(self, 保存路径='./charts/'):
        """
        生成用户行为分析图表
        """
        print("👥 生成用户行为分析图...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🎯 用户行为深度分析', fontsize=20, fontweight='bold')
        
        # 1. 行为类型分布饼图
        行为统计 = self.行为数据['行为类型'].value_counts()
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
        
        wedges, texts, autotexts = axes[0,0].pie(行为统计.values, labels=行为统计.index, 
                                                autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0,0].set_title('🔍 用户行为类型分布', fontsize=14, fontweight='bold')
        
        # 2. 用户年龄分布
        axes[0,1].hist(self.用户数据['年龄'], bins=20, 
                      color=self.颜色方案['主色'], alpha=0.7, edgecolor='black')
        axes[0,1].set_title('👤 用户年龄分布', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('年龄')
        axes[0,1].set_ylabel('用户数')
        
        # 3. 城市等级vs消费金额箱线图
        订单用户 = self.订单数据.merge(self.用户数据, on='用户ID')
        
        城市消费 = []
        城市标签 = []
        for 城市 in 订单用户['城市等级'].unique():
            城市数据 = 订单用户[订单用户['城市等级'] == 城市]['总金额']
            if len(城市数据) > 0:  # 确保有数据
                城市消费.append(城市数据)
                城市标签.append(城市)
        
        if len(城市消费) > 0:
            bp = axes[1,0].boxplot(城市消费, labels=城市标签, patch_artist=True)
            # 确保颜色数量匹配
            colors_to_use = colors[:len(bp['boxes'])]
            for patch, color in zip(bp['boxes'], colors_to_use):
                patch.set_facecolor(color)
        else:
            axes[1,0].text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=axes[1,0].transAxes)
        
        axes[1,0].set_title('🏙️ 不同城市等级消费分布', fontsize=14, fontweight='bold')
        axes[1,0].set_ylabel('消费金额 (元)')
        
        # 4. 会员等级vs订单频次
        会员订单 = 订单用户.groupby(['会员等级', '用户ID']).size().reset_index(name='订单数')
        会员统计 = 会员订单.groupby('会员等级')['订单数'].mean()
        
        bars = axes[1,1].bar(会员统计.index, 会员统计.values, 
                           color=self.颜色方案['强调色'], alpha=0.8)
        axes[1,1].set_title('👑 会员等级vs平均订单数', fontsize=14, fontweight='bold')
        axes[1,1].set_ylabel('平均订单数')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            axes[1,1].text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'{保存路径}/用户行为分析.png', dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表以避免阻塞
    
    def 产品分析图(self, 保存路径='./charts/'):
        """
        生成产品分析图表
        """
        print("🎁 生成产品分析图...")
        
        # 计算产品销售统计
        产品销售 = self.订单数据.groupby('产品ID').agg({
            '总金额': 'sum',
            '订单ID': 'count',
            '数量': 'sum'
        }).reset_index()
        
        产品销售 = 产品销售.merge(self.产品数据, on='产品ID')
        # 动态设置列名，避免长度不匹配
        expected_cols = ['产品ID', '总销售额', '订单数', '销售量', '产品名称', '品牌', '产品类型', '价格', '功率', '重量', '颜色', '上架日期', '库存数量', '评分', '评价数量']
        actual_cols = 产品销售.columns.tolist()
        print(f"实际列数: {len(actual_cols)}, 预期列数: {len(expected_cols)}")
        print(f"实际列名: {actual_cols}")
        
        # 只重命名关键列，保持原有列名结构
        if len(actual_cols) >= 4:
            # 重命名前4列（来自订单聚合的列）
            rename_dict = {
                actual_cols[0]: '产品ID',
                actual_cols[1]: '总销售额', 
                actual_cols[2]: '订单数',
                actual_cols[3]: '销售量'
            }
            产品销售 = 产品销售.rename(columns=rename_dict)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🎁 产品销售分析报告', fontsize=20, fontweight='bold')
        
        # 1. 品牌销售额对比
        品牌销售 = 产品销售.groupby('品牌')['总销售额'].sum().sort_values(ascending=False)
        
        bars = axes[0,0].bar(品牌销售.index, 品牌销售.values, 
                           color=plt.cm.Set3(np.linspace(0, 1, len(品牌销售))))
        axes[0,0].set_title('🏆 品牌销售额排行', fontsize=14, fontweight='bold')
        axes[0,0].set_ylabel('销售额 (元)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. 价格vs销量散点图
        scatter = axes[0,1].scatter(产品销售['价格'], 产品销售['销售量'], 
                                  c=产品销售['总销售额'], cmap='viridis', 
                                  s=100, alpha=0.7)
        axes[0,1].set_title('💰 价格vs销量关系', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('价格 (元)')
        axes[0,1].set_ylabel('销售量')
        plt.colorbar(scatter, ax=axes[0,1], label='总销售额')
        
        # 3. 功率分布
        功率数据 = self.产品数据['功率'].dropna()
        if len(功率数据) > 0:
            # 动态计算bins数量，避免超过数据点数量
            bins_count = min(15, len(功率数据.unique()))
            axes[1,0].hist(功率数据, bins=bins_count, 
                          color=self.颜色方案['辅色'], alpha=0.7, edgecolor='black')
        else:
            axes[1,0].text(0.5, 0.5, '暂无功率数据', ha='center', va='center', transform=axes[1,0].transAxes)
        axes[1,0].set_title('⚡ 产品功率分布', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('功率 (W)')
        axes[1,0].set_ylabel('产品数量')
        
        # 4. 热销产品TOP10
        热销产品 = 产品销售.nlargest(10, '总销售额')
        
        if len(热销产品) > 0:
            bars = axes[1,1].barh(range(len(热销产品)), 热销产品['总销售额'], 
                                color=self.颜色方案['强调色'], alpha=0.8)
            axes[1,1].set_title('🔥 热销产品TOP10', fontsize=14, fontweight='bold')
            axes[1,1].set_xlabel('销售额 (元)')
            axes[1,1].set_yticks(range(len(热销产品)))
            产品名称列表 = [f'{name[:10]}...' if len(str(name)) > 10 else str(name) 
                         for name in 热销产品['产品名称']]
            axes[1,1].set_yticklabels(产品名称列表)
        else:
            axes[1,1].text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=axes[1,1].transAxes)
            axes[1,1].set_title('🔥 热销产品TOP10', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{保存路径}/产品分析.png', dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表以避免阻塞
        
        return 产品销售
    
    def 客户价值分群可视化(self, 特征数据, 保存路径='./charts/'):
        """
        生成客户价值分群可视化图表
        """
        print("👥 生成客户分群可视化...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🎯 客户价值分群分析', fontsize=20, fontweight='bold')
        
        # 1. RFM 3D散点图（投影到2D）
        scatter = axes[0,0].scatter(特征数据['R_最近购买天数'], 特征数据['M_消费金额'], 
                                  c=特征数据['客户价值等级'].astype('category').cat.codes, cmap='tab10', s=50, alpha=0.7)
        axes[0,0].set_title('📊 RFM客户分群 (R vs M)', fontsize=14, fontweight='bold')
        axes[0,0].set_xlabel('最近购买天数 (R)')
        axes[0,0].set_ylabel('消费金额 (M)')
        plt.colorbar(scatter, ax=axes[0,0], label='客户分群')
        
        # 2. 各分群LTV分布箱线图
        分群数据 = []
        分群标签 = []
        for 分群 in sorted(特征数据['客户价值等级'].unique()):
            分群LTV = 特征数据[特征数据['客户价值等级'] == 分群]['LTV']
            分群数据.append(分群LTV)
            分群标签.append(f'{分群}')
        
        bp = axes[0,1].boxplot(分群数据, labels=分群标签, patch_artist=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(分群数据)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        axes[0,1].set_title('💎 各分群LTV分布', fontsize=14, fontweight='bold')
        axes[0,1].set_ylabel('LTV (元)')
        
        # 3. 分群用户数量饼图
        分群统计 = 特征数据['客户价值等级'].value_counts()
        
        wedges, texts, autotexts = axes[1,0].pie(分群统计.values, 
                                               labels=分群统计.index,
                                               autopct='%1.1f%%', 
                                               colors=colors, startangle=90)
        axes[1,0].set_title('👥 客户价值分群占比', fontsize=14, fontweight='bold')
        
        # 4. 分群特征雷达图（简化版）
        分群特征 = 特征数据.groupby('客户价值等级').agg({
            'R_最近购买天数': 'mean',
            'F_购买频率': 'mean', 
            'M_消费金额': 'mean',
            'LTV': 'mean'
        }).round(2)
        
        # 标准化特征用于雷达图
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        分群特征_标准化 = pd.DataFrame(
            scaler.fit_transform(分群特征),
            columns=分群特征.columns,
            index=分群特征.index
        )
        
        # 绘制热力图代替雷达图
        sns.heatmap(分群特征_标准化.T, annot=True, cmap='YlOrRd', 
                   ax=axes[1,1], cbar_kws={'label': '标准化值'})
        axes[1,1].set_title('🔥 分群特征热力图', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('客户价值等级')
        
        plt.tight_layout()
        plt.savefig(f'{保存路径}/客户价值分群.png', dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表以避免阻塞
        
        return 分群特征
    
    def 模型性能可视化(self, 模型, 特征数据, 保存路径='./charts/'):
        """
        生成机器学习模型性能可视化
        """
        print("🤖 生成模型性能可视化...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🤖 随机森林模型性能分析', fontsize=20, fontweight='bold')
        
        # 1. 特征重要性图（购买概率模型）
        if hasattr(模型, '购买概率模型') and 模型.购买概率模型 is not None:
            特征列 = ['年龄', '性别_编码', '城市等级_编码', '收入水平_编码', '会员等级_编码',
                    '总行为次数', '平均停留时长', '浏览_次数', '收藏_次数', '加购物车_次数']
            
            重要性 = 模型.购买概率模型.feature_importances_
            
            # 排序
            indices = np.argsort(重要性)[::-1]
            
            bars = axes[0,0].bar(range(len(重要性)), 重要性[indices], 
                               color=self.颜色方案['主色'], alpha=0.8)
            axes[0,0].set_title('📊 购买概率预测-特征重要性', fontsize=14, fontweight='bold')
            axes[0,0].set_ylabel('重要性')
            axes[0,0].set_xticks(range(len(重要性)))
            axes[0,0].set_xticklabels([特征列[i] for i in indices], rotation=45)
        
        # 2. LTV预测散点图
        if hasattr(模型, 'LTV预测模型') and 模型.LTV预测模型 is not None:
            有购买用户 = 特征数据[特征数据['是否购买'] == 1].copy()
            
            if len(有购买用户) > 0:
                特征列_LTV = ['年龄', '性别_编码', '城市等级_编码', '收入水平_编码', '会员等级_编码',
                           '订单次数', '平均消费金额', '购买频率', '总行为次数', '平均停留时长',
                           'R_最近购买天数', 'F_购买频率', 'M_消费金额']
                
                X = 有购买用户[特征列_LTV].fillna(0)
                y_true = 有购买用户['LTV']
                y_pred = 模型.LTV预测模型.predict(X)
                
                axes[0,1].scatter(y_true, y_pred, alpha=0.6, color=self.颜色方案['辅色'])
                axes[0,1].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 
                             'r--', lw=2)
                axes[0,1].set_title('🎯 LTV预测 vs 实际值', fontsize=14, fontweight='bold')
                axes[0,1].set_xlabel('实际LTV')
                axes[0,1].set_ylabel('预测LTV')
        
        # 3. 客户分群轮廓图
        分群统计 = 特征数据.groupby('客户价值等级').agg({
            'LTV': ['count', 'mean'],
            '总消费金额': 'mean'
        }).round(2)
        
        分群统计.columns = ['用户数', '平均LTV', '平均消费']
        
        x = np.arange(len(分群统计))
        width = 0.35
        
        bars1 = axes[1,0].bar(x - width/2, 分群统计['用户数'], width, 
                            label='用户数', color=self.颜色方案['强调色'], alpha=0.8)
        
        ax2 = axes[1,0].twinx()
        bars2 = ax2.bar(x + width/2, 分群统计['平均LTV'], width, 
                       label='平均LTV', color=self.颜色方案['警告色'], alpha=0.8)
        
        axes[1,0].set_title('📈 客户分群价值分析', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('客户分群')
        axes[1,0].set_ylabel('用户数', color=self.颜色方案['强调色'])
        ax2.set_ylabel('平均LTV', color=self.颜色方案['警告色'])
        axes[1,0].set_xticks(x)
        axes[1,0].set_xticklabels([f'{i}' for i in 分群统计.index])
        
        # 4. 消费行为时间序列
        if '订单日期' in 特征数据.columns:
            # 这里需要从订单数据重新计算
            日消费 = self.订单数据.groupby('订单日期')['总金额'].sum().reset_index()
            
            axes[1,1].plot(日消费['订单日期'], 日消费['总金额'], 
                         color=self.颜色方案['信息色'], linewidth=2)
            axes[1,1].set_title('📅 消费趋势时间序列', fontsize=14, fontweight='bold')
            axes[1,1].set_ylabel('日消费金额')
            axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{保存路径}/模型性能分析.png', dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表以避免阻塞
    
    def 生成交互式仪表板(self, 特征数据, 保存路径='./charts/'):
        """
        生成交互式Plotly仪表板
        """
        print("📊 生成交互式仪表板...")
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('客户分群分布', 'LTV分布', '消费金额vs年龄', '购买频率分析'),
            specs=[[{"type": "pie"}, {"type": "histogram"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 1. 客户分群饼图
        分群统计 = 特征数据['客户价值等级'].value_counts()
        fig.add_trace(
            go.Pie(labels=分群统计.index, 
                  values=分群统计.values,
                  name="客户价值等级"),
            row=1, col=1
        )
        
        # 2. LTV分布直方图
        fig.add_trace(
            go.Histogram(x=特征数据['LTV'], name="LTV分布", nbinsx=30),
            row=1, col=2
        )
        
        # 3. 消费金额vs年龄散点图
        fig.add_trace(
            go.Scatter(x=特征数据['年龄'], y=特征数据['总消费金额'],
                      mode='markers', name="年龄vs消费",
                      marker=dict(color=特征数据['客户价值等级'].astype('category').cat.codes, 
                                colorscale='Viridis', size=8)),
            row=2, col=1
        )
        
        # 4. 购买频率柱状图
        频率统计 = 特征数据.groupby('客户价值等级')['F_购买频率'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=频率统计['客户价值等级'], 
                  y=频率统计['F_购买频率'],
                  name="平均购买频率"),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title_text="🎯 电商数据分析交互式仪表板",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # 保存HTML文件
        fig.write_html(f'{保存路径}/交互式仪表板.html')
        fig.show()
        
        print(f"✅ 交互式仪表板已保存到：{保存路径}/交互式仪表板.html")
    
    def 生成综合报告图表(self, 特征数据, 模型=None, 保存路径='./charts/'):
        """
        生成综合分析报告的所有图表
        """
        print("🎨 开始生成综合报告图表...")
        
        import os
        os.makedirs(保存路径, exist_ok=True)
        
        # 生成所有图表
        日销售, 月度统计 = self.销售趋势分析图(保存路径)
        self.用户行为分析图(保存路径)
        产品销售 = self.产品分析图(保存路径)
        分群特征 = self.客户价值分群可视化(特征数据, 保存路径)
        
        if 模型 is not None:
            self.模型性能可视化(模型, 特征数据, 保存路径)
        
        self.生成交互式仪表板(特征数据, 保存路径)
        
        print("🎊 所有图表生成完成！")
        
        return {
            '日销售数据': 日销售,
            '月度统计': 月度统计,
            '产品销售': 产品销售,
            '分群特征': 分群特征
        }

def main():
    """
    主函数：生成所有可视化图表
    """
    print("🎨 欢迎使用电商数据可视化分析系统！")
    print("=" * 50)
    
    # 创建可视化实例
    可视化 = 电商数据可视化()
    
    # 加载数据
    if not 可视化.加载数据():
        print("❌ 请先生成数据")
        return
    
    # 加载特征数据（如果存在）
    try:
        特征数据 = pd.read_csv('./data/特征数据.csv')
        print("✅ 特征数据加载成功")
    except:
        print("⚠️ 特征数据不存在，将只生成基础图表")
        特征数据 = None
    
    # 生成图表
    if 特征数据 is not None:
        图表数据 = 可视化.生成综合报告图表(特征数据)
    else:
        # 只生成基础图表
        可视化.销售趋势分析图()
        可视化.用户行为分析图()
        可视化.产品分析图()
    
    print("\n🎉 数据可视化完成！")
    print("📁 所有图表已保存到 ./charts/ 目录")

if __name__ == "__main__":
    main()
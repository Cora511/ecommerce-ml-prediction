#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from 数据可视化分析 import 电商数据可视化

def debug_产品分析():
    try:
        print("🔍 开始调试产品分析图...")
        
        # 创建可视化对象
        可视化 = 电商数据可视化()
        
        # 加载数据
        print("📂 加载数据...")
        可视化.加载数据('./data/')
        
        print(f"产品数据形状: {可视化.产品数据.shape}")
        print(f"订单数据形状: {可视化.订单数据.shape}")
        
        print("\n产品数据列名:")
        print(可视化.产品数据.columns.tolist())
        
        print("\n订单数据列名:")
        print(可视化.订单数据.columns.tolist())
        
        print("\n产品数据前5行:")
        print(可视化.产品数据.head())
        
        # 尝试生成产品分析图
        print("\n🎁 开始生成产品分析图...")
        可视化.产品分析图('./charts/')
        
        print("✅ 产品分析图生成成功！")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        print("\n完整错误信息:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_产品分析()
import pandas as pd

df = pd.read_csv('./data/特征数据.csv')
print('是否有客户分群列:', '客户分群' in df.columns)
print('是否有客户价值等级列:', '客户价值等级' in df.columns)
print('\n所有列名:')
for i, col in enumerate(df.columns):
    print(f'{i}: {col}')

if '客户分群' in df.columns:
    print('\n客户分群的唯一值:', df['客户分群'].unique())
if '客户价值等级' in df.columns:
    print('\n客户价值等级的唯一值:', df['客户价值等级'].unique())
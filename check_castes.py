import pandas as pd

df = pd.read_csv('cet_official_data.csv')
print("📊 Caste categories in CSV:")
print(df['caste_category'].unique())
print(f"\n🎯 Total unique castes: {len(df['caste_category'].unique())}")
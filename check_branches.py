import pandas as pd

df = pd.read_csv('cet_official_data.csv')
print("📊 Course names in CSV:")
print(df['course_name'].unique())
print(f"\n🎯 Total unique courses: {len(df['course_name'].unique())}")


df = pd.read_csv('cet_official_data.csv')
coep_colleges = df[df['college_name'].str.contains('COEP Technological University', case=False, na=False)]
print("COEP colleges in CSV:")
print(coep_colleges[['college_name', 'course_name', 'caste_category', 'cutoff_percentile']].head(20))
import pandas as pd

# Read your existing CSV
df = pd.read_csv('cet_official_data.csv')

# COEP data from your screenshot
coep_rows = [
    # Civil Engineering
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'GOPEN', 'cutoff_percentile': 96.05, 'cutoff_rank': 138},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'GST', 'cutoff_percentile': 93.53, 'cutoff_rank': 848},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'GOBC', 'cutoff_percentile': 95.53, 'cutoff_rank': 220},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'LOPEN', 'cutoff_percentile': 98.00, 'cutoff_rank': 21},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'LSC', 'cutoff_percentile': 95.10, 'cutoff_rank': 322},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'LOBC', 'cutoff_percentile': 95.16, 'cutoff_rank': 306},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'LSEBC', 'cutoff_percentile': 95.79, 'cutoff_rank': 174},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Civil Engineering', 'caste_category': 'EWS', 'cutoff_percentile': 95.21, 'cutoff_rank': 286},
    
    # Computer Science and Engineering
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GOPEN', 'cutoff_percentile': 97.65, 'cutoff_rank': 33},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GSC', 'cutoff_percentile': 96.05, 'cutoff_rank': 136},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GST', 'cutoff_percentile': 94.82, 'cutoff_rank': 400},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GNTA', 'cutoff_percentile': 94.11, 'cutoff_rank': 614},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GNTD', 'cutoff_percentile': 96.00, 'cutoff_rank': 140},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GOBC', 'cutoff_percentile': 97.06, 'cutoff_rank': 51},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'GSEBC', 'cutoff_percentile': 97.18, 'cutoff_rank': 45},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'LOPEN', 'cutoff_percentile': 99.70, 'cutoff_rank': 5},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'LOBC', 'cutoff_percentile': 98.80, 'cutoff_rank': 13},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'PWDR-SC', 'cutoff_percentile': 91.09, 'cutoff_rank': 2500},
    {'college_code': '16006', 'college_name': 'COEP Technological University (University Autonomous)', 'course_name': 'Computer Science and Engineering', 'caste_category': 'EWS', 'cutoff_percentile': 96.63, 'cutoff_rank': 74},
    
    # Add more courses as needed...
]

# Convert to DataFrame and append
coep_df = pd.DataFrame(coep_rows)
updated_df = pd.concat([df, coep_df], ignore_index=True)

# Save updated CSV
updated_df.to_csv('cet_official_data_with_coep.csv', index=False)
print(f"✅ Added {len(coep_rows)} COEP records!")
print(f"📊 Total records: {len(updated_df)}")
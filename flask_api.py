from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import ExtraTreesClassifier
import pickle

# Import your existing ML code
from ml_api import COLLEGES_DATA

def ml_powered_recommender(percentile, caste_input, branch_input):
    print("🎓 ML-POWERED COLLEGE RECOMMENDER")
    print("=" * 45)

    # Use parameters instead of input()
    percentile = float(percentile)
    caste_input = caste_input.upper()
    branch_input = branch_input.upper()

    print(f"\n🤖 ML Model analyzing colleges for {percentile}% - {caste_input} caste...")

    # Import ML libraries
    from sklearn.ensemble import ExtraTreesClassifier
    import pandas as pd
    import numpy as np
    import pickle

    # SMART CASTE MAPPING
    caste_mapping = {
        'OPEN': ['GOPEN', 'LOPEN'],
        'OBC': ['GOBC', 'LOBC', 'GSEBC', 'LSEBC', 'PWD-OBC', 'DEFR-OBC'],
        'SC': ['GSC', 'LSC', 'PWD-SC'],
        'ST': ['GST', 'LST', 'PWD-ST'],
        'EWS': ['EWS'],
        'NT': ['GNTA', 'GNTB', 'GNTC', 'GNTD', 'LNTA', 'LNTB', 'LNTC', 'LNTD'],
        'PWD': ['PWD-O', 'PWD-OBC', 'PWD-SC', 'PWD-ST', 'PWDR-OBC', 'PWDR-SC']
    }

    # Get all possible caste categories for the input
    if caste_input in caste_mapping:
        caste_categories = caste_mapping[caste_input]
    else:
        caste_categories = []
        for category_group in caste_mapping.values():
            for cat in category_group:
                if caste_input in cat or cat in caste_input:
                    caste_categories.append(cat)
        if not caste_categories:
            caste_categories = ['GOPEN', 'GOBC', 'GSC', 'GST']

    # Branch groups
    branch_groups = {
        'CS': ['computer science', 'cse', 'computer engineering', 'computer science and engineering',
               'artificial intelligence', 'ai', 'data science', 'aids', 'aiml', 'ai&ml', 'computer'],
        'IT': ['information technology', 'it'],
        'MECH': ['mechanical engineering', 'mechanical'],
        'CIVIL': ['civil engineering', 'civil'],
        'ECE': ['electronics', 'ece', 'electronics and communication', 'electronics and telecommunication'],
        'EEE': ['electrical', 'eee', 'electrical and electronics']
    }

    # CREATE AND TRAIN THE BEST ML MODEL
    def create_ml_model(colleges_data):
        print("🔄 Training Best ML Model (Extra Trees Classifier)...")

        training_data = []
        for college_name, college_data in colleges_data.items():
            for course_name, course_data in college_data.items():
                if isinstance(course_data, dict):
                    for category, cutoff in course_data.items():
                        if isinstance(cutoff, (int, float)) and cutoff > 0:
                            for student_pct in range(40, 101, 5):
                                safety_margin = student_pct - cutoff
                                admission_possible = 1 if safety_margin >= 0 else 0
                                training_data.append({
                                    'student_percentile': student_pct,
                                    'college_cutoff': cutoff,
                                    'safety_margin': safety_margin,
                                    'admission_possible': admission_possible
                                })

        if not training_data:
            print("❌ No training data found!")
            return None

        df = pd.DataFrame(training_data)
        X = df[['student_percentile', 'college_cutoff', 'safety_margin']]
        y = df['admission_possible']

        model = ExtraTreesClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        print(f"✅ Best ML Model Trained: Extra Trees Classifier")
        print(f"📊 Training Accuracy: {model.score(X, y):.2%}")
        print(f"📈 Training Samples: {len(training_data)}")

        # Save model
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        print("✅ Model saved as model.pkl")

        return model

    # ML prediction function
    def ml_predict_admission(student_percentile, college_cutoff, safety_margin, model):
        features = np.array([[student_percentile, college_cutoff, safety_margin]])
        probability = model.predict_proba(features)[0][1]
        return probability

    # ML-based chance calculation
    def ml_calculate_chance(ml_probability):
        if ml_probability >= 0.95:
            return "🟢 ML-GUARANTEED", "🟢"
        elif ml_probability >= 0.85:
            return "🟢 ML-HIGH", "🟢"
        elif ml_probability >= 0.70:
            return "🟡 ML-GOOD", "🟡"
        elif ml_probability >= 0.50:
            return "🟡 ML-MODERATE", "🟡"
        elif ml_probability >= 0.30:
            return "🔴 ML-RISKY", "🔴"
        elif ml_probability >= 0.10:
            return "🔴 ML-DREAM", "🔴"
        else:
            return "🔴 ML-IMPOSSIBLE", "🔴"

    # Train the ML model (COLLEGES_DATA must exist)
    ml_model = create_ml_model(COLLEGES_DATA)
    if ml_model is None:
        print("❌ ML Model training failed! Using rule-based system.")
        return []

    all_recommendations = []

    # Prediction loop
    for college_name, college_data in COLLEGES_DATA.items():
        for course_name, course_data in college_data.items():
            if isinstance(course_data, dict):
                course_lower = course_name.lower()

                if branch_input != "ALL":
                    matched = False
                    if branch_input in branch_groups:
                        for keyword in branch_groups[branch_input]:
                            if keyword in course_lower:
                                matched = True
                                break
                    if not matched:
                        continue

                for caste_category in caste_categories:
                    if caste_category in course_data:
                        cutoff_value = course_data[caste_category]
                        if not isinstance(cutoff_value, (int, float)) or cutoff_value <= 0:
                            continue

                        safety_margin = percentile - cutoff_value
                        ml_probability = ml_predict_admission(percentile, cutoff_value, safety_margin, ml_model)
                        ml_chance, status = ml_calculate_chance(ml_probability)

                        all_recommendations.append({
                            'college': college_name,
                            'course': course_name,
                            'category': caste_category,
                            'cutoff': cutoff_value,
                            'safety_margin': safety_margin,
                            'chance': ml_chance,
                            'status': status,
                            'ml_probability': ml_probability,
                            'your_score': percentile
                        })
                        break

    # Sort and print summary
    all_recommendations.sort(key=lambda x: x['ml_probability'], reverse=True)

    print(f"\n🏫 ML-PREDICTED COLLEGES: {len(all_recommendations)} COLLEGES")
    print("=" * 100)
    print("🤖 Using Best ML Model: Extra Trees Classifier")
    print("=" * 100)

    guaranteed = len([r for r in all_recommendations if 'GUARANTEED' in r['chance']])
    high = len([r for r in all_recommendations if 'HIGH' in r['chance']])
    good = len([r for r in all_recommendations if 'GOOD' in r['chance']])
    moderate = len([r for r in all_recommendations if 'MODERATE' in r['chance']])
    risky = len([r for r in all_recommendations if 'RISKY' in r['chance']])
    dream = len([r for r in all_recommendations if 'DREAM' in r['chance']])

    print(f"📊 ML PREDICTION SUMMARY:")
    print(f"   🟢 Guaranteed (>95%): {guaranteed} colleges")
    print(f"   🟢 High (85-94%): {high} colleges")
    print(f"   🟡 Good (70-84%): {good} colleges")
    print(f"   🟡 Moderate (50-69%): {moderate} colleges")
    print(f"   🔴 Risky (30-49%): {risky} colleges")
    print(f"   🔴 Dream (5-29%): {dream} colleges")
    print()

    for i, c in enumerate(all_recommendations[:50], 1):
        print(f"{i:2d}. {c['status']} {c['college']}")
        print(f"    📚 {c['course']}")
        print(f"    🏷️ {c['category']}")
        print(f"    📊 Cutoff: {c['cutoff']}% | Your: {c['your_score']}%")
        print(f"    📈 Margin: {c['safety_margin']:+.1f}%")
        print(f"    🤖 ML Prediction: {c['chance']} ({c['ml_probability']:.1%})")
        print()

# Run the main function
    return all_recommendations


app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    print("🎯 Flask received a request!")
    try:
        data = request.json
        cet_percentage = float(data['cetPercentage'])
        caste = data['caste'].upper()
        preferred_branch = data['preferredBranch'].upper()
        
        # Call your existing ML function
        results = ml_powered_recommender(cet_percentage, caste, preferred_branch)
        
        return jsonify({
            "success": True,
            "colleges": results
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
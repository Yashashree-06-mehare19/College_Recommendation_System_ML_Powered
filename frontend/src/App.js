import { useState } from 'react';
import './App.css';

function App() {
  const [cetPercentage, setCetPercentage] = useState('');
  const [caste, setCaste] = useState('');
  const [preferredBranch, setPreferredBranch] = useState('');
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(false);

  // NEW: location filter state
  const [locationFilter, setLocationFilter] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cetPercentage: cetPercentage,
          caste: caste,
          preferredBranch: preferredBranch
        })
      });
      
      const data = await response.json();
      console.log(data);
      
      if (data.success) {
        setColleges(data.colleges);
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      alert('Failed to connect to backend: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const getCardClass = (chance) => {
    if (chance.includes('GUARANTEED') || chance.includes('HIGH')) return 'college-card guaranteed';
    if (chance.includes('GOOD')) return 'college-card high';
    if (chance.includes('MODERATE')) return 'college-card moderate';
    if (chance.includes('RISKY')) return 'college-card risky';
    return 'college-card dream';
  };

  return (
    <div className="app">
      <div className="header">
        <h1>College Recommendation System</h1>
        <p>AI-Powered Direct second year College Admissions Predictor (MAHARASHTRA)</p>
      </div>
      
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>CET Percentage:</label>
            <input
              type="number"
              value={cetPercentage}
              onChange={(e) => setCetPercentage(e.target.value)}
              min="0"
              max="100"
              step="0.01"
              required
              placeholder="Enter your CET percentage"
            />
          </div>

          <div className="form-group">
            <label>Caste Category:</label>
            <select 
              value={caste} 
              onChange={(e) => setCaste(e.target.value)}
              required
            >
              <option value="">Select Caste Category</option>
              <option value="OPEN">OPEN</option>
              <option value="OBC">OBC</option>
              <option value="SC">SC</option>
              <option value="ST">ST</option>
            </select>
          </div>

          <div className="form-group">
            <label>Preferred Branch:</label>
            <select 
              value={preferredBranch} 
              onChange={(e) => setPreferredBranch(e.target.value)}
            >
              <option value="">All Branches</option>
              <option value="CS">Computer Science</option>
              <option value="IT">Information Technology</option>
              <option value="MECH">Mechanical Engineering</option>
              <option value="CIVIL">Civil Engineering</option>
              <option value="ECE">Electronics & Telecommunication</option>
            </select>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? '🔄 Analyzing...' : '🎓 Get Recommendations'}
          </button>
        </form>
      </div>

      {/* NEW: City Filter Dropdown */}
      <div className="form-group" style={{ marginTop: "25px", width: "300px" }}>
        <label>Filter by Location:</label>
        <select 
          value={locationFilter} 
          onChange={(e) => setLocationFilter(e.target.value)}
        >
          <option value="">All Locations</option>
          <option value="PUNE">Pune</option>
          <option value="MUMBAI">Mumbai</option>
          <option value="NASHIK">Nashik</option>
          <option value="AURANGABAD">Aurangabad</option>
          <option value="NAGPUR">Nagpur</option>
          <option value="SANGLI">Sangli</option>
          <option value="KOLHAPUR">Kolhapur</option>
          <option value="AMRAVATI">Amravati</option>
        </select>
      </div>

      {loading && (
        <div className="loading">
          <p>🤖 ML Model is analyzing your chances...</p>
        </div>
      )}

      <div className="colleges-container">
        <div className="results-header">
          <h2>Recommended Colleges</h2>
          {colleges.length > 0 && (
            <div className="results-count">Found {colleges.length} colleges</div>
          )}
        </div>

        {colleges.length > 0 ? (
          <div>
            {[...colleges]
              // .filter(college => 
              //   locationFilter === "" ||
              //   college.college.toUpperCase().includes(locationFilter) 
              // )
              .filter(college => {
  if (locationFilter === "") return true;

  const name = college.college.toUpperCase();

  // special rule for COEP
  if (locationFilter === "PUNE" && (name.includes("COEP") || name.includes("COLLEGE OF ENGINEERING"))) {
    return true;
  }

  return name.includes(locationFilter);
})

              .reverse()
              .map((college, index) => (
                <div key={index} className={getCardClass(college.chance)}>
                  <div className="college-header">
                    <h3 className="college-name">{college.college}</h3>
                    <span className="ml-badge">{college.chance}</span>
                  </div>
                  
                  <div className="college-details">
                    <div className="detail-item">
                      <span>📚</span>
                      <strong>{college.course}</strong>
                    </div>
                    <div className="detail-item">
                      <span>🏷️</span>
                      <strong>Category:</strong> {college.category}
                    </div>
                    <div className="detail-item">
                      <span>📊</span>
                      <strong>Cutoff:</strong> {college.cutoff}% | 
                      <strong> Your Score:</strong> {college.your_score}%
                    </div>
                    <div className="detail-item">
                      <span>📈</span>
                      <strong>Margin:</strong> {college.safety_margin >= 0 ? '+' : ''}{college.safety_margin}%
                    </div>
                    <div className="detail-item">
                      <span>🤖</span>
                      <strong>ML Confidence:</strong> {(college.ml_probability * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
          </div>
        ) : (
          !loading && (
            <div className="no-results">
              <p>Submit the form above to see your personalized college recommendations</p>
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default App;

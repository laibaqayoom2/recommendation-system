### MovieLens Recommendation System
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/1a37916a-613f-4b7b-8f08-aaa77ab33314" />
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/db419ff7-aac2-471f-9893-c5b752489bf6" />

**Full-Stack Machine Learning Application**

**Tech Stack:** Python, Flask, Pandas, NumPy, Scikit-learn, React, Tailwind CSS, Lucide React

**Key Achievements:**
* Designed and deployed production-ready recommendation engine processing real-world dataset with 100,000 user ratings across 1,682 movies
* Implemented content-based filtering using TF-IDF vectorization and cosine similarity matrix calculation for genre-based recommendations
* Developed RESTful API architecture with Flask serving multiple endpoints (recommendations, statistics, health checks) with average response time under 500ms
* Built data preprocessing pipeline handling CSV data parsing, feature extraction, similarity matrix computation, and weighted scoring algorithms
* Created modern single-page React application with real-time API integration, loading states, error boundaries, and responsive design
* Engineered smart recommendation algorithm combining genre matching, rating analysis, and popularity metrics to generate top-5 personalized suggestions
* Applied machine learning concepts including feature engineering, similarity measurements, data normalization, and ranking algorithms

**Technical Highlights:**
* Processed 100,000+ ratings using Pandas for efficient data manipulation
* Computed 1,682×1,682 similarity matrix using Scikit-learn's cosine similarity
* Implemented weighted scoring: `score = genre_match × (avg_rating / 5.0)`
* Built CORS-enabled REST API with JSON request/response handling
* Designed responsive UI with Tailwind CSS supporting mobile and desktop views
* Included automated testing scripts and setup verification tools

---

**Backend (Python/Flask)**
```python
# Core Technologies
- Flask 3.0.0 for RESTful API
- Pandas 2.1.4 for data manipulation
- Scikit-learn 1.3.2 for ML algorithms
- NumPy 1.26.2 for numerical computing
```

**Frontend (React)**
```javascript
// UI Technologies
- React 18+ for component architecture
- Tailwind CSS for responsive design
- Fetch API for asynchronous requests
- Real-time state management
```

**Machine Learning Pipeline**
1. **Data Preprocessing:** Load and clean 100k ratings, extract features from 19 genre categories
2. **Feature Engineering:** Create genre vectors, compute average ratings, filter by popularity
3. **Similarity Calculation:** Generate cosine similarity matrix (1682×1682) for genre-based matching
4. **Scoring Algorithm:** Weight matches by rating quality: `score = match × (rating/5.0)`
5. **Recommendation Generation:** Return top-5 ranked movies with metadata and reasoning

#### Key Technical Achievements

**Data Engineering:**
- Processed CSV files with 100k+ rows using Pandas
- Engineered features from 19 binary genre columns
- Computed rating statistics (mean, count) per movie
- Built efficient data structures for fast lookups

**Machine Learning:**
- Implemented content-based filtering algorithm
- Applied TF-IDF vectorization for text analysis
- Calculated cosine similarity for 2.8M pairwise comparisons
- Developed weighted scoring with multiple factors

**API Development:**
- Created 4 RESTful endpoints with JSON responses
- Implemented CORS for cross-origin requests
- Added error handling and validation
- Achieved <500ms average response time

**Frontend Development:**
- Built responsive React SPA with 1000+ lines of code
- Implemented real-time data fetching and state management
- Created dynamic UI components with conditional rendering
- Added loading states and error boundaries

#### Performance Metrics
```
Dataset Size: 1,682 movies, 100k ratings, 943 users
API Response: <500ms average
Similarity Matrix: 1,682 × 1,682 = 2,831,124 calculations
Memory Efficient: Processes dataset in <2GB RAM
```

#### Code Quality
- **Modular Architecture:** Separated concerns (data, API, ML logic)
- **Testing:** Automated test scripts for verification
- **Documentation:** Comprehensive README and setup guides
- **Error Handling:** Robust validation and fallback mechanisms
- **Type Safety:** Proper data validation and type checking

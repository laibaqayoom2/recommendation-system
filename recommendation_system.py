from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
CORS(app)

# Sample data (replace with real database)
movies_data = pd.DataFrame({
    'title': ['The Matrix', 'Inception', 'Interstellar', 'The Dark Knight', 'Pulp Fiction'],
    'genre': ['Sci-Fi Action', 'Sci-Fi Thriller', 'Sci-Fi Drama', 'Action Thriller', 'Crime Drama'],
    'description': [
        'A hacker discovers reality is a simulation',
        'Thieves enter dreams to plant ideas',
        'Astronauts travel through a wormhole',
        'Batman fights the Joker in Gotham',
        'Interconnected crime stories in LA'
    ],
    'rating': [4.5, 4.7, 4.8, 4.9, 4.6]
})

def get_content_based_recommendations(user_prefs, n=5):
    """Content-based filtering using TF-IDF"""
    
    # Combine all text features
    movies_data['combined'] = movies_data['genre'] + ' ' + movies_data['description']
    
    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_data['combined'])
    
    # Transform user preferences
    user_vector = tfidf.transform([user_prefs])
    
    # Calculate similarity
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)[0]
    
    # Get top N recommendations
    top_indices = similarity_scores.argsort()[-n:][::-1]
    
    recommendations = []
    for idx in top_indices:
        recommendations.append({
            'title': movies_data.iloc[idx]['title'],
            'description': movies_data.iloc[idx]['description'],
            'rating': float(movies_data.iloc[idx]['rating']),
            'similarity_score': float(similarity_scores[idx]),
            'reason': f"Matches your preference for {movies_data.iloc[idx]['genre']}"
        })
    
    return recommendations

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        preferences = data.get('preferences', '')
        category = data.get('category', 'movies')
        
        if not preferences:
            return jsonify({'error': 'No preferences provided'}), 400
        
        recommendations = get_content_based_recommendations(preferences)
        
        return jsonify({
            'recommendations': recommendations,
            'category': category
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
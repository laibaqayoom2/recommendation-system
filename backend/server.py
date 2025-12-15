from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)
CORS(app)

class MovieLensRecommender:
    def __init__(self, data_path='ml-100k'):
        """Initialize the recommender with MovieLens 100k dataset"""
        self.data_path = data_path
        self.movies_df = None
        self.ratings_df = None
        self.users_df = None
        self.genres = []
        self.user_item_matrix = None
        self.item_similarity = None
        
        self.load_data()
        self.preprocess_data()
        self.build_similarity_matrices()
    
    def load_data(self):
        """Load MovieLens 100k dataset files"""
        print("Loading MovieLens 100k dataset...")
        
        # Load movies (u.item)
        # Format: movie id | movie title | release date | video release date | IMDb URL | genres (19 binary columns)
        movie_columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
        genre_columns = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 
                        'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 
                        'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        
        self.movies_df = pd.read_csv(
            f'{self.data_path}/u.item', 
            sep='|', 
            encoding='latin-1',
            names=movie_columns + genre_columns,
            header=None
        )
        
        # Load ratings (u.data)
        # Format: user id | item id | rating | timestamp
        self.ratings_df = pd.read_csv(
            f'{self.data_path}/u.data',
            sep='\t',
            names=['user_id', 'movie_id', 'rating', 'timestamp'],
            header=None
        )
        
        # Load users (u.user)
        # Format: user id | age | gender | occupation | zip code
        self.users_df = pd.read_csv(
            f'{self.data_path}/u.user',
            sep='|',
            names=['user_id', 'age', 'gender', 'occupation', 'zip_code'],
            header=None
        )
        
        self.genres = genre_columns
        print(f"Loaded {len(self.movies_df)} movies, {len(self.ratings_df)} ratings, {len(self.users_df)} users")
    
    def preprocess_data(self):
        """Preprocess data for recommendations"""
        # Extract year from title (format: "Movie Name (Year)")
        self.movies_df['year'] = self.movies_df['title'].str.extract(r'\((\d{4})\)')
        self.movies_df['clean_title'] = self.movies_df['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)
        
        # Create genre list for each movie
        self.movies_df['genre_list'] = self.movies_df[self.genres].apply(
            lambda row: ', '.join([genre for genre, val in row.items() if val == 1]), 
            axis=1
        )
        
        # Calculate average rating and rating count for each movie
        movie_stats = self.ratings_df.groupby('movie_id').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movie_id', 'avg_rating', 'rating_count']
        
        self.movies_df = self.movies_df.merge(movie_stats, on='movie_id', how='left')
        self.movies_df['avg_rating'] = self.movies_df['avg_rating'].fillna(3.0)
        self.movies_df['rating_count'] = self.movies_df['rating_count'].fillna(0)
        
    def build_similarity_matrices(self):
        """Build similarity matrices for recommendations"""
        print("Building similarity matrices...")
        
        # Content-based similarity (genre-based)
        genre_matrix = self.movies_df[self.genres].values
        self.item_similarity = cosine_similarity(genre_matrix)
        
        # User-item matrix for collaborative filtering
        self.user_item_matrix = self.ratings_df.pivot_table(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
        
        print("Similarity matrices built successfully")
    
    def content_based_recommendations(self, preferences, n=5):
        """Content-based filtering using user preferences"""
        # Create a preference vector based on keywords
        preferences_lower = preferences.lower()
        
        # Score movies based on genre and title matching
        scores = []
        for idx, movie in self.movies_df.iterrows():
            score = 0
            
            # Check genre matches
            genre_list_lower = movie['genre_list'].lower()
            for genre in self.genres:
                if genre.lower() in preferences_lower and genre.lower() in genre_list_lower:
                    score += 2
            
            # Check title matches
            title_lower = movie['clean_title'].lower()
            words = preferences_lower.split()
            for word in words:
                if len(word) > 3 and word in title_lower:
                    score += 1
            
            # Boost score based on average rating
            score *= (movie['avg_rating'] / 5.0)
            
            # Only consider movies with at least 5 ratings
            if movie['rating_count'] >= 5:
                scores.append((idx, score, movie))
        
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        recommendations = []
        for idx, score, movie in scores[:n]:
            if score > 0:  # Only include movies with positive scores
                recommendations.append({
                    'title': movie['clean_title'],
                    'year': movie['year'] if pd.notna(movie['year']) else 'N/A',
                    'genres': movie['genre_list'],
                    'description': f"{movie['genre_list']} film from {movie['year'] if pd.notna(movie['year']) else 'unknown year'}",
                    'rating': round(float(movie['avg_rating']), 1),
                    'rating_count': int(movie['rating_count']),
                    'reason': f"Matches your preferences for {movie['genre_list']}"
                })
        
        # If no matches, return top-rated movies
        if len(recommendations) == 0:
            return self.get_top_rated(n)
        
        return recommendations
    
    def get_top_rated(self, n=5, min_ratings=20):
        """Get top-rated movies with minimum number of ratings"""
        top_movies = self.movies_df[
            self.movies_df['rating_count'] >= min_ratings
        ].nlargest(n, 'avg_rating')
        
        recommendations = []
        for idx, movie in top_movies.iterrows():
            recommendations.append({
                'title': movie['clean_title'],
                'year': movie['year'] if pd.notna(movie['year']) else 'N/A',
                'genres': movie['genre_list'],
                'description': f"{movie['genre_list']} film from {movie['year'] if pd.notna(movie['year']) else 'unknown year'}",
                'rating': round(float(movie['avg_rating']), 1),
                'rating_count': int(movie['rating_count']),
                'reason': f"Highly rated by {int(movie['rating_count'])} users"
            })
        
        return recommendations
    
    def collaborative_recommendations(self, user_id=None, n=5):
        """Item-based collaborative filtering"""
        if user_id and user_id in self.user_item_matrix.index:
            # Get user's rated movies
            user_ratings = self.user_item_matrix.loc[user_id]
            rated_movies = user_ratings[user_ratings > 0].index.tolist()
            
            # Calculate scores for unrated movies
            scores = {}
            for movie_id in self.user_item_matrix.columns:
                if movie_id not in rated_movies:
                    movie_idx = movie_id - 1  # Adjust for 0-based indexing
                    if movie_idx < len(self.item_similarity):
                        # Calculate weighted score based on similar movies
                        similar_scores = []
                        for rated_movie in rated_movies:
                            rated_idx = rated_movie - 1
                            if rated_idx < len(self.item_similarity):
                                similarity = self.item_similarity[movie_idx][rated_idx]
                                similar_scores.append(similarity * user_ratings[rated_movie])
                        
                        if similar_scores:
                            scores[movie_id] = np.mean(similar_scores)
            
            # Get top N recommendations
            top_movie_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:n]
        else:
            # If no user_id, return top-rated movies
            return self.get_top_rated(n)
        
        # Build recommendations
        recommendations = []
        for movie_id in top_movie_ids:
            movie = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]
            recommendations.append({
                'title': movie['clean_title'],
                'year': movie['year'] if pd.notna(movie['year']) else 'N/A',
                'genres': movie['genre_list'],
                'description': f"{movie['genre_list']} film from {movie['year'] if pd.notna(movie['year']) else 'unknown year'}",
                'rating': round(float(movie['avg_rating']), 1),
                'rating_count': int(movie['rating_count']),
                'reason': "Based on similar movies you might like"
            })
        
        return recommendations

# Initialize recommender
recommender = None

def initialize_recommender(data_path='ml-100k'):
    """Initialize the recommender system"""
    global recommender
    try:
        recommender = MovieLensRecommender(data_path)
        print("Recommender initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing recommender: {e}")
        return False

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint for recommendations"""
    if recommender is None:
        return jsonify({
            'error': 'Recommender not initialized. Please check if ml-100k folder exists.'
        }), 500
    
    try:
        data = request.json
        preferences = data.get('preferences', '')
        category = data.get('category', 'movies')
        method = data.get('method', 'content')  # 'content', 'collaborative', or 'hybrid'
        
        # Get recommendations based on method
        if method == 'collaborative':
            user_id = data.get('user_id', None)
            recommendations = recommender.collaborative_recommendations(user_id, n=5)
        else:  # content-based
            recommendations = recommender.content_based_recommendations(preferences, n=5)
        
        return jsonify({
            'recommendations': recommendations,
            'method': method
        })
    
    except Exception as e:
        print(f"Error in recommend endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dataset statistics"""
    if recommender is None:
        return jsonify({'error': 'Recommender not initialized'}), 500
    
    return jsonify({
        'total_movies': len(recommender.movies_df),
        'total_ratings': len(recommender.ratings_df),
        'total_users': len(recommender.users_df),
        'genres': recommender.genres,
        'avg_rating': float(recommender.ratings_df['rating'].mean()),
        'top_genres': recommender.movies_df['genre_list'].value_counts().head(10).to_dict()
    })

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get list of movies with filters"""
    if recommender is None:
        return jsonify({'error': 'Recommender not initialized'}), 500
    
    genre = request.args.get('genre', None)
    limit = int(request.args.get('limit', 20))
    
    df = recommender.movies_df.copy()
    
    if genre and genre in recommender.genres:
        df = df[df[genre] == 1]
    
    df = df.nlargest(limit, 'rating_count')
    
    movies = []
    for _, movie in df.iterrows():
        movies.append({
            'id': int(movie['movie_id']),
            'title': movie['clean_title'],
            'year': movie['year'] if pd.notna(movie['year']) else 'N/A',
            'genres': movie['genre_list'],
            'rating': round(float(movie['avg_rating']), 1),
            'rating_count': int(movie['rating_count'])
        })
    
    return jsonify({'movies': movies})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'recommender_initialized': recommender is not None
    })

if __name__ == '__main__':
    # Initialize recommender with MovieLens data
    # Make sure the ml-100k folder is in the same directory as this script
    import sys
    
    data_path = 'ml-100k'
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    
    print(f"Initializing recommender with data from: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"ERROR: Data path '{data_path}' does not exist!")
        print("Please download MovieLens 100k dataset and extract it.")
        sys.exit(1)
    
    if initialize_recommender(data_path):
        print("Starting Flask server on http://127.0.0.1:5002")
        app.run(host='0.0.0.0', port=5002, debug=True)
    else:
        print("Failed to initialize recommender. Exiting.")
        sys.exit(1)
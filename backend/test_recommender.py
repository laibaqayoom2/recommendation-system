#!/usr/bin/env python3
"""
Test script for MovieLens Recommendation System
Tests the recommendation engine without running the web server
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_recommender():
    """Test the recommendation system"""
    print("🧪 Testing MovieLens Recommendation System\n")
    
    try:
        from server import MovieLensRecommender
        
        print("📊 Loading dataset...")
        recommender = MovieLensRecommender('ml-100k')
        
        print(f"✅ Loaded {len(recommender.movies_df)} movies")
        print(f"✅ Loaded {len(recommender.ratings_df)} ratings")
        print(f"✅ Loaded {len(recommender.users_df)} users\n")
        
        # Test 1: Content-based recommendations
        print("=" * 70)
        print("Test 1: Content-Based Recommendations")
        print("=" * 70)
        
        test_preferences = [
            "I love action movies with sci-fi themes",
            "Looking for romantic comedies",
            "Dark thrillers with mystery",
            "Classic drama films"
        ]
        
        for pref in test_preferences:
            print(f"\n🔍 Preferences: \"{pref}\"")
            print("-" * 70)
            
            recommendations = recommender.content_based_recommendations(pref, n=3)
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n{i}. {rec['title']} ({rec['year']})")
                    print(f"   ⭐ Rating: {rec['rating']}/5.0 ({rec['rating_count']} ratings)")
                    print(f"   🎭 Genres: {rec['genres']}")
                    print(f"   💡 {rec['reason']}")
            else:
                print("   ❌ No recommendations found")
        
        # Test 2: Top-rated movies
        print("\n\n" + "=" * 70)
        print("Test 2: Top-Rated Movies (minimum 50 ratings)")
        print("=" * 70)
        
        top_movies = recommender.get_top_rated(n=5, min_ratings=50)
        
        for i, movie in enumerate(top_movies, 1):
            print(f"\n{i}. {movie['title']} ({movie['year']})")
            print(f"   ⭐ Rating: {movie['rating']}/5.0 ({movie['rating_count']} ratings)")
            print(f"   🎭 Genres: {movie['genres']}")
        
        # Test 3: Genre distribution
        print("\n\n" + "=" * 70)
        print("Test 3: Genre Distribution")
        print("=" * 70)
        
        for genre in recommender.genres[:10]:  # First 10 genres
            count = recommender.movies_df[recommender.movies_df[genre] == 1].shape[0]
            if count > 0:
                print(f"{genre:15s}: {count:4d} movies")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: Dataset not found")
        print(f"Details: {e}")
        print("\nPlease ensure the ml-100k folder exists in the backend directory")
        print("Download from: https://grouplens.org/datasets/movielens/100k/")
        return False
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_recommender()
    sys.exit(0 if success else 1)
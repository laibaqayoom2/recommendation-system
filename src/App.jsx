import React, { useState, useEffect } from 'react';
import { Star, Sparkles, ThumbsUp, BookOpen, Film, Music, ShoppingBag, TrendingUp, Database } from 'lucide-react';

export default function RecommendationSystem() {
  const [category, setCategory] = useState('movies');
  const [preferences, setPreferences] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [systemReady, setSystemReady] = useState(false);

  const categories = [
    { id: 'movies', name: 'Movies', icon: Film, description: 'MovieLens 100k Dataset' }
  ];

  // Check if backend is ready
  useEffect(() => {
    checkBackendHealth();
    fetchStats();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5002/api/health');
      const data = await response.json();
      setSystemReady(data.recommender_initialized);
    } catch (error) {
      console.error('Backend not available:', error);
      setSystemReady(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5002/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const getRecommendations = async () => {
    if (!preferences.trim()) return;

    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5002/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          preferences: preferences,
          category: category,
          method: 'content'
        })
      });

      const data = await response.json();
      
      if (data.error) {
        console.error('Error:', data.error);
        setRecommendations([]);
      } else {
        setRecommendations(data.recommendations || []);
      }
    } catch (error) {
      console.error('Error:', error);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const renderStars = (rating) => {
    return [...Array(5)].map((_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${i < rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`}
      />
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Sparkles className="w-10 h-10 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-800">MovieLens Recommendation System</h1>
          </div>
          <p className="text-gray-600">Powered by MovieLens 100k Dataset - Real Movie Ratings & Data</p>
          
          {/* System Status */}
          <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md">
            <div className={`w-3 h-3 rounded-full ${systemReady ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm font-semibold text-gray-700">
              {systemReady ? 'System Ready' : 'Backend Offline'}
            </span>
          </div>
        </div>

        {/* Dataset Statistics */}
        {stats && (
          <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <Database className="w-6 h-6 text-indigo-600" />
              <h2 className="text-xl font-bold text-gray-800">Dataset Information</h2>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-indigo-50 rounded-xl">
                <div className="text-3xl font-bold text-indigo-600">{stats.total_movies}</div>
                <div className="text-sm text-gray-600">Movies</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-xl">
                <div className="text-3xl font-bold text-purple-600">{stats.total_ratings.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Ratings</div>
              </div>
              <div className="text-center p-4 bg-pink-50 rounded-xl">
                <div className="text-3xl font-bold text-pink-600">{stats.total_users}</div>
                <div className="text-sm text-gray-600">Users</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-xl">
                <div className="text-3xl font-bold text-blue-600">{stats.avg_rating.toFixed(1)}</div>
                <div className="text-sm text-gray-600">Avg Rating</div>
              </div>
            </div>
          </div>
        )}

        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Tell Us Your Movie Preferences</h2>
          <textarea
            value={preferences}
            onChange={(e) => setPreferences(e.target.value)}
            placeholder="Example: I love action movies with sci-fi elements, especially movies like The Matrix or Inception. I also enjoy thrillers with complex plots..."
            className="w-full h-32 p-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          />
          <button
            onClick={getRecommendations}
            disabled={loading || !preferences.trim() || !systemReady}
            className="w-full mt-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                Analyzing MovieLens Database...
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5" />
                Get Movie Recommendations
              </>
            )}
          </button>
          
          {!systemReady && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-sm text-red-800">
                <strong>Backend not connected.</strong> Please make sure the Flask server is running on port 5002.
              </p>
            </div>
          )}
        </div>

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Film className="w-7 h-7 text-indigo-600" />
              Recommended Movies For You
            </h2>
            {recommendations.map((rec, idx) => (
              <div
                key={idx}
                className="bg-white rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-start gap-3">
                      <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full text-white font-bold text-xl flex-shrink-0">
                        {idx + 1}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-800 mb-1">
                          {rec.title}
                          {rec.year && rec.year !== 'N/A' && (
                            <span className="text-gray-500 font-normal ml-2">({rec.year})</span>
                          )}
                        </h3>
                        <div className="flex items-center gap-3 mb-2">
                          <div className="flex items-center gap-1">
                            {renderStars(rec.rating)}
                            <span className="ml-2 text-sm font-semibold text-gray-700">{rec.rating}/5</span>
                          </div>
                          {rec.rating_count && (
                            <span className="text-xs text-gray-500">
                              ({rec.rating_count} ratings)
                            </span>
                          )}
                        </div>
                        <div className="flex flex-wrap gap-2 mb-3">
                          {rec.genres && rec.genres.split(', ').map((genre, i) => (
                            <span
                              key={i}
                              className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-full"
                            >
                              {genre}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <p className="text-gray-700 mb-3">{rec.description}</p>
                <div className="flex items-start gap-2 p-3 bg-indigo-50 rounded-lg">
                  <ThumbsUp className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-semibold text-indigo-900 mb-1">Why we recommend this:</p>
                    <p className="text-sm text-indigo-800">{rec.reason}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && recommendations.length === 0 && preferences && systemReady && (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <Film className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No recommendations found. Try different preferences!</p>
          </div>
        )}

        {/* How It Works */}
        {recommendations.length === 0 && !preferences && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl font-bold text-indigo-600">1</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Real Dataset</h3>
                <p className="text-sm text-gray-600">Uses MovieLens 100k with 100,000 real user ratings on 1,682 movies</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl font-bold text-indigo-600">2</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Content-Based Filtering</h3>
                <p className="text-sm text-gray-600">Matches your preferences with movie genres and characteristics</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl font-bold text-indigo-600">3</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Smart Rankings</h3>
                <p className="text-sm text-gray-600">Ranks based on genre match, ratings, and popularity</p>
              </div>
            </div>
            
            <div className="mt-8 p-4 bg-indigo-50 rounded-xl">
              <h3 className="font-semibold text-gray-800 mb-2">💡 Example Preferences to Try:</h3>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• "I love sci-fi action movies with great special effects"</li>
                <li>• "Looking for romantic comedies that are funny and heartwarming"</li>
                <li>• "Dark thrillers with complex plots and mystery"</li>
                <li>• "Classic drama films with strong character development"</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
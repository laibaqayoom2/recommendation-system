#!/usr/bin/env python3
"""
MovieLens Recommendation System - Setup Verification Script
This script checks if everything is set up correctly before running the server.
"""

import os
import sys

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking required packages...")
    required = ['flask', 'flask_cors', 'pandas', 'numpy', 'sklearn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_dataset():
    """Check if MovieLens 100k dataset exists"""
    print("\n🔍 Checking MovieLens 100k dataset...")
    
    data_path = 'ml-100k'
    required_files = ['u.data', 'u.item', 'u.user', 'u.genre']
    
    if not os.path.exists(data_path):
        print(f"❌ Dataset folder '{data_path}' not found")
        print("\n📥 Please download the dataset:")
        print("1. Go to: https://grouplens.org/datasets/movielens/100k/")
        print("2. Download ml-100k.zip")
        print("3. Extract it in the backend folder")
        return False
    
    print(f"✅ Dataset folder found: {data_path}/")
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(data_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file} - {size:,} bytes")
        else:
            print(f"❌ {file} - NOT found")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_port():
    """Check if port 5002 is available"""
    print("\n🔍 Checking if port 5002 is available...")
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', 5002))
        sock.close()
        print("✅ Port 5002 is available")
        return True
    except OSError:
        print("⚠️  Port 5002 is already in use")
        print("The server might already be running, or another application is using this port")
        return True  # Not a critical error

def display_dataset_info():
    """Display information about the dataset"""
    print("\n📊 Dataset Information:")
    print("=" * 60)
    
    try:
        import pandas as pd
        
        # Load and display stats
        ratings_df = pd.read_csv('ml-100k/u.data', sep='\t', 
                                names=['user_id', 'movie_id', 'rating', 'timestamp'])
        
        movies_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1',
                               names=['movie_id', 'title'] + ['col' + str(i) for i in range(22)],
                               usecols=[0, 1])
        
        users_df = pd.read_csv('ml-100k/u.user', sep='|',
                              names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
        
        print(f"🎬 Movies: {len(movies_df):,}")
        print(f"⭐ Ratings: {len(ratings_df):,}")
        print(f"👥 Users: {len(users_df):,}")
        print(f"📈 Avg Rating: {ratings_df['rating'].mean():.2f}/5.0")
        print(f"📊 Rating Distribution:")
        for rating in sorted(ratings_df['rating'].unique()):
            count = len(ratings_df[ratings_df['rating'] == rating])
            pct = (count / len(ratings_df)) * 100
            print(f"   {rating}⭐: {count:6,} ({pct:5.1f}%)")
        
    except Exception as e:
        print(f"⚠️  Could not load dataset details: {e}")

def main():
    """Run all checks"""
    print("=" * 60)
    print("🎬 MovieLens Recommendation System - Setup Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_dataset(),
        check_port()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("✅ All checks passed! You're ready to run the server.")
        print("\n🚀 To start the server, run:")
        print("   python server.py")
        print("\n🌐 The server will be available at:")
        print("   http://127.0.0.1:5002")
        
        display_dataset_info()
        
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📖 For help, see SETUP_GUIDE.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())
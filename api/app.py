from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import sqlite3

app = Flask(__name__)

DB_FILE = 'restaurants.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

def load_data():
    cursor.execute("SELECT * FROM restaurants")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    df['combined_features'] = df.apply(lambda x: f"{x['name']} {x['cuisine']} {x['city']} {x['price']}", axis=1)
    return df

df = load_data()

vectorizer = TfidfVectorizer()
vectorizer.fit(df['combined_features'])

def get_user_pref_vector(user_ratings, df, vectorizer):
    user_rated_restaurants = df[df['name'].isin(user_ratings.keys())]
    user_profile = []
    for _, row in user_rated_restaurants.iterrows():
        vector = vectorizer.transform([row['combined_features']])
        user_profile.append(vector * user_ratings[row['name']])
    user_pref_vector = sum(user_profile)
    return user_pref_vector

def get_user_recommendations(user_ratings, df, vectorizer, top_n=10):
    user_pref_vector = get_user_pref_vector(user_ratings, df, vectorizer)
    sim_scores = cosine_similarity(user_pref_vector, vectorizer.transform(df['combined_features'])).flatten()
    sim_scores = sorted(enumerate(sim_scores), key=lambda x: x[1], reverse=True)
    rated_restaurant_indices = df[df['name'].isin(user_ratings.keys())].index
    sim_scores = [(i, score) for i, score in sim_scores if i not in rated_restaurant_indices]
    sim_scores = sim_scores[:top_n]
    restaurant_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[restaurant_indices][['id', 'name', 'cuisine', 'city', 'rating', 'price', 'phone', 'image_url', 'address1', 'state', 'zip_code']]
    recommendations['similarity_score'] = [score for _, score in sim_scores]
    return recommendations

@app.route('/recommend', methods=['POST'])

def recommend():
    user_ratings = request.json.get('user_ratings')
    if not user_ratings:
        return jsonify({'error': 'user_ratings is required'}), 400
    
    recommendations = get_user_recommendations(user_ratings, df, vectorizer)
    recommendations = recommendations.to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

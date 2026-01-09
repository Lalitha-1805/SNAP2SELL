"""
Machine Learning Modules
Includes crop recommendation, price prediction, and product recommendation
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from datetime import datetime, timedelta
from models import Product, Review, PriceHistory
from bson import ObjectId


class CropRecommendationModel:
    """Random Forest based crop recommendation system"""
    
    MODEL_PATH = 'models/crop_recommendation_model.pkl'
    LABEL_ENCODER_PATH = 'models/crop_label_encoder.pkl'
    
    CROPS = ['Rice', 'Wheat', 'Corn', 'Cotton', 'Sugarcane', 'Potato', 
             'Tomato', 'Onion', 'Carrot', 'Cabbage']
    
    SOIL_TYPES = ['Loam', 'Clay', 'Sandy', 'Silt', 'Chalk']
    SEASONS = ['Spring', 'Summer', 'Monsoon', 'Winter']
    RAINFALL_RANGES = ['Low', 'Medium', 'High']
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.load_or_train()
    
    def load_or_train(self):
        """Load model from disk or train if not exists"""
        if os.path.exists(self.MODEL_PATH) and os.path.exists(self.LABEL_ENCODER_PATH):
            self.model = joblib.load(self.MODEL_PATH)
            self.label_encoder = joblib.load(self.LABEL_ENCODER_PATH)
            print("[OK] Crop recommendation model loaded from disk")
        else:
            self.train()
    
    def train(self):
        """Train crop recommendation model"""
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 500
        
        soil_encoded = np.array([self.SOIL_TYPES.index(s) for s in np.random.choice(self.SOIL_TYPES, n_samples)])
        season_encoded = np.array([self.SEASONS.index(s) for s in np.random.choice(self.SEASONS, n_samples)])
        rainfall_encoded = np.array([self.RAINFALL_RANGES.index(r) for r in np.random.choice(self.RAINFALL_RANGES, n_samples)])
        temperature = np.random.randint(10, 40, n_samples)
        humidity = np.random.randint(30, 90, n_samples)
        
        X = np.column_stack([soil_encoded, season_encoded, rainfall_encoded, temperature, humidity])
        
        # Generate labels based on simple rules
        y = []
        for i in range(n_samples):
            if soil_encoded[i] == 0 and rainfall_encoded[i] == 2:  # Loam + High rainfall
                y.append('Rice')
            elif soil_encoded[i] == 1 and temperature[i] > 25:  # Clay + High temp
                y.append('Cotton')
            elif season_encoded[i] == 3:  # Winter
                y.append('Wheat')
            else:
                y.append(np.random.choice(self.CROPS))
        
        y = np.array(y)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Store label encoder
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(y)
        
        # Save to disk
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.MODEL_PATH)
        joblib.dump(self.label_encoder, self.LABEL_ENCODER_PATH)
        
        print("[OK] Crop recommendation model trained and saved")
    
    def predict(self, soil_type, season, rainfall, temperature, humidity):
        """Predict suitable crops"""
        try:
            soil_idx = self.SOIL_TYPES.index(soil_type)
            season_idx = self.SEASONS.index(season)
            rainfall_idx = self.RAINFALL_RANGES.index(rainfall)
            
            X = np.array([[soil_idx, season_idx, rainfall_idx, temperature, humidity]])
            
            # Get predictions
            predictions = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            # Get top 3 recommendations
            top_indices = np.argsort(probabilities)[-3:][::-1]
            recommendations = [
                {
                    'crop': self.model.classes_[idx],
                    'confidence': float(probabilities[idx]) * 100
                }
                for idx in top_indices
            ]
            
            return recommendations
        
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")


class PricePredictionModel:
    """Random Forest regression model for price prediction"""
    
    MODEL_PATH = 'models/price_prediction_model.pkl'
    
    def __init__(self):
        self.model = None
        self.load_or_train()
    
    def load_or_train(self):
        """Load model from disk or train if not exists"""
        if os.path.exists(self.MODEL_PATH):
            self.model = joblib.load(self.MODEL_PATH)
            print("[OK] Price prediction model loaded from disk")
        else:
            self.train()
    
    def train(self):
        """Train price prediction model with synthetic data"""
        np.random.seed(42)
        
        # Create synthetic training data
        n_samples = 300
        
        # Features: [days_since_start, season_encoded, product_category_encoded, quantity]
        days = np.random.randint(0, 365, n_samples)
        season_encoded = np.random.randint(0, 4, n_samples)
        category_encoded = np.random.randint(0, 5, n_samples)
        quantity = np.random.randint(10, 1000, n_samples)
        
        X = np.column_stack([days, season_encoded, category_encoded, quantity])
        
        # Generate prices based on features (higher quantity = lower price per unit)
        y = 100 + (season_encoded * 10) + (category_encoded * 5) - (quantity / 100) + np.random.normal(0, 10, n_samples)
        y = np.maximum(y, 10)  # Ensure positive prices
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Save to disk
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.MODEL_PATH)
        
        print("[OK] Price prediction model trained and saved")
    
    def predict(self, days_from_now=7, season=0, category=0, quantity=100):
        """Predict future price"""
        try:
            X = np.array([[days_from_now, season, category, quantity]])
            predicted_price = float(self.model.predict(X)[0])
            return {
                'predicted_price': max(predicted_price, 10),
                'days_from_now': days_from_now,
                'confidence': 85  # Static confidence for demo
            }
        except Exception as e:
            raise ValueError(f"Price prediction failed: {str(e)}")


class ProductRecommendationModel:
    """Collaborative filtering based product recommendation"""
    
    def __init__(self):
        self.user_item_matrix = None
        self.products = None
    
    def build_user_item_matrix(self):
        """Build user-item interaction matrix from reviews"""
        try:
            # Get all reviews
            from extensions import get_db
            reviews_collection = get_db()['reviews']
            reviews = list(reviews_collection.find())
            
            if not reviews:
                return None
            
            # Create dataframe
            df = pd.DataFrame([
                {
                    'buyer_id': str(r['buyer_id']),
                    'product_id': str(r['product_id']),
                    'rating': r['rating']
                }
                for r in reviews
            ])
            
            # Create pivot table
            self.user_item_matrix = df.pivot_table(
                index='buyer_id',
                columns='product_id',
                values='rating',
                fill_value=0
            )
            
            return True
        
        except Exception as e:
            print(f"Failed to build user-item matrix: {str(e)}")
            return False
    
    def recommend_products(self, buyer_id, n_recommendations=5):
        """Recommend products for a buyer"""
        try:
            if self.user_item_matrix is None or self.user_item_matrix.empty:
                self.build_user_item_matrix()
            
            if self.user_item_matrix is None or buyer_id not in self.user_item_matrix.index:
                # Return popular products if no data
                return self._get_popular_products(n_recommendations)
            
            # Calculate similarity
            user_vector = self.user_item_matrix.loc[buyer_id].values.reshape(1, -1)
            similarities = cosine_similarity(user_vector, self.user_item_matrix)[0]
            
            # Get similar users
            similar_user_indices = np.argsort(similarities)[-5:-1]  # Top 4 similar users
            
            # Get products rated by similar users but not by this user
            recommendations = set()
            for idx in similar_user_indices:
                similar_user = self.user_item_matrix.index[idx]
                rated_products = self.user_item_matrix.loc[similar_user]
                rated_products = rated_products[rated_products > 0].index.tolist()
                user_rated = self.user_item_matrix.loc[buyer_id]
                user_rated = user_rated[user_rated > 0].index.tolist()
                
                recommendations.update(set(rated_products) - set(user_rated))
            
            # Get product details
            product_list = []
            for product_id in list(recommendations)[:n_recommendations]:
                product = Product.find_by_id(product_id)
                if product:
                    product_list.append({
                        'product_id': str(product['_id']),
                        'name': product.get('name'),
                        'category': product.get('category'),
                        'price': product.get('price'),
                        'rating': product.get('rating')
                    })
            
            return product_list
        
        except Exception as e:
            print(f"Recommendation failed: {str(e)}")
            return self._get_popular_products(n_recommendations)
    
    def _get_popular_products(self, n_recommendations=5):
        """Get popular products as fallback"""
        products = Product.find_many({'is_active': True}, limit=n_recommendations)
        return [
            {
                'product_id': str(p['_id']),
                'name': p.get('name'),
                'category': p.get('category'),
                'price': p.get('price'),
                'rating': p.get('rating')
            }
            for p in products
        ]


# Initialize models
crop_recommender = CropRecommendationModel()
price_predictor = PricePredictionModel()
product_recommender = ProductRecommendationModel()

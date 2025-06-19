"""
Advanced ML-based Resume-Job Fit Classifier
Uses enterprise-grade XGBoost model trained on 6.24k real resume-job pairs from HuggingFace
"""
import numpy as np
import pandas as pd
import joblib
import re
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedFitClassifier:
    """
    Production-ready resume-job fit classifier using advanced ML
    """
    
    def __init__(self):
        self.pipeline_data = None
        self.model = None
        self.vectorizers = None
        self.label_encoder = None
        self.feature_columns = None
        self.target_names = None
        self.is_loaded = False
        
        # Try to load the advanced model
        self._load_advanced_model()
    
    def _load_advanced_model(self):
        """Load the advanced ML pipeline"""
        try:
            # Find the latest model file
            models_dir = Path(__file__).parent.parent / 'models'
            model_files = list(models_dir.glob('ml_pipeline_xgboost_*.pkl'))
            
            if model_files:
                # Get the most recent model
                latest_model = max(model_files, key=os.path.getctime)
                logger.info(f"Loading advanced ML model: {latest_model}")
                
                self.pipeline_data = joblib.load(latest_model)
                self.model = self.pipeline_data['model']
                self.vectorizers = self.pipeline_data['vectorizers']
                self.label_encoder = self.pipeline_data['label_encoder']
                self.feature_columns = self.pipeline_data['feature_columns']
                self.target_names = self.pipeline_data['target_names']
                self.is_loaded = True
                
                # Log model performance
                metrics = self.pipeline_data.get('performance_metrics', {})
                logger.info(f"✅ Advanced ML model loaded successfully!")
                logger.info(f"Model: {self.pipeline_data.get('model_name', 'XGBoost')}")
                logger.info(f"Accuracy: {metrics.get('accuracy', 'N/A'):.4f}")
                logger.info(f"AUC Score: {metrics.get('auc_score', 'N/A'):.4f}")
                
            else:
                logger.warning("No advanced ML model found, falling back to basic classifier")
                self.is_loaded = False
                
        except Exception as e:
            logger.error(f"Failed to load advanced ML model: {e}")
            self.is_loaded = False
    
    def _preprocess_text(self, text):
        """Preprocess text data"""
        if pd.isna(text) or text is None:
            return ""
        
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _create_text_features(self, resume_text, job_description):
        """Create text features for the advanced model"""
        # Create DataFrame
        data = {
            'resume_text': [resume_text],
            'job_description_text': [job_description]
        }
        df = pd.DataFrame(data)
        
        # Preprocess text
        df['resume_text_processed'] = df['resume_text'].apply(self._preprocess_text)
        df['job_description_text_processed'] = df['job_description_text'].apply(self._preprocess_text)
        
        # Create statistical features
        features = df.copy()
        
        # Resume features
        features['resume_text_length'] = features['resume_text'].str.len().fillna(0)
        features['resume_text_word_count'] = features['resume_text_processed'].str.split().str.len().fillna(0)
        features['resume_text_unique_words'] = features['resume_text_processed'].apply(
            lambda x: len(set(str(x).split())) if pd.notna(x) else 0
        )
        features['resume_text_avg_word_length'] = features['resume_text_processed'].apply(
            lambda x: np.mean([len(word) for word in str(x).split()]) if pd.notna(x) and str(x).strip() else 0
        )
        features['resume_text_sentence_count'] = features['resume_text'].str.count(r'[.!?]').fillna(0)
        features['resume_text_capital_ratio'] = features['resume_text'].apply(
            lambda x: sum(1 for c in str(x) if c.isupper()) / len(str(x)) if pd.notna(x) and len(str(x)) > 0 else 0
        )
        
        # Job description features
        features['job_description_text_length'] = features['job_description_text'].str.len().fillna(0)
        features['job_description_text_word_count'] = features['job_description_text_processed'].str.split().str.len().fillna(0)
        features['job_description_text_unique_words'] = features['job_description_text_processed'].apply(
            lambda x: len(set(str(x).split())) if pd.notna(x) else 0
        )
        features['job_description_text_avg_word_length'] = features['job_description_text_processed'].apply(
            lambda x: np.mean([len(word) for word in str(x).split()]) if pd.notna(x) and str(x).strip() else 0
        )
        features['job_description_text_sentence_count'] = features['job_description_text'].str.count(r'[.!?]').fillna(0)
        features['job_description_text_capital_ratio'] = features['job_description_text'].apply(
            lambda x: sum(1 for c in str(x) if c.isupper()) / len(str(x)) if pd.notna(x) and len(str(x)) > 0 else 0
        )
        
        # Extract numerical features
        feature_cols = [col for col in features.columns if col.endswith(('_length', '_word_count', '_unique_words', '_avg_word_length', '_sentence_count', '_capital_ratio'))]
        X_features = features[feature_cols].fillna(0)
        
        # Add TF-IDF features
        for col_name, vectorizer in self.vectorizers.items():
            if col_name == 'resume_text':
                processed_col = 'resume_text_processed'
            else:  # job_description_text
                processed_col = 'job_description_text_processed'
            
            text_data = features[processed_col].fillna('').astype(str)
            tfidf_matrix = vectorizer.transform(text_data)
            
            # Create TF-IDF DataFrame
            feature_names = [f'{col_name}_tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
            
            X_features = pd.concat([X_features, tfidf_df], axis=1)
        
        # Ensure all required features are present
        missing_features = set(self.feature_columns) - set(X_features.columns)
        for feature in missing_features:
            X_features[feature] = 0
        
        # Reorder columns to match training data
        X_features = X_features[self.feature_columns].fillna(0)
        
        return X_features
    
    def predict_advanced(self, resume_text, job_description):
        """Make prediction using advanced ML model"""
        if not self.is_loaded:
            return None
        
        try:
            # Create features
            X_features = self._create_text_features(resume_text, job_description)
            
            # Make prediction
            prediction = self.model.predict(X_features)[0]
            prediction_proba = self.model.predict_proba(X_features)[0]
            
            # Convert back to original labels
            predicted_class = self.label_encoder.inverse_transform([prediction])[0]
            
            # Create result
            result = {
                'prediction': predicted_class,
                'confidence': float(max(prediction_proba)),
                'probabilities': dict(zip(self.target_names, prediction_proba.astype(float))),
                'model_type': 'advanced_ml'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in advanced prediction: {e}")
            return None
    
    def predict_basic(self, match_score, num_matched, num_missing):
        """Fallback basic prediction method"""
        try:
            # Load or create basic model
            basic_model_path = Path(__file__).parent / 'fit_classifier.pkl'
            
            if basic_model_path.exists():
                with open(basic_model_path, 'rb') as f:
                    import pickle
                    clf = pickle.load(f)
            else:
                # Create basic model
                from sklearn.ensemble import RandomForestClassifier
                X = [
                    [100, 10, 0], [90, 9, 1], [80, 8, 2], [70, 7, 3], [60, 6, 4],
                    [50, 5, 5], [40, 4, 6], [30, 3, 7], [20, 2, 8], [10, 1, 9], [0, 0, 10]
                ]
                y = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
                clf = RandomForestClassifier(n_estimators=50, random_state=42)
                clf.fit(X, y)
                
                with open(basic_model_path, 'wb') as f:
                    import pickle
                    pickle.dump(clf, f)
            
            X = np.array([[match_score, num_matched, num_missing]])
            pred = clf.predict(X)[0]
            prob = clf.predict_proba(X)[0][1]
            
            # Convert to advanced format
            result = {
                'prediction': 'Good Fit' if pred == 1 else 'No Fit',
                'confidence': float(prob) if pred == 1 else float(1 - prob),
                'probabilities': {'Good Fit': float(prob), 'No Fit': float(1 - prob)},
                'model_type': 'basic'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in basic prediction: {e}")
            return {
                'prediction': 'No Fit',
                'confidence': 0.5,
                'probabilities': {'Good Fit': 0.3, 'No Fit': 0.7},
                'model_type': 'fallback'
            }

# Global classifier instance
_classifier = AdvancedFitClassifier()

def predict_fit(resume_text=None, job_description=None, match_score=None, num_matched=None, num_missing=None):
    """
    Unified prediction function that uses advanced ML when possible, falls back to basic
    
    Args:
        resume_text (str): Full resume text (for advanced model)
        job_description (str): Full job description text (for advanced model)
        match_score (float): Match percentage (for basic model fallback)
        num_matched (int): Number of matched skills (for basic model fallback)
        num_missing (int): Number of missing skills (for basic model fallback)
    
    Returns:
        dict: Prediction result with confidence and probabilities
    """
    # Try advanced model first if we have text data
    if resume_text and job_description and _classifier.is_loaded:
        result = _classifier.predict_advanced(resume_text, job_description)
        if result:
            logger.info(f"🚀 Advanced ML prediction: {result['prediction']} ({result['confidence']:.3f})")
            return result
    
    # Fall back to basic model
    if match_score is not None and num_matched is not None and num_missing is not None:
        result = _classifier.predict_basic(match_score, num_matched, num_missing)
        logger.info(f"📊 Basic prediction: {result['prediction']} ({result['confidence']:.3f})")
        return result
    
    # Ultimate fallback
    logger.warning("Using fallback prediction")
    return {
        'prediction': 'No Fit',
        'confidence': 0.5,
        'probabilities': {'Good Fit': 0.3, 'No Fit': 0.7},
        'model_type': 'fallback'
    }

# Legacy function for backward compatibility
def load_fit_classifier():
    """Legacy function for backward compatibility"""
    return _classifier

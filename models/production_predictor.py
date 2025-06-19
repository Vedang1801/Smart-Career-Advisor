
import pandas as pd
import numpy as np
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class ResumeJobFitPredictor:
    def __init__(self, pipeline_path):
        """Load the trained pipeline"""
        self.pipeline_data = joblib.load(pipeline_path)
        self.model = self.pipeline_data['model']
        self.vectorizers = self.pipeline_data['vectorizers']
        self.label_encoder = self.pipeline_data['label_encoder']
        self.feature_columns = self.pipeline_data['feature_columns']
        self.target_names = self.pipeline_data['target_names']

        # Initialize NLTK components
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Preprocess text data"""
        if pd.isna(text):
            return ""

        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(tokens)

    def create_text_features(self, df, text_cols):
        """Create text features"""
        features = df.copy()

        for col in text_cols:
            processed_col = f'{col}_processed'
            features[processed_col] = features[col].apply(self.preprocess_text)

            # Basic text statistics
            features[f'{col}_length'] = features[col].str.len().fillna(0)
            features[f'{col}_word_count'] = features[processed_col].str.split().str.len().fillna(0)
            features[f'{col}_unique_words'] = features[processed_col].apply(
                lambda x: len(set(str(x).split())) if pd.notna(x) else 0
            )
            features[f'{col}_avg_word_length'] = features[processed_col].apply(
                lambda x: np.mean([len(word) for word in str(x).split()]) if pd.notna(x) and str(x).strip() else 0
            )
            features[f'{col}_sentence_count'] = features[col].str.count(r'[.!?]').fillna(0)
            features[f'{col}_capital_ratio'] = features[col].apply(
                lambda x: sum(1 for c in str(x) if c.isupper()) / len(str(x)) if pd.notna(x) and len(str(x)) > 0 else 0
            )

        return features

    def predict(self, resume_text=None, job_description=None):
        """Make prediction for resume-job fit"""
        # Create input DataFrame
        data = {}
        text_columns = []

        if resume_text is not None:
            data['resume'] = [resume_text]
            text_columns.append('resume')

        if job_description is not None:
            data['job_description'] = [job_description]
            text_columns.append('job_description')

        if not data:
            raise ValueError("At least one of resume_text or job_description must be provided")

        df = pd.DataFrame(data)

        # Create features
        df_features = self.create_text_features(df, text_columns)

        # Extract numerical features
        feature_cols = [col for col in df_features.columns if col in self.feature_columns and 
                       not col.startswith(tuple(text_columns)) and not col.endswith('_processed')]
        X_features = df_features[feature_cols].fillna(0)

        # Add TF-IDF features
        for col in text_columns:
            if col in self.vectorizers:
                processed_col = f'{col}_processed'
                text_data = df_features[processed_col].fillna('').astype(str)
                tfidf_matrix = self.vectorizers[col].transform(text_data)

                # Create TF-IDF DataFrame
                feature_names = [f'{col}_tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
                tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

                X_features = pd.concat([X_features, tfidf_df], axis=1)

        # Ensure all required features are present
        missing_features = set(self.feature_columns) - set(X_features.columns)
        for feature in missing_features:
            X_features[feature] = 0

        # Reorder columns to match training data
        X_features = X_features[self.feature_columns].fillna(0)

        # Make prediction
        prediction = self.model.predict(X_features)[0]
        prediction_proba = self.model.predict_proba(X_features)[0]

        # Convert back to original labels
        predicted_class = self.label_encoder.inverse_transform([prediction])[0]

        # Create result
        result = {
            'prediction': predicted_class,
            'confidence': float(max(prediction_proba)),
            'probabilities': dict(zip(self.target_names, prediction_proba.astype(float)))
        }

        return result

# Usage example:
# predictor = ResumeJobFitPredictor('../models/ml_pipeline_xgboost_20250619_172840.pkl')
# result = predictor.predict(resume_text="Your resume text here", job_description="Job description here")
# print(result)

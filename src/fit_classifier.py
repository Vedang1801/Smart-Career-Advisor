import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

def train_fit_classifier():
    # Dummy training data: [match_score, num_matched_skills, num_missing_skills]
    X = [
        [100, 10, 0], [90, 9, 1], [80, 8, 2], [70, 7, 3], [60, 6, 4],
        [50, 5, 5], [40, 4, 6], [30, 3, 7], [20, 2, 8], [10, 1, 9], [0, 0, 10]
    ]
    y = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]  # 1 = Good Fit, 0 = Not Fit
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    with open('src/fit_classifier.pkl', 'wb') as f:
        pickle.dump(clf, f)
    return clf

def load_fit_classifier():
    try:
        with open('src/fit_classifier.pkl', 'rb') as f:
            clf = pickle.load(f)
    except Exception:
        clf = train_fit_classifier()
    return clf

def predict_fit(match_score, num_matched, num_missing):
    clf = load_fit_classifier()
    X = np.array([[match_score, num_matched, num_missing]])
    pred = clf.predict(X)[0]
    prob = clf.predict_proba(X)[0][1]
    return pred, prob

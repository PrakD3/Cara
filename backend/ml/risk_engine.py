import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging

logger = logging.getLogger("cara.ml.risk_engine")

class AdherenceRiskEngine:
    def __init__(self):
        self.model_path = "ml_models/rf_adherence_model.pkl"
        self.model = None
        self._load_or_mock_model()

    def _load_or_mock_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            logger.warning("No pre-trained RandomForest model found. Using mock simulation.")
            self.model = "MOCK"

    def predict_risk(self, patient_age: int, missed_doses_7d: int, disease_severity: int) -> float:
        """
        Predicts the risk of hospitalization or critical deterioration based on adherence history.
        Returns a float between 0.0 (low risk) and 1.0 (high risk).
        """
        if self.model == "MOCK":
            # Heuristic mock calculation
            base_risk = 0.1
            age_factor = (patient_age / 100) * 0.2
            missed_factor = (missed_doses_7d / 14) * 0.5  # assuming 2 doses a day
            disease_factor = (disease_severity / 10) * 0.2
            
            risk = base_risk + age_factor + missed_factor + disease_factor
            return min(risk, 0.99)
            
        else:
            # Actual sklearn inference
            features = np.array([[patient_age, missed_doses_7d, disease_severity]])
            risk_prob = self.model.predict_proba(features)[0][1]
            return risk_prob

risk_engine = AdherenceRiskEngine()

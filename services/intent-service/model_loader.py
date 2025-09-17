import os
import mlflow
import logging
from typing import Any
from models import IntentResponse

logger = logging.getLogger(__name__)

class ModelLoader:
    """Loads a model from MLflow (pyfunc) and caches it.
    Falls back to a local rule-based predictor when MLflow URI isn't provided or loading fails.
    """

    def __init__(self):
        self.model = None
        self.ml_model_version = None
        self.mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000")
        self.model_name = os.environ.get("MLFLOW_MODEL_NAME", "customer_intent_classifier")
        self.model_stage = os.environ.get("MLFLOW_MODEL_STAGE", "Production")

        if self.mlflow_tracking_uri:
            mlflow.set_tracking_uri(self.mlflow_tracking_uri)
    
    def load(self, uri: str | None = None):
        uri = uri or f"models:/{self.model_name}/{self.model_stage}"
        if not uri:
            logger.warning("MLflow tracking URI not provided. Using rule-based predictor.")
            self.model = None
            self.model_version = "mock-v1"
            return
        
        try:
            logger.info(f"Loading model from MLflow URI: {uri}")
            self.model = mlflow.pyfunc.load_model(uri)
            self.model_version = uri
            logger.info("Model loaded from MLflow successfully.")
        except Exception as e:
            logger.error(f"Failed to load model from MLflow: {e}. Falling to mock model.")
            self.model = None
            self.model_version = "mock-v1"
    
    def predict(self, text: str) -> dict:
        """Return a dict with intents list and optional slots.
        If a real model is loaded (pyfunc), we call model.predict with a pandas Series or list.
        The function returns a consistent dict: {"intents": [{"name":..., "score":...}], "ml_model_version":...}
        """
        if self.model is None:
            txt = text.lower()
            if any(x in txt for x in ["refund", "money back", "return"]):
                return {"intents": ["refund"], "ml_model_version": self.model_version}
            if any(x in txt for x in ["hello", "hi", "hey"]):
                return {"intents": ["greeting"], "ml_model_version": self.model_version}
            return {"intents": ["unknown"], "ml_model_version": self.model_version}
        try:
            import pandas as pd
            input_data = pd.Series([text])
            preds = self.model.predict(input_data)

            if hasattr(preds, 'to_dict'):
                out = preds.to_dict(orient='records')
                first = out[0] if out else {}
                return {"intents": first.get("intents", out), "ml_model_version": self.model_version}
            return {"intents": preds, "ml_model_version": self.model_version}
        except Exception as e:
            logger.exception("Error during model prediction. - returning fallback.")
            return {"intents": ["unknown"], "ml_model_version": self.model_version}

# Singleton pattern for ModelLoader
_loader: ModelLoader | None = None

def get_loader() -> ModelLoader:
    global _loader
    if _loader is None:
        _loader = ModelLoader()
        _loader.load()
    return _loader
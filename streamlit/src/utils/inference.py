"""Theme prediction via the deployed FastAPI inference service.
Pure functions (no Streamlit) so they can be unit-tested.
"""
import requests
import streamlit as st

API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["INFERENCE_API_KEY"]


def predict_theme(text: str, topk: int = 3):
    """Return (cleaned_text, [(sentiment, theme, similarity), ...]) ranked best-first.
    Calls the FastAPI /infer endpoint instead of loading the model locally."""
    payload = {"reviews": [{"id": "warmup", "text": text}]}
    headers = {"X-API-Key": API_KEY}

    try:
        response = requests.post(f"{API_URL}/infer", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to reach inference API: {e}")

    data = response.json()["results"][0]

    if data.get("error"):
        return data.get("cleaned_text", ""), []

    cleaned = data.get("cleaned_text", "")
    ranked = [(data["sentiment"], data["theme"], data["similarity"])]
    return cleaned, ranked
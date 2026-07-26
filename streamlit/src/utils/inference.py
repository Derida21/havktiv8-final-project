import requests
import streamlit as st

API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["INFERENCE_API_KEY"]


def predict_theme(text: str, topk: int = 3):
    payload = {"reviews": [{"id": "warmup", "text": text}]}
    headers = {"X-API-Key": API_KEY}

    try:
        response = requests.post(f"{API_URL}/infer", json=payload, headers=headers, timeout=60)
    except requests.exceptions.Timeout:
        raise TimeoutError("FastAPI service is waking up or unreachable (timeout).")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Cannot reach the FastAPI service (Space may be down).")

    if response.status_code == 401:
        raise PermissionError("Invalid API key configuration.")
    if response.status_code != 200:
        raise RuntimeError(f"Inference API returned {response.status_code}: {response.text}")

    data = response.json()["results"][0]
    if data.get("error"):
        return data.get("cleaned_text", ""), []

    cleaned = data.get("cleaned_text", "")
    ranked = [(data["sentiment"], data["theme"], data["similarity"])]
    return cleaned, ranked
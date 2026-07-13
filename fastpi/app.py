import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from utils.inference import predict_theme

app = FastAPI(title="Topic Pulse - Inference API")

API_KEY = os.environ.get("INFERENCE_API_KEY")


class ReviewIn(BaseModel):
    id: str = Field(..., description="Row id from db")
    text: str = Field(..., description="Raw review text")


class InferRequest(BaseModel):
    reviews: list[ReviewIn]


class ReviewOut(BaseModel):
    id: str
    theme: str | None = None
    sentiment: str | None = None
    similarity: float | None = None
    cleaned_text: str | None = None
    error: str | None = None


class InferResponse(BaseModel):
    results: list[ReviewOut]


def _check_key(x_api_key: str | None):
    if not API_KEY:
        # Fail closed: refuse to serve if the secret was never configured on the Space.
        raise HTTPException(status_code=500, detail="INFERENCE_API_KEY is not set on this Space")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header")


@app.get("/")
def root():
    return {"status": "ok", "service": "topic-pulse-inference"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/infer", response_model=InferResponse)
def infer(payload: InferRequest, x_api_key: str | None = Header(default=None)):
    _check_key(x_api_key)

    if not payload.reviews:
        raise HTTPException(status_code=400, detail="reviews list is empty")
    if len(payload.reviews) > 200:
        raise HTTPException(status_code=400, detail="max 200 reviews per request - send smaller batches")

    results: list[ReviewOut] = []
    for r in payload.reviews:
        try:
            cleaned, ranked = predict_theme(r.text)
            if not ranked:
                results.append(ReviewOut(id=r.id, error="empty after cleaning - no usable text"))
                continue
            sentiment, theme, sim = ranked[0]
            results.append(ReviewOut(
                id=r.id,
                theme=theme,
                sentiment=sentiment,
                similarity=round(sim, 4),
                cleaned_text=cleaned,
            ))
        except Exception as e:
            results.append(ReviewOut(id=r.id, error=str(e)))

    return InferResponse(results=results)

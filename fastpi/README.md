---
title: Topic Pulse Inference API
emoji: 🔮
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Topic Pulse - Inference API

Inference-only companion to the Topic Pulse Streamlit Space. Exposes a single batch
endpoint so an external scheduler (e.g. n8n) can predict the theme of reviews sitting
in the database, on a schedule. Same prediction logic as the interactive app -
embed with `paraphrase-multilingual-MiniLM-L12-v2`, cosine-match against the exported
topic vectors in `artifacts/topic_index.npz`. No BERTopic/UMAP/HDBSCAN at runtime.

## Endpoints

### `GET /health`
Liveness check. No auth required.

### `POST /infer`
Auth: header `X-API-Key: <your key>`, must match the `INFERENCE_API_KEY` Space secret.

Request body:
```json
{
  "reviews": [
    { "id": "row-123", "text": "barang sampai pecah, packing asal asalan" },
    { "id": "row-124", "text": "pengiriman cepat, seller ramah" }
  ]
}
```
Max 200 reviews per request - batch larger sets into multiple calls.

Response body:
```json
{
  "results": [
    { "id": "row-123", "theme": "Item damaged", "sentiment": "Negative", "similarity": 0.81, "cleaned_text": "barang sampai pecah packing asal asalan" },
    { "id": "row-124", "theme": "Fast delivery", "sentiment": "Positive", "similarity": 0.77, "cleaned_text": "pengiriman cepat seller ramah" }
  ]
}
```
If a review fails to process, its entry has `"error": "<message>"` and null theme/sentiment
instead - the rest of the batch still returns normally.

## Deploy to Hugging Face Spaces
1. Create a new Space -> **SDK: Docker**.
2. Upload this whole folder (`app.py`, `Dockerfile`, `requirements.txt`, `utils/`,
   `artifacts/`, `colloquial-indonesian-lexicon.csv`, this `README.md`).
3. Space -> Settings -> Secrets -> add `INFERENCE_API_KEY` with a strong random value.
4. Wait for the build to finish, then call `https://<your-space>.hf.space/infer`.

## Cold start
Free-tier Spaces sleep after inactivity. The first request after a sleep can take
30s-a few minutes while the container restarts and the model loads. Give your caller
(n8n's HTTP Request node) a generous timeout (60-120s) and a retry with backoff.

## Notes
- Keep this Space **separate** from the Streamlit dashboard Space - this one is a
  plain container with no UI, meant to be called machine-to-machine.
- The Streamlit Space keeps working exactly as before; nothing here changes it.

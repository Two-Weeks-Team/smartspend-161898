import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from routes import router

app = FastAPI()

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.get("/")
async def root() -> HTMLResponse:
    html_content = """
    <html>
    <head>
      <title>SmartSpend API</title>
      <style>
        body { background-color: #121212; color: #e0e0e0; font-family: Arial, Helvetica, sans-serif; padding: 2rem; }
        a { color: #66b2ff; }
        h1 { color: #66b2ff; }
        .endpoint { margin-bottom: 1rem; }
        .code { background: #1e1e1e; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; }
      </style>
    </head>
    <body>
      <h1>SmartSpend API</h1>
      <p>AI‑powered personal finance assistant.</p>
      <h2>Available Endpoints</h2>
      <div class="endpoint"><span class="code">GET /health</span> – health check.</div>
      <div class="endpoint"><span class="code">GET /api/transactions/categorize</span> – AI categorizes uncategorized transactions.</div>
      <div class="endpoint"><span class="code">GET /api/budget/suggestions</span> – AI suggests budget adjustments.</div>
      <div class="endpoint"><span class="code">GET /api/anomalies</span> – Detect spending anomalies.</div>
      <h2>Tech Stack</h2>
      <ul>
        <li>FastAPI 0.115.0</li>
        <li>PostgreSQL via SQLAlchemy 2.0.35</li>
        <li>DigitalOcean Serverless Inference (model: openai-gpt-oss-120b)</li>
        <li>Python 3.12+</li>
      </ul>
      <p>Interactive docs: <a href="/docs" target="_blank">/docs</a> | <a href="/redoc" target="_blank">/redoc</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

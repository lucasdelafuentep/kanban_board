from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

# Serve frontend static files
if os.path.exists("/app/frontend/out"):
    # Serve specific static assets first
    if os.path.exists("/app/frontend/out/_next/static"):
        app.mount("/_next/static", StaticFiles(directory="/app/frontend/out/_next/static"), name="next-static")
    if os.path.exists("/app/frontend/out/static"):
        app.mount("/static", StaticFiles(directory="/app/frontend/out/static"), name="static")

    @app.get("/")
    def read_root():
        return FileResponse("/app/frontend/out/index.html")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        # Skip API routes - they should be handled above
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
        path = f"/app/frontend/out/{full_path}"
        if os.path.exists(path) and os.path.isfile(path):
            return FileResponse(path)
        return FileResponse("/app/frontend/out/index.html")
else:
    @app.get("/", response_class=HTMLResponse)
    def read_root():
        return """
        <html>
            <head><title>Hello World</title></head>
            <body><h1>Hello, World! FastAPI is running.</h1></body>
        </html>
        """

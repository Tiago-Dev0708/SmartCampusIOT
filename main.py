"""Bootstrap entrypoint for the Smart Campus IoT application.

Exposes the FastAPI 'app' instance so Uvicorn can run it from the root directory,
and provides a CLI entrypoint to run directly via 'python main.py'.
"""
import uvicorn
from src.presentation.api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

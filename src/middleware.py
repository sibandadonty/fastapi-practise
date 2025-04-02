from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def htt_middleware(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
         
        processing_time = time.time() - start_time

        message = f"{request.client.host} {request.client.port} {request.url.path} {response.status_code} completed after {processing_time:.2f}s"
        print(message)
        return response
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
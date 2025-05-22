from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import httpx
import time
from typing import Dict, List
import secrets
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = FastAPI(title="API Gateway")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic authentication
security = HTTPBasic()

# Rate limiting configuration
RATE_LIMIT = 100  # requests per minute
rate_limit_store: Dict[str, List[float]] = {}

# Service URLs
SERVICE1_URL = os.getenv("SERVICE1_URL", "http://service1:8001")
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://service2:8002")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("API_USERNAME", "admin")
    correct_password = os.getenv("API_PASSWORD", "admin")
    
    is_correct_username = secrets.compare_digest(credentials.username.encode("utf8"), correct_username.encode("utf8"))
    is_correct_password = secrets.compare_digest(credentials.password.encode("utf8"), correct_password.encode("utf8"))
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

def check_rate_limit(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    
    # Initialize rate limit store for new clients
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    
    # Remove old requests (older than 1 minute)
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if current_time - t < 60]
    
    # Check if rate limit is exceeded
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Add current request timestamp
    rate_limit_store[client_ip].append(current_time)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    check_rate_limit(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "API Gateway is running"}

@app.get("/service1/{path:path}")
async def service1_proxy(path: str, request: Request, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICE1_URL}/{path}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/service2/{path:path}")
async def service2_proxy(path: str, request: Request, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICE2_URL}/{path}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
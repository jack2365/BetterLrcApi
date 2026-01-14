from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import cover
from routers import lyrics

app = FastAPI(
    title="MuseMeta API",
    description="High-quality lyrics and cover art provider from multiple sources.",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_auth = os.getenv("API_AUTH")
        # Check if authentication is enabled and not skipped
        if api_auth:
            # Check headers
            auth_header = request.headers.get("Authorization") or request.headers.get("Authentication")
            if auth_header != api_auth:
                return JSONResponse(
                    status_code=403,
                    content={"code": 403, "message": "Unauthorized"}
                )
        return await call_next(request)

app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(cover.router, tags=["Cover"])
app.include_router(lyrics.router, tags=["Lyrics"])

@app.get("/")
async def root():
    return {"message": "Welcome to BetterLrcApi. Use /cover?keyword=Song Name to get active."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

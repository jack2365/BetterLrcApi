from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import cover
from routers import lyrics

app = FastAPI(
    title="BetterLrcApi",
    description="An improved Lyrics and Cover API using Apple Music for covers.",
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

# Include routers
app.include_router(cover.router, tags=["Cover"])
app.include_router(lyrics.router, tags=["Lyrics"])

@app.get("/")
async def root():
    return {"message": "Welcome to BetterLrcApi. Use /cover?keyword=Song Name to get active."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

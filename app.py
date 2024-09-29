from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastAPI.routers import completition_router, retrevial_router
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include your routers
app.include_router(completition_router)
app.include_router(retrevial_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

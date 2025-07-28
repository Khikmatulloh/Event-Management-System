from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Request
app = FastAPI()
from app.routers import auth,events,users


app = FastAPI() 

app.include_router(users.router, prefix="/users", tags=["Users"])
app = FastAPI()

app.include_router(auth.router) 
app.include_router(events.router)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware (example)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response

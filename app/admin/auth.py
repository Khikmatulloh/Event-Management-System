from app.admin.settings import init_admin
from fastapi import FastAPI,HTTPException
from app.dependencies import get_current_admin_user
app = FastAPI()

# JWT autentifikatsiya
@app.middleware("http")
async def jwt_admin_auth(request, call_next):
    if request.url.path.startswith("/admin"):
        user = await get_current_admin_user(request)
        if not user or not user.is_admin:
            return HTTPException(status_code=403, content={"detail": "Admin access required"})
    return await call_next(request)

init_admin(app)

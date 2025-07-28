from starlette_admin.contrib.sqla import Admin, ModelView
from app.models import User, Event, EventRegistration
from app.database import engine, Base, SessionLocal
from fastapi import FastAPI, Depends
from app.dependencies import get_current_admin_user  # JWT tekshiruvchi funksiya

admin = Admin(engine, title="Event Management Admin")

admin.add_view(ModelView(User))
admin.add_view(ModelView(Event))
admin.add_view(ModelView(EventRegistration))

def init_admin(app: FastAPI):
    admin.mount_to(app)

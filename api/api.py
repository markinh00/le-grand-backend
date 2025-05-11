from fastapi import FastAPI
from api.routes import customer
from api.routes.auth import register, login
from api.services.db.database import populate_database

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(customer.router)

@app.get("/")
def read_root():
    return

@app.post("/populate")
def populate():
    populate_database()
    return
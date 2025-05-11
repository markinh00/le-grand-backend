from fastapi import FastAPI
from api.dependencies.populate import populate_database
from api.routes import customer, address
from api.routes.auth import register, login

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(customer.router)
app.include_router(address.router)

@app.get("/")
def read_root():
    return

# This route will override everything inside the database. Be careful while using it
@app.post("/populate", description="This route will override everything inside the database. Be careful while using it")
def populate():
    try:
        populate_database()
        return True
    except Exception as e:
        print(e)
        return False
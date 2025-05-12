from fastapi import FastAPI
from api.routes import customer, address, product, image, reset
from api.routes.auth import register, login


app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(customer.router)
app.include_router(address.router)
app.include_router(product.router)
app.include_router(image.router)
app.include_router(reset.router)

@app.get("/")
def read_root():
    return

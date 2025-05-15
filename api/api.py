from fastapi import FastAPI, Security
from starlette.middleware.cors import CORSMiddleware
from api.dependencies.auth import get_api_key
from api.routes import customer, address, product, image, reset, discount, order
from api.routes.auth import register, login


app = FastAPI(dependencies=[Security(get_api_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(customer.router)
app.include_router(address.router)
app.include_router(product.router)
app.include_router(discount.router)
app.include_router(order.router)

app.include_router(image.router)
app.include_router(reset.router)

@app.get("/")
def read_root():
    return

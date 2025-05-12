from fastapi import APIRouter
from sqlmodel import select
from api.dependencies.populate import populate_database
from api.models.product import Product
from api.services.db.image_storage import delete_image
from api.services.db.sqlmodel.database import get_session

router = APIRouter(prefix="/reset", tags=["Reset"])


# This route will override everything inside the database. Be careful while using it
@router.delete("/", description="This route will override everything inside the database. Be careful while using it")
def reset_database():
    try:
        session = next(get_session())
        statement = (select(Product))
        products = list(session.exec(statement).all())

        for product in products:
            delete_image(product.img_url)

        populate_database()
        return True
    except Exception as e:
        print(e)
        return False
from api.dependencies.auth import get_password_hash
from api.models.address import Address
from api.models.admin import Admin
from api.models.customer import Customer
from api.models.discount import Discount
from api.models.product import Product
from api.services.db.sqlmodel.database import reset_database, get_session


def populate_database():
    reset_database()

    session = next(get_session())

    admin1 = Admin(name="Maria Souza", email="maria@lojadocookie.com", password=get_password_hash("123456"))
    admin2 = Admin(name="João Lima", email="joao@lojadocookie.com", password=get_password_hash("123456"))

    customer1 = Customer(name="Carlos Silva", email="carlos@gmail.com", phone="11999998888", password=get_password_hash("123456"))
    customer2 = Customer(name="Ana Costa", email="ana@gmail.com", phone="21988887777", password=get_password_hash("123456"))

    session.add_all([admin1, admin2, customer1, customer2])
    session.commit()

    address1 = Address(
        street="Rua das Flores", number=123, neighborhood="Centro", city="São Paulo",
        state="SP", zip_code="01000-000", customer_id=customer1.id
    )
    address2 = Address(
        street="Av. Brasil", number=456, neighborhood="Jardins", city="Rio de Janeiro",
        state="RJ", zip_code="20000-000", customer_id=customer2.id, complement="Apto 101"
    )

    discount1 = Discount(name="Desconto de Inauguração", value=10)
    discount2 = Discount(name="Promoção de Pães", value=5)

    product1 = Product(name="Cookie de Chocolate", price=4.5, description="Feito com chocolate belga",
                       category="Cookies", img_url="http://localhost:8000/image/572cb3da-e0d7-4849-afca-3bb7c4be24f6.jpeg")
    product2 = Product(name="Cookie de Aveia e Mel", price=3.5, description="Saudável e saboroso",
                       category="Cookies", img_url="http://localhost:8000/image/75804a10-0407-478d-9cc0-384960dd55a0.jpg")
    product3 = Product(name="Pão Francês", price=0.8, description="Crocante por fora, macio por dentro",
                       category="Pães", img_url="http://localhost:8000/image/fc99b584-0b45-4b3f-aa7b-f1ed50e40031.jpg")
    product4 = Product(name="Pão de Queijo", price=2.5, description="Feito com queijo da Serra da Canastra",
                       category="Pães", img_url="http://localhost:8000/image/ca00107e-4498-4e6a-9567-bc6ebed9a2f5.jpg")

    session.add_all([address1, address2, discount1, discount2, product1, product2, product3, product4])
    session.commit()

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies.auth import get_password_hash
from api.dependencies.calculate_total_price import calculate_total_price
from api.models.address import Address
from api.models.admin import Admin
from api.models.customer import Customer
from api.models.discount import Discount
from api.models.order import Delivery, Card, PickUp, Money
from api.models.product import Product
from api.schemas.address import AddressInOrderRead
from api.schemas.customer import CustomerInOrder
from api.schemas.discount import DiscountInOrder
from api.schemas.product import ProductInOrderRead
from api.services.db.image_storage import delete_unprotected_images
from api.services.db.mongodb.database import MongoDB
from api.services.db.sqlmodel.database import reset_postgresql, get_session

mongo = MongoDB()

def populate_database():
    try:
        delete_unprotected_images()

        reset_postgresql()
        session = next(get_session())

        # Admins
        admin1 = Admin(name="Maria Souza", email="maria@lojadocookie.com", password=get_password_hash("123456"))
        admin2 = Admin(name="João Lima", email="joao@lojadocookie.com", password=get_password_hash("123456"))

        # Customers
        customer1 = Customer(name="Carlos Silva", email="carlos@gmail.com", phone="11999998888",
                             password=get_password_hash("123456"))
        customer2 = Customer(name="Ana Costa", email="ana@gmail.com", phone="21988887777",
                             password=get_password_hash("123456"))
        customer3 = Customer(name="Lucas Almeida", email="lucas@gmail.com", phone="31999997777",
                             password=get_password_hash("123456"))
        customer4 = Customer(name="Juliana Pereira", email="juliana@gmail.com", phone="41988886666",
                             password=get_password_hash("123456"))

        session.add_all([admin1, admin2, customer1, customer2, customer3, customer4])
        session.commit()

        # Addresses
        address1 = Address(street="Rua das Flores", number=123, neighborhood="Centro", city="São Paulo", state="SP", zip_code="01000-000", customer_id=customer1.id)
        address2 = Address(street="Av. Brasil", number=456, neighborhood="Jardins", city="Rio de Janeiro", state="RJ", zip_code="20000-000", customer_id=customer2.id, complement="Apto 101")
        address3 = Address(street="Rua do Sol", number=321, neighborhood="Centro", city="Belo Horizonte", state="MG", zip_code="30100-000", customer_id=customer3.id)
        address4 = Address(street="Rua das Palmeiras", number=89, neighborhood="Boa Vista", city="Curitiba", state="PR", zip_code="80000-000", customer_id=customer4.id, complement="Casa dos fundos")

        # Discounts
        discount1 = Discount(name="Desconto de Inauguração", value=10, enabled=True)
        discount2 = Discount(name="Promoção de Pães", value=5, enabled=True)
        discount3 = Discount(name="Desconto de Aniversário", value=15, enabled=True)
        discount4 = Discount(name="Combo Cookies", value=20, enabled=True)

        # Products
        product1 = Product(name="Cookie de Chocolate", price=4.5, description="Feito com chocolate belga", category="Cookies", img_url="http://localhost:8000/image/572cb3da-e0d7-4849-afca-3bb7c4be24f6.jpeg")
        product2 = Product(name="Cookie de Aveia e Mel", price=3.5, description="Saudável e saboroso", category="Cookies", img_url="http://localhost:8000/image/75804a10-0407-478d-9cc0-384960dd55a0.jpg")
        product3 = Product(name="Pão Francês", price=0.8, description="Crocante por fora, macio por dentro", category="Pães", img_url="http://localhost:8000/image/fc99b584-0b45-4b3f-aa7b-f1ed50e40031.jpg")
        product4 = Product(name="Pão de Queijo", price=2.5, description="Feito com queijo da Serra da Canastra", category="Pães", img_url="http://localhost:8000/image/ca00107e-4498-4e6a-9567-bc6ebed9a2f5.jpg")
        product5 = Product(name="Cookie Recheado", price=5.5, description="Recheado com doce de leite", category="Cookies", img_url="http://localhost:8000/image/845b25f1-a7bf-4d89-aab8-17a068b51943.jpg")
        product6 = Product(name="Baguete Integral", price=3.0, description="Pão baguete com farinha integral", category="Pães", img_url="http://localhost:8000/image/cee3f6f9-4fc3-4c82-a22d-aaf4828b9cc7.jpg")
        product7 = Product(name="Pão Australiano", price=3.8, description="Macio e levemente adocicado", category="Pães", img_url="http://localhost:8000/image/49054b39-9ac1-48ab-a623-7d93b1a005b3.jpg")
        product8 = Product(name="Cookie Triplo de Chocolate", price=6.0, description="Feito com três tipos de chocolate", category="Cookies", img_url="http://localhost:8000/image/a788f776-6075-4a03-9564-f4f8c4dae1b6.jpg")
        product9 = Product(name="Bolo de Cenoura com Cobertura de Chocolate", price=7.5, description="Tradicional e delicioso", category="Bolos", img_url="http://localhost:8000/image/dad8efde-26d7-4a4f-ab11-476b133caadb.jpg")
        product10 = Product(name="Bolo Red Velvet", price=8.5, description="Com cobertura de cream cheese", category="Bolos", img_url="http://localhost:8000/image/743af917-aefe-44fd-9bf7-10f232e2f925.jpg")
        product11 = Product(name="Bolo de Fubá com Goiabada", price=6.5, description="Sabor de fazenda", category="Bolos", img_url="http://localhost:8000/image/72b68733-6e78-4d22-ad25-35792486f9ec.jpg")
        product12 = Product(name="Bolo de Laranja", price=6.0, description="Feito com suco natural de laranja", category="Bolos", img_url="http://localhost:8000/image/56083f38-e518-4589-9cfc-065fc0069dd5.jpg")

        session.add_all([address1, address2, address3, address4,
                         discount1, discount2, discount3, discount4,
                         product1, product2, product3, product4, product5, product6,
                         product7, product8, product9, product10, product11, product12])
        session.commit()

        for obj in [admin1, admin2, customer1, customer2, customer3, customer4,
                    address1, address2, address3, address4,
                    discount1, discount2, discount3, discount4,
                    product1, product2, product3, product4, product5, product6,
                    product7, product8, product9, product10, product11, product12]:
            session.refresh(obj)

        result = mongo.collection.delete_many({})
        if not result.acknowledged:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while resetting database")

        # Orders
        order1_products = [ProductInOrderRead(**product1.model_dump(), quantity=2), ProductInOrderRead(**product2.model_dump(), quantity=2)]
        order1 = Delivery(customer=CustomerInOrder(**customer1.model_dump()), products=order1_products, delivery_fee=10,
                          address=AddressInOrderRead(**address1.model_dump()), payment="pix",
                          total=calculate_total_price(products=order1_products, delivery_fee=10))

        order2_products = [ProductInOrderRead(**product3.model_dump(), quantity=3), ProductInOrderRead(**product4.model_dump(), quantity=3)]
        order2 = Delivery(customer=CustomerInOrder(**customer2.model_dump()), products=order2_products,
                          discount=DiscountInOrder(**discount2.model_dump()), delivery_fee=5,
                          address=AddressInOrderRead(**address2.model_dump()), payment=Card(card="debit"),
                          total=calculate_total_price(products=order2_products, delivery_fee=5, discount_value=discount2.value))

        order3_products = [ProductInOrderRead(**product3.model_dump(), quantity=3), ProductInOrderRead(**product4.model_dump(), quantity=3)]
        order3 = PickUp(customer=CustomerInOrder(**customer3.model_dump()), products=order3_products,
                        payment=Money(change_for=50),
                        date=datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(hours=5),
                        total=calculate_total_price(products=order3_products))

        order4_products = [ProductInOrderRead(**product5.model_dump(), quantity=1), ProductInOrderRead(**product6.model_dump(), quantity=2)]
        order4 = Delivery(customer=CustomerInOrder(name="José Almeida", phone="(24) 91234-5678"), products=order4_products,
                          discount=DiscountInOrder(**discount4.model_dump()), delivery_fee=7,
                          address=AddressInOrderRead(**address4.model_dump()), payment=Card(card="credit"),
                          total=calculate_total_price(products=order4_products, delivery_fee=7, discount_value=discount4.value))

        order5_products = [ProductInOrderRead(**product2.model_dump(), quantity=1), ProductInOrderRead(**product4.model_dump(), quantity=2), ProductInOrderRead(**product6.model_dump(), quantity=1)]
        order5 = PickUp(customer=CustomerInOrder(**customer1.model_dump()), products=order5_products,
                        discount=DiscountInOrder(**discount1.model_dump()), payment="pix",
                        date=datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(days=1, hours=2),
                        total=calculate_total_price(products=order5_products, discount_value=discount1.value))

        order6_products = [ProductInOrderRead(**product1.model_dump(), quantity=1), ProductInOrderRead(**product3.model_dump(), quantity=4)]
        order6 = Delivery(customer=CustomerInOrder(**customer2.model_dump()), products=order6_products,
                          delivery_fee=6, address=AddressInOrderRead(**address2.model_dump()), payment=Card(card="credit"),
                          total=calculate_total_price(products=order6_products, delivery_fee=6))

        order7_products = [ProductInOrderRead(**product9.model_dump(), quantity=1), ProductInOrderRead(**product10.model_dump(), quantity=1), ProductInOrderRead(**product11.model_dump(), quantity=1)]
        order7 = Delivery(customer=CustomerInOrder(**customer4.model_dump()), products=order7_products,
                          discount=DiscountInOrder(**discount1.model_dump()), delivery_fee=8,
                          address=AddressInOrderRead(**address4.model_dump()), payment=Card(card="debit"),
                          total=calculate_total_price(products=order7_products, delivery_fee=8, discount_value=discount1.value))

        order8_products = [ProductInOrderRead(**product7.model_dump(), quantity=2), ProductInOrderRead(**product8.model_dump(), quantity=1), ProductInOrderRead(**product12.model_dump(), quantity=1)]
        order8 = PickUp(customer=CustomerInOrder(**customer3.model_dump()), products=order8_products,
                        payment="pix",
                        date=datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(days=2, hours=3),
                        total=calculate_total_price(products=order8_products))

        mongo.collection.insert_many([
            order1.to_pymongo(),
            order2.to_pymongo(),
            order3.to_pymongo(),
            order4.to_pymongo(),
            order5.to_pymongo(),
            order6.to_pymongo(),
            order7.to_pymongo(),
            order8.to_pymongo()
        ])
    except Exception as e:
        raise e


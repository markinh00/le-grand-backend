from sqlmodel import select
from starlette import status
from starlette.exceptions import HTTPException
from api.models.customer import Customer
from api.models.discount import Discount
from api.models.order import Money, Delivery, PickUp
from api.models.product import Product
from api.repositories.order import OrderRepository
from api.schemas.address import AddressInOrderRead
from api.schemas.customer import CustomerInOrder
from api.schemas.discount import DiscountInOrder
from api.schemas.order import DeliveryCreate, PickUpCreate, PickUpUpdate, DeliveryUpdate
from api.schemas.pagination import OrderPagination
from api.schemas.product import ProductInOrderRead
from api.services.db.mongodb.database import MongoDB
from api.services.db.sqlmodel.database import get_session


class OrderService:
    def __init__(self):
        self.repository = OrderRepository(collection=MongoDB().collection, session=next(get_session()))

    def create_order(self, order_data: DeliveryCreate | PickUpCreate) -> Delivery | PickUp:
        if order_data.customer.id:
            customer: Customer |CustomerInOrder | None = self.repository.session.get(Customer, order_data.customer_id)
            if not customer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
        else:
            customer = order_data.customer

        product_ids = [p.id for p in order_data.products]
        statement = select(Product).where(Product.id.in_(product_ids))
        products: list[Product] = self.repository.session.exec(statement).all()

        if len(products) != len(order_data.products):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find all products in the order"
            )

        products_in_order: list[ProductInOrderRead] = []
        for product in products:
            products_in_order.append(ProductInOrderRead(
                **product.model_dump(),
                quantity=[p.quantity for p in order_data.products if p.id == product.id][0],
            ))

        discount: Discount | None = None
        if order_data.discount_name:
            statement = select(Discount).where(Discount.name == order_data.discount_name)
            discount = self.repository.session.exec(statement).first()

            if not discount:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Discount not found"
                )

            if not discount.enabled:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Discount not enabled"
                )


        order: Delivery | PickUp | None = None

        if isinstance(order_data, DeliveryCreate):
            order = Delivery(
                customer=CustomerInOrder(**customer.model_dump()),
                address=AddressInOrderRead(**order_data.address.model_dump()),
                products=products_in_order,
                discount=DiscountInOrder(**discount.model_dump()) if order_data.discount_name else None,
                delivery_fee=order_data.delivery_fee,
                total=order_data.total,
                payment=order_data.payment
            )

        if isinstance(order_data, PickUpCreate):
            order = PickUp(
                customer=CustomerInOrder(**customer.model_dump()),
                products=products_in_order,
                discount=DiscountInOrder(**discount.model_dump()) if order_data.discount_name else None,
                total=order_data.total,
                payment=order_data.payment,
                date=order_data.date
            )

        return self.repository.create(order)

    def get_all_orders(self, query: OrderPagination) -> list[Delivery | PickUp]:
        return self.repository.get_all(query)

    def get_customer_orders(self, customer_id: int) -> list[Delivery | PickUp]:
        return self.repository.get_by_customer_id(customer_id)

    def get_order_by_id(self, order_id: str) -> Delivery | PickUp:
        return self.repository.get_by_id(order_id)

    def update_order(self, order_id: str, new_data: DeliveryUpdate | PickUpUpdate) -> Delivery | PickUp:
        return self.repository.update(order_id, new_data)

    def delete_order(self, order_id: str) -> bool:
        return self.repository.delete(order_id)

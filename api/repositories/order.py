import copy
from bson import ObjectId
from pymongo.synchronous.collection import Collection
from sqlmodel import Session
from starlette import status
from starlette.exceptions import HTTPException
from api.models.order import Delivery, PickUp
from api.models.product import Product
from api.schemas.order import DeliveryUpdate, PickUpUpdate
from api.schemas.pagination import OrderPagination
from api.schemas.product import ProductInOrderRead


class OrderRepository:
    def __init__(self, collection: Collection, session: Session):
        self.collection = collection
        self.session = session

    def create(self, order: Delivery | PickUp) -> Delivery | PickUp:
        response = self.collection.insert_one(order.to_pymongo())

        if not response.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating order"
            )

        order.id = response.inserted_id

        return order

    def get_all(self, query: OrderPagination) -> list[Delivery | PickUp]:
        response = (self.collection.find({})
                    .skip((query.page - 1) * query.size)
                    .limit(query.size)
                    .sort(query.order.value, -1 if query.desc else 1))

        orders: list[Delivery | PickUp] = []

        for order in response:
            print(order)
            if "delivery_fee" in order.keys():
                orders.append(Delivery(**order))
            else:
                orders.append(PickUp(**order))

        return orders

    def get_by_customer_id(self, customer_id: int) -> list[Delivery | PickUp]:
        response = self.collection.find({"customer.id": customer_id})

        orders: list[Delivery | PickUp] = []

        for order in response:
            print(order)
            if "delivery_fee" in order.keys():
                orders.append(Delivery(**order))
            else:
                orders.append(PickUp(**order))

        return orders

    def get_by_id(self, order_id: str) -> Delivery | PickUp:
        order = self.collection.find_one({"_id": ObjectId(order_id)})

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        if "delivery_fee" in order.keys():
            return Delivery(**order)
        else:
            return PickUp(**order)

    def update(self, order_id: str, new_data: DeliveryUpdate | PickUpUpdate) -> Delivery | PickUp:
        order = self.get_by_id(order_id)

        product_ids = [product.id for product in order.products]
        product_map = {p_id: i for i, p_id in enumerate(product_ids)}
        new_products: list[ProductInOrderRead] = copy.deepcopy(order.products)

        if new_data.add_product:
            for product in new_data.add_product:
                if product.id in product_ids:
                    index = product_map[product.id]
                    new_products[index].quantity += product.quantity
                else:
                    found_product: Product | None = self.session.get(Product, product.id)

                    if not found_product:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product {product.id} not found"
                        )

                    new_products.append(ProductInOrderRead(**found_product.model_dump(), quantity=product.quantity))
                    product_map[product.id] = len(new_products)

        if new_data.remove_product:
            for product in new_data.remove_product:
                if product.id not in product_ids:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {product.id} not found"
                    )

                index = product_map[product.id]
                if new_products[index].quantity - product.quantity > 0:
                    new_products[index].quantity -= product.quantity
                else:
                    new_products.pop(index)
                    product_ids = [product.id for product in new_products]
                    product_map = {p_id: i for i, p_id in enumerate(product_ids)}

        if len(new_products) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot leave the order without any products"
            )

        print("old products:")
        for product in order.products:
            print("old product:", product)
        print("new products:")
        for product in new_products:
            print("new product:", product)

        total: float = 0
        for product in new_products:
            total += (product.price * product.quantity)

        new_order: Delivery | PickUp | None = None

        if isinstance(order, Delivery):
            try:
                new_data = DeliveryUpdate(**new_data.model_dump())
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update a delivery order with pickup data"
                )

            total += order.delivery_fee

            if order.discount and order.discount.value > 0:
                total *= (1 - (order.discount.value / 100))
            total = round(total, 2)

            order_data = order.model_dump()
            order_data.pop("products", None)
            order_data.pop("total", None)
            order_data.pop("address", None)
            order_data.pop("state", None)

            new_order = Delivery(
                **order_data,
                products=new_products,
                total=total,
                address=new_data.address if new_data.address else order.address,
                state=new_data.state if new_data.state else order.state
            )

        elif isinstance(order, PickUp):
            try:
                new_data = PickUpUpdate(**new_data.model_dump())
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update a pickup order with delivery data"
                )

            if order.discount and order.discount.value > 0:
                total *= (1 - (order.discount.value / 100))
            total = round(total, 2)

            order_data = order.model_dump()
            order_data.pop("products", None)
            order_data.pop("total", None)
            order_data.pop("date", None)
            order_data.pop("state", None)

            new_order = PickUp(
                **order_data,
                products=new_products,
                total=total,
                date=new_data.date if new_data.date else order.date,
                state = new_data.state if new_data.state else order.state
            )

        result = self.collection.update_one({"_id": ObjectId(order_id)}, {"$set": new_order.to_pymongo()})

        if not result.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while updating order"
            )

        return  new_order

    def delete(self, order_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(order_id)})

        if not result.acknowledged:
            return False

        return True

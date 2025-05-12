from api.services.db.mongodb.database import MongoDB


class OrdersRepository:
    def __init__(self):
        self.collection = MongoDB().collection

    # def create(self, order: OrderCreate):
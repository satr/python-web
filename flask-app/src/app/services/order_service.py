from app.clients.fast_api.fast_api_client.api.orders.get_order_orders_id_get import  \
    sync_detailed as get_order_detail
from app.clients.fast_api.fast_api_client.api.orders.create_order_orders_post import sync_detailed as create_order
from app.clients.fast_api.fast_api_client.api.orders.list_orders_orders_get import sync_detailed as get_orders_list
from app.clients.fast_api.fast_api_client.models.order_item_schema import OrderItemSchema
from app.clients.fast_api.fast_api_client.models.order_schema import OrderSchema


class OrderService:
    def __init__(self, api_client=None):
        self.client = api_client

    def get_orders(self):
        response = get_orders_list(client=self.client)
        return response.parsed if response.parsed is not None else []

    def create_order(self, items):
        order = OrderSchema(items=items)
        response = create_order(client=self.client, body=order)
        return response.parsed

    def get_order_detail(self, id):
        response = get_order_detail(client=self.client, id=id)
        return response.parsed if response.parsed is not None else None

    def parse_order_form(self, form, products):
        items = []
        for product in products:
            id = getattr(product, "id", None)
            quantity = int(form.get(f"quantity_{id}", 0))
            price = float(form.get(f"price_{id}", 0))
            if quantity > 0:
                item = OrderItemSchema(product_id=id, quantity=quantity, price=price)
                items.append(item)
        return items


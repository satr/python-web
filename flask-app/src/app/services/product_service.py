from app.clients.fast_api.fast_api_client.api.products.list_products_products_get import sync_detailed as get_products_list
from app.clients.fast_api.fast_api_client.api.products.create_product_products_post import sync_detailed as create_product
from app.clients.fast_api.fast_api_client.models.product_schema import ProductSchema


class ProductService:
    def __init__(self, api_client=None):
        self.client = api_client

    def get_products(self):
        response = get_products_list(client=self.client)
        return response.parsed if response.parsed is not None else []

    def parse_product_form(self, form):
        name = form.get(f"product_name")
        price = float(form.get(f"product_price", 0))
        return ProductSchema(name=name, price=price)

    def post_product(self, product):
        response = create_product(client=self.client, body=product)
        return response.parsed


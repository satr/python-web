from fastapi import APIRouter, HTTPException
from schemas.product_schema import ProductSchema, ProductResponseSchema, convert_to_product_schema, convert_to_product
from services.product_service import ProductService


def get_product_router(product_service: ProductService) -> APIRouter:
    router = APIRouter(prefix="/products", tags=["products"])

    @router.post("/", response_model=ProductResponseSchema)
    @router.post("", response_model=ProductResponseSchema)
    def upsert_product(product: ProductSchema):
        try:
            id = product_service.upsert_product(convert_to_product(product))
            return ProductResponseSchema(id=id)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to create Product: {ex}")


    @router.get("/{id}", response_model=ProductSchema)
    def get_product(id: str):
        try:
            product = product_service.get_product(id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return convert_to_product_schema(product)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to get Product: {ex}")

    @router.get("/", response_model=list[ProductSchema])
    @router.get("", response_model=list[ProductSchema])
    def list_products():
        try:
            products = product_service.list_products()
            return [convert_to_product_schema(product) for product in products]
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to get list of Products: {ex}")

    return router


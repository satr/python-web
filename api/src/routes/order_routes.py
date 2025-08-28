import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from api.src.models.order import Order, OrderItem
from api.src.schemas.order_schema import OrderSchema, OrderItemSchema, OrderResponseSchema
from api.src.services.order_service import OrderService


def get_order_router(order_service: OrderService) -> APIRouter:
    router = APIRouter(prefix="/orders", tags=["orders"])

    @router.post("/", response_model=OrderResponseSchema)
    @router.post("", response_model=OrderResponseSchema)
    def create_order(order: OrderSchema):
        if not order.items or len(order.items) == 0:
            raise HTTPException(status_code=400, detail="Order must have at least one item")
        try:
            order_id = order_service.create_order(convert_to_order(order))
            return OrderResponseSchema(order_id=order_id)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to create an Order: {ex}")

    @router.get("/{order_id}", response_model=OrderSchema)
    def get_order(order_id: str):
        try:
            order = order_service.get_order(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return convert_to_order_schema(order)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to get Order: {ex}")

    @router.get("/", response_model=list[OrderSchema])
    @router.get("", response_model=list[OrderSchema])
    def list_orders():
        try:
            orders_ = [convert_to_order_schema(order) for order in order_service.list_orders()]
            return orders_
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to get list of Orders: {ex}")

    return router


def convert_to_order(order_schema: OrderSchema) -> Order:
    order = Order()
    order.items=order_schema.items
    order.user_id=order_schema.user_id or "anonymous"
    order.updated_at = order.created_at = datetime.now()
    order.items = [convert_to_order_item(item) for item in order_schema.items]
    return order


def convert_to_order_item(order_item_schema: OrderItemSchema) -> OrderItem:
    item = OrderItem()
    item.product_id = order_item_schema.product_id
    item.quantity = order_item_schema.quantity
    item.price = order_item_schema.price
    return item


def convert_to_order_item_schema(order_item: OrderItem) -> OrderItemSchema:
    return OrderItemSchema(
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price=order_item.price,
    )


def convert_to_order_schema(order) -> OrderSchema:
    return OrderSchema(
        order_id=order.id,
        user_id=order.user_id,
        created_at=order.created_at,
        updated_at=order.updated_at,
        total=order.total,
        status=order.status,
        items=[convert_to_order_item_schema(item) for item in order.items]
    )

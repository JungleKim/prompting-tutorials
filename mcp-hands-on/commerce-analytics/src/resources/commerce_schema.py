from typing import List
from fastmcp.resources.base import Resource

from .schema import ORDER_ITEM_TABLE, ORDER_TABLE, PAYMENT_TABLE, CUSTOMER_TABLE, PRODUCT_TABLE, PRODUCT_CATEGORY_TABLE


def get_order_schema() -> str:
    return ORDER_TABLE

def get_order_item_schema() -> str:
    return ORDER_ITEM_TABLE

def get_payment_schema() -> str:
    return PAYMENT_TABLE

def get_customer_schema() -> str:
    return CUSTOMER_TABLE

def get_product_schema() -> str:
    return PRODUCT_TABLE

def get_product_category_schema() -> str:
    return PRODUCT_CATEGORY_TABLE





   
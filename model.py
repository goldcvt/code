from datetime import date
from typing import Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int

class Batch:
    def __init__(self, available_quantity: int, sku: str, eta: Optional[date], on_warehouse: bool) -> None:
        self.available_quantity = available_quantity
        self.sku = sku
        self.eta = eta
        self.on_warehouse = on_warehouse

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.available_quantity >= order_line.qty and self.sku == order_line.sku

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self.available_quantity -= order_line.qty
        else:
            raise Exception('Cannot allocate OrderLine in batch!')




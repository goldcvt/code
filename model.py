from datetime import date
from typing import List, Optional
from dataclasses import dataclass


class OutOfStockException(Exception):
    pass

@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int

class Batch:
    def __init__(self, reference: str, qty: int, sku: str, eta: Optional[date], on_warehouse: bool) -> None:
        self.reference = reference
        self._purchased_quantity = qty
        self._allocations = set() # Set[OrderLine]
        self.sku = sku
        self.eta = eta
        self.on_warehouse = on_warehouse

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.available_quantity >= order_line.qty and self.sku == order_line.sku

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)
    
    def deallocate(self, order_line: OrderLine) -> None:
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    # actually objects with identity rarely need to have any __hash__
    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta



def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        used_batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
            )
        used_batch.allocate(line)
        return used_batch.reference
    except StopIteration:
        raise OutOfStockException


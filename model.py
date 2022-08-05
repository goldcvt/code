from datetime import date
from typing import List, Optional, Union, Set
from attr import dataclass


class OutOfStock(Exception):
    pass

@dataclass(frozen=True)
class OrderLine():
    ref: str
    sku: str
    qty: int


class Batch():
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date] = None) -> None:
        self._purchased_qty = qty
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self._allocations: Set[OrderLine] = set()

    # self gt than other
    def __gt__(self, other) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.ref == other.ref

    def __hash__(self) -> int:
        return hash(self.ref)

    @property
    def en_route(self) -> bool:
        return self.eta is not None

    @property
    def allocated_qty(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_qty(self) -> int:
        return self._purchased_qty - self.allocated_qty

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def sku_match(self, line: OrderLine):
        return line.sku == self.sku

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_qty >= line.qty and self.sku_match(line)


def allocate(line: OrderLine, batches: Union[Batch, List[Batch]]):
    if isinstance(batches, list):
        try:
            batch = next(
                b for b in sorted(batches) if b.can_allocate(line)
            )
            print(list(b for b in sorted(batches) if b.can_allocate(line)))
            print("yay")
            batch.allocate(line)
        except StopIteration:
            raise OutOfStock(f"SKU {line.sku} is out of stock")
    else:
        if not batches.can_allocate(line) and batches.sku_match(line):
            raise OutOfStock(f"SKU {line.sku} is out of stock")
        batches.allocate(line)


from datetime import date, datetime
from typing import List, Union, Set

from attr import dataclass


@dataclass(frozen=True)
class OrderLine():
    ref: str
    sku: str
    qty: int

class Batch():
    def __init__(self, ref: str, sku: str, qty: int, eta: date) -> None:
        self._purchased_qty = qty
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self._allocations: Set[OrderLine] = set()

    @property
    def en_route(self) -> bool:
        return self.eta > date.today()

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

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_qty >= line.qty and line.sku == self.sku

def allocate(line: OrderLine, batches: Union[Batch, List[Batch]]):
    if isinstance(batches, list):
        available_batches = list(filter(lambda batch: batch.can_allocate(line) == True, batches))
        if len(available_batches) > 0:
            available_batches.sort(reverse=True, key=lambda batch: int(not batch.en_route))
            available_batches.sort(reverse=False, key=lambda batch: datetime.timestamp(datetime(
                year=batch.eta.year,
                month=batch.eta.month,
                day=batch.eta.day
            )))
            available_batches[0].allocate(line)
    else:
        batches.allocate(line)


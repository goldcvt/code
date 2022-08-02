from typing import Tuple
from datetime import date, timedelta
import pytest
from random import choice
from string import ascii_uppercase, digits

from model import Batch, OrderLine, allocate



today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def create_id() -> str:
    return "".join(choice(ascii_uppercase + digits) for i in range(1, 10, 1))

def create_batch_and_orderline(batch_qty = 10, orderline_qty = 2, sku = "Lamp Unique", eta = today) -> Tuple[Batch, OrderLine]:
    batch = Batch(create_id(), sku, batch_qty, eta)
    line = OrderLine(create_id(), sku, orderline_qty)
    return batch, line

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = create_batch_and_orderline()
    batch.allocate(line)
    assert batch.available_qty == 8


def test_can_allocate_if_available_greater_than_required():
    batch, line = create_batch_and_orderline()
    assert batch.can_allocate(line) == True


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = create_batch_and_orderline(2, 5)
    assert batch.can_allocate(line) == False


def test_can_allocate_if_available_equal_to_required():
    batch, line = create_batch_and_orderline(5, 5)
    assert batch.can_allocate(line) == True

def test_same_order_not_dups():
    batch, line = create_batch_and_orderline()
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_qty == 8

def test_prefers_warehouse_batches_to_shipments():
    sku = "Faceless Rollex"
    warehouse_batch = Batch(create_id(), sku, 10)
    shipment_batch = Batch(create_id(), sku, 10, tomorrow)
    line = OrderLine(create_id(), sku, 5)
    allocate(line, [warehouse_batch, shipment_batch])
    assert warehouse_batch.available_qty == 5
    assert shipment_batch.available_qty == 10


def test_prefers_earlier_batches():
    sku = "Faceless Rollex 2"
    shipment_batch = Batch(create_id(), sku, 10, tomorrow)
    shipment_later_batch = Batch(create_id(), sku, 10, tomorrow + timedelta(days=2))
    line = OrderLine(create_id(), sku, 5)
    allocate(line, [shipment_later_batch, shipment_batch])
    assert shipment_batch.available_qty == 5
    assert shipment_later_batch.available_qty == 10

def test_allocate_proc_works_one_batch():
    batch, line = create_batch_and_orderline(5, 5)
    allocate(line, batch)
    assert batch.available_qty == 0

def test_deallocate_replenishes_qty():
    batch, line = create_batch_and_orderline(5, 5)
    allocate(line, batch)
    batch.deallocate(line)
    assert batch.available_qty == 5

def test_cant_deallocate_unallocated():
    batch, line = create_batch_and_orderline(5, 5)
    batch.deallocate(line)
    assert batch.available_qty == 5

def test_cant_allocate_different_sku():
    batch = Batch(create_id(), "aaa", 10, today)
    line = OrderLine(create_id(), "bbb", 10)
    allocate(line, batch)
    assert batch.available_qty == 10


from datetime import date, timedelta
import pytest

from model import Batch, OrderLine


today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def create_batch_and_order_line(sku, batch_qty, order_line_qty):
    return (
            Batch('121', batch_qty, sku, today, on_warehouse=True),
            OrderLine('Order 228', sku, order_line_qty)
            )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    # pytest.fail("todo")
    batch, order_line = create_batch_and_order_line('red-chair', 10, 2)
    batch.allocate(order_line)
    assert batch.available_quantity == 8


def test_can_allocate_if_available_greater_than_required():
    batch, order_line = create_batch_and_order_line('red-chair', 10, 2)
    assert batch.can_allocate(order_line) == True


def test_cannot_allocate_if_available_smaller_than_required():
    batch, order_line = create_batch_and_order_line('red-chair', 10, 22)
    assert batch.can_allocate(order_line) == False


def test_can_allocate_if_available_equal_to_required():
    batch, order_line = create_batch_and_order_line('red-chair', 10, 10)
    assert batch.can_allocate(order_line) == True


def test_cannot_allocate_if_skus_dont_match():
    batch = Batch('123132', 10, 'ololol', today, on_warehouse=True)
    order_line_different_sku = OrderLine('myOrder', 'black-flag', 10)
    assert batch.can_allocate(order_line_different_sku) == False


def test_can_only_deallocate_already_allocated():
    # probably not the smartest test ever
    # even if deallocation actually worked, we could've seen correct qty bc dealloc is broken
    batch, unallocated_line = create_batch_and_order_line('hot-rod', 10, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 10


def test_deallocation_possible():
    batch, line = create_batch_and_order_line('hot-rod', 10, 2)
    batch.allocate(line)
    assert batch.available_quantity == 8
    batch.deallocate(line)
    assert batch.available_quantity == 10


def test_allocation_is_idempotent():
    batch, line = create_batch_and_order_line('hot-rod', 10, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 8

def test_different_refs_batches_not_same():
    batch = Batch('290821', 10, 'ololol', today, on_warehouse=True)
    batch2 = Batch('123132', 123, 'ololol', today, on_warehouse=True)
    assert (batch == batch2) is False

def test_same_refs_batches_same():
    batch = Batch('123132', 10, 'ololol', today, on_warehouse=True)
    batch2 = Batch('123132', 123, 'ololol', today, on_warehouse=True)
    assert (batch == batch2) is True

def test_batch_and_not_batch_not_same():
    batch = Batch('290821', 10, 'ololol', today, on_warehouse=True)
    order_line = OrderLine('123132', '123', 213)
    assert (batch == order_line) is False


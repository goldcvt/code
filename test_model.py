from datetime import date, timedelta
import pytest

from model import Batch, OrderLine


today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def create_batch_and_order_line(sku, batch_qty, order_line_qty):
    return (
            Batch(batch_qty, sku, today, on_warehouse=True),
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

def cannot_allocate_if_skus_dont_match():
    batch = Batch(10, 'ololol', today, on_warehouse=True)
    order_line_different_sku = OrderLine('myOrder', 'black-flag', 10)
    assert batch.can_allocate(order_line_different_sku) == False

def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")

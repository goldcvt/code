import pytest
from model import Batch, OrderLine, OutOfStockException, allocate
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch('in-stock-batch', 10, 'RED-CHAIR', eta=today, on_warehouse=True)
    en_route_batch = Batch('en-route-batch', 10, 'RED-CHAIR', eta=today, on_warehouse=False)
    line = OrderLine('awesome-order', 'RED-CHAIR', 2)

    used_batch_ref = allocate(line, [in_stock_batch, en_route_batch])

    assert in_stock_batch.available_quantity == 8
    assert en_route_batch.available_quantity == 10
    assert used_batch_ref == in_stock_batch.reference

def test_prefers_earlier_batches():
    today_batch = Batch('today-batch', 10, 'RED-CHAIR', eta=today, on_warehouse=True)
    tomorrow_batch = Batch('tomorrow-batch', 10, 'RED-CHAIR', eta=tomorrow, on_warehouse=True)
    later_batch = Batch('later-batch', 10, 'RED-CHAIR', eta=later, on_warehouse=True)
    line = OrderLine('awesome-order', 'RED-CHAIR', 2)

    used_batch_ref = allocate(line, [
        tomorrow_batch,
        today_batch,
        later_batch
        ])

    assert used_batch_ref == 'today-batch'
    assert today_batch.available_quantity == 8
    assert tomorrow_batch.available_quantity == 10
    assert later_batch.available_quantity == 10

def test_out_of_stock():
    batch = Batch('today-batch', 10, 'RED-CHAIR', eta=today, on_warehouse=True)
    line_one = OrderLine('awesome-order', 'RED-CHAIR', 10)
    line_two = OrderLine('awesome-order', 'RED-CHAIR', 2)

    allocate(line_one, [batch])

    with pytest.raises(OutOfStockException, match='RED-CHAIR'):
        allocate(line_two, [batch])

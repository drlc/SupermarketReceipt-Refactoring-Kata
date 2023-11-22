
import pytest
from tests.factories import DiscountFactory, ProductFactory, ProductQuantityFactory

from receipt import Receipt

@pytest.fixture
def receipt():
    return Receipt()

class TestReceiptAddProduct:
    #omitted for brevity
    pass

class TestReceiptAddDiscount:
    def test_error_giving_discount_to_not_existing_product(
            self, receipt: Receipt
    ):  
        # given
        products_in_receipt = ProductQuantityFactory()
        products_missing = ProductQuantityFactory()
        receipt.add_product(products_in_receipt.product, products_in_receipt.quantity, 1, 1 * products_in_receipt.quantity)
        discount = DiscountFactory(product=products_missing.product, discount_amount=-1)
        receipt.add_discount(discount)
        # when & then
        with pytest.raises(Exception):
            receipt.add_discount(discount)

    #further tests omitted for brevity


class TestReceiptTotalPrice:

    def test_given_no_products_and_no_discounts(
        self, receipt: Receipt
    ):
        # given
        # when
        total = receipt.total_price()
        # then
        assert total == 0

    def test_given_with_products_and_no_discounts(
        self, receipt: Receipt
    ):
        # given
        products = ProductFactory.create_batch(3)
        prices = [0.5, 1.0, 1.5]
        quantities = [1, 2, 3]
        product_quantities = [ProductQuantityFactory(base_product=p, quantity=q) for p, q in zip(products, quantities)]
        [receipt.add_product(pq.product, pq.quantity, prices[i], prices[i] * pq.quantity) for i, pq in enumerate(product_quantities)]
        # when
        total = receipt.total_price()
        # then
        expected_total = 7
        assert total == expected_total

    def test_given_with_products_and_discounts(
            self, receipt: Receipt
    ):  
        # given
        products = ProductFactory.create_batch(3)
        prices = [0.5, 1.0, 1.5]
        quantities = [1, 2, 3]
        product_quantities = [ProductQuantityFactory(base_product=p, quantity=q) for p, q in zip(products, quantities)]
        [receipt.add_product(pq.product, pq.quantity, prices[i], prices[i] * pq.quantity) for i, pq in enumerate(product_quantities)]
        discount_amount = [0, 0, -1]
        discounts = [DiscountFactory(base_product=p, discount_amount=discount_amount[i]) for i, p in enumerate(products)]
        [receipt.add_discount(discount) for discount in discounts]
        # when
        total = receipt.total_price()
        # then
        expected_total = 6
        assert total == expected_total


        
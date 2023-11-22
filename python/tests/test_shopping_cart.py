
from typing import Dict, List
import pytest
from model_objects import ProductQuantity, SpecialOfferType
from catalog import SupermarketCatalog
from receipt import Receipt
from shopping_cart import ShoppingCart
from tests.factories import OfferFactory, ProductQuantityFactory


@pytest.fixture
def cart():
    return ShoppingCart()

class TestShoppingCartAddItem:
    #omitted for brevity
    pass

class TestShoppingCartAddItemQuantity:
    def test_add_not_existing_item_empty_list(
            self, cart: ShoppingCart
    ):  
        # given
        product_quantity = ProductQuantityFactory()
        # when
        cart.add_item_quantity(product_quantity.product, product_quantity.quantity)
        # then
        assert cart._product_quantities[product_quantity.product] == product_quantity.quantity

    def test_add_not_existing_item_not_empty_list(
            self, cart: ShoppingCart
    ):  
        # given
        product_quantity = ProductQuantityFactory(product="product-not-existing")
        product_quantity_existing = ProductQuantityFactory(product="product-existing")
        cart.add_item_quantity(product_quantity_existing.product, product_quantity_existing.quantity)
        # when
        cart.add_item_quantity(product_quantity.product, product_quantity.quantity)
        # then
        assert cart._product_quantities[product_quantity.product] == product_quantity.quantity

    def test_add_existing_item(
            self, cart: ShoppingCart
    ):  
        # given
        product_name = "product-existing"
        product_quantity = ProductQuantityFactory(product=product_name)
        product_quantity_existing = ProductQuantityFactory(product=product_name)
        cart.add_item_quantity(product_quantity_existing.product, product_quantity_existing.quantity)
        # when
        cart.add_item_quantity(product_quantity.product, product_quantity.quantity)
        # then
        assert cart._product_quantities[product_name] == product_quantity_existing.quantity + product_quantity.quantity

class TestShoppingCartHandleOffers:

    @pytest.fixture
    def receipt(self, mocker):
        return mocker.Mock()
    
    @pytest.fixture
    def catalog(self, mocker):
        catalog = mocker.Mock()

        def inner(prices: Dict[str, float]):
            catalog.unit_price.side_effect = lambda product: prices[product]
            return catalog

        return inner
    
    def fill_cart(self, cart: ShoppingCart, products=List[ProductQuantity]):
        for product in products:
            cart.add_item_quantity(product.product, product.quantity)
    
    def test_no_offers(
            self, cart: ShoppingCart, receipt: Receipt, catalog: SupermarketCatalog
    ):  
        #given
        pqs = ProductQuantityFactory.create_batch(3)
        self.fill_cart(cart, pqs)
        prices_amounts = [1,1,1]
        prices = {pq.product: pr for pq, pr in zip(pqs, prices_amounts)}
        #when
        cart.handle_offers(receipt, {}, catalog(prices))
        #then
        receipt.add_discount.assert_not_called()

    @pytest.mark.parametrize(
        "quantity,expected_discount",
        [
            pytest.param(3,-2),
            pytest.param(7,-4)
        ]
    )
    def test_single_correct_offer_three_for_two_ok_quantity(
            self, cart: ShoppingCart, receipt: Receipt, catalog: SupermarketCatalog,
            quantity: int, expected_discount
    ):  
        #given
        pqs = ProductQuantityFactory.create_batch(2, quantity=1)
        discounted_product_name = "my-product"
        pqs.append(ProductQuantityFactory(product=discounted_product_name, quantity=quantity))
        self.fill_cart(cart, pqs)
        prices_amounts = [1,1,2]
        prices = {pq.product: pr for pq, pr in zip(pqs, prices_amounts)}
        offers = {
            pqs[0].product: OfferFactory(offer_type=SpecialOfferType.TWO_FOR_AMOUNT, product=pqs[0].product),
            discounted_product_name: OfferFactory(offer_type=SpecialOfferType.THREE_FOR_TWO, product=discounted_product_name)
        }
        #when
        cart.handle_offers(receipt, offers, catalog(prices))
        #then
        receipt.add_discount.assert_called_once()
        assert receipt.add_discount.call_args.args[0].product == discounted_product_name
        assert receipt.add_discount.call_args.args[0].discount_amount == expected_discount


    @pytest.mark.parametrize(
        "quantity",
        [
            pytest.param(1),
            pytest.param(2)
        ]
    )
    def test_single_correct_offer_three_for_two_not_ok_quanitity(
            self, cart: ShoppingCart, receipt: Receipt, catalog: SupermarketCatalog,
            quantity: int
    ):  
       #given
        pqs = ProductQuantityFactory.create_batch(2, quantity=1)
        discounted_product_name = "my-product"
        pqs.append(ProductQuantityFactory(product=discounted_product_name, quantity=quantity))
        self.fill_cart(cart, pqs)
        prices_amounts = [1,1,2]
        prices = {pq.product: pr for pq, pr in zip(pqs, prices_amounts)}
        offers = {
            pqs[0].product: OfferFactory(offer_type=SpecialOfferType.TWO_FOR_AMOUNT, product=pqs[0].product),
            discounted_product_name: OfferFactory(offer_type=SpecialOfferType.THREE_FOR_TWO, product=discounted_product_name)
        }
        #when
        cart.handle_offers(receipt, offers, catalog(prices))
        #then
        receipt.add_discount.assert_not_called()

    def test_single_correct_offer_ten_percent(
            self, cart: ShoppingCart
    ):  
        #omitted for brevity
        pass

    def test_single_correct_offer_two_for_amount(
            self, cart: ShoppingCart
    ):  
        #omitted for brevity
        pass

    def test_single_correct_offer_five_for_amount_ok_quantity(
            self, cart: ShoppingCart
    ):  
        #omitted for brevity
        pass

    def test_single_correct_offer_five_for_amount_not_ok_quanitity(
            self, cart: ShoppingCart
    ):  
        #omitted for brevity
        pass

    def test_multiple_correct_offer(
            self, cart: ShoppingCart
    ):  
        #omitted for brevity
        pass

    

    
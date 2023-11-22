from model_objects import Discount, Offer, Product, ProductQuantity, ProductUnit, SpecialOfferType
import factory 

__all__ = [
    "ProductFactory",
    "ProductQuantityFactory",
    "OfferFactory",
    "DiscountFactory",
]

class ProductFactory(factory.Factory):
    name = factory.Sequence(lambda n: f"name-{n}")
    unit = ProductUnit.EACH

    class Meta:
        model = Product


class ProductQuantityFactory(factory.Factory):
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pydecimal", right_digits=0, min_value=1, max_value=100)

    class Meta:
        model = ProductQuantity


class OfferFactory(factory.Factory):
    offer_type = SpecialOfferType.THREE_FOR_TWO
    product = factory.SubFactory(ProductFactory)
    argument = None

    class Meta:
        model = Offer


class DiscountFactory(factory.Factory):
    product = factory.SubFactory(ProductFactory)
    description = factory.Sequence(lambda n: f"description-{n}")
    discount_amount = factory.Faker("pydecimal", right_digits=0, min_value=1, max_value=100)

    class Meta:
        model = Discount

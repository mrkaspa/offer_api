import factory
from business import Business


class BusinessFactory(factory.Factory):
    class Meta:
        model = Business

    name = factory.Faker('company')
    description = factory.Faker('sentence')


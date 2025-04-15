from datetime import date, timedelta
import factory
from app.domain.models import Promotion, PromotionType


class PromotionFactory(factory.Factory):
    class Meta:
        model = Promotion

    name = factory.Faker("company")
    description = factory.Faker("sentence")
    promotion_type = factory.Iterator([pt.value for pt in PromotionType])
    start_date = factory.LazyFunction(lambda: date.today())
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=30))
    is_active = True

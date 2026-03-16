import factory

from app.users.domain.entities import UserEntity
from app.users.domain.enums import UserRole


class UserFactory(factory.Factory):
    class Meta:
        model = UserEntity

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    role = factory.Faker("random_element", elements=list(UserRole))
    is_active = True

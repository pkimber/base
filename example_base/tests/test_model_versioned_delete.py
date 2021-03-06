# -*- encoding: utf-8 -*-
import pytest

from django.utils import timezone

from base.model_utils import BaseError
from example_base.models import FruitCake
from login.tests.factories import UserFactory
from .factories import FruitCakeFactory


@pytest.mark.django_db
def test_factory():
    FruitCakeFactory()


@pytest.mark.django_db
def test_str():
    str(FruitCakeFactory())


@pytest.mark.django_db
def test_set_deleted():
    obj = FruitCakeFactory()
    assert 0 == obj.deleted_version
    user = UserFactory()
    FruitCake.objects.set_deleted(obj, user)
    obj.refresh_from_db()
    assert obj.deleted is True
    assert obj.user_deleted == user
    assert obj.date_deleted is not None
    assert 1 == obj.deleted_version


@pytest.mark.django_db
def test_set_deleted_multi():
    user = UserFactory()
    c1 = FruitCakeFactory(number=19, description='c1')
    FruitCake.objects.set_deleted(c1, user)
    c2 = FruitCakeFactory(number=19, description='c2')
    FruitCake.objects.set_deleted(c2, user)
    FruitCakeFactory(number=19, description='c3')
    result = FruitCake.objects.filter(number=19).order_by('description')
    assert 3 == result.count()
    assert [
        (19, True, 1),
        (19, True, 2),
        (19, False, 0),
    ] == [(o.number, o.deleted, o.deleted_version) for o in result]


@pytest.mark.django_db
def test_set_deleted_model():
    """Standard way to delete rows from non-versioned delete models"""
    obj = FruitCakeFactory()
    with pytest.raises(BaseError) as e:
        obj.set_deleted(UserFactory())
    assert 'model with deleted version tracking' in str(e.value)


@pytest.mark.django_db
def test_undelete():
    obj = FruitCakeFactory()
    user = UserFactory()
    FruitCake.objects.set_deleted(obj, user)
    assert obj.deleted_version > 0
    obj.refresh_from_db()
    obj.undelete()
    obj.refresh_from_db()
    assert obj.deleted is False
    assert obj.user_deleted is None
    assert obj.date_deleted is None
    assert 0 == obj.deleted_version

# -*- encoding: utf-8 -*-
import pytest

from django.utils import timezone

from base.model_utils import BaseError
from login.tests.factories import UserFactory
from .factories import LemonCakeFactory


@pytest.mark.django_db
def test_factory():
    LemonCakeFactory()


@pytest.mark.django_db
def test_str():
    str(LemonCakeFactory())


@pytest.mark.django_db
def test_set_deleted():
    obj = LemonCakeFactory()
    user = UserFactory()
    before = timezone.now()
    obj.set_deleted(user)
    after = timezone.now()
    obj.refresh_from_db()
    assert obj.deleted is True
    assert obj.user_deleted == user
    assert obj.date_deleted >= before
    assert obj.date_deleted <= after


@pytest.mark.django_db
def test_set_deleted_already_deleted():
    obj = LemonCakeFactory()
    user = UserFactory()
    obj.set_deleted(user)
    obj.refresh_from_db()
    with pytest.raises(BaseError) as e:
        obj.set_deleted(user)
    assert 'is already deleted' in str(e.value)


@pytest.mark.django_db
def test_undelete():
    obj = LemonCakeFactory()
    user = UserFactory()
    obj.set_deleted(user)
    obj.refresh_from_db()
    obj.undelete()
    obj.refresh_from_db()
    assert obj.deleted is False
    assert obj.user_deleted is None
    assert obj.date_deleted is None


@pytest.mark.django_db
def test_undelete_not_deleted():
    obj = LemonCakeFactory()
    with pytest.raises(BaseError) as e:
        obj.undelete()
    assert 'is not deleted' in str(e.value)

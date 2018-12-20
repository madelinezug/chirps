import pytest

from .models import Individual

pytestmark = pytest.mark.django_db


def test_save():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    indiv.save()
    free = Individual.objects.get(email='email@gmail.com')
    assert indiv.first == free.first
    assert indiv.admin_status == free.admin_status


def test_makeadmin():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    indiv.make_admin()
    assert indiv.admin_status == 1


def test_isadmin():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    admin = Individual.objects.create(email='email2@gmail.com',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=1)
    assert not indiv.is_admin()
    assert admin.is_admin()

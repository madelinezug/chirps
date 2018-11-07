import pytest

from .models import Individual

pytestmark = pytest.mark.django_db


def test_save():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      password='password',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    assert indiv.first == 'firstname'
    assert indiv.admin_status == 0


def test_makeadmin():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      password='password',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    indiv.make_admin()
    assert indiv.admin_status == 1


def test_isadmin():
    indiv = Individual.objects.create(email='email@gmail.com',
                                      password='password',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=0)
    admin = Individual.objects.create(email='email2@gmail.com',
                                      password='password',
                                      first='firstname',
                                      last='lastname',
                                      admin_status=1)
    assert not indiv.is_admin()
    assert admin.is_admin()

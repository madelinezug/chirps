import pytest
from .models import Individual
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import reset_pw, detail, individual_detail
pytestmark = pytest.mark.django_db


def test_reset_pw_get():
    factory = RequestFactory()
    request = factory.get(reverse('reset_pw'))

    response = reset_pw(request)

    assert response.status_code == 302
    assert response.url == '/accounts/password_reset'


def test_reset_pw_mismatched():
    factory = RequestFactory()
    request = factory.post(reverse('reset_pw'))
    request.POST = {
        'password': 'passwordpassword1',
        'redo_password': 'passwordpassword'
    }
    print(request)
    response = reset_pw(request)

    assert response.status_code == 302
    assert response.url == '/accounts/password_reset'


def test_reset_pw_success():
    factory = RequestFactory()
    request = factory.post(reverse('reset_pw'))
    request.POST = {
        'password': 'passwordpassword1',
        'redo_password': 'passwordpassword1',
        'user_email': 'gerard.bentley@pomona.edu'
    }
    print(request)
    response = reset_pw(request)

    assert response.status_code == 302
    assert response.url == '/accounts/login'


def test_detail_anon():
    factory = RequestFactory()
    request = factory.get('/announcements/9/')
    request.user = AnonymousUser()

    response = detail(request, 9)
    assert response.status_code == 302
    assert '/accounts/login' in response.url


def test_detail_unapproved_owner():
    factory = RequestFactory()
    request = factory.get('/announcements/9/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')

    response = detail(request, 9)
    assert response.status_code == 200
    assert b'test text' in response.content


def test_detail_unapproved_visitor():
    factory = RequestFactory()
    request = factory.get('/announcements/9/')
    request.user = User.objects.get(email='gb@pomona.edu')

    response = detail(request, 9)
    assert response.status_code == 302
    assert response.url == reverse('index')


def test_detail_approved_visitor():
    factory = RequestFactory()
    request = factory.get('/announcements/10/')
    request.user = User.objects.get(email='gb@pomona.edu')

    response = detail(request, 10)

    assert response.status_code == 200
    assert b'approved dchirp' in response.content


def test_detail_admin():
    factory = RequestFactory()
    request = factory.get('/announcements/9/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = detail(request, 9)
    assert response.status_code == 200
    assert b'test text' in response.content
    assert b'approve' in response.content


def test_detail_nopost():
    factory = RequestFactory()
    request = factory.get('/announcements/47/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = detail(request, 47)
    assert response.status_code == 200
    assert b'No announcement' in response.content


def test_ind_detail_anon():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = AnonymousUser()

    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    assert response.status_code == 302
    assert '/accounts/login' in response.url


def test_ind_detail_non_admin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')

    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_ind_detail_admin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    assert response.status_code == 200
    assert b'Not blocked' in response.content
    assert b'Not admin' in response.content


def test_ind_detail_nouser():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/ger@pomona.edu/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = individual_detail(request, 'ger@pomona.edu')
    assert response.status_code == 200
    assert b'No user' in response.content

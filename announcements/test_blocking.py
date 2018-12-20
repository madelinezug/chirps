import pytest
from .models import Individual
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import detail, individual_detail
pytestmark = pytest.mark.django_db


def test_block_admin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'block': 'block'
    }
    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    print(response.content)
    assert response.status_code == 200
    assert b'gerard.bentley' in response.content
    assert b'Blocked' in response.content


def test_block_nonadmin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'block': 'block'
    }
    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_unblock_admin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/third@pomona.edu/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'unblock': 'unblock'
    }
    response = individual_detail(request, 'third@pomona.edu')
    print(response.content)
    assert response.status_code == 200
    assert b'third@pomona' in response.content
    assert b'Not blocked' in response.content


def test_unblock_nonadmin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/third@pomona.edu/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'unblock': 'unblock'
    }
    response = individual_detail(request, 'third@pomona.edu')
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_make_admin_admin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'make_admin': 'make_admin'
    }
    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    print(response.content)
    assert response.status_code == 200
    assert b'gerard.bentley' in response.content
    assert b'Admin' in response.content


def test_make_admin_nonadmin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/gerard.bentley@pomona.edu/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'make_admin': 'make_admin'
    }
    response = individual_detail(request, 'gerard.bentley@pomona.edu')
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_revoke_admin_admin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/admin@admin.com/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'revoke_admin': 'revoke_admin'
    }
    response = individual_detail(request, 'admin@admin.com')
    print(response.content)
    assert response.status_code == 200
    assert b'admin@admin' in response.content
    assert b'Not admin' in response.content


def test_revoke_admin_nonadmin():
    factory = RequestFactory()
    request = factory.post(
        '/announcements/individuals/admin@admin.com/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'revoke_admin': 'revoke_admin'
    }
    response = individual_detail(request, 'admin@admin.com')
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'

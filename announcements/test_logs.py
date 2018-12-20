import pytest
from .models import Individual
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import logs, individuals, admin_logs
pytestmark = pytest.mark.django_db


def test_logs_admin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/logs/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = logs(request)
    print(response.content)
    assert response.status_code == 200
    assert b'Admin privileges' in response.content


def test_logs_nonadmin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/logs/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')

    response = logs(request)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_individuals_admin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')

    response = individuals(request)
    print(response.content)
    assert response.status_code == 200
    assert b'Manage Users' in response.content


def test_individuals_nonadmin():
    factory = RequestFactory()
    request = factory.get(
        '/announcements/individuals/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')

    response = individuals(request)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'

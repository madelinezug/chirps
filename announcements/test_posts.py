import pytest
from .models import Individual
from django.test import Client
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import detail, individual_detail
pytestmark = pytest.mark.django_db


def test_approve_admin():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'approve': 'approve'
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 200
    assert b'test text' in response.content
    assert b'Approved' in response.content


def test_approve_nonadmin():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'approve': 'approve'
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 200
    assert b'test text' in response.content
    assert b'Approved' not in response.content


def test_reject_admin():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'reject': 'reject',
        'reject_msg': 'bad post'
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_reject_nonadmin_owner():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'reject': 'reject'
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 200
    assert b'test text' in response.content
    assert b'Approved' not in response.content


def test_delete_nonowner():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gbkh2015@mymail.pomona.edu')
    request.POST = {
        'delete': 'delete',
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 200
    assert b'test text' in response.content


def test_delete_owner():
    factory = RequestFactory()
    request = factory.post('/announcements/9/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'delete': 'delete'
    }
    response = detail(request, 9)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/'


def test_save_nonowner():
    factory = RequestFactory()
    request = factory.post('/announcements/11/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'save': 'save',
    }
    response = detail(request, 11)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/saved'


def test_unsave_nonowner():
    factory = RequestFactory()
    request = factory.post('/announcements/12/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'unsave': 'unsave',
    }
    response = detail(request, 12)
    print(response.content)
    assert response.status_code == 302
    assert response.url == '/announcements/saved'


def test_search_user():
    factory = RequestFactory()
    request = factory.post('/announcements/11/')
    request.user = User.objects.get(email='gerard.bentley@pomona.edu')
    request.POST = {
        'search': 'search',
        'search_key': 'mysearch'
    }
    response = detail(request, 11)
    print(response.content)
    assert response.status_code == 302
    assert '/announcements/search' in response.url

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from test_task.password_manager.models import PasswordEntry


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def password_entries(db):
    entries = [
        PasswordEntry.objects.create(service_name='gmail'),
        PasswordEntry.objects.create(service_name='facebook'),
        PasswordEntry.objects.create(service_name='twitter'),
    ]

    passwords = ['password1', 'password2', 'password3']
    for entry, password in zip(entries, passwords):
        entry.set_password(password)
        entry.save()

    return entries

def test_list_password_entries(api_client, password_entries):
    url = reverse('password-list-create')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

def test_list_password_entries_filter(api_client, password_entries):
    url = reverse('password-list-create')
    response = api_client.get(url, {'service_name': 'face'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['service_name'] == 'facebook'

@pytest.mark.django_db
def test_create_password_entry(api_client):
    url = reverse('password-list-create')
    data = {'service_name': 'instagram', 'password': 'password4'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert PasswordEntry.objects.filter(service_name='instagram').exists()

def test_update_existing_password_entry(api_client, password_entries):
    url = reverse('password-list-create')
    data = {'service_name': 'gmail', 'password': 'newpassword'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    entry = PasswordEntry.objects.get(service_name='gmail')
    assert entry.get_password() == 'newpassword'

@pytest.mark.django_db
def test_retrieve_password_entry(api_client, password_entries):
    url = reverse('password-retrieve', kwargs={'service_name': 'gmail'})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['service_name'] == 'gmail'

@pytest.mark.django_db
def test_retrieve_nonexistent_password_entry(api_client):
    url = reverse('password-retrieve', kwargs={'service_name': 'nonexistent'})
    response = api_client.get(url)
    assert response.status_code == 404

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from students.models import Course


@pytest.mark.django_db
def test_courses_retrieve(api_client, course_factory):
    course = course_factory()
    url = reverse("courses-detail", args=(course.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_data = resp.data
    assert course.id == resp_data['id']


@pytest.mark.django_db
def test_courses_list(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse("courses-list")
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert len(courses) == len(resp.data)


@pytest.mark.django_db
def test_filter_id(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse("courses-list")
    resp = api_client.get(url, data={'id': f'{courses[0].id}'})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert courses[0].id == resp_json[0]['id']


@pytest.mark.django_db
def test_filter_name(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse("courses-list")
    resp = api_client.get(url, data={'name': f'{courses[0].name}'})
    assert resp.status_code == HTTP_200_OK
    resp_data = resp.data
    assert courses[0].name == resp_data[0]['name']


@pytest.mark.django_db
def test_course_create(api_client):
    course = {'name': 'test_Course'}
    url = reverse("courses-list")
    resp = api_client.post(url, data=course)
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_course_update(api_client):
    course = {'name': 'test_course'}
    course_update = {'name': 'test_course_update'}

    url = reverse("courses-list")
    resp = api_client.post(url, data=course)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    url_upd = reverse("courses-detail", args=(resp_json["id"], ))
    resp_upd = api_client.patch(url_upd, data=course_update)
    assert resp_upd.status_code == HTTP_200_OK

@pytest.mark.django_db
def test_curse_delete(api_client):
    course = {'name': 'test_course'}
    url = reverse("courses-list")
    resp = api_client.post(url, data=course)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    url_to_del = reverse("courses-detail", args=(resp_json["id"], ))
    resp_del = api_client.delete(url_to_del)
    assert resp_del.status_code == HTTP_204_NO_CONTENT

import pytest

from data_extractor import get_cases


@pytest.fixture(scope='module')
def scrap_data():
    return get_cases()


@pytest.fixture(scope='module')
def world_data(scrap_data):
    return scrap_data['World']


@pytest.fixture(scope='module')
def poland_data(scrap_data):
    return scrap_data['Poland']


def test_world_name(world_data):
    assert world_data['name'].lower() == 'world'


def test_world_cases(world_data):
    assert world_data['cases'].replace(',', '').isdigit()


def test_world_new(world_data):
    assert world_data['new'].replace(',', '').replace('+', '').isdigit()


def test_world_recovered(world_data):
    assert world_data['recovered'].replace(',', '').isdigit()


def test_world_active(world_data):
    assert world_data['active'].replace(',', '').isdigit()


def test_poland_name(poland_data):
    assert poland_data['name'].lower() == 'poland'


def test_poland_cases(poland_data):
    assert poland_data['cases'].replace(',', '').isdigit()


def test_poland_new(poland_data):
    assert poland_data['new'].replace(',', '').replace('+', '').isdigit()


def test_poland_recovered(poland_data):
    assert poland_data['recovered'].replace(',', '').isdigit()


def test_poland_active(poland_data):
    assert poland_data['active'].replace(',', '').isdigit()


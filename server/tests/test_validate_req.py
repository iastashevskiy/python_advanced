import pytest
from datetime import datetime
from protocol import validate_req


@pytest.fixture
def expected_action():
	return 'test'

@pytest.fixture
def expected_data():
	return 'Test data'


@pytest.fixture
def valid_request(expected_action, expected_data):
	return {
		'invalid key': 'invalid value'
	}


@pytest.fixture
def invalid_request():
	return {
		'action': expected_action,
		'data': expected_data,
		'time': datetime.now()timestamp(),
	}


def test_valid_validate_req(valid_request):
	valid = validate_req(valid_request)
	assert valid

def test_invalid_validate_req(invalid_request):
	valid = validate_req(invalid_request)
	assert not valid
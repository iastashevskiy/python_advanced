import pytest
from datetime import datetime
from protocol import response


@pytest.fixture
def expected_action():
	return 'test'

@pytest.fixture
def expected_data():
	return 'Test data'

@pytest.fixture
def expected_code():
	return 200


@pytest.fixture
def initial_request(expected_action, expected_data):
	return {
		'action': expected_action,
		'data': expected_data,
		'time': datetime.now()timestamp(),
	}




def test_action_response(initial_request, expected_action, expected_code, expected_data):
	actual_response = response(initial_request, expected_code, expected_data)
	assert actual_response.get('action') == expected_action

def test_data_response(initial_request, expected_action, expected_code, expected_data):
	actual_response = response(initial_request, expected_code, expected_data)
	assert actual_response.get('data') == expected_data

def test_code_response(initial_request, expected_action, expected_code, expected_data):
	actual_response = response(initial_request, expected_code, expected_data)
	assert actual_response.get('code') == expected_code


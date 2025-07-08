import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_encode_valid_input(client):
    response = client.post('/encode', json={"text": "TEST"})
    assert response.status_code == 200
    assert response.json == {"morse": "– · ··· –"}


def test_encode_valid_input_with_spaces(client):
    response = client.post('/encode', json={"text": "T E S T"})
    assert response.status_code == 200
    assert response.json == {"morse": "– · ··· –"}


def test_encode_input_with_digits(client):
    response = client.post('/encode', json={"text": "TEST123"})
    assert response.status_code == 200
    assert response.json == {"morse": "– · ··· – ·–––– ··––– ···––"}


def test_encode_invalid_input_special_chars(client):
    response = client.post('/encode', json={"text": "TEST%"})
    assert response.status_code == 400
    assert response.json == {"error": "Character '%' not supported."}


def test_encode_empty_input(client):
    response = client.post('/encode', json={"text": ""})
    assert response.status_code == 400
    assert response.json == {"error": "Input cannot be empty."}


def test_encode_missing_text(client):
    response = client.post('/encode', json={})
    assert response.status_code == 400
    assert response.json == {"error": "Missing 'text' in request body."}


def test_encode_non_string_input(client):
    response = client.post('/encode', json={"text": 123})
    assert response.status_code == 400
    assert response.json == {"error": "'text' must be a string."}


def test_encode_with_punctuation(client):
    response = client.post('/encode', json={"text": "HI,?!"})
    assert response.status_code == 200
    assert response.json == {"morse": "···· ·· ––··–– ··––·· –·–·––"}


def test_encode_with_special_chars(client):
    response = client.post('/encode', json={"text": "SOS/AR"})
    assert response.status_code == 200
    assert response.json == {"morse": "···––·–– –··–· ·–·–·"}


def test_encode_long_input_with_digits(client):
    response = client.post('/encode', json={"text": "MESSAGE123"})
    assert response.status_code == 200
    assert response.json == {"morse": '–– · ··· ··· ·– ––· · ·–––– ··––– ···––'}


def test_decode_valid_morse(client):
    response = client.post('/decode', json={"morse": "– · ··· –"})
    assert response.status_code == 200
    assert response.json == {"text": "TEST"}


def test_decode_invalid_morse(client):
    response = client.post('/decode', json={"morse": "– · ### –"})
    assert response.status_code == 400
    assert response.json == {"error": "Only Morse code characters (·, –, space) allowed."}


def test_decode_empty_morse(client):
    response = client.post('/decode', json={"morse": ""})
    assert response.status_code == 400
    assert response.json == {"error": "No Morse code found."}


def test_decode_missing_morse(client):
    response = client.post('/decode', json={})
    assert response.status_code == 400
    assert response.json == {"error": "Missing 'morse' in request body."}


def test_decode_non_string_input(client):
    response = client.post('/decode', json={"morse": 123})
    assert response.status_code == 400
    assert response.json == {"error": "'morse' must be a string."}


def test_decode_with_punctuation(client):
    response = client.post('/decode', json={"morse": "···· ·· ––··–– ··––·· –·–·––"})
    assert response.status_code == 200
    assert response.json == {"text": "HI,?!"}


def test_decode_with_special_chars(client):
    response = client.post('/decode', json={"morse": "···––·–– –··–· ·–·–·"})
    assert response.status_code == 200
    assert response.json == {"text": "SOS/AR"}


def test_decode_invalid_code(client):
    response = client.post('/decode', json={"morse": "––·–· ––·–·"})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid Morse code: '––·–·' not recognized."}


def test_decode_extra_spaces(client):
    response = client.post('/decode', json={"morse": " ·–  –· "})
    assert response.status_code == 200
    assert response.json == {"text": "AN"}


def test_decode_long_morse(client):
    response = client.post('/decode', json={"morse": "–– · ··· ··· ·– ––· · ·–––– ··––– ···––"})
    assert response.status_code == 200
    assert response.json == {"text": "MESSAGE123"}

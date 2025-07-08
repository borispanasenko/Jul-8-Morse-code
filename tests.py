from unittest.mock import patch
import io
from contextlib import redirect_stdout
from morsedict import morse_dict


def run_morse_program(input_values):
    user_input = ''.join(input_values.upper().split())
    if user_input == "F":
        return False
    try:
        for char in user_input:
            if not char.isalpha() and not char.isdigit():
                raise TypeError
    except TypeError:
        print("Only alphabetical letters and numbers.", end=' ')
        return True
    else:
        for char in user_input:
            print(f"{morse_dict[char]}", end=' ')
    return True


def test_valid_input():
    inputs = ["ROCK"]
    expected_output = "·–· ––– –·–· –·– "

    with patch('builtins.input', side_effect=inputs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_morse_program(inputs[0])
        assert result == True
        assert f.getvalue() == expected_output


def test_valid_input_with_spaces():
    inputs = ["R O C K"]
    expected_output = "·–· ––– –·–· –·– "

    with patch('builtins.input', side_effect=inputs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_morse_program(inputs[0])
        assert result == True
        assert f.getvalue() == expected_output


def test_with_numerical_input():
    inputs = ["ROCK123"]
    expected_output = "·–· ––– –·–· –·– ·–––– ··––– ···–– "

    with patch('builtins.input', side_effect=inputs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_morse_program(inputs[0])
        assert result == True
        assert f.getvalue() == expected_output


def test_exit_program():
    inputs = ["F"]

    with patch('builtins.input', side_effect=inputs):
        result = run_morse_program(inputs[0])
        assert result == False


def test_empty_input():
    inputs = [""]
    expected_output = ""

    with patch('builtins.input', side_effect=inputs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_morse_program(inputs[0])
        assert result == True
        assert f.getvalue() == expected_output


def test_mixed_case_input():
    inputs = ["RoCk"]
    expected_output = "·–· ––– –·–· –·– "

    with patch('builtins.input', side_effect=inputs):
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_morse_program(inputs[0])
        assert result == True
        assert f.getvalue() == expected_output

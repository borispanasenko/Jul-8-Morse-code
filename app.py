from flask import Flask, request, jsonify
from morsedict import morse_dict, reverse_morse_dict


app = Flask(__name__)


def encode_morse(text):
    if not isinstance(text, str):
        return {"error": "'text' must be a string."}, 400
    text = ''.join(text.upper().split())
    if not text:
        return {"error": "Input cannot be empty."}, 400

    codes = []
    i = 0
    while i < len(text):
        if text[i:i + 3] == 'SOS':
            codes.append('SOS')
            i += 3
        elif text[i:i + 2] == 'AR':
            codes.append('AR')
            i += 2
        else:
            char = text[i]
            if char not in morse_dict:
                return {"error": f"Character '{char}' not supported."}, 400
            codes.append(char)
            i += 1

    try:
        result = ' '.join(morse_dict[symbol] for symbol in codes)
        return {"morse": result}, 200
    except Exception as e:
        return {"error": f"Error encoding Morse code: {str(e)}"}, 400


def decode_morse(morse):
    if not isinstance(morse, str):
        return {"error": "'morse' must be a string."}, 400
    if not morse.strip():
        return {"error": "No Morse code found."}, 400
    morse_code_chars = {'·', '–', ' '}
    if not all(char in morse_code_chars for char in morse):
        return {"error": "Only Morse code characters (·, –, space) allowed."}, 400
    try:
        codes = morse.strip().split()
        if not codes:
            return {"error": "Invalid Morse code. No valid codes found."}, 400
        for code in codes:
            if code not in reverse_morse_dict:
                return {"error": f"Invalid Morse code: '{code}' not recognized."}, 400
        result = ''.join(reverse_morse_dict.get(code_symbol) for code_symbol in codes)
        return {"text": result}, 200
    except Exception as e:
        return {"error": f"Error processing Morse code: {str(e)}"}, 400


@app.route('/encode', methods=['POST'])
def encode_endpoint():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body."}), 400
    result, status = encode_morse(data['text'])
    return jsonify(result), status


@app.route('/decode', methods=['POST'])
def decode_endpoint():
    data = request.get_json()
    if not data or 'morse' not in data:
        return jsonify({"error": "Missing 'morse' in request body."}), 400
    result, status = decode_morse(data['morse'])
    return jsonify(result), status


if __name__ == '__main__':
    app.run(debug=False)

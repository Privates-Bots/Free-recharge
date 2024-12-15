from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Set your Google Cloud Translation API key
API_KEY = 'AIzaSyA9KagdjpK-QmGQn26JOBz0YFsXYTE2ni8'

@app.route('/translate', methods=['GET'])
def translate():
    # Get URL parameters
    to_translate = request.args.get('toTrans')
    text = request.args.get('text')

    if not to_translate or not text:
        return jsonify({
            'status': 'error',
            'message': 'Missing required parameters: toTrans (language code) and text.'
        }), 400

    # Prepare the API URL
    url = f"https://translation.googleapis.com/language/translate/v2"
    params = {
        'key': API_KEY,
        'q': text,
        'target': to_translate
    }

    # Make the GET request
    try:
        response = requests.get(url, params=params)
        response_data = response.json()
        
        print(response_data)  # Debugging line to log response

        if 'data' in response_data and 'translations' in response_data['data']:
            translated_text = response_data['data']['translations'][0]['translatedText']
            return jsonify({
                'status': 'success',
                'translated_text': translated_text,
                'language_code': to_translate
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Translation not found. Please check the language code and text.'
            }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

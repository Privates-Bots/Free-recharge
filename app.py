from flask import Flask, request, jsonify
from google.cloud import translate_v2 as translate

app = Flask(__name__)
translator = translate.Client()

@app.route('/translate', methods=['GET'])
def translate_text():
    to_trans = request.args.get('toTrans')
    text = request.args.get('text')

    if not to_trans or not text:
        return jsonify({'error': 'Missing required parameters: toTrans and text'}), 400

    try:
        # Translate the text
        result = translator.translate(text, target_language=to_trans)
        return jsonify({'translatedText': result['translatedText']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

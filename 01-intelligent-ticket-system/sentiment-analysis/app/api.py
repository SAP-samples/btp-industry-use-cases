from flask import Flask, request, jsonify
from flask_cors import CORS

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

def get_text_from_request():
    request_data = request.get_json()
    return request_data['text']

def sentiment_vader(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sid_obj.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    neutral = sentiment_dict['neu']
    positive = sentiment_dict['pos']
    compound = sentiment_dict['compound']

    if sentiment_dict['compound'] >= 0.05 :
        overall_sentiment = "Compliment"

    elif sentiment_dict['compound'] <= - 0.05 :
        overall_sentiment = "Complaint"

    else :
        overall_sentiment = "Request"
  
    return negative, neutral, positive, compound, overall_sentiment

@app.route('/', methods=['GET'])
def root():
    return 'Sentiment Analysis API: Health Check Successfull.', 200

@app.route('/do-analysis', methods=['POST'])
def do_analysis():
    sentence = get_text_from_request()
    analysis_result = sentiment_vader(sentence)
    
    try:
        return jsonify({'negative': analysis_result[0], 'neutral': analysis_result[1], 'positive': analysis_result[2], 'compound': analysis_result[3],'overall_classification': analysis_result[4]}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def create_app():
    return app

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)

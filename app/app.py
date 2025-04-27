from flask import Flask, request, jsonify, render_template
from src.react_agent.react_agent import Agent

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_message = data['message']

    bot_reply = Agent.run(user_message)

    return jsonify({'reply': bot_reply})


if __name__ == '__main__':
    app.run(debug=True)

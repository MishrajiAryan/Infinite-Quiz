# app.py
import os
import json
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

QUES_FOLDER = 'ques'

@app.route('/')
def index():
    topics = [f[:-5] for f in os.listdir(QUES_FOLDER) if f.endswith('.json')]
    return render_template('index.html', topics=topics)

@app.route('/get_question/<topic>', methods=['GET'])
def get_question(topic):
    filepath = os.path.join(QUES_FOLDER, f'{topic}.json')
    if not os.path.exists(filepath):
        return jsonify({'error': 'Topic not found'}), 404
    with open(filepath, 'r') as f:
        questions = json.load(f)
    question = random.choice(questions)
    return jsonify(question)

@app.route('/flag_question', methods=['POST'])
def flag_question():
    data = request.json
    topic = data['topic']
    question_text = data['question']
    filepath = os.path.join(QUES_FOLDER, f'{topic}.json')
    with open(filepath, 'r+') as f:
        questions = json.load(f)
        for q in questions:
            if q['question'] == question_text:
                q['flag'] = not q.get('flag', False)
                break
        f.seek(0)
        json.dump(questions, f, indent=4)
        f.truncate()
    return jsonify({'status': 'toggled'})

# app.py
import os
import json
import random
from flask import Flask, render_template, jsonify, request, redirect, url_for

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

# --- New routes for creating and updating topics ---

@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        topic_name = request.form['topic_name'].strip()
        content = request.form['topic_content']
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return "Invalid JSON content. Please correct and try again.", 400

        filepath = os.path.join(QUES_FOLDER, f'{topic_name}.json')
        if os.path.exists(filepath):
            return f"Topic '{topic_name}' already exists.", 400

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return redirect(url_for('index'))

    return render_template('create_topic.html')

@app.route('/update_topic', methods=['GET', 'POST'])
def update_topic():
    topics = [f[:-5] for f in os.listdir(QUES_FOLDER) if f.endswith('.json')]
    selected_topic = None
    content = None

    if request.method == 'POST':
        # If form submitted with content to update
        if 'topic_content' in request.form and 'topic_name' in request.form:
            selected_topic = request.form['topic_name']
            content = request.form['topic_content']
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                return "Invalid JSON content. Please correct and try again.", 400

            filepath = os.path.join(QUES_FOLDER, f'{selected_topic}.json')
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return redirect(url_for('index'))

        # If only topic_name is sent (dropdown change), load that topic content
        if 'topic_name' in request.form:
            selected_topic = request.form['topic_name']

    if selected_topic:
        filepath = os.path.join(QUES_FOLDER, f'{selected_topic}.json')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
        else:
            content = None

    return render_template('update_topic.html', topics=topics, selected_topic=selected_topic, content=content)

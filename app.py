import random
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    flag = db.Column(db.Boolean, default=False)

# Home Page
@app.route('/')
def index():
    topics = db.session.query(QuizQuestion.Title).distinct().all()
    topics = [t[0] for t in topics]
    return render_template('index.html', topics=topics)

# Get random question by topic
@app.route('/get_question/<topic>')
def get_question(topic):
    questions = QuizQuestion.query.filter_by(Title=topic).all()
    if not questions:
        return jsonify({'error': 'Topic not found'}), 404
    q = random.choice(questions)
    return jsonify({
        "question": q.question,
        "option_a": q.option_a,
        "option_b": q.option_b,
        "option_c": q.option_c,
        "option_d": q.option_d,
        "correct_option": q.correct_option,
        "flag": q.flag
    })

# Flag/Unflag question
@app.route('/flag_question', methods=['POST'])
def flag_question():
    data = request.json
    question_text = data['question']
    topic = data['topic']
    q = QuizQuestion.query.filter_by(Title=topic, question=question_text).first()
    if q:
        q.flag = not q.flag
        db.session.commit()
        return jsonify({'status': 'toggled'})
    return jsonify({'error': 'Question not found'}), 404

# Create new topic (append)
@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        topic_name = request.form['topic_name'].strip()
        content = request.form['topic_content']
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return "Invalid JSON format", 400

        for item in data:
            q = QuizQuestion(
                Title=topic_name,
                question=item['question'],
                option_a=item['option_a'],
                option_b=item['option_b'],
                option_c=item['option_c'],
                option_d=item['option_d'],
                correct_option=item['correct_option'],
                flag=item.get('flag', False)
            )
            db.session.add(q)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_topic.html')

# Update topic: delete + insert fresh
@app.route('/update_topic', methods=['GET', 'POST'])
def update_topic():
    topics = db.session.query(QuizQuestion.Title).distinct().all()
    topics = [t[0] for t in topics]
    selected_topic = None
    content = None

    if request.method == 'POST':
        if 'topic_content' in request.form and 'topic_name' in request.form:
            selected_topic = request.form['topic_name']
            content = request.form['topic_content']
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                return "Invalid JSON content", 400

            # Delete existing
            QuizQuestion.query.filter_by(Title=selected_topic).delete()
            db.session.commit()

            # Add new records
            for item in data:
                q = QuizQuestion(
                    Title=selected_topic,
                    question=item['question'],
                    option_a=item['option_a'],
                    option_b=item['option_b'],
                    option_c=item['option_c'],
                    option_d=item['option_d'],
                    correct_option=item['correct_option'],
                    flag=item.get('flag', False)
                )
                db.session.add(q)
            db.session.commit()
            return redirect(url_for('index'))

        if 'topic_name' in request.form:
            selected_topic = request.form['topic_name']

    if selected_topic:
        questions = QuizQuestion.query.filter_by(Title=selected_topic).all()
        content = json.dumps([
            {
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option,
                "flag": q.flag
            } for q in questions
        ], indent=4)

    return render_template('update_topic.html', topics=topics, selected_topic=selected_topic, content=content)

@app.route('/delete_topic', methods=['POST'])
def delete_topic():
    data = request.get_json()
    topic = data.get("topic")
    if not topic:
        return "No topic specified", 400

    QuizQuestion.query.filter_by(Title=topic).delete()
    db.session.commit()
    return "Deleted", 200


if __name__ == '__main__':
    app.run(debug=True)
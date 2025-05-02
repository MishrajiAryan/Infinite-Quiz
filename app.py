from flask import Flask, send_from_directory, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join('db', 'quiz.db')

# Serve the index.html from the root directory
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# API to fetch all questions
@app.route('/api/questions')
def get_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, option_a, option_b, option_c, option_d, correct_option, flagged FROM questions')
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({
            'id': row[0],
            'question': row[1],
            'option_a': row[2],
            'option_b': row[3],
            'option_c': row[4],
            'option_d': row[5],
            'correct_option': row[6],
            'flagged': bool(row[7])
        })
    return jsonify(questions)

# API to update flagged status
@app.route('/api/questions/<int:question_id>/flag', methods=['POST'])
def flag_question(question_id):
    data = request.get_json()
    flagged = data.get('flagged', False)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE questions SET flagged = ? WHERE id = ?', (int(flagged), question_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'flagged': flagged})

PORT = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

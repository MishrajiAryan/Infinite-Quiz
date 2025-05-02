import sqlite3

# List of questions to append - replace this list to update questions
questions = [
    {
        "question": "Who founded the Brahmo Samaj?",
        "option_a": "Ram Mohan Roy",
        "option_b": "Swami Vivekananda",
        "option_c": "Gopal Krishna Gokhale",
        "option_d": "Rambai Ranade",
        "correct_option": "A"
    }
    # Add more questions as needed
]

def batch_insert_questions(questions_list):
    conn = sqlite3.connect('db/quiz.db')
    cursor = conn.cursor()
    for q in questions_list:
        cursor.execute(
            "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?)",
            (q['question'], q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct_option'])
        )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    batch_insert_questions(questions)
    print(f"Inserted {len(questions)} questions into the database.")

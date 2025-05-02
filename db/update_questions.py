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
]

def batch_insert_questions(questions_list):
    conn = sqlite3.connect('db/quiz.db')
    cursor = conn.cursor()
    skipped = []

    for q in questions_list:
        # Check for duplicate by question text
        cursor.execute("SELECT COUNT(*) FROM questions WHERE question = ?", (q['question'],))
        count = cursor.fetchone()[0]
        if count > 0:
            skipped.append(q['question'])
            continue
        cursor.execute(
            "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?)",
            (q['question'], q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct_option'])
        )
    conn.commit()
    conn.close()
    return skipped

if __name__ == '__main__':
    skipped = batch_insert_questions(questions)
    if skipped:
        print("Skipped duplicate questions:")
        for s in skipped:
            print("-", s)
    else:
        print(f"Inserted {len(questions)} questions into the database (no duplicates found).")

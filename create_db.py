from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os

# 1. Initialize Flask App and SQLAlchemy
app = Flask(__name__)

# Configure the SQLite database URI
# It will create a 'quiz_database.db' file in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking modifications for better performance

db = SQLAlchemy(app)

# 2. Define the Model (Table Schema)
class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions' # Explicitly set table name

    id = db.Column(db.Integer, primary_key=True) # Primary key is usually good practice
    Title = db.Column(db.String(255)) # The new 'Title' column, String for normal text
    question = db.Column(db.Text, nullable=False) # Text for potentially long questions
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', 'D'
    flag = db.Column(db.Boolean, nullable=False) # Flask-SQLAlchemy handles Boolean directly

    def __repr__(self):
        return f"<QuizQuestion {self.id}: {self.question[:30]}...>"

# 3. Function to Create the Table
def create_quiz_table_flask_sqlalchemy():
    """
    Creates the 'quiz_questions' table using Flask-SQLAlchemy.
    """
    with app.app_context():
        try:
            db.create_all() # This command creates all tables defined in your models
            print("Database table 'quiz_questions' created successfully or already exists.")
        except Exception as e:
            print(f"Error creating database table: {e}")

# 4. Example Usage: Create the table
if __name__ == '__main__':
    # Ensure the database file doesn't exist from a previous run if you want a fresh start
    # os.remove('quiz_database.db') # Uncomment this line to delete the existing DB file before creating

    create_quiz_table_flask_sqlalchemy()

    # Optional: Verify table creation by attempting to add data (not required, but good for testing)
    # from sqlalchemy.exc import IntegrityError
    #
    # with app.app_context():
    #     try:
    #         new_question = QuizQuestion(
    #             Title="Sample Title",
    #             question="What is 2+2?",
    #             option_a="3",
    #             option_b="4",
    #             option_c="5",
    #             option_d="6",
    #             correct_option="B",
    #             flag=False
    #         )
    #         db.session.add(new_question)
    #         db.session.commit()
    #         print("Sample data inserted successfully.")
    #
    #         # Fetch and print to verify
    #         first_question = QuizQuestion.query.first()
    #         if first_question:
    #             print(f"Retrieved: {first_question.question}, Title: {first_question.Title}, Flag: {first_question.flag}")
    #
    #     except IntegrityError:
    #         db.session.rollback() # Rollback on error, e.g., if a NOT NULL constraint is violated
    #         print("Could not insert sample data due to integrity error (e.g., duplicate primary key).")
    #     except Exception as e:
    #         print(f"An error occurred during sample data insertion: {e}")
    #     finally:
    #         # Clean up the sample data if you only wanted to test creation
    #         # If you want to keep it, comment out or remove this block
    #         # if 'new_question' in locals() and new_question.id:
    #         #     db.session.delete(new_question)
    #         #     db.session.commit()
    #         #     print("Sample data rolled back.")
    pass
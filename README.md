# Students CRUD App

## Setup
1. Create database `students_db` in pgAdmin.
2. Run db/schema.sql and db/seed.sql in pgAdmin.
3. Create a .env file using .env.example and fill in your PostgreSQL credentials.

## Run
python3 app/main.py list
python3 app/main.py add FIRST LAST EMAIL YYYY-MM-DD
python3 app/main.py update STUDENT_ID NEW_EMAIL
python3 app/main.py delete STUDENT_ID

## Demo Video
https://youtu.be/ESe7YFnPaBU



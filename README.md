# ImparaC — Educational Web App

This is a small educational web application built with **Flask** and **MongoDB**.  
It allows students to learn basic programming concepts in C through quizzes, theory sections, and progress tracking.

---

## Features
- User profile creation and saving  
- Quizzes divided into three levels: beginner, intermediate, advanced  
- Automatic correction and score calculation  
- Results and errors stored in MongoDB  
- Export results as CSV  
- Simple and responsive user interface  

---

## Technologies Used
- **Python (Flask)** for the web application  
- **HTML / CSS** for the frontend  
- **MongoDB** for data storage  

---

## How to Run the Project

1. **Install dependencies**
   ```bash
   pip install flask pymongo

2. Run the server 
   python app.py 

3. Open th web app
 Open your browser and go to:
 http://127.0.0.1:5000

4. Database Structure
 MongoDB automatically creates two collections:
 utenti: stores user names and course information
 risultati: stores quiz scores and error counts
 You can view the collections using MongoDB Compass or the shell.

Author 
IGNUTI MARA 0124002637
Department of Computer Science
University Project — Educational Web App (Flask + MongoDB)

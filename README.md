# MediMate

**Understand Your Health. Find the Right Care. Keep Your Medical Journey Organized.**

MediMate is a modern healthcare platform that helps patients analyze medical reports, find doctors and hospitals, and maintain their medical history securely.

## Features
- **Medical Report Analysis**: Upload PDF or image reports and get an AI-powered simple explanation of your results, in English and Tamil.
- **Doctor Discovery**: Search for doctors based on specialization, location, and hospital.
- **Hospital Discovery**: Find nearby hospitals, view available services and departments.
- **Medical History & Documents**: Securely store and organize your medical timeline and past documents.

## Architecture & Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript.
- **Backend**: Python, FastAPI.
- **Database**: PostgreSQL with SQLAlchemy.
- **AI Integration**: Google Gemini API for report analysis and summarization.

## Setup Instructions
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file based on `.env.example` and fill in your database and API credentials.
4. Run the database migrations or setup script to initialize tables.
5. Start the backend: `uvicorn backend.main:app --reload`.
6. Open `frontend/index.html` in your browser.

*Note: MediMate is for educational purposes and is not a substitute for professional medical advice.*
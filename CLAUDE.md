# NeuroFit AI — Project Context for Claude Code

## What is NeuroFit AI?
A Production AI/ML SaaS fitness app built with FastAPI, PostgreSQL, Streamlit, Docker, and AWS EC2.
Users can signup, create fitness profiles, get ML predictions, AI meal plans, AI chatbot, and download PDF reports.

## Developer
- Name: Ahmad
- GitHub: https://github.com/Ahmad-0925/neurofit-ai
- Goal: Build portfolio project to get AI/ML Engineer / Data Scientist job

## Tech Stack
- Backend: FastAPI + SQLAlchemy + PostgreSQL + Alembic
- Frontend: Streamlit
- ML: scikit-learn + XGBoost + SHAP + MLflow
- AI: DeepSeek API
- Auth: JWT (python-jose + passlib + bcrypt)
- DevOps: Docker + docker-compose + GitHub Actions + AWS EC2
- PDF: fpdf2
- Rate limiting: slowapi

## Project Structure
```
neurofit-ai/
├── env/                         # virtual environment
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── alembic/                 # database migrations
│   ├── alembic.ini              # alembic config
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py              # signup + login endpoints
│   │   └── profile.py           # profile CRUD endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # pydantic settings + env vars
│   │   ├── database.py          # SQLAlchemy engine + session + Base
│   │   └── security.py          # JWT + bcrypt + get_current_user
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py            # SQLAlchemy table models
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── user_schema.py       # UserCreate, UserLogin, UserResponse
│   │   └── profile_schema.py    # ProfileCreate, ProfileUpdate, ProfileResponse
│   └── services/
│       ├── __init__.py
│       ├── calculation.py       # BMI, TDEE, height conversion
│       └── profile_service.py   # profile CRUD business logic
├── frontend/                    # Streamlit app (not built yet)
├── ml/                          # ML models + notebooks (not built yet)
├── docker/                      # Dockerfiles (not built yet)
├── .env                         # secrets (never commit to GitHub)
├── .gitignore
└── CLAUDE.md                    # this file

```

## Database Tables (PostgreSQL — db: neurofit)
1. **users** — id, name, email, hashed_password, created_at
2. **fitness_profiles** — id, user_id(FK), age, weight, height, gender, goal, activity_level, bmi, tdee
3. **ml_predictions** — id, user_id(FK), model_name, input_data, output_data, timestamp
4. **ai_chats** — id, user_id(FK), message, response, timestamp

## Environment Variables (.env)
```
DATABASE_URL=postgresql://postgres:Ahmad786g%40@localhost:5432/neurofit
SECRET_KEY=mysecretkey123456789
```

## How to Run Locally
```bash
cd neurofit-ai
env\Scripts\activate
cd backend
python -m uvicorn main:app --reload
# open http://127.0.0.1:8000/docs
```

## Auth Flow
- POST /auth/signup → hash password → save user → return JWT token
- POST /auth/login → verify password → return JWT token
- All protected endpoints use Depends(get_current_user)
- get_current_user reads HTTPBearer token → decodes JWT → returns user object
- Token expires in 30 minutes

## Calculations (services/calculation.py)
- BMI = weight(kg) / height(m)²
- BMR (Mifflin-St Jeor):
  - Male: 10×weight + 6.25×height - 5×age + 5
  - Female: 10×weight + 6.25×height - 5×age - 161
- TDEE = BMR × activity factor
  - sedentary=1.2, light=1.375, moderate=1.55, active=1.725
- Height input: feet + inches → converted to cm

## Progress Completed
### Day 1 ✅
- Project structure + GitHub setup
- Virtual environment
- PostgreSQL connected
- 4 database tables created
- Alembic migrations configured
- JWT Authentication (signup + login working)
- get_current_user security guard
- Tested in Swagger

### Day 2 ✅
- Pydantic schemas (UserCreate, UserLogin, ProfileCreate, ProfileUpdate, ProfileResponse)
- BMI + TDEE calculations
- Height conversion (feet/inches to cm)
- Profile CRUD (Create, Read, Update, Delete) — all tested and working
- Services layer (clean architecture)
- Pushed to GitHub

## What's Next (Day 3+)
### Day 3 — Streamlit Frontend
- Login + signup pages
- Sidebar navigation
- Profile form with BMI/TDEE display
- Dashboard page

### Day 4 — ML Models
- Download datasets from Kaggle
- EDA + feature engineering
- Model 1: Body type prediction (RandomForestClassifier)
- Model 2: Calorie prediction (RandomForestRegressor)
- Save as .pkl files + MLflow tracking

### Day 5 — Model 3 + SHAP + MLflow
- Weight progress prediction (XGBoost)
- SHAP explainability for all models
- MLflow experiment tracking

### Day 6 — ML API Endpoints
- /predict/body-type
- /predict/calories
- /predict/weight-progress
- /recommend/workout
- Save predictions to DB

### Day 7 — Streamlit ML Dashboard
- Prediction forms + results
- SHAP charts
- Workout recommendations
- Prediction history

### Day 8 — Buffer day
- Fix bugs, clean code, push

### Day 9 — DeepSeek AI
- Meal planner endpoint
- Workout generator endpoint

### Day 10 — Streaming Chatbot
- FastAPI StreamingResponse
- Chat history in DB
- Rate limiting (10 calls/day)
- Logging system

### Day 11 — PDF Reports + UI Polish
- fpdf2 PDF generation
- Download endpoint
- Full Streamlit UI polish

### Day 12 — Docker
- Backend + Frontend Dockerfiles
- docker-compose with PostgreSQL
- Push to Docker Hub

### Day 13 — GitHub Actions CI/CD
- CI pipeline (test on PR)
- CD pipeline (auto deploy on push to main)

### Day 14 — AWS EC2 Deployment
- Launch EC2 t2.micro
- Install Docker on EC2
- Deploy with docker-compose
- Production hardening

### Day 15 — Portfolio
- README with architecture diagram
- Demo video
- LinkedIn post
- Update CV

## Key Decisions Made
- Using HTTPBearer instead of OAuth2PasswordBearer (cleaner Swagger UI)
- Height input in feet/inches (more user friendly for Pakistani users)
- bcrypt==4.0.1 (newer versions have compatibility issues with passlib)
- python:3.11-slim for Docker (smaller image size)
- Render for deployment if AWS card not available
- DeepSeek AI instead of OpenAI (cheaper, same API format)

## Important Notes
- Always run server from inside backend/ folder: cd backend → python -m uvicorn main:app --reload
- Virtual env activation: env\Scripts\activate (from neurofit-ai root)
- bcrypt must be version 4.0.1 — newer versions break passlib
- alembic.ini password uses %%40 for @ symbol in .ini files
- .env uses %40 for @ symbol in URLs
- Token expires in 30 min — re-login if getting 401 errors

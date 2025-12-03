# Citizen Wellness Portal

A Streamlit-based web application for citizen registration, authentication, and dashboard management.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv env
```

### 2. Activate the Virtual Environment

**On Linux/Mac:**
```bash
source env/bin/activate
```

**On Windows:**
```bash
env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

## Features

- User registration with validation
- Secure login system
- Personalized dashboard with metrics
- Session management

## Usage

1. **Register**: Create a new account with a username and password (minimum 4 characters)
2. **Login**: Access your dashboard with your credentials
3. **Dashboard**: View your citizen metrics and clearance information
4. **Logout**: Safely end your session

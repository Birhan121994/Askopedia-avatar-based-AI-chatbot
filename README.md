# 🤖 Askopedia – Avatar-Based AI Chatbot

> An AI-powered conversational chatbot with an avatar-based interface for interactive, engaging, and accessible question-answering experiences.

---

## 📖 Overview

**Askopedia** is an AI-powered conversational chatbot designed to provide users with an interactive and engaging way to ask questions and receive intelligent responses through an avatar-based interface.

The project combines **conversational AI**, **web technologies**, and **text-to-speech capabilities** to create a more human-like interaction experience. Instead of interacting with a traditional text-only chatbot, users can communicate with an AI assistant through a visual avatar, making the experience more interactive and accessible.

---

## 🚀 Project Overview

Askopedia aims to make information access easier through an intelligent virtual assistant. Users can ask questions and interact with the chatbot through a web-based interface.

The application uses **Django** as its backend framework and integrates Python-based libraries for HTTP requests and speech generation.

---

## ✨ Key Features

- 🧠 **AI-Powered Conversations** — Enables users to interact with an AI chatbot and receive responses to their questions.
- 🧑‍💼 **Avatar-Based Interaction** — Provides a visual avatar-based chatbot experience.
- 🔊 **Text-to-Speech** — Supports speech generation to make chatbot interactions more engaging.
- 🌐 **Interactive Web Interface** — Provides a browser-based environment for interacting with the chatbot.
- ⚙️ **Backend Integration** — Uses Django to handle application logic and backend functionality.
- 🗣️ **Speech Generation Support** — Integrates Edge TTS and Google Text-to-Speech libraries.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Django 4.2.7** | Backend web framework |
| **HTML, CSS, JavaScript** | Frontend development |
| **Requests** | HTTP communication and API integration |
| **Edge TTS** | Text-to-speech generation |
| **gTTS** | Google Text-to-Speech |
| **Python-dotenv** | Environment variable management |
| **SQLite** | Database |
| **Gunicorn** | Production WSGI server |
| **WhiteNoise** | Static file serving |

---

## 🏗️ Project Structure

```text
Askopedia-avatar-based-AI-chatbot/
│
├── askopedia/          # Main Django application
├── core/               # Core application components
├── static/             # Static assets
├── staticfiles/        # Collected static files
├── templates/          # HTML templates
│
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment configuration
├── runtime.txt         # Python runtime configuration
└── .gitignore
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/Birhan121994/Askopedia-avatar-based-AI-chatbot.git
```

### 2. Navigate to the project directory

```bash
cd Askopedia-avatar-based-AI-chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```
### 5. Configure environment variables

Create a `.env` file in the project root and add any required API credentials or configuration values used by the application.

```env
# Example .env file
SECRET_KEY=your_secret_key
DEBUG=True
# Add any API keys or configuration values required by the application
```
### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```
### 8. Access the application

Open your browser and navigate to:

```text
http://127.0.0.1:8000/
```
## 🎯 Project Objectives

The main objectives of Askopedia are:

- 🔍 To explore the integration of artificial intelligence into web-based applications.
- 💬 To develop an interactive chatbot that improves the traditional text-based conversation experience.
- 🧑‍💼 To integrate avatar-based interaction into conversational AI.
- 🔊 To explore speech synthesis technologies for more accessible human-computer interaction.
- 🐍 To demonstrate the development of an AI-powered application using Django and Python.

---

## 🔮 Future Improvements

Potential improvements include:

- 🎞️ Real-time avatar animation and lip synchronization.
- 🎙️ Speech-to-text functionality for voice-based questions.
- 🧠 Improved conversational memory and contextual understanding.
- 🌍 Multilingual conversational support.
- 🎨 Enhanced user interface and responsive design.
- 🔐 User authentication and personalized conversation history.

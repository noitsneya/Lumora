# Lumora – AI-Powered Memory Assistant
Lumora is an AI-powered memory companion designed to assist dementia patients with daily routines, memory recall, and emotional well-being. It provides a personalized, conversational experience that adapts and learns over time, while also offering caretakers a dashboard for oversight and support.

# Features & Scope
## Memory Log (Personalized Recall System)
    Helps patients recall important events, people, and conversations.
    Caretakers can add or edit memory logs with text and images.
    Patients can ask questions like "What did I do yesterday?" and Lumora provides contextual recall.
## Routine & Task Management
    Custom reminders for medications, meals, and daily tasks.
    AI-driven voice prompts to guide patients.
    Caretakers can track missed tasks and adjust routines.
## Adaptive Conversational AI
    Learns from interactions and adjusts responses accordingly.
    Remembers preferences, relationships, and recurring topics.
    Provides a more human-like and empathetic experience.
## Mood Forecast & Emotional Support
    Daily mood check-ins to assess well-being.
    AI suggests activities, calming techniques, or familiar stories.
    Caretakers receive mood analytics and trends for better support.
## Caretaker Dashboard & Oversight
    View daily activity logs, routines, and emotional trends.
    Add memories, photos, and personal notes to assist recall.
    Monitor adherence to tasks and receive alerts.
# Tech Stack
## Component	Tech Stack
    Frontend	Next.js (React), Tailwind CSS
    Backend	Firebase (Auth, Realtime DB), PostgreSQL
    AI/NLP	Google Gemini API (Conversational AI), OpenAI Whisper (Speech)
    Voice UI	Web Speech API (for voice interactions)
    Hosting	Vercel (Web), Firebase Functions
    Authentication	Firebase Auth (Caretaker-Patient linking)
# Getting Started
## 1. Clone the Repository
    git clone https://github.com/noitsneya/Lumora.git
    cd Lumora
## 2. Install Dependencies
    npm install
## 3. Start Development Server

    npm run dev
## 4. Environment Variables
Set up .env.local with necessary API keys:

    NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key_here
    NEXT_PUBLIC_GEMINI_API_KEY=your_api_key_here
# Roadmap
Phase 1 – Set up project structure and authentication.

Phase 2 – Implement memory log and conversational AI.

Phase 3 – Develop caretaker dashboard and routines.

Phase 4 – Fine-tune voice UI and personalize interactions.
# Contributing
We welcome contributions! Feel free to fork, submit pull requests, or discuss ideas in issues.

License
MIT License – Free to modify and build upon.

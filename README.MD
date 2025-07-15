Reddit User Persona Generator
This project takes a Reddit username, scrapes their public posts and comments, and generates a detailed user persona using Groq's LLaMA3 model. It includes traits, interests, tone, and behavioral cues — all backed by citations from Reddit content.

Built using:

Groq API (LLaMA3-8B)

 PRAW (Python Reddit API Wrapper)

 Streamlit (UI)

 .env for secure credentials

Features
Input any Reddit username

 Scrapes latest posts and comments

 Generates structured user persona with citations

 Saves output to .txt

 One-click download from UI

 ###folder structure

 RedditPersonaGroq/
│
├── .env                      # Credentials file (not uploaded)
├── streamlit_app.py          # Main Streamlit app
├── requirements.txt          # Python dependencies
├── kojied_persona.txt        # Example output
└── README.md                 # This file

Instrucations

pip install -r requirements.txt


 Create a .env File
 Add your API credentials in .env:

REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_app_name

GROQ_API_KEY=your_groq_api_key


to run write:
 streamlit run app.py







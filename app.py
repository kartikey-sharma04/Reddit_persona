import os
import praw
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def fetch_reddit_data(username, limit=30):
    user = reddit.redditor(username)
    posts, comments = [], []

    try:
        for post in user.submissions.new(limit=limit):
            posts.append(f"[POST] {post.title}\n{post.selftext}\nURL: {post.url}")
        for comment in user.comments.new(limit=limit):
            comments.append(f"[COMMENT] {comment.body}")
    except Exception as e:
        st.error(f" Error while fetching Reddit data: {e}")
    return posts, comments


def generate_persona(posts, comments):
    prompt = f"""
You are an expert personality profiler.

Based on the Reddit user's posts and comments, generate a structured persona.

Include:
- Personality traits
- Interests and hobbies
- Beliefs or values
- Writing tone or style

For each point, cite the content using [SOURCE: ...].

== POSTS ==
{chr(10).join(posts)}

== COMMENTS ==
{chr(10).join(comments)}
"""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def save_persona_to_file(username, persona_text):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    return filename

st.set_page_config(page_title="Reddit User Profiler")
st.title("Reddit User Persona Generator (Groq + Streamlit)")

username = st.text_input("Enter Reddit username (just the name, no URL):")

if st.button("Generate Persona"):
    if not username:
        st.warning("Please enter a username.")
    else:
        with st.spinner("Scraping Reddit..."):
            posts, comments = fetch_reddit_data(username)

        if not posts and not comments:
            st.error("No content found for this user.")
        else:
            with st.spinner("Generating persona using Groq..."):
                persona = generate_persona(posts, comments)

            st.success("Persona generated!")
            st.text_area("Persona:", value=persona, height=500)

            file_path = save_persona_to_file(username, persona)
            st.download_button(
                label="Download Persona as TXT",
                data=persona,
                file_name=file_path,
                mime="text/plain"
            )

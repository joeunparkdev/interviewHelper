import streamlit as st
# import openai
import os

# Set OpenAI API key
# openai.api_key = st.secrets["openai"]["api_key"]

# response = openai.Completion.create(
#     model="gpt-3.5-turbo",
#     prompt="Translate the following English text to French: 'Hello, how are you?'",
#     max_tokens=60
# )
# print(response['choices'][0]['message']['content'].strip())

# Title and introduction
st.title("Interview Helper")
st.write("Welcome to the Interview Helper App! Use this app to prepare for your interviews.")

# Sidebar for navigation
st.sidebar.title("Interview Sections")
section = st.sidebar.selectbox("Choose the section", ["Behavioral", "Technical", "HR", "Case Studies"])

# Questions and example answers for each section
questions_answers = {
    "Behavioral": [
        "Tell me about a time you faced a significant challenge.",
        "How do you handle stress and pressure?",
        "Describe a time when you had to work as part of a team."
    ],
    "Technical": [
        "Explain the concept of OOP.",
        "What is a linked list?",
        "How do you manage memory in Python?"
    ],
    "HR": [
        "Why do you want to work here?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in 5 years?"
    ],
    "Case Studies": [
        "How would you approach solving a major problem at our company?",
        "Describe a case where you improved a process.",
        "What strategies would you use to increase our market share?"
    ]
}

# Function to get a response from OpenAI
def get_openai_response(question, user_answer):
    prompt = f"Interview question: {question}\n\nUser answer: {user_answer}\n\nProvide feedback on the user's answer and give an example answer:"
    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[
            {"role": "system", "content": "You are an interview coach."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Practice section
st.header("Practice Your Answers")
if section in questions_answers:
    practice_question = st.selectbox("Select a question to practice", questions_answers[section])
    user_answer = st.text_area("Your Answer")
    if st.button("Submit"):
        with st.spinner("Evaluating your answer..."):
            ai_response = get_openai_response(practice_question, user_answer)
            st.write("Thank you for your answer! Here's the feedback and an example answer from the AI:")
            st.write(f"{ai_response}")
            st.write("Remember to be concise and to the point.")

# Chat-like interface for interview practice
st.header("AI-Powered Interview Chat At This Point Unavailable")
chat_history = st.session_state.get('chat_history', [])

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(f"You: {user_input}")
        with st.spinner("AI is thinking..."):
            ai_response = openai.ChatCompletion.create(
                model="text-davinci-003",
                messages=[
                    {"role": "system", "content": "You are an interview coach."},
                    *[{"role": "user", "content": message.split(": ", 1)[1]} if message.startswith("You:") else {"role": "assistant", "content": message.split(": ", 1)[1]} for message in st.session_state.chat_history],
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                stop=["\n", " You:", " AI:"]
            ).choices[0].message['content'].strip()
            st.session_state.chat_history.append(f"AI: {ai_response}")
            user_input = ""

# Display chat history
for message in st.session_state.chat_history:
    st.write(message)

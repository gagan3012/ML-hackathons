import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

st.sidebar.image("images/DSC University of British Columbia  Light Vertical-Logo.png", width=300, height=500)

st.sidebar.header("""
© ML Workshop By DSC UBC
""")
st.sidebar.markdown(
    "This app allows users to input text of their choice using the tools provided, and ask questions with the answer "
    "being extracted from the text.")
st.sidebar.markdown(
    "_When running the app the first time, it may take some time to initialise due to the requirements needing to be "
    "downloaded._")
tool = st.sidebar.selectbox("Tool", ["Website Q&A", "Sentiment Analysis", "Text Generation", "Summary Generation"])


@st.cache(suppress_st_warning=True)
def generateAnswer(question, context):
    nlp = pipeline("question-answering")
    answer = nlp(question=question, context=context)
    return answer


@st.cache(suppress_st_warning=True)
def generatesentiment(text):
    nlp = pipeline('sentiment-analysis')
    answer = nlp(text)
    return answer


@st.cache(suppress_st_warning=True)
def generatetext(starting_text):
    gpt2 = pipeline('text-generation')
    answer = gpt2(starting_text, max_length=50, num_return_sequences=2)
    return answer


@st.cache(suppress_st_warning=True)
def generatesummary(text):
    summarizer = pipeline("summarization")
    answer = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return answer


def sentiment():
    st.write("# What sentence describes your mood?")
    user_input = st.text_input("Enter Text")

    if st.button('Get my mood'):
        answer = generate_sentiment(user_input)
        st.header("Answer")
        if answer[0]["label"] == "POSITIVE":
            st.write("You seem to be in a great mood! Go gettem king")
        else:
            st.write("Your mood doesn't seem so great right now.. but don't worry! Your future is bright")


def text():
    st.write("# Help Me Write My Essay")
    user_input = st.text_input("Enter what you've already written")

    if st.button('Finish my essay'):
        answer = generate_text(user_input)
        st.header("Answer")
        st.write(answer[0]["generated_text"])
        st.write(answer[1]["generated_text"])


def summary():
    st.write("# Help Me Summarize A Passage")
    user_input = st.text_area("Enter passage")

    if st.button('Get summary'):
        answer = generate_summary(user_input)
        st.header("Answer")
        st.write(answer[0]["summary_text"])


def wiki_answers():
    st.write("# Wikipedia Answers")
    question = st.text_input("Question:")

    if st.button("Get Answer"):
        url = get_wiki_url(question)
        scraped_data = requests.get(url)
        article = scraped_data.text
        parsed_article = BeautifulSoup(article, 'lxml')
        paragraphs = parsed_article.find_all('p')
        article_text = ""
        for p in paragraphs:
            article_text += p.text

    if st.button('Get Text Answer'):
        answer = generatetext(user_input)
        st.header("Answer")
        st.write(answer)


def summary():
    st.write("# Summary Generation")
    user_input = st.text_area("Enter Text",value="")

    if st.button('Get Sentiment'):
        answer = generatesummary(user_input)
        st.header("Answer")
        st.write(answer)


if tool == "Website Q&A":
    website_qna()

if tool == "Sentiment Analysis":
    sentiment()

if tool == "Text Generation":
    text()

if tool == "Summary Generation":
    summary()
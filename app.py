import streamlit as st
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator


# Load the model and vectorizer
vectorizer = joblib.load("vectorizer.jbl")
model = joblib.load("model.pkl")

def detect_language(text):
    tran_text = vectorizer.transform([text])
    predicted_language = model.predict(tran_text)[0]
    return predicted_language

# Streamlit app with styling and effects
def main():
    # HTML and CSS style
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to bottom right, #ffffff, #ccddeeff);
            padding: 20px;
        }
        .title {
            font-size: 2rem;
            font-weight: lighter;
            text-align: center;
            margin-bottom: 30px;
        }
        .detected-language {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .detected-language:hover {
            font-weight: bold;
            color: #1E90FF;
        }
        .detected-language-greek {
            font-weight: bold;
        }
        .button:hover {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🔍 Language Detection")
    st.write("Enter text below to detect its language:")

    # Input text area
    user_input = st.text_area("Input Text:", "Hello, how are you?", height=150)

    # Detect language button
    if st.button("Detect Language", help="Click to detect language"):
        if user_input:
            detected_language = detect_language(user_input)
            # Apply bold style if detected language is Greek
            if detected_language.lower() == 'greek':
                st.write(f"Detected Language: <span class='detected-language detected-language-greek'>{detected_language.capitalize()}</span>", 
                         unsafe_allow_html=True,
                         key='detected_language_output',
                         )
            else:
                st.write(f"Detected Language: <span class='detected-language'>{detected_language.capitalize()}</span>", 
                         unsafe_allow_html=True,
                         key='detected_language_output',
                         )
        else:
            st.warning("Please enter some text.")

    # Language translation section
    if st.checkbox("Translate Detected Text", help="Check to translate detected text"):
        if user_input:
            text_to_translate = user_input
            languages = ['English', 'Malayalam', 'Hindi', 'Tamil', 'Portugeese', 'French',
                         'Dutch', 'Spanish', 'Greek', 'Russian', 'Danish', 'Italian',
                         'Turkish', 'Swedish', 'Arabic', 'German', 'Kannada']
            selected_language = st.selectbox("Select Language to Translate:", languages, help="Select language to translate to")

            if st.button("Translate", help="Click to translate text"):
                translator = Translator()
                translated_text = translator.translate(text_to_translate, dest=selected_language).text
                st.write(f"Translated Text ({selected_language}):")
                st.write(translated_text)
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()

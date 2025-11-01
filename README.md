WhatsApp Chat Analyzer is a Streamlit-based web app that helps you explore and understand your WhatsApp conversations. By uploading a .txt file exported from WhatsApp (without media), the app reveals patterns in messaging behavior, emoji usage, sentiment, and more. It’s designed to be simple, insightful, and emoji-friendly — perfect for personal reflection or group analysis.
 
 Once you upload your chat file, the app displays a preview of your messages at the top. You can filter by date range and choose to analyze either the entire group or a specific participant. The app then shows key 
 
 statistics like total messages, word count, media shared, and links sent. It also visualizes daily and monthly activity trends, highlights the most active users and days, and generates a word cloud of frequently used terms.

One of the standout features is emoji analysis. The app extracts all emojis used in the chat, displays their frequency, and visualizes the top ones in a pie chart. It also groups emojis by emotion (happy, sad, angry, annoyed) and shows how often each type appears. Sentiment analysis is included too, using VADER to classify messages as positive, negative, or neutral.

To run the app locally, clone the repository, install the required Python libraries, and launch it with Streamlit. You’ll also need to download the VADER lexicon from NLTK for sentiment analysis. The app is lightweight, easy to deploy, and works well on both desktop and cloud platforms.

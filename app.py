import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors="ignore")
    df = preprocessor.preprocess(data)

    df['only_date'] = pd.to_datetime(df['only_date'])

    st.sidebar.subheader("Filter by Date Range")
    start_date = st.sidebar.date_input("Start Date", df['only_date'].min().date())
    end_date = st.sidebar.date_input("End Date", df['only_date'].max().date())
    df = df[(df['only_date'].dt.date >= start_date) & (df['only_date'].dt.date <= end_date)]

    st.markdown(f"**Analyzing messages from {start_date} to {end_date}**")
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Top statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        time_line = helper.monthly_time_line(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time_line['time'], time_line['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        # Busiest user
        if selected_user == 'overall':
            st.title("Most Busy User")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.subheader("Download Word Frequency Data")
        word_csv = most_common_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Word Data as CSV", word_csv, "word_frequency.csv", "text/csv")

        # ✅ Emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        st.subheader("All Emojis Used in Chat")
        st.dataframe(emoji_df)

        st.subheader("Top 5 Emojis (Pie Chart)")
        if not emoji_df.empty:
            try:
                fig, ax = plt.subplots()
                labels = [str(e) for e in emoji_df['emoji'].head()]
                sizes = emoji_df['count'].head().tolist()
                ax.pie(sizes, labels=labels, autopct="%0.2f")
                st.pyplot(fig)
            except:
                st.warning("Pie chart failed to render emojis. Showing bar chart instead.")
                fig, ax = plt.subplots()
                ax.barh(emoji_df['emoji'].head(), emoji_df['count'].head(), color='skyblue')
                st.pyplot(fig)
        else:
            st.info("No emojis found in this chat.")

        st.subheader("Download Emoji Usage Data")
        emoji_csv = emoji_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Emoji Data as CSV", emoji_csv, "emoji_usage.csv", "text/csv")

        # ✅ Emoji emotion summary
        st.title("Emoji Emotion Summary")
        emotion_df = helper.emoji_emotion_summary(selected_user, df)
        st.dataframe(emotion_df)

        fig, ax = plt.subplots()
        ax.bar(emotion_df['emotion'], emotion_df['count'], color=['green', 'blue', 'red', 'orange'])
        st.pyplot(fig)

        # ✅ Sentiment analysis
        st.title("Sentiment Analysis")
        sentiment_df = helper.sentiment_analysis(selected_user, df)
        st.dataframe(sentiment_df)

        fig, ax = plt.subplots()
        ax.pie(sentiment_df['messages'], labels=sentiment_df['sentiment'], autopct="%0.2f")
        st.pyplot(fig)

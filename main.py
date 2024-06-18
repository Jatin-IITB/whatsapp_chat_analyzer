import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analzser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocess.preprocess(data)

    #fetch unique users
    user_list= df['user'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis WRT",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with(col1):
            st.header("Total Messages")
            st.title(num_messages)
        with(col2):
            st.header("Total Words")
            st.title(words)
        with(col3):
            st.header("Total Media Messages")
            st.title(num_media)
        with(col4):
            st.header("Total Links")
            st.title(num_links)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,ne_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
               st.dataframe(ne_df)

        # Monthly timeline analysis
        timeline = helper.monthly_analysis(selected_user,df)
        timeline['time'] = pd.to_datetime(timeline['time'], format='%B-%Y')
        # Convert 'time' and 'message' columns to numpy arrays
        time_array = timeline['time'].to_numpy()
        message_array = timeline['message'].to_numpy()
        # fig,ax = plt.subplots()
        # ax.plot(time_array,message_array)
        fig, ax = plt.subplots()
        ax.plot(time_array, message_array, marker='o',color='black')
        # Set labels and title
        ax.set_xlabel('Time')
        ax.set_ylabel('Message Count')
        ax.set_title('Monthly Timeline')
        # Rotate x-axis labels and adjust layout
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        # Display the plot in Streamlit
        st.pyplot(fig)

        st.title("Daily Analysis")
        daily_timeline = helper.daily_analysis(selected_user, df)
        daily_timeline['time'] = pd.to_datetime(timeline['time'], format='%B-%Y')
        time_array_1 = daily_timeline['only_date'].to_numpy()
        message_array_1= daily_timeline['message'].to_numpy()
        fig, ax = plt.subplots()
        ax.plot(time_array_1, message_array_1, marker='*')
        # Set labels and title
        ax.set_xlabel('Time')
        ax.set_ylabel('Message Count')
        ax.set_title('Daily Timeline')
        # Rotate x-axis labels and adjust layout
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        # Display the plot in Streamlit
        st.pyplot(fig)

        #activity Map

        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            # Call the helper function to get the busy_day data
            busy_day = helper.weekly_analysis(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            # Set labels and title
            ax.set_xlabel('Day of the Week')
            ax.set_ylabel('Message Count')
            ax.set_title('Weekly Timeline')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Months")
            # Call the helper function to get the busy_day data
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            # Set labels and title
            ax.set_xlabel('Months')
            ax.set_ylabel('Message Count')
            ax.set_title('Monthly Timeline')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(fig)
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.title("WordCloud")
        df_wc = helper.create_worldcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('----------------Most Common Words-----------------------')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        df_emoji = helper.emoji_analysis(selected_user, df)
        df_emoji_top5 = df_emoji.head(5)
        st.title("------------Emoji Analysis----------")
        col1, col2 = st.columns(2)

        # with col1:
        #     st.dataframe(df_emoji)

        with col1:
            fig1, ax1 = plt.subplots()
            ax1.pie(df_emoji_top5['count'], labels=df_emoji_top5['emoji'], autopct='%0.2f%%')
            st.pyplot(fig1)






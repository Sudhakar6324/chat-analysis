import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

#to upload the file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)
        
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links shared")
            st.title(num_links)    

        #finding the busiest users in the group(group level)
        if selected_user =='overall':
            st.title('Most Busy users')
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title('% of users_chat')
            st.dataframe(new_df)

    #WordCloud
    st.title('Word_cloud')
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    
    #most common words
    most_common_df = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)
    st.dataframe(most_common_df)
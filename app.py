import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

GA_SCRIPT = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QNHC9ESRHD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-QNHC9ESRHD');
</script>
"""

# Inject the script (use a small nonzero height so it runs)
st.components.v1.html(GA_SCRIPT, height=1, width=1)



st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    user_list=df['user'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        st.title('Whatsapp chat in-depth analysis')
        st.title('Top Statistics')
        col1,col2,col3,col4 =st.columns(4)
        with  col1:
            st.header("Total Messages")
            st.title(num_messages)
        with  col2:
            st.header("Total Words")
            st.title(words)
        with  col3:
            st.header("Total Media Files Shared")
            st.title(num_media_messages)
        with  col4:
            st.header("Total Hyperlinks Shared")
            st.title(links)



        #monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'], timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #most busy users
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(selected_user,df)
            fig, ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        #wordcloud
        st.title('Wordcloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        if most_common_df.shape[0]>0:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.title('Most Common Words')
            st.pyplot(fig)
        else:
            st.header("No words has been sent")

        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            if emoji_df.shape[0] > 0:
                st.dataframe(emoji_df)
        with col2:
            if emoji_df.shape[0]>0:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
                st.pyplot(fig)
            else:
                st.header("No emoji has been sent")

        st.text('*** Created by Aalekh vishwakarma as ml project ***')


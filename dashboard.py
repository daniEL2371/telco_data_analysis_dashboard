import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px


import os
import sys

cleaned_data_csv = "./Data/cleaned_data.csv"
user_engagement_csv = "./Data/user_engagement.csv"
user_experience_metrics_csv = "./Data/user_experience_metrics.csv"



def top_handset_type(df, top=5):

        return df['handset_type'].value_counts().head(top)

def top_manufacturer(df, top=5):
        
        return df['handset_manufacturer'].value_counts().head(top)
    
def top_handset_by_manufacturer(df, manufacturer, top=5):
        
        return df.groupby('handset_manufacturer')['handset_type'].value_counts()[manufacturer].head(top)




st.set_page_config(page_title="Telecom Data Analysis", layout="wide")


def read_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print("file read as csv")
        return df
    except FileNotFoundError:
        print("file not found")



class Dashboard:

    def __init__(self, title: str) -> None:
        self.title = title
        self.page = None
        self.df: pd.DataFrame = self.load_data(
            cleaned_data_csv).copy(deep=True)
        self.engagement_df: pd.DataFrame = self.load_data(
            user_engagement_csv).copy(deep=True)
        self.experience_df: pd.DataFrame = self.load_data(
            user_experience_metrics_csv).copy(deep=True)

        self.engagement_df['msisdn'] = self.engagement_df['msisdn'].astype(
            "int")
        self.engagement_df['msisdn'] = self.engagement_df['msisdn'].astype(
            "str")

        self.experience_df['msisdn'] = self.experience_df['msisdn'].astype(
            "int")
        self.experience_df['msisdn'] = self.experience_df['msisdn'].astype(
            "str")



    @st.cache()
    def load_data(self, path):
        print("Data loaded")
        return read_csv(path)

    def barChart(self, data, X, Y):

        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q"))
        st.altair_chart(msgChart, use_container_width=True)

    def render_siderbar(self, pages, select_label):
        st.sidebar.markdown("# Pages")
        self.page = st.sidebar.selectbox(f'{select_label}', pages)

    # def render_top_authors(self):
    #     st.markdown("### **Top authors**")

    #     plcae_filters = st.multiselect(
    #         label="Select location to include", options=self.df['place'].unique(), key="author_places")

    #     top = st.number_input(label="Top", step=1, value=5, key="top_authors")

    #     df_res = self.tweeterDataExplorator.authors(
    #         top=int(top), places=plcae_filters)

    #     st.bar_chart(data=df_res, width=0, height=0,
    #                  use_container_width=True)

    # def render_top_hashtags(self):
    #     st.markdown("### **Top hashtags** ")

    #     plcae_filters = st.multiselect(
    #         label="Select location to include", options=self.df['place'].unique())

    #     top = st.number_input(label="Top", step=1, value=5, key="top_hashtags")
    #     df_res = self.tweeterDataExplorator.most_used_hash_tag(
    #         top=int(top), places=plcae_filters)

    #     st.bar_chart(data=df_res, width=0, height=0,
    #                  use_container_width=True)

    # def render_polarity(self):
    #     st.markdown("### **Polarity score**")

    #     plcae_filters = st.multiselect(
    #         label="Select location to include", options=self.df['place'].unique(), key="polarity_places")
    #     df = self.tweeterDataExplorator.get_polarities_count(
    #         places=plcae_filters)
        
    #     fig = px.pie(df, values="Count",
    #                  names="Polarity", width=500, height=400)
    #     fig.update_traces(textposition='inside', textinfo='percent+label')

    #     st.plotly_chart(fig)

    # def render_polarity_vs_retweet_count(self):
    #     chart_df = pd.DataFrame(columns=["polarity", "retweet_count"])

    #     chart_df['polarity'] = self.df['polarity']
    #     chart_df['retweet_count'] = self.df['retweet_count']

    #     # st.line_chart(chart_df)
    #     pass

    # def render_visulazation(self):
    #     self.render_top_hashtags()
    #     self.render_top_authors()
    #     self.render_polarity()
    #     self.render_word_cloud()
    #     self.render_polarity_vs_retweet_count()

    # def render_word_cloud(self):
    #     st.markdown("## **Tweet Text Word Cloud**")

    #     authors = places = polarity_score = []

    #     filter_mtd = st.selectbox(label="select filter method", options=[
    #                               "Location", "Authors", "Polarity Score"])

    #     if (filter_mtd and filter_mtd == "Location"):
    #         places = st.multiselect(
    #             label="Location", options=self.df['place'].unique(), key="plcae_wc")
    #     if (filter_mtd and filter_mtd == "Authors"):
    #         authors = st.multiselect(
    #             label="Authors", options=self.df['original_author'].unique(), key="authros_wc")
    #     if (filter_mtd and filter_mtd == "Polarity Score"):
    #         polarity_score = st.selectbox(
    #             label="Polarity Score", options=["None", "Positive", "Neutral", "Negative"], key="authros_wc")

    #     df = self.df

    #     if (places and len(places) > 0):
    #         df = df[df['place'].apply(
    #             lambda x: x in places)]

    #     if (authors and len(authors) > 0):
    #         df = df[df['original_author'].apply(
    #             lambda x: x in authors)]

    #     if (polarity_score and len(polarity_score) > 0):

    #         if polarity_score == "Positive":
    #             df = df[df['polarity'].apply(
    #                 lambda x: x > 0)]
    #         elif polarity_score == "Negative":
    #             df = df[df['polarity'].apply(
    #                 lambda x: x < 0)]
    #         elif polarity_score == "Neutral":
    #             df = df[df['polarity'].apply(
    #                 lambda x: x == 0)]

    #     wc = wordCloud(df)
    #     st.image(wc.to_array())

    def render_data_page(self):

        st.write(self.df.sample(100))

    def top_handset_type(self):
        st.markdown("#### Top Handset type")
        top = st.number_input(label="Top", step=1, value=5, key="top_type")

        res = top_handset_type(self.df, top)
        st.bar_chart(data=res, width=0, height=400,
                     use_container_width=True)

    def top_manufacturer(self):
        st.markdown("#### Top handset manufactruer")

        top = st.number_input(label="Top", step=1, value=5, key="top_man")
        
        res = top_manufacturer(self.df, top)

        st.bar_chart(data=res, width=0, height=400,
                     use_container_width=True)

    def top_handset_by_manufacturer(self):
        st.markdown("#### Top handset by a manufactruer")

        top = st.number_input(label="Top", step=1, value=5, key="top_hand_manu")
        manu = st.selectbox(label="select filter method",
                            options=self.df['handset_manufacturer'].unique())
    
        res = top_handset_by_manufacturer(self.df, manu, top)
        st.bar_chart(data=res, width=0, height=400,
                     use_container_width=True)

    def render_data_analysis(self):

        self.top_handset_type()
        self.top_manufacturer()
        self.top_application_used()
    
    def top_application_used(self):
        total_data = self.df[['social_media', 'google', 'email', 'youtube', 'netflix',
                                         'gaming', 'total_data']]
        social_media_total = total_data.sum()[0]
        google_total = total_data.sum()[1]
        email_total = total_data.sum()[2]
        youtube_total = total_data.sum()[3]
        netflix_total = total_data.sum()[4]
        gaming_total = total_data.sum()[5]


        app_total_count_df = pd.DataFrame(columns=['app', 'total'])
        app_total_count_df['app'] = ['social_media', 'google',
                                    'email', 'youtube', 'netflix', 'gaming']

        app_total_count_df['total'] = [social_media_total, google_total,
                                    email_total, youtube_total, netflix_total, gaming_total]

        st.markdown("#### Top application used by customers")

        fig = px.bar(app_total_count_df.sort_values(by=["total"], ascending=False), x='app', y='total')
        st.plotly_chart(fig)

    def top_customers_session_freq(self):

        print(self.engagement_df)
        st.markdown("#### Top Customers with highest engagement score")

        top_customers = self.engagement_df.sort_values(
            by=['score'], ascending=False).head(10)

        fig = px.bar(top_customers, x='msisdn', y='score')
        st.plotly_chart(fig)

        print(self.engagement_df)
        st.markdown("#### Top Customers with highest frequency")

        top_customers = self.engagement_df.sort_values(
            by=['sessions_frequency'], ascending=False).head(10)
       
        fig = px.bar(top_customers, x='msisdn', y='sessions_frequency')
        st.plotly_chart(fig)
   
        print(self.engagement_df)
        st.markdown("#### Top Customers with highest duration")

        top_customers = self.engagement_df.sort_values(
            by=['duration'], ascending=False).head(10)

        fig = px.bar(top_customers, x='msisdn', y='duration')
        st.plotly_chart(fig)

        st.markdown("#### Engagment clusters")

        fig = px.scatter(self.engagement_df, x='duration', y="total_traffic",
                         color='clusters', size='total_traffic')
        st.plotly_chart(fig)




       


    
    def render(self):
        st.title(f"Welcome To {self.title}")
        self.render_siderbar([
        'Data Analysis', "User Overview Analysis", 
        'User Engagement Analysis', 'User Experience Analysis',
        "User Satsfaction Analysis"
        ], "select page: ")

        if (self.page == "Data Analysis"):

            st.title("3000 Sample Data Overview")
            self.render_data_analysis()

        elif (self.page == "User Overview Analysis"):
            st.title("User Overview Analysis")
            self.render_data_analysis()
            # self.render_visulazation()
        elif (self.page == "User Satsfaction Analysis"):
            st.title("User Satsfaction Analysis")
            # self.render_visulazation()
        elif (self.page == "User Engagement Analysis"):
            st.title("User Engagement Analysis")
            self.top_customers_session_freq()
        elif (self.page == "User Experience Analysis"):
            st.title("User Experience Analysis")
            # self.render_visulazation()


if __name__ == "__main__":
    dashboard = Dashboard("TellCo Data Analytics")
    dashboard.render()

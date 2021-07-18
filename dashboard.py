import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go


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


def top_customers_engaged_to_app(df, app, top=5):

    res_df = df.groupby('msisdn').agg({app: 'sum'}).sort_values(
        by=[app], ascending=False).head(top)
    res_df['msisdn'] = res_df.index
    return res_df


def get_top_app_df(df, top=6):
    app_cols = ['social_media', 'google',
                'email', 'youtube', 'netflix', 'gaming']
    app_metrics = df[app_cols]

    app_total_df = pd.DataFrame(columns=['app', 'total'])

    app_total_df['app'] = app_cols
    app_totals = []
    for app in app_cols:
        app_totals.append(app_metrics.sum()[app])
    app_total_df['total'] = app_totals

    return app_total_df.sort_values(by=['total'], ascending=False).head(top)


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

        self.df = self.df.rename(columns={'msisdn/number': 'msisdn'})
        self.df = self.df.rename(columns={'dur._(ms)': 'duration'})

        self.df['msisdn'] = self.df['msisdn'].astype(
            "int")
        self.df['msisdn'] = self.df['msisdn'].astype(
            "str")

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

    def render_siderbar(self, pages, select_label):
        st.sidebar.markdown("# Pages")
        self.page = st.sidebar.selectbox(f'{select_label}', pages)

    def render_top_application(self, type_="pie"):
        st.markdown("#### Top applications used by customers")

        top = st.number_input(label="Top", max_value=6,
                              step=1, value=5, key="top_type")

        top_df = get_top_app_df(self.df, top)

        if (type_ == "pie"):
            fig = px.pie(top_df, values="total",
                         names="app", width=500, height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')

            st.plotly_chart(fig)
        else:
            fig = px.bar(top_df, x='app', y='total')
            st.plotly_chart(fig)

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

        top = st.number_input(label="Top", step=1,
                              value=5, key="top_hand_manu")
        manu = st.selectbox(label="select filter method",
                            options=self.df['handset_manufacturer'].unique())

        res = top_handset_by_manufacturer(self.df, manu, top)
        st.bar_chart(data=res, width=0, height=400,
                     use_container_width=True)

    def top_freq_users(self):
        st.markdown("#### Top Customers with has frequent sessions")

        top = st.number_input(label="Top", step=1,
                              value=5, key="top1")
        res_df = self.engagement_df.sort_values(
            by=['sessions_frequency'], ascending=False).head(top)
        fig = px.bar(res_df, x='msisdn', y='sessions_frequency')
        st.plotly_chart(fig)

    def top_customers_by_duration(self):
        st.markdown("#### Top Customers with has spent more time")
        top = st.number_input(label="Top", step=1,
                              value=5, key="top2")
        res_df = self.engagement_df.sort_values(
            by=['duration'], ascending=False).head(top)
        fig = px.bar(res_df, x='msisdn', y='duration')
        st.plotly_chart(fig)

    def top_customers_by_data(self):
        st.markdown("#### Top Customers with has uses more data traffic")

        top = st.number_input(label="Top", step=1,
                              value=5, key="top3")
        res_df = self.engagement_df.sort_values(
            by=['total_traffic'], ascending=False).head(top)
        fig = px.bar(res_df, x='msisdn', y='total_traffic')
        st.plotly_chart(fig)

    def render_data_analysis(self):

        self.top_handset_type()
        self.top_manufacturer()
        self.top_freq_users()
        self.top_customers_by_data()
        self.top_customers_by_duration()
        # self.top_application_used()

    def render_top_customers_for_app(self):
        app_cols = sorted(['gaming', 'social_media', 'google',
                           'email', 'youtube', 'netflix'])

        app = st.selectbox(
            label="Select application to include", options=app_cols)

        top = st.number_input(label="Top", step=1,
                              value=5, key="top_hand_manu")
        res_df = top_customers_engaged_to_app(self.df, app=app, top=top)

        fig = px.bar(res_df, x='msisdn', y=app)
        st.plotly_chart(fig)

    def top_customers_session_freq(self):

        self.render_top_application()
        self.render_top_customers_for_app()

        st.markdown("#### Top Customers with highest engagement score")

        top_customers = self.engagement_df.sort_values(
            by=['score'], ascending=False).head(10)

        fig = px.bar(top_customers, x='msisdn', y='score')
        st.plotly_chart(fig)

        st.markdown("#### Top Customers with highest session frequency")

        top_customers = self.engagement_df.sort_values(
            by=['sessions_frequency'], ascending=False).head(10)

        fig = px.bar(top_customers, x='msisdn', y='sessions_frequency')
        st.plotly_chart(fig)

        st.markdown("#### Top Customers with highest duration")

        top_customers = self.engagement_df.sort_values(
            by=['duration'], ascending=False).head(10)

        fig = px.bar(top_customers, x='msisdn', y='duration')
        st.plotly_chart(fig)

        st.markdown("#### Engagement clusters")

        fig = px.scatter(self.engagement_df, x='duration', y="total_traffic",
                         color='clusters', size='total_traffic')
        st.plotly_chart(fig)

        self.cluster_info()

    def application_heat_map(self):

        st.markdown("#### Specific Application coorelation")

        total_data_2 = self.df[['social_media', 'google', 'email', 'youtube', 'netflix',
                                'gaming']]
        corr = total_data_2.corr()

        fig = px.imshow(corr)
        st.plotly_chart(fig)

    def decile_graph(self):
        scaled_explore_feature_df = self.df[[
            'msisdn', 'total_data', 'duration']]
        scaled_explore_feature_df['duration'] = self.df['duration']/1000

        scaled_explore_feature_df_agg = scaled_explore_feature_df.groupby(
            'msisdn').agg({'duration': 'sum', 'total_data': 'sum'})

        deciles = pd.qcut(scaled_explore_feature_df_agg['duration'], 5, labels=["1st_decile", "2nd_decile",
                                                                                "3rd_decile", "4th_decile",
                                                                                "5th_decile"])

        _df = scaled_explore_feature_df_agg.copy()

        _df['decile'] = deciles

        res_df = _df.groupby('decile').agg(
            {'total_data': 'sum', 'duration': 'sum'})
        res_df['decile'] = res_df.index

        st.markdown("#### duraton vs decile graph")

        fig = px.line(res_df,
                      x="decile", y=['duration'])
        st.plotly_chart(fig)

        st.markdown("#### total data vs decile graph")

        fig = px.line(res_df,
                      x="decile", y=['total_data'])
        st.plotly_chart(fig)

    def cluster_info(self):
        cluster_avg = self.engagement_df.groupby('clusters').agg({'sessions_frequency': 'mean',
                                                                  'duration': 'mean', 'total_traffic': 'mean'})
        cluster_avg['clusters'] = cluster_avg.index

        st.markdown("#### average duration per clusters")   
        fig = px.bar(cluster_avg, x='clusters', y='duration')
        st.plotly_chart(fig)

        st.markdown("#### average sessions frequency per clusters")
        fig = px.bar(cluster_avg, x='clusters', y='sessions_frequency')
        st.plotly_chart(fig)

        st.markdown("#### average total data per clusters")
        fig = px.bar(cluster_avg, x='clusters', y='total_traffic')
        st.plotly_chart(fig)

    def render(self):
        st.title(f"Welcome To {self.title}")
        self.render_siderbar([
            'Data overview', "User Overview Analysis",
            'User Engagement Analysis', 'User Experience Analysis',
            "User Satsfaction Analysis"
        ], "select page: ")

        sample = st.number_input(label="Sample", step=1,
                                 value=1000, key="sample")
        if (self.page == "Data overview"):

            st.markdown(f"### Sample {sample} Data Over View")
            st.write(self.df.sample(sample))

            st.markdown(f"### Sample {sample} Engagement metrics df")
            st.write(self.engagement_df.sample(sample))

            st.markdown(f"### Sample {sample} Experience metrics df")
            st.write(self.experience_df.sample(sample))

            self.application_heat_map()
            self.decile_graph()

        elif (self.page == "User Overview Analysis"):
            st.markdown("### User Overview Analysis")
            self.render_data_analysis()
            # self.render_visulazation()
        elif (self.page == "User Satsfaction Analysis"):
            st.markdown("### User Satsfaction Analysis")
            # self.render_visulazation()
        elif (self.page == "User Engagement Analysis"):
            st.markdown("### User Engagement Analysis")
            self.top_customers_session_freq()
        elif (self.page == "User Experience Analysis"):
            st.markdown("### User Experience Analysis")
            # self.render_visulazation()


if __name__ == "__main__":
    dashboard = Dashboard("TellCo Data Analytics")
    dashboard.render()

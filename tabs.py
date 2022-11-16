def select_season(season, user_menu):
    
    # importing necessary libraries
    import streamlit as st
    import pandas as pd
    import preprocessor, helper
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    
    # Updated dataframe is imported from preprocessor.py that is merged with region_df
    # Also the season ["Summer","Winter"] is selected
    df = preprocessor.preprocess(df, region_df, season)

    # Selection for user menu in the sidebar
    if user_menu == 'Medal Tally':
        # CASE: Medal Tally
        # List of all the Years and Countries is imported from helper.py
        # Two drop-down selections are made for year, country and df is returned
        years, country = helper.country_year_list(df)

        user_year = st.selectbox("Select Year", years)
        user_country = st.selectbox("Select Country", country)

        medal_tally = helper.fetch_medal_tally(df, user_year, user_country)
        if user_year == 'Overall' and user_country == 'Overall':
            st.title("Overall Tally")
        if user_year != 'Overall' and user_country == 'Overall':
            st.title("Medal Tally in " + str(user_year) + " Olympics")
        if user_year == 'Overall' and user_country != 'Overall':
            st.title(user_country + " overall performance")
        if user_year != 'Overall' and user_country != 'Overall':
            st.title(user_country + " performance in " + str(user_year) + " Olympics")
        st.table(medal_tally)

    if user_menu == 'Overall Stats':
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Hosts")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Nations")
            st.title(nations)
        with col3:
            st.header("Athletes")
            st.title(athletes)

        nations_over_time = helper.data_over_time(df,'region')
        fig = px.line(nations_over_time, x="Edition", y="region")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Edition", y="Event")
        st.title("Events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athlete_over_time, x="Edition", y="Name")
        st.title("Athletes over the years")
        st.plotly_chart(fig)

        st.title("No. of Events over time(Every Sport)")
        fig, ax = plt.subplots(figsize=(20,20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                    annot=True)
        st.pyplot(fig)

        # User selects a sport choice
        # Successfully athletes by their sports
        st.title("Most successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        user_sport = st.selectbox('Select a Sport', sport_list)
        x = helper.most_successful(df, user_sport)
        st.table(x)

    if user_menu == 'Country-wise Stats':
        # CASE: Country-wise Stats
        # List of all the Countries is imported from df
        # One drop-down selection is made for country and df is returned
        # Line chart and Heatmap is created for medals and various sports

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        user_country = st.selectbox('Select a Country', country_list)

        # Line chart
        country_df = helper.yearwise_medal_tally(df, user_country)
        fig = px.line(country_df, x="Year", y="Medal")
        st.title(user_country + " performance over the years")
        st.plotly_chart(fig)

        # Heat-map chart
        st.title(user_country + " excels in the following sports")
        pt = helper.country_event_heatmap(df,user_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)

        # List of Top Athletes
        st.title("Top athletes for" + user_country)
        top10_df = helper.most_successful_countrywise(df,user_country)
        st.table(top10_df)

def select_season(season, user_menu):
    
    # importing necessary libraries
    import streamlit as st
    import pandas as pd
    import preprocessor, helper
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns

    categories = ['Year', 'City', 'Sport', 'Event', 'Name', 'region']
    categories_head = ['Editions', 'Hosts', 'Sports', 'Events', 'Athletes', 'Nations']

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
        # CASE: Overall statistics
        # Listing overall stats for all the Years, event host, sports etc.
        # plot for categories over the years
        # heatmap count for sports vs years

        overall_stats = []
        for i in range(len(categories)):
            overall_stats.append(helper.ucount(df, categories[i]))
        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader(categories_head[0])
            st.title(overall_stats[0])
        with col2:
            st.subheader(categories_head[1])
            st.title(overall_stats[1])
        with col3:
            st.subheader(categories_head[2])
            st.title(overall_stats[2])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader(categories_head[3])
            st.title(overall_stats[3])
        with col2:
            st.subheader(categories_head[4])
            st.title(overall_stats[4])
        with col3:
            st.subheader(categories_head[5])
            st.title(overall_stats[5])

        helper.overall_plot(df, 'region', 'Participating nations over the years')
        helper.overall_plot(df, 'Event', 'Events over the years')
        helper.overall_plot(df, 'Name', 'Athletes over the years')

        st.title("No. of Events over time(Every Sport)")
        fig, ax = plt.subplots(figsize=(20,20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = (sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event',
                aggfunc ='count').fillna(0).astype('int'), annot=True))
        st.pyplot(fig)

        # User selects a sport choice
        # Top Successful athletes for a user selected sports
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
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

        # List of Top Athletes
        st.title("Top athletes for" + user_country)
        top10_df = helper.most_successful_countrywise(df,user_country)
        st.table(top10_df)

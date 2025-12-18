import streamlit as st
import plotly.express as px
import helper
import preprocessor
import pandas as pd
import matplotlib
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)
    # helper.fetch_medal_tally(df, selected_year, selected_country)
    # st.text(df.columns)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

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

    # Regions per year plot
    st.title('Participating Nations Over the Year')
    regions_per_year = helper.regions_per_year(df)
    fig = px.line(regions_per_year, x=regions_per_year.index, y='region')
    st.plotly_chart(fig, use_container_width=False)

    # events per year
    st.title('Events per Edition')
    events_per_year = helper.events_per_year(df)
    fig = px.line(events_per_year, x=events_per_year.index, y='Event')
    st.plotly_chart(fig, use_container_width=False)

    # unique events(per sport) each year
    st.title('No. of Events Over Time(Each Sport')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    #   most successful athlete
    st.title('Most Successful Athletes')
    sports = df.Sport.unique()
    sports.sort()
    sports = np.insert(sports, 0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sports)
    medals_by_athlete = helper.most_successful(df, selected_sport)
    st.table(medals_by_athlete)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    selected_country = st.sidebar.selectbox('Select a Country', countries)

    # country medal tally graph
    st.title(selected_country + ' Medal Tally Over the Years')
    medals_per_year = helper.medals_per_country_per_year(df, selected_country)
    fig = px.line(medals_per_year, x=medals_per_year.index, y='Medal')
    st.plotly_chart(fig, use_container_width=False)

    # medal tally in all sports over the years
    st.title('Medals Won in Different Sports Over the Years')
    pt = helper.medals_per_country_per_year_per_game(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

#     top 10 athletes of this country
    st.title('Most Successful Athletes of ' + selected_country)

    medals_by_athlete = helper.most_successful_country_wise(df, selected_country)
    medals_by_athlete=medals_by_athlete.drop('index', axis=1)
    st.table(medals_by_athlete)

if user_menu == 'Athlete wise Analysis':
    # distribution of age medal wise
    st.title('Distribution of Age')
    st.text('probability of winning a medal at certain age')
    unique_athletes = df.drop_duplicates(subset=['Name', 'region'])
    x1 = unique_athletes.Age.dropna()
    x2 = unique_athletes[unique_athletes.Medal == 'Gold']['Age'].dropna()
    x3 = unique_athletes[unique_athletes.Medal == 'Silver']['Age'].dropna()
    x4 = unique_athletes[unique_athletes.Medal == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Age Distribution', 'Gold', 'Silver', 'Bronze'],show_rug=False, show_hist=False)
    fig.update_layout(autosize=False, width=1000, height = 700)
    st.plotly_chart(fig)

#     chances of medal in every sport age wise
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = unique_athletes[unique_athletes['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height',data=temp_df, hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
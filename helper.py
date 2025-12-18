import numpy as np
import pandas as pd
import preprocessor
import streamlit as st


# def medal_tally(df):
#     medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal'])
#     medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
#                                                                                                 ascending=False).reset_index()
#     medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#
#     return medal_tally


def country_year_list(df):
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    years = df.Year.unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def regions_per_year(df):
    regions_per_year = df.groupby('Year')['region'].nunique()
    regions_per_year = pd.DataFrame(regions_per_year)

    return regions_per_year


def events_per_year(df):
    events_per_year = df.groupby('Year')['Event'].nunique()
    events_per_year = pd.DataFrame(events_per_year)

    return events_per_year


def most_successful(df, sport):

    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    medals_by_athlete = temp_df.groupby(['Name', 'Sport', 'region'])['Medal'].count().reset_index()
    # medals_by_athlete.columns = ['Athlete', 'Total Medals']
    medals_by_athlete = medals_by_athlete.sort_values(by='Medal', ascending=False)
    top_athletes = medals_by_athlete.head(15)
    top_athletes=top_athletes.reset_index()
    return top_athletes


def medals_per_country_per_year(df, country):
    df2 = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal'])
    medal_per_country = df2.groupby(['region', 'Year'])['Medal'].count()
    medals_per_year=medal_per_country.loc[country]

    return medals_per_year


def medals_per_country_per_year_per_game(df, country):
    df2 = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal'])
    medals_by_country = df2[df2.region == country]

    pt = medals_by_country.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_country_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    medals_by_athlete = temp_df.groupby(['Name', 'Sport', 'region'])['Medal'].count().reset_index()
    medals_by_athlete = medals_by_athlete.sort_values(by='Medal', ascending=False)
    top_athletes = medals_by_athlete.head(15)
    top_athletes = top_athletes.reset_index()
    return top_athletes



def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
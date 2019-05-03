import pandas as pd
import numpy as np


def bool_to_int(bool_val):
    '''used to tally up wins (positive) and losses (negative)'''

    if bool_val:
        return 1
    else:
        return -1


def home_streak(df, team, date):
    '''return consecutive number of wins or losses for home team
       - if home team won last game, will return the active win streak in all
         home matches prior to that one
       - if home team lost last game, will return the active losing streak'''

    # filter only results from before the chosen date
    date_df = df[df['Date'] < date]
    # filter only matches for the chosen home team
    team_df = date_df[date_df['Home_Team']==team].sort_values('Date', ascending=False)

    # count each row backwards in time until streak ends
    results = team_df.itertuples()
    try:
        last_result = bool_to_int(next(results)[-1])
        streak = last_result
    except:
        streak = 0

    while True:
        try:
            next_result = bool_to_int(next(results)[-1])
            if next_result == last_result:
                streak += next_result
            else:
                break
        except:
            break

    return streak


def away_streak(df, team, date):
    '''same as home_streak(), but for away team'''

    date_df = df[df['Date'] < date]
    team_df = date_df[date_df['Away_Team']==team].sort_values('Date', ascending=False)
    results = team_df.itertuples()
    try:
        last_result = bool_to_int(next(results)[-1])*-1
        streak = last_result
    except:
        streak = 0

    while True:
        try:
            next_result = bool_to_int(next(results)[-1])*-1
            if next_result == last_result:
                streak += next_result
            else:
                break
        except:
            break

    return streak


def home_avg_margin(df, team, date, num_games=5):
    '''return average home margin by home team in last n games'''

    date_df = df[df['Date'] < date]
    team_df = date_df[date_df['Home_Team']==team].sort_values('Date', ascending=False)

    # for fixtures at start of the data records return avg home score
    if len(team_df) == 0:
        return df['home_margin'].agg('mean')

    team_df = team_df[:num_games]

    home_margin_mean = team_df['home_margin'].agg('mean')

    return home_margin_mean


def away_avg_margin(df, team, date, num_games=5):
    '''return average away margin by away team in last n games'''

    date_df = df[df['Date'] < date]
    team_df = date_df[date_df['Away_Team']==team].sort_values('Date', ascending=False)

    # for fixtures at start of the data records return avg away score
    if len(team_df) == 0:
        return df['home_margin'].agg('mean')*-1

    team_df = team_df[:num_games]

    away_margin_mean = team_df['home_margin'].agg('mean')*-1

    return away_margin_mean


def cleanup(op_df, dummies=True):
    '''
    performs all necessary data cleaning, processing and feature engineering

    Params:
        op_df dataframe : dataframe
            in format as provided by OddsPortal
        dummies : bool, default True
            if True, uses one-hot encoding on team name and nationality columns
    '''

    # used for assigning countries to teams
    countries = {'Crusaders': 'NZ',
                 'Chiefs': 'NZ',
                 'Blues': 'NZ',
                 'Hurricanes': 'NZ',
                 'Highlanders': 'NZ',
                 'Bulls': 'SA',
                 'Cheetahs': 'SA',
                 'Kings': 'SA',
                 'Lions': 'SA',
                 'Sharks': 'SA',
                 'Stormers': 'SA',
                 'Brumbies': 'AUS',
                 'Force': 'AUS',
                 'Rebels': 'AUS',
                 'Reds': 'AUS',
                 'Waratahs': 'AUS',
                 'Jaguares': 'ARG',
                 'Sunwolves': 'JPN'}

    # create copy of odds portal dataframe
    df = pd.DataFrame(op_df)

    # replace spaces in column names with underscores
    df.columns = df.columns.str.replace(' ', '_')

    # convert Date column to datetime dtype
    df['Date'] = pd.to_datetime(df.Date)

    # create response variable
    df['home_margin'] = df['Home_Score'] - df['Away_Score']

    # create home_win column (for use in classification models)
    df['home_win'] = (df['Home_Score'] > df['Away_Score'])

    # create team form columns
    home_streaks = []
    home_avg_margins = []
    away_streaks = []
    away_avg_margins = []

    # iterate through each row in df, adding form features for home and away
    for row in df.itertuples():
        home_team = row.Home_Team
        away_team = row.Away_Team
        date = row.Date
        home_streaks.append(home_streak(df, home_team, date))
        home_avg_margins.append(home_avg_margin(df, home_team, date))
        away_streaks.append(away_streak(df, away_team, date))
        away_avg_margins.append(away_avg_margin(df, away_team, date))

    df['home_streak'] = home_streaks
    df['home_avg_marg'] = home_avg_margins
    df['away_streak'] = away_streaks
    df['away_avg_marg'] = away_avg_margins

    # aggregate odds into single probability variable
    df['home_win_prob'] = df['Away_Odds'] / (df['Home_Odds'] + df['Away_Odds'])

    # add nationalities
    df['home_nationality'] = df['Home_Team'].replace(countries)
    df['away_nationality'] = df['Away_Team'].replace(countries)

    if dummies:
        # encode nationalities
        df = pd.get_dummies(df, prefix='home_country', columns=['home_nationality'])
        df = pd.get_dummies(df, prefix='away_country', columns=['away_nationality'])

        # encode team names
        df = pd.get_dummies(df, prefix='home_team', columns=['Home_Team'])
        df = pd.get_dummies(df, prefix='away_team', columns=['Away_Team'])

        # drop irrelevent columns
        df.drop(['Home_Score', 'Away_Score', 'Home_Odds', 'Draw_Odds', 'Away_Odds',
                 'Bookmakers_Surveyed', 'home_country_ARG', 'home_country_JPN',
                 'away_country_ARG', 'away_country_JPN', 'home_team_Cheetahs',
                 'away_team_Cheetahs', 'home_team_Kings', 'away_team_Kings',
                 'home_team_Force', 'away_team_Force'],
                 axis=1,
                 inplace=True)

    else:
        # create year column for dashboard slider
        df['Year'] = df['Date'].apply(lambda datetime: datetime.year)
        # round the win prob column
        df['home_win_prob'] = df['home_win_prob'].apply(lambda x: np.round(x,3))
        # drop irrelevent columns
        df.drop(['Home_Odds', 'Draw_Odds', 'Away_Odds', 'Bookmakers_Surveyed'],
                 axis=1,
                 inplace=True)

    return df.sort_values('Date', ascending=False)

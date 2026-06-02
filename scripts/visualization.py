#importing necessary libraries

import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
VISUALS_PATH=os.getenv('VISUALS_PATH')
#creating database connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


#creating visualization for vw_monthly_trend
def visualization_monthly_trend():
    #creating query to fetch data from PSQL database, calling engine to execute the query and fetch the data, and storing the result in a pandas dataframe
    query = 'SELECT * FROM vw_monthly_trend;'
    monthly_trend = pd.read_sql(query, engine)
    #printing monthly_trend to confirm 
    #print(monthly_trend.head())
    #using temporary style context to create a line plot to visualize the monthly trend of traffic accidents where X-axis is the month while y-axis is the total number of accidents. Adding gridlines for better readability and setting labels and title for the plot.
    with plt.style.context('ggplot'):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly_trend['month_name'], monthly_trend['total_accidents'], marker='o', linestyle='-', color='b', zorder=3)
        ax.grid(True, which='major', linestyle='--', linewidth=0.6)
        ax.set(xlabel='Month', ylabel='Total Accidents', title='Monthly Trend of Traffic Accidents (2013-2025)')
        print(f'Saving monthly_trend.png - rows returned: {len(monthly_trend)}')
        plt.savefig(os.path.join(VISUALS_PATH, 'monthly_trend.png'), dpi=300, bbox_inches='tight')


#creating visualization for vw_seasonal_trend
def visualization_seasonal_trend():
    query = 'SELECT * FROM vw_seasonal_trend;'
    seasonal_trend = pd.read_sql(query, engine)
    with plt.style.context('ggplot'):
        fig, ax = plt.subplots()
        season_colors = {'Spring': 'green', 'Summer': 'yellow', 'Fall': 'orange', 'Winter': 'blue'}
        ax.bar(seasonal_trend['season'], seasonal_trend['total_accidents'], zorder=3, color=[season_colors[season] for season in seasonal_trend['season']])
        ax.set_xticks(range(len(seasonal_trend['season'])))
        ax.set_xticklabels(['Spring\nMar-May', 'Summer\nJun-Aug', 'Fall\nSep-Nov', 'Winter\nDec-Feb'])
        ax.set(xlabel='Season', ylabel='Total Accidents', title='Seasonal Trend of Traffic Accidents')
        print(f'Saving seasonal_trend.png - rows returned: {len(seasonal_trend)}')
        plt.savefig(os.path.join(VISUALS_PATH, 'seasonal_trend.png'), dpi=300, bbox_inches='tight')

#creating visualization for vw_cause_severity_analysis
def visualization_cause_severity():
    query = 'SELECT * FROM vw_cause_severity_analysis;'
    cause_severity = pd.read_sql(query, engine)
    with plt.style.context('ggplot'):
        #going to use horizontal bar plot using 
        fig, ax = plt.subplots()
        ax.barh(cause_severity['cause_category'], cause_severity['average_severity_score'], zorder=3, color='indigo')
        ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xticklabels(['0.0 \n Minor', '0.2 \n Low', '0.4 \n Moderate', '0.6 \n High', '0.8 \n Severe', '1.0 \n Fatal'])
        ax.set(ylabel='Cause Category', title='Accident Impact and Frequency by cause category')
        ax.set_xlabel('Average Severity Score', labelpad=15)
        print(f'Saving cause_severity.png - rows returned: {len(cause_severity)}')
        plt.savefig(os.path.join(VISUALS_PATH, 'cause_severity.png'), dpi=300, bbox_inches='tight')

def visualization_total_injury_by_day():
    query = 'SELECT * FROM vw_total_injury_by_day;'
    total_injury_by_day = pd.read_sql(query, engine)
    order = ['Daytime', 'Afternoon', 'Evening', 'Unknown']
    total_injury_by_day = (
    total_injury_by_day
    .set_index('time_of_day')
    .reindex(order)
    .reset_index()
    .fillna(0))
    fig, ax = plt.subplots()
    ax.bar(total_injury_by_day['time_of_day'], total_injury_by_day['total_accidents_with_injuries'], zorder=3 , color='deepskyblue')
    ax2=ax.twinx()
    ax2.plot(total_injury_by_day['time_of_day'], total_injury_by_day['average_severity_score'], marker='o', linestyle='-', color='red', zorder=2)
    ax2.set_ylabel('Average Severity Score', color='red', labelpad=15)
    ax.set_xticks(range(len(total_injury_by_day['time_of_day'])))
    ax.set_xticklabels(['Morning\n6AM-12PM', 'Afternoon\n12PM-6PM', 'Evening\n6PM-12AM', 'Unknown\n12AM-12AM'])
    ax.set_ylabel('Total Accidents with Injuries', color='deepskyblue', labelpad=15)
    ax.set(xlabel = 'Time of Day', title='Total Accidents with Injuries and Average Severity Score by Time of Day')
    ax.grid(True, which='major', linestyle='--', linewidth=0.6)
    print(f'Saving total_injury_by_day.png - rows returned: {len(total_injury_by_day)}')
    plt.savefig(os.path.join(VISUALS_PATH, 'total_injury_by_day.png'), dpi=300, bbox_inches='tight')


#creating visualization for damage_level_distribution
def visualization_damage_level_distribution():
    query = 'SELECT * FROM vw_damage_level_distribution;'
    damage_level_distribution = pd.read_sql(query, engine)
    with plt.style.context('ggplot'):
        order = ['Low', 'Medium', 'High']
        damage_level_distribution = (
            damage_level_distribution
            .set_index('damage_level')
            .reindex(order)
            .reset_index()
            .fillna(0)
        )
        fig, ax = plt.subplots()
        ax.bar(damage_level_distribution['damage_level'], damage_level_distribution['total_accidents'], zorder=3, color ='green')
        ax2=ax.twinx()
        ax2.plot(damage_level_distribution['damage_level'], damage_level_distribution['average_severity_score'], marker='o', linestyle='-', color='red', zorder=4)
        ax.set_xticks(range(len(damage_level_distribution['damage_level'])))
        ax.set_xticklabels(['Low \n (UNDER $500)', 'Medium \n ($500 - $1,500)', 'High \n (OVER $1,500)'])
        ax.set_title('Distribution of Accidents by Damage Level')
        ax.set_xlabel('Damage Level', labelpad=15)
        ax.set_ylabel('Total Accidents', color='green', labelpad=15)
        ax2.set_ylabel('Severity Score', color = 'red' , labelpad=15)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_axisbelow(True)
        ax2.patch.set_alpha(0)
        print(f'Saving damage_level_distribution.png - rows returned: {len(damage_level_distribution)}')
        plt.savefig(os.path.join(VISUALS_PATH, 'damage_level_distribution.png'), dpi=300, bbox_inches='tight')

#this should be stacked bar plot
def visualization_multi_single_unit():
    with plt.style.context('ggplot'):
        query = 'SELECT * FROM vw_multi_single_unit_comparison;'
        multi_single_unit = pd.read_sql(query, engine)
        labels = multi_single_unit['multi_unit'].replace({True: 'Multi-Unit', False: 'Single-Unit'})
        total_accidents = multi_single_unit['total_accidents']
        injuries = multi_single_unit['total_accident_with_injuries']
        x = range(len(labels))
        width = 0.35
        fig, ax = plt.subplots(figsize=(8,5))
        # Bar 1
        bar1= ax.bar(
        [i - width/2 for i in x],
        total_accidents,
        width=width,
        label='Total Accidents',
        color='steelblue')
        # Bar 2
        bar2= ax.bar(
            [i + width/2 for i in x],
            injuries,
            width=width,
            label='Injuries',
            color='tomato')
        ax.bar_label(bar1, padding=3)
        ax.bar_label(bar2, padding=3)
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels)
        ax.set_title('Multi-Unit and Single-Unit comparison')
        ax.set_ylabel('Count of total accidents and injuries')
        ax.set_xlabel('Multi-Unit vs Single-Unit', labelpad=15)
        ax.legend()
        ax.set_axisbelow(True)
        ax.grid(True, linestyle='--', alpha=0.4)
        print(f'Saving multi_single_unit_comparison.png - rows returned: {len(multi_single_unit)}')
        plt.savefig(os.path.join(VISUALS_PATH, 'multi_single_unit_comparison.png'), dpi=300, bbox_inches='tight')
        


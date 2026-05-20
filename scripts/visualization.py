#importing necessary libraries
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd

#creating database connection
engine = create_engine('postgresql://postgres:!Langlang55!@localhost:5432/traffics_db')


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
        ax.set(xlabel='Month', ylabel='Total Accidents', title='Monthly Trend of Traffic Accidents')
        plt.savefig('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\scripts\\views_py\\monthly_trend.png', dpi=300, bbox_inches='tight')
    
#visualization_monthly_trend()

    
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
        plt.savefig('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\scripts\\views_py\\seasonal_trend.png', dpi=300, bbox_inches='tight')

#visualization_seasonal_trend()

#creating visualization for vw_cause_severity_analysis
def visualization_cause_severity():
    query = 'SELECT * FROM vw_cause_severity_analysis;'
    cause_severity = pd.read_sql(query, engine)
    with plt.style.context('ggplot'):
        #going to use horizontal bar plot using 
        fig, ax = plt.subplots()

        ax.barh(cause_severity['cause_category'], cause_severity['avg_severity_score'], zorder=3, color='indigo')
        ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_xticklabels(['Minor', 'Low', 'Moderate', 'High', 'Severe', 'Fatal'])
        ax.set(xlabel='Average Severity Score', ylabel='Cause Category', title='Accident Impact and Frequency by cause category')
        plt.savefig('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\scripts\\views_py\\cause_severity.png', dpi=300, bbox_inches='tight')

visualization_cause_severity()
print('successful call')




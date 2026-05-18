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
    
visualization_monthly_trend()
print('successful call')
    
import pandas as pd
from sqlalchemy import create_engine

#setting the data variable to read the csv file and print the head, info and columns of the data
data=pd.read_csv('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\Data\\archive\\traffic_accidents.csv')
#print(data.head())
#print(data.info())
#print(data.columns)

#road = data[''].value_counts()
#print(road)

# Creating a pipeline now

def extract_data(file_path):
    data = pd.read_csv(file_path)
    return data

def transform_data(data):
    #Conversions of date and datatypes of injuries and, day, month, and hour of injuries
    data['crash_date'] = pd.to_datetime(data['crash_date'])
    list_to_int = [
        'injuries_total',
        'injuries_fatal',
        'injuries_incapacitating',
        'injuries_non_incapacitating',
        'injuries_reported_not_evident',
        'injuries_no_indication',
        'crash_hour',
        'crash_day_of_week',
        'crash_month'
    ]
    data[list_to_int] = data[list_to_int].fillna(0).astype(int)
    return data

    #***** Feature Engineering section ******
    
    #adding severity score, to determine how fatal the accident
    data['severity_score'] = (
        data['injuries_fatal'] * 5 +
        data['injuries_incapacitating'] * 3 +
        data['injuries_non_incapacitating'] * 2 +
        data['injuries_reported_not_evident'] * 1
    )

    #adding multi_unit column to determine if the accident involved more than one vehicle
    data['multi_unit'] = (data['num_units'] > 1).astype(int)

    #adding time-based feature layer by converting day of the week, hour of the day, season, and month to their equivalents
    data['day_type'] = data['crash_day_of_week'].apply(lambda x: 'Weekend' if x in [6, 7] else 'Weekday')
    data['time_of_day'] = data['crash_hour'].apply(lambda x: 'Evening' if 17 <= x < 21 else ('Midnight' if 21 <= x < 5 else 'Daytime' if 5 <= x < 12 else 'Afternoon' if 12 <= x < 17 else 'Unknown'))
    data['month'] = data['crash_month'].apply(lambda x: 'January' if x == 1 else ('February' if x == 2 else ('March' if x == 3 else ('April' if x == 4 else ('May' if x == 5 else ('June' if x == 6 else ('July' if x == 7 else ('August' if x == 8 else ('September' if x == 9 else ('October' if x == 10 else ('November' if x == 11 else 'December')))))))))))
    data['season'] = data['crash_month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Fall')))

    #adding damage cost estimation    
    data ['damage_level'] = data['damage'].apply(lambda x: 'High' if x == 'OVER $1,500' else ('Medium' if x == '$501 - $1,500' else ('Low' if x == '$500 OR LESS' else 'Unknown')))


def load_data(data, database_url, table_name):
    pass

print('successful run')
road = data['prim_contributory_cause'].value_counts()
print(road)
#print(transform_data(extract_data('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\Data\\archive\\traffic_accidents.csv')).info())
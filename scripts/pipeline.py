import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from datetime import datetime
#to map the datatypes of my database schema to the datatypes of my cleaned dataset, which will ensure that the data is loaded correctly into the database and that the integrity of the data is maintained.
from sqlalchemy.types import Integer, Boolean, String, Date, DateTime

#setting the data variable to read the csv file and print the head, info and columns of the data
data=pd.read_csv('C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\Data\\archive\\traffic_accidents.csv')

# Creating pipeline

#Extraction
def extract_data(file_path):
    data = pd.read_csv(file_path)
    return data

#Transformation
def transform_data(data):
    #Conversions of date and datatypes of injuries and, day, month, and hour of injuries
    #adding cleaned_data to avoid modifying the original data, just practicing data integrity 
    cleaned_data = data.copy()
    cleaned_data['crash_date'] = pd.to_datetime(
    cleaned_data['crash_date'],
    errors='coerce'
    )
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
    cleaned_data[list_to_int] = cleaned_data[list_to_int].fillna(0).astype(int)
    

    #***** Feature Engineering section ******
    
    #adding severity score, to determine how fatal the accident
    cleaned_data['severity_score'] = (
        cleaned_data['injuries_fatal'] * 5 +
        cleaned_data['injuries_incapacitating'] * 3 +
        cleaned_data['injuries_non_incapacitating'] * 2 +
        cleaned_data['injuries_reported_not_evident'] * 1
    )

    #adding a binary column to indicate if the accident was severe or not
    cleaned_data['is_severe'] = cleaned_data['severity_score'] >= 3

    #adding multi_unit column to determine if the accident involved more than one vehicle
    cleaned_data['multi_unit'] = (cleaned_data['num_units'] > 1)

    #adding time-based feature layer by converting day of the week, hour of the day, season, and month to their equivalents
    cleaned_data['day_type'] = cleaned_data['crash_day_of_week'].apply(lambda x: 'Weekend' if x in [6, 7] else 'Weekday')
    cleaned_data['time_of_day'] = cleaned_data['crash_hour'].apply(lambda x: 'Evening' if 17 <= x < 21 else ('Midnight' if 21 <= x < 5 else 'Daytime' if 5 <= x < 12 else 'Afternoon' if 12 <= x < 17 else 'Unknown'))
    
    cleaned_data['month_name'] = cleaned_data['crash_month'].apply(lambda x: 'January' if x == 1 else ('February' if x == 2 else ('March' if x == 3 else ('April' if x == 4 else ('May' if x == 5 else ('June' if x == 6 else ('July' if x == 7 else ('August' if x == 8 else ('September' if x == 9 else ('October' if x == 10 else ('November' if x == 11 else 'December')))))))))))
   
    cleaned_data['season'] = cleaned_data['crash_month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else ('Spring' if x in [3, 4, 5] else ('Summer' if x in [6, 7, 8] else 'Fall')))

    #adding damage cost estimation    
    cleaned_data ['damage_level'] = cleaned_data['damage'].fillna('Unknown').apply(lambda x: 'High' if 'OVER' in x else ('Medium' if '$501' in x and '$1,500' in x else ('Low' if 'LESS' in x else 'Unknown')))
    
    #for prim_contributory_cause feature, we can categorize the causes into broader categories such as driver-related, road-related, environment-related, and other. This will help in analyzing the data more effectively and identifying patterns in the causes of accidents.
    
    #creating lists of causes for each category
    driver_causes = [
        'FAILING TO YIELD RIGHT-OF-WAY',
        'FOLLOWING TOO CLOSELY',
        'DISREGARDING TRAFFIC SIGNALS',
        'IMPROPER TURNING/NO SIGNAL',
        'FAILING TO REDUCE SPEED TO AVOID CRASH',
        'IMPROPER OVERTAKING/PASSING',
        'DISREGARDING STOP SIGNS',
        'IMPROPER LANE USAGE',
        'DRIVING SKILLS/KNOWLEDGE/EXPERIENCE',
        'IMPROPER BACKING',
        'OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER',
        'VISION OBSCURED (DARK CLOTHING, WEATHER, ETC.)',
        'DISTRACTION - FROM INSIDE VEHICLE',
        'DRIVING ON WRONG SIDE/WAY',
        'DISREGARDING OTHER TRAFFIC SIGNS',
        'EQUIPMENT VEHICLE CONDITION',
        'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (ALCOHOL, DRUGS, MEDICATION)',
        'PHYSICAL CONDITION OF DRIVER',
        'DISTRACTION - FROM OUTSIDE VEHICLE',
        'EXCEEDING SAFE SPEED FOR CONDITIONS',
        'TURNING RIGHT ON RED',
        'EXCEEDING AUTHORIZED SPEED LIMIT',
        'DISREGARDING ROAD MARKINGS',
        'CELL PHONE USE OTHER THAN TEXTING',
        'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)',
        'DISREGARDING YIELD SIGNS',
        'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)',
        'TEXTING',
        'PASSING STOPPED SCHOOL BUS',
        'BICYCLE ADVANCING LEGALLY ON RED LIGHT',
        'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT',
    ]

    road_causes = [
        'NOT APPLICABLE',
        'ROAD CONSTRUCTION/MAINTENANCE',
        'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST',
        'ROAD ENGINEERING/SURFACE/MARKING DEFECTS',
        'RELATED TO BUS STOP',
        'ANIMAL',
        'OBSTRUCTED CROSSWALK',
    ]

    environment_causes = ['WEATHER']
        
    
    #function for categorization
    def categorize_cause(cause):
        clean_cause = cause.strip().upper()

        if clean_cause in driver_causes:
            return 'DRIVER'
        elif clean_cause in road_causes:
            return 'ROAD'
        elif clean_cause in environment_causes:
            return 'ENVIRONMENT'
        elif clean_cause == 'UNABLE TO DETERMINE':
            return 'UNKNOWN'
        else:
            return 'OTHER'
        
        
            
    cleaned_data['cause_category'] = cleaned_data['prim_contributory_cause'].apply(categorize_cause)
    #these are new columns for aggregated analysis of the causes of accidents, which will help in identifying patterns and trends in the data.
    cleaned_data['is_driver_related'] = cleaned_data['cause_category'] == 'DRIVER'
    cleaned_data['is_road_related'] = cleaned_data['cause_category'] == 'ROAD'
    cleaned_data['is_environment_related'] = cleaned_data['cause_category'] == 'ENVIRONMENT'
    cleaned_data['is_unknown_cause'] = cleaned_data['cause_category'] == 'UNKNOWN'
    cleaned_data['is_other_cause'] = cleaned_data['cause_category'] == 'OTHER'

    # Highest cause of injury based on severity and total injuries
    highest_injury_cause = (
        cleaned_data.groupby("cause_category")
        .agg(
            average_severity=("severity_score", "mean"),
            total_injuries=("injuries_total", "sum"),
            accidents_count=("cause_category", "count")
        )
        .sort_values(by="average_severity", ascending=False)
    )
    #assigning percentage of accidents for each cause category
    highest_injury_cause['injury_accident_percentage'] = highest_injury_cause['accidents_count'] / highest_injury_cause['accidents_count'].sum() * 100
    highest_injury_cause = highest_injury_cause.sort_values(by='injury_accident_percentage', ascending=False
    )

    #featuring worst day of the week for accidents based on severity and total injuries
    worst_day_of_week = (
        cleaned_data.groupby('crash_day_of_week')
        .agg(average_severity = ('severity_score', 'mean'),
             total_injuries = ('injuries_total', 'sum'),
             accidents_count = ('crash_day_of_week', 'count'))
    ) 
    worst_day_of_week['day_accident_percentage'] = worst_day_of_week['accidents_count'] / worst_day_of_week['accidents_count'].sum() * 100
    worst_day_of_week = worst_day_of_week.sort_values(by='day_accident_percentage', ascending=False)

    #adding average damage cost
    average_damage_cost = (
        cleaned_data.groupby('damage_level')
        .agg(average_severity = ('severity_score', 'mean'),
             total_injuries = ('injuries_total', 'sum'),
             accidents_count = ('damage_level', 'count'))
    )
    average_damage_cost['damage_accident_percentage'] = average_damage_cost['accidents_count'] / average_damage_cost['accidents_count'].sum() * 100
    average_damage_cost = average_damage_cost.sort_values(by='damage_accident_percentage', ascending=False)   

    #Adding single or multi unit accidents
    single_multi_unit_analysis = cleaned_data.groupby('multi_unit').agg(
        average_severity = ('severity_score', 'mean'),
        total_injuries = ('injuries_total', 'sum'),
        accidents_count = ('multi_unit', 'count')
    )
    single_multi_unit_analysis['multi_unit_accident_percentage'] = single_multi_unit_analysis['accidents_count'] / single_multi_unit_analysis['accidents_count'].sum() * 100
    single_multi_unit_analysis = single_multi_unit_analysis.sort_values(by='multi_unit_accident_percentage', ascending=False)

    return cleaned_data

#Loading data
def load_data(data, database_url, table_name):
    engine = create_engine(database_url)

    #truncating the table before loading new data for idempotency of this project.
    with engine.begin() as connection:
        connection.execute(text(f'TRUNCATE TABLE public.{table_name};'))
    dtype={
        'crash_date' : Date,

        'traffic_control_device' : String(100) ,
        'weather_condition' : String(255) ,
        'lighting_condition' : String(255) ,
        'first_crash_type' : String(255) ,
        'trafficway_type' : String(255) ,
        'alignment' : String(100) ,
        'roadway_surface_cond' : String(255) ,
        'road_defect' : String(255) ,
        'crash_type' : String(255) ,
        'intersection_related_i' : String(255) ,
        'damage' : String(255) ,
        'prim_contributory_cause' : String(255) ,
        'day_type' : String(10) ,
        'time_of_day' : String(20) ,
        'season' : String(10) ,
        'month_name' : String(20) ,
        'damage_level' : String(20) ,
        'cause_category' : String(20) ,

        'num_units' : Integer,
        'injuries_total' : Integer,
        'injuries_fatal' : Integer,
        'injuries_incapacitating' : Integer,
        'injuries_non_incapacitating' : Integer,
        'injuries_reported_not_evident' : Integer,
        'injuries_no_indication' : Integer,
        'crash_hour' : Integer,
        'crash_day_of_week' : Integer,
        'crash_month' : Integer,
        'severity_score' : Integer,

        'is_severe' : Boolean,
        'multi_unit' : Boolean,
        'is_driver_related' : Boolean,
        'is_road_related' : Boolean,
        'is_environment_related' : Boolean,
        'is_unknown_cause' : Boolean,
        'is_other_cause' : Boolean
    }
    data.to_sql('traffic_accidents_final', engine, if_exists='append', dtype=dtype, index=False)

#after ETL, i'll call the views.sql file to create the views for analysis and visualization, to make the views available in the database.

def create_views(database_url, views_sql_file):
    engine = create_engine(database_url)

    with open(views_sql_file, 'r') as file:
        views_sql = file.read()

    statements = [
        stmt.strip()
        for stmt in views_sql.split(";")
        if stmt.strip()
    ]

    with engine.begin() as connection:
        for stmt in statements:
            connection.execute(text(stmt))

#executing the pipeline by calling the main function. 
 
def main():
    file_path = 'C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\Data\\archive\\traffic_accidents.csv'
    data = extract_data(file_path)
    transformed_data = transform_data(data)
    load_data(transformed_data, "postgresql://postgres:!Langlang55!@localhost:5432/traffics_db", "traffic_accidents_final")
    create_views("postgresql://postgres:!Langlang55!@localhost:5432/traffics_db", 'C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\sql\\views\\views.sql')

# Execute the pipeline by calling the main function, if name is main, which ensures that the pipeline runs only when this script is executed directly and not when imported as a module in another script.  
if __name__ == "__main__":
    main()
print('successful run')

# Generate a unique run ID based on current timestamp for reproducibility and tracking and takes the date and time now 
run_id = datetime.now().strftime("%Y%m%d%H%M%S")
# save the cleaned dataset for version control and auditability 
cleaned_data = transform_data(data)
cleaned_data.to_csv(f'C:\\Users\\DELL\\Desktop\\Luap\\Data Engineering\\ThirdProject\\Data\\versions\\cleaned_traffic_accidents_{run_id}.csv', index=False)

# Log basic execution metadata for auditability

print(f'Run ID: {run_id}')
print(f'Rows: {len(cleaned_data)}')




## Name: Park Chang Whan
## Student ID: 1129623
## Part A Task 1

import pandas as pd
import argparse

# Using argparse to read CSV file name for the output
parser = argparse.ArgumentParser(description='Find the monthly data for covid in 2020')
parser.add_argument('file_name', type=str, metavar='', help='Name of output file for the monthly data')
args = parser.parse_args()

def covid_monthly_data_2020(name):
    """ 
    Get dataframe for covid 19 data on location, month, case fatility rate, 
    total cases, new cases, total deaths, and new deaths in 2020
    
    Prints the first five row of new dataframe
    Outputs dataframe to csv file given 'name'
    """
    
    # Get the full data into a DataFrame + extra column which contains the months only (mm)
    covid_df = pd.read_csv('owid-covid-data.csv', encoding = 'ISO-8859-1')
    covid_df['date'] = pd.to_datetime(covid_df['date'], yearfirst = True) # Change to DateTime format for easy manipulation
    covid_df['month'] = covid_df['date'].dt.strftime('%m')

    # Get subset of year 2020 only for 6 columns:
    #     ('location', 'month', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths')
    covid_df_2020 = covid_df.loc[(covid_df['date'] >= '2020-01-01') & (covid_df['date'] < '2021-01-01')
                                 , ['location' , 'month' , 'total_cases' , 'new_cases' , 'total_deaths' , 'new_deaths']]

    # Aggregate values of ('total_cases', 'new_cases', 'total_deaths', 'new_deaths') by month and location(sorted) in 2020
    # Take the last value for 'total_cases' and 'total_deaths' as they are already summed up
    # Take the sum of 'new_cases' and 'new_deaths' to find the total new cases and deaths for that each month
    covid_2020_agg = covid_df_2020.groupby(['location', 'month'], sort = True).agg(total_cases = pd.NamedAgg(column = "total_cases", 
                                                                                                             aggfunc = "max"),
                                                                                    new_cases = pd.NamedAgg(column = "new_cases", 
                                                                                                            aggfunc = "sum"),
                                                                                    total_deaths = pd.NamedAgg(column = "total_deaths", 
                                                                                                               aggfunc = "max"),
                                                                                    new_deaths = pd.NamedAgg(column = "new_deaths", 
                                                                                                             aggfunc = "sum")
                                                                                    ).reset_index() # Get all the column headings in place


    # Adding new variable 'case_fatality_rate' = number of deaths/ confirmed case in given period (from start of 2020 till current month)
    covid_2020_agg.insert(2, 'case_fatality_rate', covid_2020_agg['total_deaths'] / covid_2020_agg['total_cases'])
    
    # Save new dataframe to CSV file given 'name'
    covid_2020_agg.to_csv(name, index=False)
    
    # return first 5 rows of final dataframe
    return(covid_2020_agg.head())


if __name__ == '__main__':
    
    # Get first five rows of new
    print(covid_monthly_data_2020(args.file_name).to_string(index=False))

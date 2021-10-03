## Name: Park Chang Whan
## Student ID: 1129623
## Part A Task 2

import pandas as pd
import argparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools
import numpy as np
 
# argparse to run this file and get scatterplot names
parser = argparse.ArgumentParser(description='Find the monthly data for covid in 2020')
parser.add_argument('scatter1', type=str, metavar='', help='Name of scatterplot for case_fatality_rate by locations in 2020')
parser.add_argument('scatter2', type=str, metavar='', help='Name of scatterplot for case_fatality_rate by locations(log-scale) in 2020')
args = parser.parse_args()

def get_data_2020():
    """ 
    Get data for locations' case fatility rate and confirmed new cases in 2020 
    
    Returns data of covid 19 for location, case fatality rate and new cases in a dataframe
    """

    # Get the full data into a DataFrame + extra column which contains the year only (YYYY)
    covid_df = pd.read_csv('owid-covid-data.csv', encoding = 'ISO-8859-1')
    covid_df['date'] = pd.to_datetime(covid_df['date'], yearfirst = True) # Change to DateTime format for easy manipulation
    covid_df['year'] = covid_df['date'].dt.strftime('%Y')
    
    
    # Get subset of year 2020 only for 4 columns:
    #     ('location', 'total_cases', 'total_deaths', 'new_cases')
    covid_2020 = covid_df.loc[covid_df['year'] == '2020' , ['location', 'total_cases', 'total_deaths', 'new_cases']]
    
    
    # Get the total cases, new cases and deaths for each location in 2020
    covid_2020_loc = covid_2020.groupby(['location'], sort = True).agg(total_cases = pd.NamedAgg(column = "total_cases", 
                                                                                                             aggfunc = "max"),
                                                                                    new_cases = pd.NamedAgg(column = "new_cases", 
                                                                                                            aggfunc = "sum"),
                                                                                    total_deaths = pd.NamedAgg(column = "total_deaths", 
                                                                                                               aggfunc = "max")
                                                                                    ).reset_index() # Get all the column headings in place
    
    # Get case_fatality_rate for each location 
    covid_2020_loc.insert(1, 'case_fatality_rate', covid_2020_loc['total_deaths'] / covid_2020_loc['total_cases'])

    
    return(covid_2020_loc.loc[:,['location', 'case_fatality_rate', 'new_cases']])




def scatterplot(name, covid_2020_loc, log):
    """ 
    We will have a Scatterplot of all the locations with case fatility rate(y-axis) and confirmed new cases(x-axis)
        - x-axis is either in log scale or not
    
    Outputs scatterplot to given 'name'
    """
    
    # Create a set of colors for every location 
    colors = iter(cm.rainbow(np.linspace(0, 1, len(covid_2020_loc.index))))
    
    # Plot the point in scatterplot for each location with different color
    for index, row in covid_2020_loc.iterrows():
        plt.scatter(row['new_cases'], row['case_fatality_rate'], color = next(colors))
    
    plt.grid(True)
    plt.xlabel("Confirmed New Cases")
    plt.ylabel("Case Fatality Rate")
    plt.title('Case Fatility Rate and Confirmed New Cases in 2020 for Each Location')
    
    if(log):
        plt.xscale('log')
        plt.xlabel("Confirmed New Cases (Log Scaled)")
    
    plt.savefig(name)


    
    
                                  
if __name__ == '__main__':
    
    # Get case fatality rate for each location 
    covid_2020_loc = get_data_2020()
    
    # Make a scatterplot for given output png name with no log scale
    scatterplot(args.scatter1, covid_2020_loc, False)
    
    # Make scatterplot for given output png name with log scale
    scatterplot(args.scatter2, covid_2020_loc, True)
    

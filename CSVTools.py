# coding: utf-8

from datetime import datetime, timedelta
from urllib.request import urlopen
import os


def scrape_station(station):
    '''
    This function scrapes the weather data web pages from wunderground.com
    for the station you provide it.
    You can look up your city's weather station by performing a search for
    it on wunderground.com then clicking on the "History" section.
    The 4-letter name of the station will appear on that page.
    '''

    # Scrape between July 1, 2014 and July 1, 2015
    # You can change the dates here if you prefer to scrape a different range
    current_date = datetime(year=2014, month=7, day=1)
    end_date = datetime(year=2015, month=7, day=1)

    # Make sure a directory exists for the station web pages
    os.mkdir(station)

    # Use .format(station, YYYY, M, D)
    lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'

    while current_date != end_date:

        if current_date.day == 1:
            print(current_date)

        formatted_lookup_URL = lookup_URL.format(station,
                                                 current_date.year,
                                                 current_date.month,
                                                 current_date.day)
        html = urlopen(formatted_lookup_URL).read().decode('utf-8')

        out_file_name = '{}/{}-{}-{}.html'.format(station, current_date.year,
                                                  current_date.month,
                                                  current_date.day)

        with open(out_file_name, 'w') as out_file:
            out_file.write(html)

        current_date += timedelta(days=1)


        
        
        
        
        
        
        

        
        
from bs4 import BeautifulSoup

def parse_station(station):
    '''
    This function parses the web pages downloaded from wunderground.com
    into a flat CSV file for the station you provide it.
p
    Make sure to run the wunderground scraper first so you have the web
    pages downloaded.
    '''

    # Scrape between July 1, 2014 and July 1, 2015
    # You can change the dates here if you prefer to parse a different range
    current_date = datetime(year=2014, month=7, day=1)
    end_date = datetime(year=2015, month=7, day=1)

    with open('{}.csv'.format(station), 'w') as out_file:
        out_file.write('date,actual_mean_temp,actual_min_temp,actual_max_temp,'
                       'average_min_temp,average_max_temp,'
                       'record_min_temp,record_max_temp,'
                       'record_min_temp_year,record_max_temp_year,'
                       'actual_precipitation,average_precipitation,'
                       'record_precipitation\n')

        while current_date != end_date:
            try_again = False
            with open('{}/{}-{}-{}.html'.format(station,
                                                current_date.year,
                                                current_date.month,
                                                current_date.day)) as in_file:
                soup = BeautifulSoup(in_file.read(), 'html.parser')

                weather_data = soup.find(id='historyTable').find_all('span', class_='wx-value')
                weather_data_units = soup.find(id='historyTable').find_all('td')

                try:
                    actual_mean_temp = weather_data[0].text
                    actual_max_temp = weather_data[2].text
                    average_max_temp = weather_data[3].text
                    record_max_temp = weather_data[4].text
                    actual_min_temp = weather_data[5].text
                    average_min_temp = weather_data[6].text
                    record_min_temp = weather_data[7].text
                    record_max_temp_year = weather_data_units[
                        9].text.split('(')[-1].strip(')')
                    record_min_temp_year = weather_data_units[
                        13].text.split('(')[-1].strip(')')

                    actual_precipitation = weather_data[9].text
                    if actual_precipitation == 'T':
                        actual_precipitation = '0.0'
                    average_precipitation = weather_data[10].text
                    record_precipitation = weather_data[11].text

                    # Verify that the parsed data is valid
                    if (record_max_temp_year == '-1' or record_min_temp_year == '-1' or
                            int(record_max_temp) < max(int(actual_max_temp), int(average_max_temp)) or
                            int(record_min_temp) > min(int(actual_min_temp), int(average_min_temp)) or
                            float(actual_precipitation) > float(record_precipitation) or
                            float(average_precipitation) > float(record_precipitation)):
                        raise Exception

                    out_file.write('{}-{}-{},'.format(current_date.year, current_date.month, current_date.day))
                    out_file.write(','.join([actual_mean_temp, actual_min_temp, actual_max_temp,
                                             average_min_temp, average_max_temp,
                                             record_min_temp, record_max_temp,
                                             record_min_temp_year, record_max_temp_year,
                                             actual_precipitation, average_precipitation,
                                             record_precipitation]))
                    out_file.write('\n')
                    current_date += timedelta(days=1)
                except:
                    # If the web page is formatted improperly, signal that the page may need
                    # to be downloaded again.
                    try_again = True

            # If the web page needs to be downloaded again, re-download it from
            # wunderground.com

            # If the parser gets stuck on a certain date, you may need to investigate
            # the page to find out what is going on. Sometimes data is missing, in
            # which case the parser will get stuck. You can manually put in the data
            # yourself in that case, or just tell the parser to skip this day.
            if try_again:
                
                print('Error with date {}'.format(current_date))
                
                actual_mean_temp = '0.0'
                actual_max_temp = '0.0'
                average_max_temp = '0.0'
                record_max_temp = '0.0'
                actual_min_temp = '0.0'
                average_min_temp = '0.0'
                record_min_temp = '0.0'
                record_max_temp_year = '0.0'
                record_min_temp_year = '0.0'

                actual_precipitation = '0.0'
                average_precipitation = '0.0'
                record_precipitation = '0.0'

                out_file.write('{}-{}-{},'.format(current_date.year, current_date.month, current_date.day))
                out_file.write(','.join([actual_mean_temp, actual_min_temp, actual_max_temp,
                                         average_min_temp, average_max_temp,
                                         record_min_temp, record_max_temp,
                                         record_min_temp_year, record_max_temp_year,
                                         actual_precipitation, average_precipitation,
                                         record_precipitation]))
                out_file.write('\n')
                current_date += timedelta(days=1)







import pandas as pd

def interim_process(main, replacement):
    """Enter the main and replacement in the following form('main.csv', 'replacement.csv')"""
    import pandas as pd
    main = pd.read_csv(main)
    replacement = pd.read_csv(replacement)
    
    row = main.query('actual_mean_temp == actual_min_temp').index
    for i in row:
        main.loc[i:i,'date':'record_precipitation'] = replacement.loc[i:i, 'date':'record_precipitation']
    
    return (main)



def csvMERGER(main, replacement):
    """Enter the main and replacement in the following form('main.csv', 'replacement.csv').
    This replaces the zero rows of main.csv with the rows from replacement.csv
    Note: the two csv's must be the same lengh, so as long as you scraped and parsed the same dates, you're fine.
    Further Note: rewriting the file creates an extra column named 'Unnamed: 0', this won't mess up the visualization.
    Example:
    main = 'KMIE.csv'
    replacement = 'KIND.csv'
    csvMERGER(main, replacement)"""
    
    import pandas as pd
    length = len(pd.read_csv(main))
    df = interim_process(main, replacement).loc[0:length,'date':'record_precipitation']
    #This next step will produce an unnecessary column during the rewrite.
    #Don't worry about it. It doesn't change the visualizations.
    df.to_csv(main)
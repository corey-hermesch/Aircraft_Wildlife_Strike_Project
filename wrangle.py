## IMPORTS
import numpy as np
import pandas as pd

import os

from sklearn.model_selection import train_test_split

np.random.seed(42)

import warnings
warnings.filterwarnings('ignore')

## FUNCTIONS

# defining function to wrangle wildlife_strike data
def wrangle_wildlife_strike_df(filename = 'strike_reports.csv'):
    """
    This function will
    - take about 12-15 seconds to run
    - accept a .csv filename for wildlife strikes; default is 'strike_reports.csv'
    - read the filename into a dataframe
    - make column names lowercase and change 'size' to 'size_of_species'
    - change the date column to datetime and set as index
    - discard unused columns (drop from 100 columns down to 20)
    - Handle nulls - mostly fill nulls with 'Unknown'/'U'/'UNK'/'Z''ZZ'/-1/'99'
    - for nr_injuries and nr_fatalities fill nulls with 0
    - change floats to ints
    """
    # check for cached csv (file_prepared.csv) which is smaller and quicker to read
    cache_file_name = filename.split('.')[0] + '_prepared.csv'
    if os.path.isfile(cache_file_name):
        df = pd.read_csv(cache_file_name)
        df.date = df.date.astype('datetime64')
        df = df.set_index('date')
        df = df.sort_index()
        print ("cached csv file found and read")
    
    else:
    
        # read in dataframe; errors out without the encoding variable set to latin1
        df = pd.read_csv(filename, encoding='latin1')

        # make column names lowercase
        df.columns = df.columns.str.lower()

        # make the date column a datetime and set it as index (Takes about 7 seconds)
        df = df.rename(columns={'incident_date' : 'date'})
        df.date = df.date.astype('datetime64')
        df = df.set_index('date')
        df = df.sort_index()

        # only keep these 20 columns
        keep_cols = ['time_of_day', 'airport_id', 'airport', 'runway', 'state', 'opid', 'operator'
                 , 'aircraft', 'ac_class', 'ac_mass', 'type_eng', 'num_engs', 'phase_of_flight'
                 , 'precipitation', 'damage_level', 'species_id', 'species', 'size', 'nr_injuries', 'nr_fatalities']
        df = df[keep_cols]

        # changing nulls to 'Unknown' for time of day (Dusk, Dawn, ..., Unknown)
        df.time_of_day = df.time_of_day.fillna('Unknown')

        # there are only 5 nulls for airport_id, so I'm just going to remove them
        df = df[df.airport_id.notnull()]

        # fill runway nulls with 99 (only valid runways are 01-36 or variant (18L, 18/36, etc.))
        df.runway = df.runway.fillna('99')

        # fill state nulls with 'ZZ'; this column also may be of marginal utility
        df.state = df.state.fillna('ZZ')

        # fill phase_of_flight nulls with Unknown
        df.phase_of_flight = df.phase_of_flight.fillna('Unknown')

        # fill precipitation nulls with 'Unknown'
        df.precipitation = df.precipitation.fillna('Unknown')

        # fill ac_class nulls with 'Z' which is the database code for Unknown
        df.ac_class = df.ac_class.fillna('Z')

        # fill ac_mass nulls with 0 (unknown)
        df.ac_mass = df.ac_mass.fillna(0)

        # fill type_eng nulls with 'Z' - Unknown
        df.type_eng = df.type_eng.fillna('Z')

        # if type_eng = 'E' that means it's a glider; for those rows, change num_engs to 0
        df.num_engs = np.where(df.type_eng == 'E', 0, df.num_engs)
        # fill num_engs remaining nulls with -1 (unknown)
        df.num_engs = df.num_engs.fillna(-1)

        # fill nulls in damage_level with 'N' - negligible
        df.damage_level = np.where(df.damage_level.isnull(), 'N', df.damage_level)
        df.damage_level = np.where(df.damage_level == 'M?', 'N', df.damage_level)

        # change size to size_of_species and fillna with 'Unknown'
        df = df.rename (columns = {'size': 'size_of_species'})
        df.size_of_species = df.size_of_species.fillna('Unknown')

        # fill nulls for species and species_id
        df.species = df.species.fillna('Unknown bird') 
        df.species_id = df.species_id.fillna('UNKB') 

        # couple of hanging chads where opid is null
        df.opid = np.where(df.opid.isnull() & (df.operator.str.contains('UNITED AIRLINES')), 'UAL', df.opid)
        df.opid = np.where(df.opid.isnull() & (df.operator.str.contains('DELTA')), 'DAL', df.opid)
        df.opid = np.where(df.opid.isnull() & (df.operator == 'UNKNOWN'), 'UNK', df.opid)

        # fill nr_injuries and nr_fatalities null values with 0 
        df.nr_injuries = df.nr_injuries.fillna(0)
        df.nr_fatalities = df.nr_fatalities.fillna(0)

        # change floats to ints
        df.ac_mass = df.ac_mass.astype(int)
        df.num_engs = df.num_engs.astype(int)
        df.nr_injuries = df.nr_injuries.astype(int)
        df.nr_fatalities = df.nr_fatalities.astype(int)
        
        # write cached file
        df.to_csv(cache_file_name, index='date')
        print(f'{filename} found, read, and prepared')
    
    return (df)

#defining function to split data for exploration and modeling
def split_function(df, target_var):
    """
    This function will
    - take in a dataframe (df) and a string (target_var)
    - split the dataframe into 3 data frames: train (60%), validate (20%), test (20%)
    -   while stratifying on the target_var
    - And finally return the three dataframes in order: train, validate, test
    """
    train, test = train_test_split(df, random_state=42, test_size=.2, stratify=df[target_var])
    
    train, validate = train_test_split(train, random_state=42, test_size=.25, stratify=train[target_var])

    print(f'Prepared df: {df.shape}')
    print()
    print(f'Train: {train.shape}')
    print(f'Validate: {validate.shape}')
    print(f'Test: {test.shape}')
    
    return train, validate, test
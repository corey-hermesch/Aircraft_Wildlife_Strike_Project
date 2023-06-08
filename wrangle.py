## IMPORTS
import numpy as np
import pandas as pd

import os

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import MinMaxScaler

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

#defining a function to get dummy columns for cleaned up wildlife_strike dataframe
def prep_w_strike_df_for_modeling(df, target='damage_level'):
    """
    This function will drop columns I'm not using for modeling, and it 
    will make dummy columns for the categorical columns I'm moving forward to modeling with.
    It will return a df ready for modeling with the target as the first column
    """
    # define columns to make into dummy columns
    keep_cols = ['size_of_species', 'ac_mass', 'ac_class', 'type_eng', 'num_engs', 'phase_of_flight', 'precipitation']

    dummy_df = pd.get_dummies(df[keep_cols], drop_first=True)
    
    modeling_df = pd.concat([df[[target]], dummy_df], axis=1)
    return modeling_df


# defining function to wrangle wildlife_strike data
def wrangle_wildlife_strike_df_mvp(filename = 'strike_reports.csv'):
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
    cache_file_name = filename.split('.')[0] + '_prepared_mvp.csv'
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
                 , 'speed', 'precipitation', 'damage_level', 'species_id', 'species', 'size'
                 , 'num_struck']
        df = df[keep_cols]

        # Drop nulls for this version
        df = df.dropna()
        df = df[df.damage_level != 'M?']
        
        # change 'size' column name to a non-reserved word
        df = df.rename (columns = {'size': 'size_of_species'})
        
        # adjust precipitation column and break it into several columns
        df['precip_none'] = np.where(df.precipitation == 'None', 1, 0)
        df['precip_rain'] = np.where(df.precipitation.str.contains('Rain'), 1, 0)
        df['precip_fog'] = np.where(df.precipitation.str.contains('Fog'), 1, 0)
        df['precip_snow'] = np.where(df.precipitation.str.contains('Snow'), 1, 0)
        df = df.drop(columns=['precipitation'])
        
        # change floats to ints
        df.ac_mass = df.ac_mass.astype(int)
        df.num_engs = df.num_engs.astype(int)
        
        # write cached file
        df.to_csv(cache_file_name, index='date')
        print(f'{filename} found, read, and prepared')
    
    return (df)

# defining a function for the second iteration to prep for modeling
def prep_w_strike_df_for_modeling_mvp(df, target='damage_level'):
    """
    This function will drop columns I'm not using for modeling, and it 
    will make dummy columns for the categorical columns I'm moving forward to modeling with.
    It will return a df ready for modeling (except for scaling) with the target as the first column
    """
    # define columns to make into dummy columns
    keep_cols = ['size_of_species', 'ac_mass', 'ac_class', 'type_eng', 'num_engs', 'phase_of_flight'
                 , 'precip_none', 'precip_rain', 'precip_fog', 'precip_snow', 'speed']

    dummy_df = pd.get_dummies(df[keep_cols], drop_first=True)
    
    modeling_df = pd.concat([df[[target]], dummy_df], axis=1)
    return modeling_df

# defining a function to get scaled data using MinMaxScaler
def get_minmax_scaled (train, validate, test, columns_to_scale):
    """ 
    This function will
    - accept train, validate, test, and which columns are to be scaled
    - makes minmax scaler, fits scaler on train columns
    - returns 3 scaled dataframes; one for train/validate/test
    """
    # make copies for scaling
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    # make and fit minmax scaler
    scaler = MinMaxScaler()
    scaler.fit(train[columns_to_scale])

    # use the thing
    train_scaled[columns_to_scale] = scaler.transform(train[columns_to_scale])
    validate_scaled[columns_to_scale] = scaler.transform(validate[columns_to_scale])
    test_scaled[columns_to_scale] = scaler.transform(test[columns_to_scale])
    
    return train_scaled, validate_scaled, test_scaled
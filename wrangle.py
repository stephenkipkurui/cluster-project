###

# This module hold data preparations functions

###

from acquire import acquire_zillow
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn libraries
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


def drop_unwanted_columns(df, cols_to_drop):
    # This function removes unwanted columns
    
    df = df.drop(columns = cols_to_drop)
    
    return df

def rename_columns(df, cols_to_rename):
    # Renames columns
    
    df = df.rename(columns = cols_to_rename)
    
    return df


def drop_and_rename():
    
    df = acquire_zillow()
    
    # Columns to drop
    cols_to_drop = ['id', 'parcelid', 'airconditioningtypeid', 'finishedfloor1squarefeet', 
                'architecturalstyletypeid','buildingclasstypeid',
               'buildingqualitytypeid', 'decktypeid','finishedsquarefeet12', 
                'finishedsquarefeet13', 'finishedsquarefeet15',
               'finishedsquarefeet50', 'finishedsquarefeet6','heatingorsystemtypeid', 
                'pooltypeid10', 'pooltypeid2', 'pooltypeid7',
               'propertylandusetypeid','storytypeid','typeconstructiontypeid',
                'yardbuildingsqft17', 'yardbuildingsqft26', 'propertycountylandusecode', 
                'propertyzoningdesc', 'calculatedbathnbr']

    # Call function to drop unwanted cols
    df = drop_unwanted_columns(df, cols_to_drop )
    
    df['city'] = df.fips.replace({6037: 'Los Angeles', 6059:'Orange', 6111:'Ventura'})

    df = get_counties(df)

    df = create_features(df)
    
    
    df = rename_columns(df, {'basementsqft':'basement_sqft','bathroomcnt':'bath_cnt', 
                                     'bedroomcnt':'bed_cnt', 'calculatedfinishedsquarefeet':'calc_square_feet',
                                     'fips':'fips','fireplacecnt':'fire_place_cnt','fullbathcnt':'full_bath_cnt',
                                     'garagecarcnt':'garage_car_cnt',
                                     'garagetotalsqft':'garage_total_sqft','hashottuborspa':'has_hot_tub_or_spa', 
                                     'latitude':'lat', 'longitude':'longt', 'lotsizesquarefeet':'lot_size_sqft',
       
                                     'poolcnt':'pool_cnt', 'poolsizesum':'pool_size_sum',
                                     'rawcensustractandblock':'census_tract_and_block', 'regionidcity':'region_id_city',
       
                                     'regionidcounty':'region_id_county', 
                                     'regionidneighborhood':'region_id_neighborhood', 'regionidzip':'region_zip', 
                                     'roomcnt':'room_cnt',
       
                                     'threequarterbathnbr':'three_qtr_bath_nbr', 'unitcnt':'unit_cnt', 'yearbuilt':'year_built', 
                                     'numberofstories':'num_stories',
       
                                     'fireplaceflag':'fireplace_flag', 'structuretaxvaluedollarcnt':'structure_tax_value_cnt', 
                                     'taxvaluedollarcnt':'tax_value_cnt',
       
                                     'assessmentyear':'assessment_year', 'landtaxvaluedollarcnt':'land_tax_value_cnt', 
                                     'taxamount':'tax_amount',
       
                                     'taxdelinquencyflag':'tax_delinquency_flag', 'taxdelinquencyyear':'tax_delinquency_year', 
                                     'censustractandblock':'census_tract_block',
       
                                     'logerror':'log_error', 'transactiondate':'transaction_date', 
                                     'airconditioningdesc':'air_cond_desc',
       
                                     'architecturalstyledesc':'architect_style_desc', 'buildingclassdesc':'bldg_class_desc', 
                                     'heatingorsystemdesc':'heat_syst_desc',
       
                                     'propertylandusedesc':'prpty_land_use_desc', 'storydesc':'story_desc', 
                                     'typeconstructiondesc':'construction_desc'})

    return df
    
    


def get_counties(df):
    '''
    This function will create dummy variables out of the original fips column. 
    And return a dataframe with all of the original columns except regionidcounty.
    We will keep fips column for data validation after making changes. 
    New columns added will be 'LA', 'Orange', and 'Ventura' which are boolean 
    The fips ids are renamed to be the name of the county each represents. 
    '''
    # create dummy vars of fips id
    county_df = pd.get_dummies(df.fips)
    # rename columns by actual county name
    county_df.columns = ['la_county', 'orange_county', 'ventura_county']
    # concatenate the dataframe with the 3 county columns to the original dataframe
    df_dummies = pd.concat([df, county_df], axis = 1)
    # drop regionidcounty and fips columns
#     df_dummies = df_dummies.drop(columns = ['regionidcounty'])
    return df_dummies


def create_features(df):
    
    df['age'] = 2017 - df.yearbuilt
    
    df['age_bin'] = pd.cut(df.age, 
                           bins = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140],
                           labels = [0, .066, .133, .20, .266, .333, .40, .466, .533, 
                                     .60, .666, .733, .8, .866, .933])

    # create taxrate variable
    df['tax_rate'] = df.taxamount/df.taxvaluedollarcnt * 100

    # create acres variable
    df['acres'] = df.lotsizesquarefeet / 43560

    # bin acres
    df['acres_bin'] = pd.cut(df.acres, bins = [0, .10, .15, .25, .5, 1, 5, 10, 20, 50, 200], 
                       labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9])

    # square feet bin
    df['sqft_bin'] = pd.cut(df.calculatedfinishedsquarefeet, 
                            bins = [0, 800, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 7000, 12000],
                            labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
                       )
    # Bed Count
    df['bedrooms_bin'] =  pd.cut(df.bedroomcnt, 
                             bins = [0, 1, 2, 3, 4, 5, 6, 7, 8 ],
                             labels = [.1, .2, .3, .4, .5, .6, .7, .8]
                             )
    
#      # Bath Count
#     df['bathrooms_bin'] = pd.cut(df.bathroomcnt, 
#                              bins = [ 0, 1, 1.5, 2, 2.5 , 3, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5], 
#                              labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .10, .11, .12, .13, .14]
#                              )
    

    # dollar per square foot-structure
    df['structure_amount_per_sqft'] = df.structuretaxvaluedollarcnt/df.calculatedfinishedsquarefeet


    df['structure_amount_sqft_bin'] = pd.cut(df.structure_amount_per_sqft, 
                                             bins = [0, 25, 50, 75, 100, 150, 200, 300, 500, 1000, 1500],
                                             labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
                                            )


    # dollar per square foot-land
    df['land_amount_per_sqft'] = df.landtaxvaluedollarcnt/df.lotsizesquarefeet

    df['lot_amount_sqft_bin'] = pd.cut(df.land_amount_per_sqft, bins = [0, 1, 5, 20, 50, 100, 250, 500, 1000, 1500, 2000],
                                       labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
                                      )


    # update datatypes of binned values to be float
    df = df.astype({'sqft_bin': 'float64', 'acres_bin': 'float64', 'age_bin': 'float64',
                    'structure_amount_sqft_bin': 'float64', 'lot_amount_sqft_bin': 'float64',
                    'bedrooms_bin':'float64'
                   
                   })


    # ratio of bathrooms to bedrooms
    df['bath_bed_ratio'] = df.bathroomcnt / df.bedroomcnt

    # 12447 is the ID for city of LA. 
    # I confirmed through sampling and plotting, as well as looking up a few addresses.
    df['cola'] = df['regionidcity'].apply(lambda x: 1 if x == 12447.0 else 0)

    return df


def strip_outliers(df):
    '''
    remove outliers in Bath, bed, square feet, full bath, latitude, longitude, lot size, census track block
    region id city, region zip, unit count, year built, structure tax value, tax value count, land tax value count, 
    tax amount, census track block
    '''

    return df[(
               (df.bath_cnt <= 7.5) & 
               (df.bed_cnt <= 8) & 
               (df.structure_amount_sqft_bin < 12000) & 
               (df.full_bath_cnt < 6) & 
#                (df.lat < 3.48) & 
#                (df.longt > -1.1910) &
#                (df.lot_size_sqft < 1) & 
               (df.unit_cnt < 1.25) & 
               (df.year_built > 1910) & 
               (df.land_tax_value_cnt < 2) & 
               (df.tax_amount <= 300000) 
              )]


def split_data(df):
    # This function spits the data and returns the train, validate and test set
    
    train_and_validate, test = train_test_split(df, random_state=123, test_size=.2)
    train, validate = train_test_split(train_and_validate, random_state=123, test_size=.2)

    print('Train: %d rows, %d cols' % train.shape)
    print('Validate: %d rows, %d cols' % validate.shape)
    print('Test: %d rows, %d cols' % test.shape)

    return train, validate, test


def nulls_by_columns(df):
    # Function return nulls by columns
    return pd.concat([
        df.isna().sum().rename('count'),
        df.isna().mean().rename('percent')
    ], axis=1)

def nulls_by_rows(df):
    # Function return nulls by rows
    
    return pd.concat([
        df.isna().sum(axis=1).rename('num_missing'),
        df.isna().mean(axis=1).rename('percent_missing'),
    ], axis=1).value_counts().sort_index()

def handle_missing_values(df, prop_required_column = .6, prop_required_row = .75):
    # Handle missing values. Drop cols with null > 70% and rows > 75%
    
    threshold = int(round(prop_required_column * len(df.index), 0))
    df.dropna(axis = 1, thresh = threshold, inplace = True)
    threshold = int(round(prop_required_row * len(df.columns), 0))
    df.dropna(axis = 0, thresh = threshold, inplace = True)
    return df


def scale_data(train, validate, test):
    # Scaling function 
    
    columns_to_scale = ['bath_cnt','bed_cnt','age', 'lot_size_sqft','calc_square_feet',  'tax_amount']
    
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()

    scaler = MinMaxScaler()
    scaler.fit(train[columns_to_scale])

    train_scaled[columns_to_scale] = scaler.transform(train[columns_to_scale])
    validate_scaled[columns_to_scale] = scaler.transform(validate[columns_to_scale])
    test_scaled[columns_to_scale] = scaler.transform(test[columns_to_scale])

    return train_scaled, validate_scaled, test_scaled



def acquire_modeling_data(scale_data = False):
    # Function return scaled, encoded data for modeling
    
    df = acquire_zillow() # get zillow data
    
    df = one_hot_encode(df) # encoding
    
    train, validate, test = split_data(df) #split data
    
    if scale_data:
        
        return scale(train, validate, test)
    
    else:
        return train, validate, test
    
    
 



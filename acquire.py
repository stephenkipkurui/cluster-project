import imp
import re
import pandas as pd
import env
import os


def db_connect():

    db = 'zillow'

    url = f'mysql+pymysql://{env.username}:{env.password}@{env.host}/{db}'

    return url


def acquire_zillow(use_cache = True):

    zillow_file = 'zillow.csv'

    if os.path.exists(zillow_file) and use_cache:

        print('Status: Acquiring data from csv file..')

        return pd.read_csv(zillow_file)

    query = '''
    
        SELECT
    prop.*,
    predictions_2017.logerror,
    predictions_2017.transactiondate,
    air.airconditioningdesc,
    arch.architecturalstyledesc,
    build.buildingclassdesc,
    heat.heatingorsystemdesc,
    landuse.propertylandusedesc,
    story.storydesc,
    construct.typeconstructiondesc
    FROM properties_2017 prop
    JOIN (
        SELECT parcelid, MAX(transactiondate) AS max_transactiondate
        FROM predictions_2017
        GROUP BY parcelid
        ) pred USING(parcelid)
    JOIN predictions_2017 ON pred.parcelid = predictions_2017.parcelid
                      AND pred.max_transactiondate = predictions_2017.transactiondate
    LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
    LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
    LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
    LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid)
    LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid)
    LEFT JOIN storytype story USING (storytypeid)
    LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid)
    WHERE prop.latitude IS NOT NULL
      AND prop.longitude IS NOT NULL
      AND transactiondate <= '2017-12-31'
      AND ((landuse.propertylandusedesc = 'Single Family Residential')
      OR (landuse.propertylandusedesc = 'Mobile Home')
          OR (landuse.propertylandusedesc = 'Manufactured, Modular, Prefabricated Homes'))
          
        '''
    
    print('Status: Acquiring data from SQL database..')

    zillow = pd.read_sql(query, db_connect())

    print('Status: Saving csv locally..')

    zillow.to_csv(zillow_file, index = False)

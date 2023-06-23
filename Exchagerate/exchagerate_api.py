import requests
import pandas as pd

from sqlalchemy import create_engine

class Exchagerate_APIConn_Daily:
    """
    1. Creates connection with 'api.exchangeratesapi.io' for data download
    2. Json data transformed into CSV structure
    3. Creates DB connection for data upload
    """
    
    def __init__(self, start_date):
        self.start_date = start_date 
        self._api_key = "api_key"
        self.api_url = 'http://api.exchangeratesapi.io/v1/'
        self.target_url = self.api_url + self.start_date + f'?access_key={self._api_key}'
        self.raw_data = {}
        self.currency = ['GBP','USD','EUR']
        self.output_data = None
        
    def get_raw_data(self):
        """
        Extracts data from the API endpoint.

        :returns: Data from the API endpoint as dict
        :raises HTTPError: raises an exception 
        """
        for item in self.currency:
            data_request = requests.get(self.target_url + f'&base={item}')
            if data_request.status_code == 200:
                self.raw_data.update({f'{item}': data_request.json()})
            else:
                raise Exception(f'API request failed with status code {request_result.status_code}')
        return self.raw_data
    
    def transform_raw_data(self):
        '''
        Transform data from dictionary to dataframe structure 

        :returns: pd.DataFrame()
        '''
        
        dfs = []
        for key, value in self.raw_data.items():
            _df = pd.DataFrame(value, columns=("base", "rates", "date")).reset_index().rename(columns = {'index':"currency",
                                                                                               'rates':'conversion rates'})
            dfs.append(_df)
            
        self.output_data = pd.concat(dfs)
        return self.output_data
            
    def save_as_csv(self):
        self.output_data.to_csv(f"{self.start_date}_conversion_rates.csv")
        
        
    def upload_to_DB(self):
        engine = create_engine('sqlite:///conversion_rates.db', echo=True)
        sqlite_connection = engine.connect()
        sqlite_table = f'rates_{self.start_date}'
        self.output_data.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
        
            
class Exchagerate_APIConn_Timerange(Exchagerate_APIConn_Daily):
    def __init__(self, start_date, end_date):
        super().__init__(start_date)
        self.end_date = end_date
        self.endpoint = 'timeseries'
        self.target_url = self.api_url + self.endpoint + f'?access_key={self._api_key}' + f'&start_date={self.start_date}' + f'&end_date={self.start_date}'
        
    def save_as_csv(self):
        self.output_data.to_csv(f"{self.start_date} - {self.end_date}_conversion_rates.csv")
        

if __name__ == '__main__':
    day = input('Enter the date (YYYY-MM-DD) for exchange rates data request: ')
    api_obj = Exchagerate_APIConn_Daily(day)
    api_obj.get_raw_data()
    api_obj.transform_raw_data()
    
    print('Conversion_rates were successfully downloaded from Exchangeratesapi.io')
    
    save_option = "Save"
    upload_option = "Upload"
    
    choice = input(f"Do you want to save the file ({save_option}) or upload it into a database ({upload_option})? ")
    
    if choice == save_option:
        api_obj.get_raw_data()
    elif choice == upload_option:
        api_obj.upload_to_DB()
    else:
        raise ValueError("Invalid choice.")

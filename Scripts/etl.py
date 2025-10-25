# Packages
import requests as req # this library is used for requeting from an API
import pandas as pd
from sqlalchemy import create_engine as center # we can use this package also to connect to DB
import mysql.connector # lets try using this
import os
from datetime import datetime as dt

# ETL class definition
class ETL  : 
    
  def __init__(self , api_key , db_config , api_url , cities) -> None :
      
    '''
        Here we recieve the DB  Connection parameters , API key , API url
        as an input from the user 
    '''
    self.api_key = api_key
    self.api_url = api_url
    self.cities = cities
    self.db_config = db_config
      
  def connect_to_DB(self) : 
      
    '''
    Here we connect with the DB, the DB used is MySql DB where we store the end data
    '''
    try : 
      conn = mysql.connector.connect(**self.db_config) # ** here is called the dictionary unpacking operator in python it expands the dictionary into keyword arguments automatically
      return conn
    except mysql.connector.Error as e:
      print(f"❌ Error connecting to database: {e}")
      return None

  def extract(self):
      
        #The extraction logic 
    
    weather_data = [] # We use a list to collect the end result of extraction

    for city in self.cities: # we Iterate through the list of cities and retrive the data for each city 
      url = f"{self.api_url}?q={city}&appid={self.api_key}&units=metric" # API
      try:
        response = req.get(url, timeout=10) # Get the response from the url
        response.raise_for_status() # check for the status code 
        data = response.json() # recieve the data in json format

        coord = data.get("coord", {})
        main = data.get("main", {})
        wind_data = data.get("wind", {})
        
        #Append the data in to the list
        weather_data.append({  
            "city": city,
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "minTemp": main.get("temp_min"),
            "maxTemp": main.get("temp_max"),
            "pressure": main.get("pressure"),
            "humidity": main.get("humidity"),
            "visibility": data.get("visibility"),
            "wind_speed": round(wind_data.get("speed", 0) * 3.6, 2),  # m/s → km/h
            "wind_deg": wind_data.get("deg"),
            "sea_level": main.get("sea_level"),
            "grnd_level": main.get("grnd_level"),
            "time_stamp": dt.now(),
            "data_source": "OpenWeatherMap"
        })

      except Exception as e: # handle exception if the status code fails
          print(f"⚠️ Unable to get data for {city}: {e}")

    df = pd.DataFrame(weather_data) # convert the list data into data frame
    df.to_csv("Indian_City_Weather.csv", index=False) # cover the dataframe into a csv
    print("✅ Weather data saved successfully.")
    return df


  def transform(self , df) :
    # Transformation logic 
# Basic Cleaninfg
    # 1.Round numerical colummns
    df = df.apply(pd.to_numeric, errors="ignore")
    df = df.round(2)
    # 2.Handle missing value
    df = df.fillna(method = "ffill" )
    # 3.Rename columns
    df = df.rename(columns = {"minTemp" : "min_Temp" , "maxTemp" : "max_Temp"})
# Unit Conversions
    # 4.Handle unit conversions
    df["temperature"] = df["temperature"].apply(lambda x : (x * 9/5) + 32)
    df["min_Temp"] = df["min_Temp"].apply(lambda x : (x * 9/5) + 32)
    df["max_Temp"] = df["max_Temp"].apply(lambda x : (x * 9/5) + 32)
    # 5.hPa----> atm
    df["pressure"] = df["pressure"].apply(lambda x : x / 1013.25) 
# Feature Engineering
    # 6.Derive columns (example temp_range = max_Temp - min_Temp)
    df["temp_range"] = df["max_Temp"] - df["min_Temp"]
    # 7.Humidity Category
    df["humidity_category"] = df["humidity"].apply(lambda x : "Humid" if x > 80 else "Moderate" if x > 50 else "Dry")
    # 8.Temp deviation
    df["temp_deviation"] = df["temperature"] - df["feels_like"]
    # 9.altitude pressure difference
    if "sea_level" in df.columns and "grnd_level" in df.columns :
        df["altitude_pressure_diff"] = df["sea_level"] - df["grnd_level"]
    else : df["altitude_pressure_diff"] = None
# Categorization
    # 10.Temperature
    df["Temperature_category"] = df["temperature"].apply(lambda p : "Cold" if p < 68 else "Moderate" if 68 <= p < 86 else "Hot")
    # 11.Pressure
    df["pressure_category"] = df["pressure"].apply(lambda p : "Low" if p < 0.98 else "Normal" if 0.98 <= p <= 1.02 else "High")
    return df
              
              
  def load(self , df) : 
      
    # Load logic
    
    # get the db connection 
    conn = self.connect_to_DB()
    if conn is None:
      print("❌ Load aborted. No database connection.")
      return
    cursor = conn.cursor()
    
    # Inserting data into city table
    try : 
      for _ , row in df.iterrows() : 
        cursor.execute("""
            insert ignore into city (city , latitude , longitude) values(%s , %s , %s)""" , (row["city"] , row["latitude"] , row["longitude"]))
        
        
        # Inserting data into weather_fact table
      for _ , row in df.iterrows() : 
        # get city_id for FK mapping
        cursor.execute("select city_id from city where city = %s" , (row["city"] , ))
        city_result = cursor.fetchone()
        if city_result : 
          city_id = city_result[0]
        else : 
          continue
        
        cursor.execute("""
            
            insert into weather_fact(city_id ,
                                      temperature , 
                                      feels_like ,
                                      min_Temp , 
                                      max_Temp , 
                                      humidity , 
                                      pressure , 
                                      wind_speed , 
                                      visibility , 
                                      temp_range , 
                                      temp_deviation , 
                                      altitude_pressure_diff , 
                                      humidity_category , 
                                      temperature_category , 
                                      pressure_category)
            values(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)
        
        """ , (city_id, row["temperature"], row["feels_like"],
        row["min_Temp"], row["max_Temp"],
        row["humidity"], row["pressure"], row["wind_speed"],
        row["visibility"], row["temp_range"], row["temp_deviation"],
        row.get("altitude_pressure_diff"),
        row["humidity_category"], row["temperature_category"],
        row["pressure_category"]
          
          ))
          
          
      conn.commit()
      print("✅ Data loaded into MySql Successfully.")
        
    except mysql.connector.Error as e : 
      print(f"❌ MySql error : {e}")
      conn.rollback()
    finally : 
      cursor.close()
      conn.close()
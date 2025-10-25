create table if not exists city
(
	city_id int auto_increment primary key , 
    city varchar(100) unique , 
    latitude float , 
    longitude float
);


create table if not exists weather_fact
(
	record_id int auto_increment primary key , 
    city_id int ,
    time_stamp datetime default current_timestamp ,
    temperature float , 
    feels_like float , 
    min_temp float , 
    max_temp float , 
    humidity float , 
    pressure float , 
    wind_speed float , 
    visibility float , 
    temp_range float , 
    temp_deviation float , 
    altitude_pressure_diff float , 
    humidity_category varchar(20) , 
    temperature_category varchar(20) , 
    pressure_category varchar(20) , 
    foreign key (city_id) references city(city_id)   
);


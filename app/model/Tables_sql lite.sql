create table users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name varchar(50) not null, user_email varchar(50) not null, user_password varchar(50) not null, 
age int not null, country varchar(20) not null, time_to_read int, old_news_interest varchar(50), local_news_interest varchar(50), popular_tweets_interest varchar(50));

select * from users;

create table topic_preferences(id INTEGER  PRIMARY KEY AUTOINCREMENT, user_id int not null, topic_type varchar(50) not null, topic_name varchar(50) not null, interest_level varchar(50) not null, FOREIGN KEY (user_id) REFERENCES users(id));

select * from topic_preferences;

create table news_source_preferences(id INTEGER  PRIMARY KEY AUTOINCREMENT, user_id int not null, source_name varchar(50) not null, interest_level varchar(50) not null, FOREIGN KEY (user_id) REFERENCES users(id));

select * from news_source_preferences;

delete from news_source_preferences;

delete from topic_preferences;

delete from users;

delete from sqlite_sequence;



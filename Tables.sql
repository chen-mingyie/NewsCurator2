create table users (id int not null AUTO_INCREMENT, user_name varchar(50) not null, user_email varchar(50) not null, user_password varchar(50) not null, 
age int not null, country varchar(20) not null, time_to_read int, old_news_interest varchar(50), local_news_interest varchar(50), popular_tweets_interest varchar(50), PRIMARY KEY (id));

select * from users;

create table topic_preferences(id int not null AUTO_INCREMENT, user_id int not null, topic_type varchar(50) not null, topic_name varchar(50) not null, interest_level varchar(50) not null, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));

select * from topic_preferences;

create table news_source_preferences(id int not null AUTO_INCREMENT, user_id int not null, source_name varchar(50) not null, interest_level varchar(50) not null, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));

select * from news_source_preferences;

SET SQL_SAFE_UPDATES=0;
drop table news_source_preferences;
create table news_source_preferences(id int not null AUTO_INCREMENT, user_id int not null, source_name varchar(50) not null, interest_level varchar(50) not null, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));

drop table topic_preferences;
create table topic_preferences(id int not null AUTO_INCREMENT, user_id int not null, topic_type varchar(50) not null, topic_name varchar(50) not null, interest_level varchar(50) not null, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));

drop table users;
create table users (id int not null AUTO_INCREMENT, user_name varchar(50) not null, user_email varchar(50) not null, user_password varchar(50) not null, 
age int not null, country varchar(20) not null, time_to_read int, old_news_interest varchar(50), local_news_interest varchar(50), popular_tweets_interest varchar(50), PRIMARY KEY (id));

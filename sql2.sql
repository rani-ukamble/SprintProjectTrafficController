-- use oes;

-- select * from users; 

-- users
-- id, email, pass, date
-- url - mongo only

-- status codes - api

-- /signin
-- json web token, id, email,  date 


USE trafficcontroller; 

CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    date DATE NOT NULL
);

insert into users values (4, "rani@email.com", "234", "2023-12-03"); 




use veg;
show tables;



CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    mobile VARCHAR(15) UNIQUE,
    password VARCHAR(50)
);


CREATE TABLE vegetables (
    veg_id INT AUTO_INCREMENT PRIMARY KEY,
    veg_name VARCHAR(50),
    quantity INT,
    sell_price INT,
    cost_price INT
);


CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    veg_name VARCHAR(50),
    quantity INT,
    price INT
);


CREATE TABLE sales_history (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(50),
    mobile VARCHAR(15),
    veg_name VARCHAR(50),
    quantity INT,
    sell_price INT,
    cost_price INT,
    total_price INT,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
 select * from users ;
 select * from vegetables;
 select * from cart;
 select * from sales_history;
 
 
 
 







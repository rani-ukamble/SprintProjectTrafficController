CREATE DATABASE trafficcontroller;
USE trafficcontroller; 



-- Table: traffic_signals
CREATE TABLE traffic_signals (
    signal_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(255),
    signal_state ENUM('RED', 'YELLOW', 'GREEN') ,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Table: vehicles
CREATE TABLE vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_number VARCHAR(20) NOT NULL UNIQUE,
    owner_name VARCHAR(255) ,
    vehicle_type VARCHAR(50) ,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: violations
CREATE TABLE violations (
    violation_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT,
    signal_id INT,
    violation_type VARCHAR(255) ,
    violation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fine_amount DECIMAL(10, 2) ,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (signal_id) REFERENCES traffic_signals(signal_id)
);



ALTER TABLE violations 
DROP FOREIGN KEY violations_ibfk_2;

ALTER TABLE violations 
ADD CONSTRAINT violations_ibfk_2 
FOREIGN KEY (signal_id) REFERENCES traffic_signals(signal_id) 
ON DELETE SET NULL;





-- Table: cameras
CREATE TABLE cameras (
    camera_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(255),
    camera_feed_url VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: sensor_data
CREATE TABLE sensor_data (
    sensor_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    traffic_count INT ,
    average_speed DECIMAL(5, 2) ,
    traffic_condition VARCHAR(255)
);

-- Table: fines
CREATE TABLE fines (
    fine_id INT PRIMARY KEY AUTO_INCREMENT,
    violation_id INT ,
    fine_status ENUM('PAID', 'UNPAID') ,
    payment_date TIMESTAMP,
    FOREIGN KEY (violation_id) REFERENCES violations(violation_id)
);   


-- *************************************************** 

-- Sample data for vehicles
INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type)
VALUES 
('ABC123', 'John Doe', 'Sedan'),
('XYZ789', 'Jane Smith', 'SUV'),
('LMN456', 'Mike Johnson', 'Truck'),
('PQR321', 'Sara Lee', 'Motorcycle');

-- Sample data for traffic signals
INSERT INTO traffic_signals (location, signal_state)
VALUES 
('Main Street & 1st Ave', 'Red'),
('Elm St & Oak Rd', 'Green'),
('Broadway & 5th Ave', 'Yellow');

-- Sample data for violations
INSERT INTO violations (vehicle_id, signal_id, violation_type, fine_amount)
VALUES 
(1, 1, 'Red Light Jump', 150.00),
(2, 2, 'Speeding', 200.00);

-- Sample data for fines
INSERT INTO fines (violation_id, fine_status)
VALUES 
(1, 'Unpaid'),
(2, 'Paid');

-- Sample data for sensor data
INSERT INTO sensor_data (location, traffic_count, average_speed, traffic_condition)
VALUES 
('Main Street', 250, 45.6, 'Moderate'),
('5th Avenue', 180, 40.0, 'Heavy'),
('Oak Road', 300, 50.0, 'Clear');

-- Sample data for cameras
INSERT INTO cameras (location, camera_feed_url)
VALUES 
('Main Street Camera 1', 'http://s3.amazonaws.com/camera1_feed'),
('5th Avenue Camera 2', 'http://s3.amazonaws.com/camera2_feed');


SELECT * FROM cameras;   
-- ***************************************************************************


use trafficcontrol;
ALTER TABLE fines
MODIFY COLUMN payment_date TIMESTAMP NULL DEFAULT NULL;
 
DELIMITER $$
 
CREATE TRIGGER set_payment_date_on_insert
BEFORE INSERT ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$
 
DELIMITER ;
 
DELIMITER $$
 
CREATE TRIGGER set_payment_date_on_update
BEFORE UPDATE ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$
 
DELIMITER ; 




select * from users;





CREATE DATABASE Delivery_System;
USE Delivery_System;
# DROP DATABASE Delivery_System;

CREATE TABLE Countries (
	CountryCode INT AUTO_INCREMENT PRIMARY KEY,
    CountryName VARCHAR(100)
);
CREATE TABLE Cities(
	CityCode INT AUTO_INCREMENT PRIMARY KEY,
    CityName VARCHAR(100),
    CountryCode INT references Countries(CountryCode)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerName VARCHAR(100),
    PhoneNumber VARBINARY(255),
    Address VARBINARY(255),
    City INT REFERENCES Cities(CityCode)
);

CREATE TABLE Vehicles (
    VehicleID INT PRIMARY KEY AUTO_INCREMENT,
    VehicleType ENUM('motorbike', 'train', 'plane', 'ship', 'other'),
    LicensePlate VARCHAR(20),
    Status ENUM('available', 'n/a') default 'available'
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATE,
    DeliveryFailCount INT default 0,
    Status ENUM('ordered', 'in transit', 'successful', 'failed') default 'ordered',
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Deliveries (
    DeliveryID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    VehicleID INT,
    DeliveryEndDate DATE Default NULL,
    Status ENUM('transit warehouse', 'transit customer', 'successful', 'failed'),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);

# SELECT * FROM Deliveries;
CREATE TABLE Expenses (
    ExpenseID INT PRIMARY KEY AUTO_INCREMENT,
    DeliveryID INT,
    ExpenseType ENUM('toll', 'fee', 'fuel', 'handling', 'other'),
    Amount DECIMAL(10,2),
    FOREIGN KEY (DeliveryID) REFERENCES Deliveries(DeliveryID)
);

INSERT INTO Countries (CountryName) VALUES
('Brunei'), ('Cambodia'), ('China'), ('Indonesia'), ('Japan'), 
('South Korea'), ('Laos'), ('Malaysia'), ('Mongolia'), ('Myanmar'),
('Phillipines'), ('Singapore'), ('Thailand'), ('Taiwan'), ('Vietnam');
# SELECT * FROM Countries;
-- Brunei
INSERT INTO Cities (CityName, CountryCode) VALUES
('Bandar Seri Begawan', (SELECT CountryCode FROM Countries WHERE CountryName = 'Brunei')),
('Kuala Belait', (SELECT CountryCode FROM Countries WHERE CountryName = 'Brunei')),
('Seria', (SELECT CountryCode FROM Countries WHERE CountryName = 'Brunei'));

-- Cambodia
INSERT INTO Cities (CityName, CountryCode) VALUES
('Phnom Penh', (SELECT CountryCode FROM Countries WHERE CountryName = 'Cambodia')),
('Siem Reap', (SELECT CountryCode FROM Countries WHERE CountryName = 'Cambodia')),
('Battambang', (SELECT CountryCode FROM Countries WHERE CountryName = 'Cambodia')),
('Sihanoukville', (SELECT CountryCode FROM Countries WHERE CountryName = 'Cambodia'));

-- China
INSERT INTO Cities (CityName, CountryCode) VALUES
('Beijing', (SELECT CountryCode FROM Countries WHERE CountryName = 'China')),
('Shanghai', (SELECT CountryCode FROM Countries WHERE CountryName = 'China')),
('Guangzhou', (SELECT CountryCode FROM Countries WHERE CountryName = 'China')),
('Shenzhen', (SELECT CountryCode FROM Countries WHERE CountryName = 'China')),
('Chengdu', (SELECT CountryCode FROM Countries WHERE CountryName = 'China')),
('Xi\'an', (SELECT CountryCode FROM Countries WHERE CountryName = 'China'));

-- Indonesia
INSERT INTO Cities (CityName, CountryCode) VALUES
('Jakarta', (SELECT CountryCode FROM Countries WHERE CountryName = 'Indonesia')),
('Surabaya', (SELECT CountryCode FROM Countries WHERE CountryName = 'Indonesia')),
('Bandung', (SELECT CountryCode FROM Countries WHERE CountryName = 'Indonesia')),
('Medan', (SELECT CountryCode FROM Countries WHERE CountryName = 'Indonesia')),
('Yogyakarta', (SELECT CountryCode FROM Countries WHERE CountryName = 'Indonesia'));

-- Japan
INSERT INTO Cities (CityName, CountryCode) VALUES
('Tokyo', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan')),
('Osaka', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan')),
('Kyoto', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan')),
('Yokohama', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan')),
('Fukuoka', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan')),
('Sapporo', (SELECT CountryCode FROM Countries WHERE CountryName = 'Japan'));

-- South Korea
INSERT INTO Cities (CityName, CountryCode) VALUES
('Seoul', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea')),
('Busan', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea')),
('Incheon', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea')),
('Daegu', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea')),
('Daejeon', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea')),
('Gwangju', (SELECT CountryCode FROM Countries WHERE CountryName = 'South Korea'));

-- Laos
INSERT INTO Cities (CityName, CountryCode) VALUES
('Vientiane', (SELECT CountryCode FROM Countries WHERE CountryName = 'Laos')),
('Luang Prabang', (SELECT CountryCode FROM Countries WHERE CountryName = 'Laos')),
('Pakse', (SELECT CountryCode FROM Countries WHERE CountryName = 'Laos')),
('Savannakhet', (SELECT CountryCode FROM Countries WHERE CountryName = 'Laos'));

-- Malaysia
INSERT INTO Cities (CityName, CountryCode) VALUES
('Kuala Lumpur', (SELECT CountryCode FROM Countries WHERE CountryName = 'Malaysia')),
('George Town', (SELECT CountryCode FROM Countries WHERE CountryName = 'Malaysia')),
('Johor Bahru', (SELECT CountryCode FROM Countries WHERE CountryName = 'Malaysia')),
('Kota Kinabalu', (SELECT CountryCode FROM Countries WHERE CountryName = 'Malaysia')),
('Kuching', (SELECT CountryCode FROM Countries WHERE CountryName = 'Malaysia'));

-- Mongolia
INSERT INTO Cities (CityName, CountryCode) VALUES
('Ulaanbaatar', (SELECT CountryCode FROM Countries WHERE CountryName = 'Mongolia')),
('Erdenet', (SELECT CountryCode FROM Countries WHERE CountryName = 'Mongolia')),
('Darkhan', (SELECT CountryCode FROM Countries WHERE CountryName = 'Mongolia')),
('Choibalsan', (SELECT CountryCode FROM Countries WHERE CountryName = 'Mongolia'));

-- Myanmar
INSERT INTO Cities (CityName, CountryCode) VALUES
('Naypyidaw', (SELECT CountryCode FROM Countries WHERE CountryName = 'Myanmar')),
('Yangon', (SELECT CountryCode FROM Countries WHERE CountryName = 'Myanmar')),
('Mandalay', (SELECT CountryCode FROM Countries WHERE CountryName = 'Myanmar')),
('Bago', (SELECT CountryCode FROM Countries WHERE CountryName = 'Myanmar'));

-- Philippines
INSERT INTO Cities (CityName, CountryCode) VALUES
('Manila', (SELECT CountryCode FROM Countries WHERE CountryName = 'Phillipines')),
('Quezon City', (SELECT CountryCode FROM Countries WHERE CountryName = 'Phillipines')),
('Davao City', (SELECT CountryCode FROM Countries WHERE CountryName = 'Phillipines')),
('Cebu City', (SELECT CountryCode FROM Countries WHERE CountryName = 'Phillipines')),
('Zamboanga City', (SELECT CountryCode FROM Countries WHERE CountryName = 'Phillipines'));

-- Singapore
INSERT INTO Cities (CityName, CountryCode) VALUES
('Singapore', (SELECT CountryCode FROM Countries WHERE CountryName = 'Singapore'));

-- Thailand
INSERT INTO Cities (CityName, CountryCode) VALUES
('Bangkok', (SELECT CountryCode FROM Countries WHERE CountryName = 'Thailand')),
('Chiang Mai', (SELECT CountryCode FROM Countries WHERE CountryName = 'Thailand')),
('Pattaya', (SELECT CountryCode FROM Countries WHERE CountryName = 'Thailand')),
('Phuket', (SELECT CountryCode FROM Countries WHERE CountryName = 'Thailand')),
('Nakhon Ratchasima', (SELECT CountryCode FROM Countries WHERE CountryName = 'Thailand'));

-- Taiwan
INSERT INTO Cities (CityName, CountryCode) VALUES
('Taipei', (SELECT CountryCode FROM Countries WHERE CountryName = 'Taiwan')),
('Kaohsiung', (SELECT CountryCode FROM Countries WHERE CountryName = 'Taiwan')),
('Taichung', (SELECT CountryCode FROM Countries WHERE CountryName = 'Taiwan')),
('Tainan', (SELECT CountryCode FROM Countries WHERE CountryName = 'Taiwan')),
('Hsinchu', (SELECT CountryCode FROM Countries WHERE CountryName = 'Taiwan'));

-- Vietnam
INSERT INTO Cities (CityName, CountryCode) VALUES
('Hanoi', (SELECT CountryCode FROM Countries WHERE CountryName = 'Vietnam')),
('Ho Chi Minh City', (SELECT CountryCode FROM Countries WHERE CountryName = 'Vietnam')),
('Da Nang', (SELECT CountryCode FROM Countries WHERE CountryName = 'Vietnam')),
('Can Tho', (SELECT CountryCode FROM Countries WHERE CountryName = 'Vietnam')),
('Hai Phong', (SELECT CountryCode FROM Countries WHERE CountryName = 'Vietnam'));


INSERT INTO Customers (CustomerName, PhoneNumber, Address, City) VALUES
('Alice Tran', '0901234567', '123 Nguyen Hue, District 1', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Bob Nguyen', '0902345678', '45 Le Loi, District 3', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Cindy Le', '0903456789', '88 Tran Hung Dao, District 5', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('David Pham', '0904567890', '12 District 7', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Singapore')),
('Emily Vo', '0905678901', '67 3 Thang 2, District 10', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Frank Bui', '0906789012', '56 Vo Van Kiet, District 2', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Grace Ho', '0907890123', '34 Ton Duc Thang, District 4', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Henry Lam', '0908901234', '78 Pham Ngu Lao, District 6', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Ivy Dang', '0909012345', '90 CMT8, District 9', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Ho Chi Minh City')),
('Jacky Do', '0910123456', '10 Ly Thuong Kiet', 
    (SELECT CityCode FROM Cities WHERE CityName = 'Hanoi'));


INSERT INTO Vehicles (VehicleType, LicensePlate) VALUES
('motorbike', '59X1-123.45'),
('ship', 'VN-SH-4567'),
('plane', 'VN-A888'),
('motorbike', '59Y2-678.90'),
('train', 'VNR-998'),
('plane', 'VN-B999'),
('ship', 'VN-SH-0001'),
('motorbike', '59Z3-890.12'),
('other', 'VEH-1001'),
('train', 'VNR-1002');

INSERT INTO Orders (CustomerID, OrderDate, Status) VALUES
(1, '2024-04-20', 'ordered'),
(2, '2024-04-21', 'ordered'),
(3, '2024-04-22', 'ordered'),
(4, '2024-04-23', 'ordered'),
(5, '2024-04-24', 'ordered'),
(6, '2024-04-25', 'ordered'),
(7, '2024-04-25', 'ordered'),
(8, '2024-04-26', 'ordered'),
(9, '2024-04-26', 'ordered'),
(10, '2024-04-27', 'ordered');


INSERT INTO Deliveries (OrderID, VehicleID, Status) VALUES
(1, 1, 'transit warehouse'),
(2, 2, 'transit customer'),
(3, 3, 'transit warehouse'),
(4, 4, 'transit warehouse'),
(5, 5, 'transit warehouse'),
(6, 6, 'transit warehouse'),
(7, 7, 'transit warehouse'),
(8, 8, 'transit warehouse'),
(9, 9, 'transit warehouse'),
(10, 10, 'transit customer');

# SET SQL_SAFE_UPDATES = 0;
INSERT INTO Expenses (DeliveryID, ExpenseType, Amount) VALUES
(1, 'fuel', 150.00),
(1, 'toll', 30.00),
(2, 'fuel', 200.00),
(3, 'fee', 50.00),
(4, 'fuel', 180.00),
(5, 'handling', 40.00),
(6, 'fuel', 170.00),
(7, 'fee', 20.00),
(8, 'fuel', 160.00),
(9, 'other', 25.00); 

CREATE INDEX idx_deliveries_orderid ON Deliveries(OrderID);
CREATE INDEX idx_orders_status ON Orders(Status);
CREATE INDEX idx_deliveries_vehicleid ON Deliveries(VehicleID);

CREATE VIEW CurrentDeliverySchedule AS
SELECT 
    d.DeliveryID, c.CustomerName, o.OrderDate,
    v.VehicleType, v.LicensePlate
FROM Deliveries d
JOIN Orders o ON d.OrderID = o.OrderID
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Vehicles v ON d.VehicleID = v.VehicleID
WHERE o.Status = 'in transit';
# SELECT * FROM CurrentDeliverySchedule;

#DROP VIEW ShipperView;
CREATE VIEW ShipperCustomerView AS
SELECT 
d.DeliveryID,
c.CustomerName,
c.PhoneNumber, 
c.Address,
Cities.CityName,
Countries.CountryName,
v.VehicleType,
v.LicensePlate,
d.Status AS DeliveryStatus
FROM Deliveries d
JOIN Orders o ON d.OrderID = o.OrderID
JOIN Customers c ON c.CustomerID = o.CustomerID
JOIN Vehicles v ON v.VehicleID = d.VehicleID
JOIN Cities ON Cities.CityCode = c.City
JOIN Countries ON Countries.CountryCode = Cities.CountryCode
WHERE d.Status = 'transit customer';

CREATE VIEW ShipperWarehouseView AS
SELECT 
d.DeliveryID,
v.VehicleType,
v.LicensePlate,
d.Status AS DeliveryStatus
FROM Deliveries d
JOIN Orders o ON d.OrderID = o.OrderID
JOIN Vehicles v ON v.VehicleID = d.VehicleID
WHERE d.Status = 'transit warehouse';

CREATE VIEW OrderCostSummary AS
SELECT 
    o.OrderID,
    SUM(e.Amount) AS TotalCost
FROM Orders o
JOIN Deliveries d ON o.OrderID = d.OrderID
JOIN Expenses e ON d.DeliveryID = e.DeliveryID
GROUP BY o.OrderID;
# SELECT * FROM OrderCostSummary;

CREATE VIEW OutstandingOrders AS
SELECT * FROM Orders
WHERE Status IN ('ordered', 'in transit');
# SELECT * FROM OutstandingOrders;

DELIMITER $$
CREATE PROCEDURE GetTotalExpenses(
    IN p_order_id INT,
    OUT p_total DECIMAL(10,2)
)
BEGIN
    SELECT TotalCost
    INTO p_total
    FROM OrderCostSummary s
    WHERE s.OrderID = p_order_id;
END $$
DELIMITER ;

#DROP PROCEDURE AssignDelivery;
DELIMITER $$
CREATE PROCEDURE AssignDelivery(
    IN p_order_id INT,
    IN p_vehicle_id INT
)
BEGIN
	INSERT INTO Deliveries(OrderID, VehicleID)
	VALUES (p_order_id, p_vehicle_id);    
	
    UPDATE Orders SET Status = 'in transit'
	WHERE OrderID = p_order_id;
    
    UPDATE Vehicles SET Status = 'n/a'
    WHERE VehicleID = p_vehicle_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER UpdateSuccessfulOrder
AFTER UPDATE ON Deliveries
FOR EACH ROW
BEGIN
    IF NEW.Status = 'successful' AND OLD.Status = 'transit customer' THEN
        UPDATE Orders
        SET Status = 'successful'
        WHERE OrderID = NEW.OrderID;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CountFailDelivery
AFTER UPDATE ON Deliveries
FOR EACH ROW
BEGIN
	IF NEW.Status = 'failed' AND OLD.Status = 'transit customer' THEN
		UPDATE Orders
        SET DeliveryFailCount = DeliveryFailCount + 1
        WHERE OrderID = NEW.OrderID;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER UpdateFailOrder
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
	IF NEW.DeliveryFailCount = 3 THEN
		UPDATE Orders
        SET Status = 'failed'
		WHERE OrderID = NEW.OrderID;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER UpdateVehicleAvailable
AFTER UPDATE ON Deliveries
FOR EACH ROW
BEGIN
    IF NEW.Status = 'successful' OR NEW.Status = 'failed' THEN
        UPDATE Vehicles
        SET Status = 'available'
        WHERE VehicleID = NEW.VehicleID;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER Encrypt2CustomerInfo
BEFORE INSERT ON Customers
FOR EACH ROW
BEGIN
	SET NEW.PhoneNumber = AES_ENCRYPT(NEW.PhoneNumber, 'key');
	SET NEW.Address = AES_ENCRYPT(NEW.Address, 'key');
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER EncryptCustomerPhone
BEFORE UPDATE ON Customers
FOR EACH ROW
BEGIN
	IF NEW.PhoneNumber != AES_DECRYPT(OLD.PhoneNumber, 'key') THEN
		SET NEW.PhoneNumber = AES_ENCRYPT(NEW.PhoneNumber, 'key');
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER EncryptCustomerAddress
BEFORE UPDATE ON Customers
FOR EACH ROW
BEGIN
    IF NEW.Address != AES_DECRYPT(OLD.Address, 'key') THEN
		SET NEW.Address = AES_ENCRYPT(NEW.Address, 'key');
	END IF;
END $$
DELIMITER ;

DELIMITER $$
# Function to calc Avg Delivery Cost
CREATE FUNCTION AvgDeliveryCost()
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE avg_cost DECIMAL(10,2);

    SELECT IFNULL(AVG(TotalCost), 0) INTO avg_cost
    FROM (
        SELECT DeliveryID, SUM(Amount) AS TotalCost
        FROM Expenses
        GROUP BY DeliveryID
    ) AS DeliverySums;

    RETURN avg_cost;
END $$
DELIMITER ;

#DROP FUNCTION DeliveryCountByVehicle;
DELIMITER $$
CREATE FUNCTION DeliveryCountByVehicle(in_VehicleID INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE delivery_count INT;

    SELECT COUNT(*) INTO delivery_count
    FROM Deliveries d
    WHERE VehicleID = in_VehicleID;

    RETURN delivery_count;
END $$
DELIMITER ;

# DROP USER 'manager'@'%';
# DROP USER 'shipper'@'%';
# DROP USER'dispatcher'@'%';
# DROP USER 'accountant'@'%';
CREATE USER 'manager'@'%' IDENTIFIED BY 'manager_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON Delivery_System.* TO 'manager'@'%';

CREATE USER 'dispatcher'@'%' IDENTIFIED BY 'dispatcher_pass';
GRANT SELECT, INSERT, UPDATE ON Orders TO 'dispatcher'@'%';
GRANT SELECT, INSERT, UPDATE ON Deliveries TO 'dispatcher'@'%';
GRANT SELECT, UPDATE ON Vehicles TO 'dispatcher'@'%';
GRANT SELECT ON Customers TO 'dispatcher'@'%';
GRANT SELECT ON Cities TO 'dispatcher'@'%';
GRANT SELECT ON Countries TO 'dispatcher'@'%';
GRANT EXECUTE ON PROCEDURE delivery_system.AssignDelivery TO 'dispatcher'@'%';

CREATE USER 'shipper'@'%' IDENTIFIED BY 'shipper_pass';
GRANT SELECT, UPDATE ON Deliveries TO 'shipper'@'%';
GRANT SELECT ON Orders TO 'shipper'@'%';
GRANT SELECT ON Customers TO 'shipper'@'%';
GRANT SELECT ON Vehicles TO 'shipper'@'%';
GRANT SELECT ON Cities TO 'shipper'@'%';
GRANT SELECT ON Countries TO 'shipper'@'%';
GRANT INSERT ON Expenses TO 'shipper'@'%';
GRANT SELECT ON ShipperCustomerView TO 'shipper'@'%';
GRANT SELECT ON ShipperWarehouseView TO 'shipper'@'%';

CREATE USER 'accountant'@'%' IDENTIFIED BY 'accountant_pass';
GRANT SELECT ON Expenses TO 'accountant'@'%';
GRANT SELECT ON Vehicles TO 'accountant'@'%';
GRANT SELECT ON Deliveries TO 'accountant'@'%';
GRANT SELECT ON Orders TO 'accountant'@'%';
GRANT SELECT ON Cities TO 'accountant'@'%';
GRANT SELECT ON Countries TO 'accountant'@'%';


# SELECT 
#     TABLE_NAME,
#     COLUMN_NAME AS PRIMARY_KEY
# FROM 
#     INFORMATION_SCHEMA.KEY_COLUMN_USAGE
# WHERE 
#     CONSTRAINT_NAME = 'PRIMARY'
#     AND TABLE_SCHEMA = 'Delivery_System';
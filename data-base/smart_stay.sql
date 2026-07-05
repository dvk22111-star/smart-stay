
-- ===================================
-- SQL Database Creation Script
-- ===================================
create database smart_stay
GO
use  smart_stay

-- 1. Permissions (אין תלויות)
CREATE TABLE permissions (
    AuthorizationID INT PRIMARY KEY IDENTITY(1,1),
    AuthorizationType VARCHAR(50) NOT NULL
);

-- 2. Users (אין תלויות)
CREATE TABLE users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Credit NUMERIC(10, 2) DEFAULT 0
);

-- 3. Preferences (אין תלויות)
CREATE TABLE preferences (
    PreferencesID INT PRIMARY KEY IDENTITY(1,1),
    PreferenceType VARCHAR(50) NOT NULL
);

-- 4. Hotels (אין תלויות)
CREATE TABLE hotels (
    HotelID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(500) NOT NULL,
    Kosher BIT DEFAULT 0,
    ContactPerson VARCHAR(255)
);

-- 5. Vacations (FK: hotels)
CREATE TABLE vacations (
    VacationID INT PRIMARY KEY IDENTITY(1,1),
    HotelID INT NOT NULL,
    StartV DATE NOT NULL,
    EndV DATE NOT NULL,
    Program TEXT,
    BasicCost FLOAT NOT NULL,
    NumberOfRooms INT,
    NumberOfFloors INT,
    FOREIGN KEY (HotelID) REFERENCES hotels(HotelID)
);

-- 6. Rooms (FK: hotels)
CREATE TABLE rooms (
    RoomID INT PRIMARY KEY IDENTITY(1,1),
    RoomNumber VARCHAR(50) NOT NULL,
    Floor INT NOT NULL,
    HotelID INT NOT NULL,
    NumberOfBeds INT NOT NULL,
    FOREIGN KEY (HotelID) REFERENCES hotels(HotelID)
);

-- 7. Groups (FK: users, vacations)
CREATE TABLE groups (
    GroupID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    GroupName VARCHAR(255),
    NumberofParticipants INT,
    VacationID INT NOT NULL,
    GroupPrice FLOAT,
    IndividualPrice FLOAT,
    PaidAsAGroup BIT,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (VacationID) REFERENCES vacations(VacationID)
);

-- 8. GroupMembers (FK: groups)
CREATE TABLE group_members (
    IDOfGroupMembers INT PRIMARY KEY IDENTITY(1,1),
    GroupID INT NOT NULL,
    Telephone VARCHAR(20) NOT NULL,
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
);

-- 9. CustomerPreferences (FK: users, preferences, vacations)
CREATE TABLE customer_preferences (
    CustomerPreferencesID INT PRIMARY KEY IDENTITY(1,1),
    Rating INT NOT NULL,
    UserID INT NOT NULL,
    PreferencesID INT NOT NULL,
    VacationID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (PreferencesID) REFERENCES preferences(PreferencesID),
    FOREIGN KEY (VacationID) REFERENCES vacations(VacationID)
);

-- 10. HotelPreferences (FK: hotels, preferences)
CREATE TABLE hotel_preferences (
    HotelPreferencesID INT PRIMARY KEY IDENTITY(1,1),
    HotelID INT NOT NULL,
    PreferenceID INT NOT NULL,
    Price FLOAT NOT NULL,
    FOREIGN KEY (HotelID) REFERENCES hotels(HotelID),
    FOREIGN KEY (PreferenceID) REFERENCES preferences(PreferencesID)
);

-- 11. RoomPreferences (FK: rooms, preferences)
CREATE TABLE room_preferences (
    RoomPreferencesID INT PRIMARY KEY IDENTITY(1,1),
    RoomID INT NOT NULL,
    IDPreferences INT NOT NULL,
    FOREIGN KEY (RoomID) REFERENCES rooms(RoomID),
    FOREIGN KEY (IDPreferences) REFERENCES preferences(PreferencesID)
);

-- 12. Workers (FK: permissions)
CREATE TABLE workers (
    IDCard INT PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255),
    permissions INT,
    FOREIGN KEY (permissions) REFERENCES permissions(AuthorizationID)
);

-- 13. VacationersCustomers (FK: users, vacations)
CREATE TABLE vacationers_customers (
    VacationIDForCustomers INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    VacationID INT NOT NULL,
    UpdateDate DATE NOT NULL,
    GroupMemberNumber INT,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (VacationID) REFERENCES vacations(VacationID)
);

-- 14. Placements (FK: rooms, vacationers_customers)
CREATE TABLE placements (
    PlacementID INT PRIMARY KEY IDENTITY(1,1),
    RoomID INT,
    Price FLOAT NOT NULL,
    VacationersCustomersID INT,
    FOREIGN KEY (RoomID) REFERENCES rooms(RoomID),
    FOREIGN KEY (VacationersCustomersID) REFERENCES vacationers_customers(VacationIDForCustomers)
);

-- 15. PartnerRequests (FK: users, vacations)
CREATE TABLE partner_requests (
    PartnerRequestID INT PRIMARY KEY IDENTITY(1,1),
    UserIDMember1 INT,
    UserIDMember2 INT,
    VacationID INT,
    FOREIGN KEY (UserIDMember1) REFERENCES users(UserID),
    FOREIGN KEY (UserIDMember2) REFERENCES users(UserID),
    FOREIGN KEY (VacationID) REFERENCES vacations(VacationID)
);


-------------
USE smart_stay;
GO

INSERT INTO permissions (AuthorizationType) VALUES
('Secretary'),
('Manager'),
('SystemAdmin');

INSERT INTO users (Name, Phone, Email, Credit) VALUES
('Sarah Cohen', '0507000001', 'sarah@test.com', 0),
('Miriam Levi', '0507000002', 'miriam@test.com', 0),
('Rivka Gold', '0507000003', 'rivka@test.com', 50),
('Esther Weiss', '0507000004', 'esther@test.com', 100),
('Chana Friedman', '0507000005', 'chana@test.com', 0),
('Leah Katz', '0507000006', 'leah@test.com', 0),
('Tamar Green', '0507000007', 'tamar@test.com', 0),
('Rachel Berger', '0507000008', 'rachel@test.com', 0),
('Yael Rosen', '0507000009', 'yael@test.com', 0),
('Shira Braun', '0507000010', 'shira@test.com', 0),
('Devorah Stern', '0507000011', 'devorah@test.com', 0),
('Malky Adler', '0507000012', 'malky@test.com', 0);

INSERT INTO hotels (Name, Address, Kosher, ContactPerson) VALUES
(
    'Blue Sea Hotel',
    'Netanya Beach Road 15',
    1,
    'David Manager'
);

INSERT INTO preferences (PreferenceType) VALUES
('Sea View'),
('Low Floor'),
('High Floor'),
('Near Elevator'),
('Balcony'),
('Quiet Area'),
('Accessible Room');

INSERT INTO vacations
    (HotelID, StartV, EndV, Program, BasicCost, NumberOfRooms, NumberOfFloors)
VALUES
(
    1,
    '2026-08-10',
    '2026-08-13',
    'Women Summer Retreat',
    1500,
    10,
    3
);

INSERT INTO rooms (RoomNumber, Floor, HotelID, NumberOfBeds) VALUES
('101', 1, 1, 2),
('102', 1, 1, 2),
('103', 1, 1, 3),
('201', 2, 1, 2),
('202', 2, 1, 2),
('203', 2, 1, 3),
('301', 3, 1, 2),
('302', 3, 1, 3),
('303', 3, 1, 2),
('304', 3, 1, 3);

INSERT INTO hotel_preferences (HotelID, PreferenceID, Price) VALUES
(1, 1, 200),
(1, 5, 100),
(1, 6, 50),
(1, 7, 150);

INSERT INTO room_preferences (RoomID, IDPreferences) VALUES
(1, 2),
(2, 1),
(3, 1),
(4, 5),
(5, 6),
(6, 1),
(7, 1),
(8, 4),
(9, 7),
(10, 1);

INSERT INTO groups
    (UserID, GroupName, NumberofParticipants, VacationID, GroupPrice, IndividualPrice, PaidAsAGroup)
VALUES
(1, 'Jerusalem Group', 5, 1, 7000, 1400, 1),
(6, 'Haifa Group', 4, 1, 0, 1500, 0);

INSERT INTO group_members (GroupID, Telephone) VALUES
(1, '0507000001'),
(1, '0507000002'),
(1, '0507000003'),
(1, '0507000004'),
(1, '0507000005'),
(2, '0507000006'),
(2, '0507000007'),
(2, '0507000008'),
(2, '0507000009');

INSERT INTO vacationers_customers
    (UserID, VacationID, UpdateDate, GroupMemberNumber)
VALUES
(1, 1, '2026-05-01', 1),
(2, 1, '2026-05-02', 2),
(3, 1, '2026-05-03', 3),
(4, 1, '2026-05-03', 4),
(5, 1, '2026-05-04', 5),
(6, 1, '2026-05-05', 1),
(7, 1, '2026-05-05', 2),
(8, 1, '2026-05-06', 3),
(9, 1, '2026-05-06', 4),
(10, 1, '2026-05-07', 1),
(11, 1, '2026-05-07', 1),
(12, 1, '2026-05-08', 1);

INSERT INTO customer_preferences
    (Rating, UserID, PreferencesID, VacationID)
VALUES
(1, 1, 1, 1),
(2, 1, 2, 1),
(1, 2, 6, 1),
(2, 2, 1, 1),
(1, 3, 5, 1),
(2, 3, 1, 1),
(1, 4, 4, 1),
(2, 4, 2, 1),
(1, 5, 7, 1),
(2, 5, 6, 1),
(1, 6, 1, 1),
(2, 6, 5, 1),
(1, 7, 6, 1),
(2, 7, 2, 1);

INSERT INTO partner_requests
    (UserIDMember1, UserIDMember2, VacationID)
VALUES
(1, 2, 1),
(2, 1, 1),
(6, 7, 1),
(7, 6, 1),
(8, 9, 1);

INSERT INTO placements
    (RoomID, Price, VacationersCustomersID)
VALUES
(1, 1400, 1),
(1, 1400, 2),
(2, 1400, 3),
(2, 1400, 4),
(3, 1400, 5),
(3, 1400, 6),
(3, 1400, 7),
(4, 1500, 8),
(4, 1500, 9),
(5, 1500, 10);

INSERT INTO workers
    (IDCard, Name, PhoneNumber, Email, permissions)
VALUES
(123456789, 'Secretary One', '0508000001', 'secretary@test.com', 1),
(987654321, 'System Manager', '0508000002', 'manager@test.com', 2),
(111222333, 'Administrator', '0508000003', 'admin@test.com', 3);
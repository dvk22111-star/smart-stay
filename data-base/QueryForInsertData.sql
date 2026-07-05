--סיטואציה 1
USE smart_stay;
GO

----------------------------------------------------
-- ניקוי
----------------------------------------------------

DELETE FROM placements;
DELETE FROM room_preferences;
DELETE FROM customer_preferences;
DELETE FROM vacationers_customers;
DELETE FROM rooms;
DELETE FROM vacations;
DELETE FROM users;
DELETE FROM hotels;

DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('customer_preferences', RESEED, 0);
DBCC CHECKIDENT ('room_preferences', RESEED, 0);
DBCC CHECKIDENT ('placements', RESEED, 0);

----------------------------------------------------
-- מלון
----------------------------------------------------

INSERT INTO hotels (Name, Address, Kosher, ContactPerson)
VALUES ('Test Hotel', 'Test City', 1, 'Manager');

----------------------------------------------------
-- נופש (VacationID = 1)
----------------------------------------------------

INSERT INTO vacations (HotelID, StartV, EndV, Program, BasicCost, NumberOfRooms, NumberOfFloors)
VALUES (1, '2026-08-01', '2026-08-05', 'Test Program', 1000, 2, 1);

----------------------------------------------------
-- חדרים (2 חדרים, 2 מיטות כל אחד)
----------------------------------------------------

INSERT INTO rooms (RoomNumber, Floor, HotelID, NumberOfBeds)
VALUES 
('101', 1, 1, 2),  -- RoomID = 1
('102', 1, 1, 2);  -- RoomID = 2

----------------------------------------------------
-- העדפות חדרים (תיקון התאמה מלאה)
----------------------------------------------------
-- 1 Sea View
-- 2 Low Floor
-- 3 High Floor
-- 5 Balcony

INSERT INTO room_preferences (RoomID, IDPreferences)
VALUES
(1, 1), -- Room 101: Sea View
(1, 5), -- Room 101: Balcony

(2, 2), -- Room 102: Low Floor
(2, 3); -- Room 102: High Floor

----------------------------------------------------
-- משתמשים
----------------------------------------------------

INSERT INTO users (Name, Phone, Email, Credit)
VALUES
('User 1', '0500000001', 'u1@test.com', 0),
('User 2', '0500000002', 'u2@test.com', 0),
('User 3', '0500000003', 'u3@test.com', 0),
('User 4', '0500000004', 'u4@test.com', 0);

----------------------------------------------------
-- משתתפים בנופש
----------------------------------------------------

INSERT INTO vacationers_customers (UserID, VacationID, UpdateDate, GroupMemberNumber)
VALUES
(1, 1, GETDATE(), 1),
(2, 1, GETDATE(), 1),
(3, 1, GETDATE(), 1),
(4, 1, GETDATE(), 1);

----------------------------------------------------
-- העדפות משתמשים (התאמה מלאה לחדרים)
----------------------------------------------------

INSERT INTO customer_preferences (Rating, UserID, PreferencesID, VacationID)
VALUES
(5, 1, 1, 1), -- Sea View -> Room 101
(5, 2, 2, 1), -- Low Floor -> Room 102
(5, 3, 3, 1), -- High Floor -> Room 102
(5, 4, 5, 1); -- Balcony -> Room 101

----------------------------------------------------
-- ניקוי שיבוצים
----------------------------------------------------

DELETE FROM placements;


-------------------
--סיטואציה 2 מורכבת לא פתירה
USE smart_stay;
GO

----------------------------------------------------
-- ניקוי
----------------------------------------------------

DELETE FROM placements;
DELETE FROM room_preferences;
DELETE FROM customer_preferences;
DELETE FROM partner_requests;
DELETE FROM vacationers_customers;
DELETE FROM rooms;
DELETE FROM vacations;
DELETE FROM users;
DELETE FROM hotels;

DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('customer_preferences', RESEED, 0);
DBCC CHECKIDENT ('room_preferences', RESEED, 0);
DBCC CHECKIDENT ('partner_requests', RESEED, 0);
DBCC CHECKIDENT ('placements', RESEED, 0);

----------------------------------------------------
-- Hotel + Vacation
----------------------------------------------------

INSERT INTO hotels (Name, Address, Kosher, ContactPerson)
VALUES ('Complex Hotel', 'Test City', 1, 'Manager');

INSERT INTO vacations (HotelID, StartV, EndV, Program, BasicCost, NumberOfRooms, NumberOfFloors)
VALUES (1, '2026-08-01', '2026-08-05', 'Complex Scenario', 1200, 3, 1);

----------------------------------------------------
-- 3 חדרים (כולם 2 מיטות)
----------------------------------------------------

INSERT INTO rooms (RoomNumber, Floor, HotelID, NumberOfBeds)
VALUES
('101', 1, 1, 2),
('102', 1, 1, 2),
('103', 1, 1, 2);

----------------------------------------------------
-- 4 משתמשים
----------------------------------------------------

INSERT INTO users (Name, Phone, Email, Credit)
VALUES
('User A', '0500000001', 'a@test.com', 0),
('User B', '0500000002', 'b@test.com', 0),
('User C', '0500000003', 'c@test.com', 0),
('User D', '0500000004', 'd@test.com', 0);

----------------------------------------------------
-- שיוך לנופש
----------------------------------------------------

INSERT INTO vacationers_customers (UserID, VacationID, UpdateDate, GroupMemberNumber)
VALUES
(1, 1, GETDATE(), 1),
(2, 1, GETDATE(), 1),
(3, 1, GETDATE(), 1),
(4, 1, GETDATE(), 1);

----------------------------------------------------
-- 7 העדפות שונות (כבר קיימות בטבלה שלך)
----------------------------------------------------
-- 1 Sea View
-- 2 Low Floor
-- 3 High Floor
-- 4 Near Elevator
-- 5 Balcony
-- 6 Quiet Area
-- 7 Accessible Room

----------------------------------------------------
-- העדפות חדרים (לא מאוזן בכוונה)
----------------------------------------------------

INSERT INTO room_preferences (RoomID, IDPreferences)
VALUES
-- Room 1 חזק מאוד
(1, 1),
(1, 5),
(1, 6),

-- Room 2 בינוני
(2, 2),
(2, 3),

-- Room 3 חלש
(3, 4);

----------------------------------------------------
-- העדפות משתמשים (עם ציונים שונים)
----------------------------------------------------

INSERT INTO customer_preferences (Rating, UserID, PreferencesID, VacationID)
VALUES
(5, 1, 1, 1), -- A wants Sea View
(4, 1, 6, 1),

(5, 2, 2, 1), -- B wants Low Floor
(2, 2, 5, 1),

(5, 3, 3, 1), -- C wants High Floor
(3, 3, 4, 1),

(5, 4, 7, 1), -- D wants Accessible
(1, 4, 6, 1);

----------------------------------------------------
-- partner requests (בדיקת אילוץ שיבוץ יחד)
----------------------------------------------------

INSERT INTO partner_requests (UserIDMember1, UserIDMember2, VacationID)
VALUES
(1, 2, 1), -- A+B חייבים להיות יחד
(3, 4, 1); -- C+D חייבים להיות יחד

----------------------------------------------------
-- ניקוי שיבוצים
----------------------------------------------------

DELETE FROM placements;


--------------סיטואציה 3 מורכבת ופתירה
USE smart_stay;
GO

----------------------------------------------------
-- ניקוי
----------------------------------------------------

DELETE FROM placements;
DELETE FROM room_preferences;
DELETE FROM customer_preferences;
DELETE FROM partner_requests;
DELETE FROM vacationers_customers;
DELETE FROM rooms;
DELETE FROM vacations;
DELETE FROM users;
DELETE FROM hotels;

DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('customer_preferences', RESEED, 0);
DBCC CHECKIDENT ('room_preferences', RESEED, 0);
DBCC CHECKIDENT ('partner_requests', RESEED, 0);
DBCC CHECKIDENT ('placements', RESEED, 0);

----------------------------------------------------
-- Hotel + Vacation
----------------------------------------------------

INSERT INTO hotels (Name, Address, Kosher, ContactPerson)
VALUES ('Feasible Hotel', 'Test City', 1, 'Manager');

INSERT INTO vacations (HotelID, StartV, EndV, Program, BasicCost, NumberOfRooms, NumberOfFloors)
VALUES (1, '2026-08-01', '2026-08-05', 'Feasible Scenario', 1000, 3, 1);

----------------------------------------------------
-- 3 חדרים (פתרון מאוזן)
----------------------------------------------------

INSERT INTO rooms (RoomNumber, Floor, HotelID, NumberOfBeds)
VALUES
('101', 1, 1, 2),
('102', 1, 1, 2),
('103', 1, 1, 2);

----------------------------------------------------
-- 4 משתמשים
----------------------------------------------------

INSERT INTO users (Name, Phone, Email, Credit)
VALUES
('User A', '0500000001', 'a@test.com', 0),
('User B', '0500000002', 'b@test.com', 0),
('User C', '0500000003', 'c@test.com', 0),
('User D', '0500000004', 'd@test.com', 0);

----------------------------------------------------
-- שיוך לנופש
----------------------------------------------------

INSERT INTO vacationers_customers (UserID, VacationID, UpdateDate, GroupMemberNumber)
VALUES
(1, 1, GETDATE(), 1),
(2, 1, GETDATE(), 1),
(3, 1, GETDATE(), 1),
(4, 1, GETDATE(), 1);

----------------------------------------------------
-- 7 העדפות (קיימות אצלך)
----------------------------------------------------

-- 1 Sea View
-- 2 Low Floor
-- 3 High Floor
-- 4 Near Elevator
-- 5 Balcony
-- 6 Quiet Area
-- 7 Accessible Room

----------------------------------------------------
-- חדרים מאוזנים (חשוב לפתירות!)
----------------------------------------------------

INSERT INTO room_preferences (RoomID, IDPreferences)
VALUES
-- Room 1: טוב ל-A+B
(1, 1),
(1, 5),

-- Room 2: טוב ל-C+D
(2, 2),
(2, 3),

-- Room 3: גיבוי לכל מי שנשאר
(3, 4),
(3, 6),
(3, 7);

----------------------------------------------------
-- העדפות משתמשים (מאוזן בכוונה)
----------------------------------------------------

INSERT INTO customer_preferences (Rating, UserID, PreferencesID, VacationID)
VALUES

-- A + B זוג טבעי
(5, 1, 1, 1),
(4, 1, 5, 1),

(5, 2, 1, 1),
(4, 2, 5, 1),

-- C + D זוג טבעי
(5, 3, 2, 1),
(4, 3, 3, 1),

(5, 4, 2, 1),
(4, 4, 3, 1);

----------------------------------------------------
-- partner requests (ללא סתירות)
----------------------------------------------------

INSERT INTO partner_requests (UserIDMember1, UserIDMember2, VacationID)
VALUES
(1, 2, 1),
(3, 4, 1);

----------------------------------------------------
-- ניקוי שיבוצים
----------------------------------------------------

DELETE FROM placements;
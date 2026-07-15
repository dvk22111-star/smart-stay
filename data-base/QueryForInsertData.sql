/*
====================================================
EXPECTED RESULT - SCRIPT 1
Registration Bonus מול Preference Priority
====================================================

נתונים:
- Room 101:
    Capacity: 1
    Preferences:
        Sea View
        Balcony

- Room 102:
    Capacity: 1
    Preferences:
        None

Users:
1. Early User
   UpdateDate: 2026-01-01
   Preferences:
       Sea View Rating 3

2. Late User
   UpdateDate: 2026-06-01
   Preferences:
       Sea View Rating 5
       Balcony Rating 5


צפי:
- Late User צריך לקבל את Room 101
  בגלל התאמת 2 העדפות חזקות.

- Early User צריך לקבל את Room 102
  בגלל שנשארה לו אפשרות ללא התאמה.

Expected placements:

User             Room
-------------------------
Late User        101
Early User       102


בדיקה:
אם Early User מקבל 101:
=> Registration Priority חזק מדי
=> Preference Weight לא משפיע מספיק.


====================================================
EXPECTED RESULT - SCRIPT 2
Groups + Partners + Preferences Competition
====================================================

Rooms:
101:
    Beds:2
    Sea View

102:
    Beds:3
    Sea View

203:
    Beds:3
    High Floor

301:
    Beds:4
    Sea View + High Floor

401:
    Beds:4
    Balcony


Groups:

Group A:
4 members
Preferences:
Sea View + Balcony

Group B:
3 members
Preference:
Quiet

Group C:
2 members
Preference:
High Floor

Group D:
5 members
Preference:
Sea View


Partner Requests:

Group B:
Member 1 + Member 2

Group D:
Member 1 + Member 3

Singles:
Single A + Single B



צפי:

1. קבוצות חייבות לקבל חדר משותף.

2. בקשות שותפים חייבות להיות באותו RoomID.

3. Group A יקבל עדיפות לחדר עם Sea View/Balcony אם קיים חדר מתאים.

4. Group C יקבל עדיפות ל-203 או 301.

5. Group D ינסה לקבל חדר גדול עם Sea View:
   301 עדיף בגלל קיבולת 4,
   אך אין חדר יחיד ל-5 אנשים ולכן יתכן פיצול בהתאם לחוקי המערכת.

6. משתמשים ללא התאמה יקבלו חדרים רגילים.


Validation Expected:

Partner Requests:
Result = MATCH


Groups:
כל חברי אותה קבוצה:
אותו RoomID


Summary:
AssignedCustomers = 18
UnassignedCustomers = 0
אם קיימת קיבולת מספיקה.


====================================================
EXPECTED RESULT - SCRIPT 3
Integration + Priority + Competition
====================================================

Rooms:

101:
Beds 2
Sea View

102:
Beds 2
Sea View

201:
Beds 4
Quiet

202:
Beds 4
Normal

301:
Beds 4
High Floor + Balcony

302:
Beds 2
Normal

303:
Beds 4
Normal


Users:

Priority Group:
2 members
Registration:
2026-01-01
2026-01-02
Preference:
Sea View


Second Group:
2 members
Registration:
2026-02-01
2026-02-02
Preference:
Quiet


Singles:
Sea User:
Sea View

Quiet User:
Quiet

High User:
High Floor

Normal Users:
Low priority


Partner:
Priority Group members together

Second Group members together


Expected:

1. Priority Group:
   חייב לקבל חדר משותף.

   בגלל רישום מוקדם + Sea View:
   צפוי לקבל:
       Room 101 או Room 102


2. Second Group:
   חייב לקבל חדר משותף.

   עדיפות:
       Room 201


3. Sea Preference User:
   יקבל Sea View רק אם נשאר חדר Sea פנוי.


4. High Floor User:
   עדיפות:
       Room 301


5. Normal Users:
   יקבלו חדרים שנשארו.


Expected placement example:

User                         Room
--------------------------------------
Priority Group Member 1      101
Priority Group Member 2      101

Second Group Member 1        201
Second Group Member 2        201

High Floor User              301

Sea Preference User          102


Validation:

Partner Requests:
-----------------
Priority Group:
MATCH

Second Group:
MATCH


Groups:
--------
Priority Group:
All members same RoomID

Second Group:
All members same RoomID


Summary:

Placements:
= Total assigned users

AssignedCustomers:
= Number of vacationers_customers

UnassignedCustomers:
= 0 אם קיימת קיבולת מספקת


====================================================
*/

USE smart_stay;
GO

----------------------------------------------------
-- TEST:
-- Registration Bonus מול Preference Priority
--
-- מטרה:
-- לבדוק שמשתמש מוקדם לא מוחק לחלוטין
-- העדפה חזקה של משתמש מאוחר.
--
-- Expected:
-- Early User יקבל יתרון רישום,
-- אבל Late User עם העדפה חזקה יותר צריך לקבל
-- את החדר המתאים יותר אם המשקל עובד נכון.
----------------------------------------------------


----------------------------------------------------
-- CLEAN
----------------------------------------------------

DELETE FROM placements;
DELETE FROM partner_requests;
DELETE FROM customer_preferences;
DELETE FROM vacationers_customers;
DELETE FROM room_preferences;
DELETE FROM rooms;
DELETE FROM vacations;
DELETE FROM users;
DELETE FROM hotels;
DELETE FROM preferences;


DBCC CHECKIDENT ('placements', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('preferences', RESEED, 0);


----------------------------------------------------
-- Preferences
----------------------------------------------------

INSERT INTO preferences
(
PreferenceType
)
VALUES
('Sea View'),
('Balcony');


----------------------------------------------------
-- Hotel
----------------------------------------------------

INSERT INTO hotels
(
Name,
Address,
Kosher,
ContactPerson
)
VALUES
(
'Priority Weight Test Hotel',
'Test',
1,
'Manager'
);


----------------------------------------------------
-- Vacation
----------------------------------------------------

INSERT INTO vacations
(
HotelID,
StartV,
EndV,
Program,
BasicCost,
NumberOfRooms,
NumberOfFloors
)
VALUES
(
1,
'2026-10-01',
'2026-10-05',
'Priority Weight Test',
1000,
2,
1
);


----------------------------------------------------
-- Rooms
--
-- Room 101:
-- Sea View + Balcony
--
-- Room 102:
-- No preferences
----------------------------------------------------

INSERT INTO rooms
(
RoomNumber,
Floor,
HotelID,
NumberOfBeds
)
VALUES
('101',1,1,1),
('102',1,1,1);



INSERT INTO room_preferences
(
RoomID,
IDPreferences
)
VALUES
(1,1),
(1,2);



----------------------------------------------------
-- Users
--
-- Early נרשם ראשון
-- Late נרשם מאוחר
----------------------------------------------------

INSERT INTO users
(
Name,
Phone,
Email,
Credit
)
VALUES
(
'Early User',
'0500000801',
'early@test.com',
0
),
(
'Late User',
'0500000802',
'late@test.com',
0
);



----------------------------------------------------
-- Vacation Customers
----------------------------------------------------

INSERT INTO vacationers_customers
(
UserID,
VacationID,
UpdateDate,
GroupMemberNumber
)
VALUES
(
1,
1,
'2026-01-01',
NULL
),
(
2,
1,
'2026-06-01',
NULL
);



----------------------------------------------------
-- Preferences
--
-- Early:
-- רק Sea View
--
-- Late:
-- Sea View + Balcony
-- דירוג גבוה יותר
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES
(
3,
1,
1,
1
),
(
5,
2,
1,
1
),
(
5,
2,
2,
1
);



----------------------------------------------------
-- CLEAR PLACEMENTS
----------------------------------------------------

DELETE FROM placements;



----------------------------------------------------
-- DEBUG DATA
----------------------------------------------------

SELECT
u.UserID,
u.Name,
vc.UpdateDate
FROM vacationers_customers vc
JOIN users u
ON u.UserID = vc.UserID
ORDER BY vc.UpdateDate;



SELECT *
FROM customer_preferences;


SELECT *
FROM room_preferences;

-----------------
----------------------
------------------------------
---------------------------------------
------------------------------------------------
-------------------------------------------------------------
----------------------------------------------------------------------------
----------------------------------------------------------------------------------------



USE smart_stay;
GO

----------------------------------------------------
-- CLEAN
----------------------------------------------------

DELETE FROM placements;
DELETE FROM partner_requests;
DELETE FROM customer_preferences;
DELETE FROM vacationers_customers;
DELETE FROM group_members;
DELETE FROM groups;
DELETE FROM room_preferences;
DELETE FROM rooms;
DELETE FROM vacations;
DELETE FROM users;
DELETE FROM hotels;
DELETE FROM preferences;


DBCC CHECKIDENT ('placements', RESEED, 0);
DBCC CHECKIDENT ('partner_requests', RESEED, 0);
DBCC CHECKIDENT ('customer_preferences', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('group_members', RESEED, 0);
DBCC CHECKIDENT ('groups', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('preferences', RESEED, 0);


----------------------------------------------------
-- PREFERENCES
----------------------------------------------------

INSERT INTO preferences
(
 PreferenceType
)
VALUES
('Sea View'),
('Quiet'),
('High Floor'),
('Balcony');


DECLARE @Sea INT;
DECLARE @Quiet INT;
DECLARE @High INT;
DECLARE @Balcony INT;


SELECT @Sea = PreferencesID
FROM preferences
WHERE PreferenceType='Sea View';

SELECT @Quiet = PreferencesID
FROM preferences
WHERE PreferenceType='Quiet';

SELECT @High = PreferencesID
FROM preferences
WHERE PreferenceType='High Floor';

SELECT @Balcony = PreferencesID
FROM preferences
WHERE PreferenceType='Balcony';


----------------------------------------------------
-- HOTEL
----------------------------------------------------

INSERT INTO hotels
(
 Name,
 Address,
 Kosher,
 ContactPerson
)
VALUES
(
 'Integration Test Hotel',
 'Test City',
 1,
 'Manager'
);


----------------------------------------------------
-- VACATION
----------------------------------------------------

INSERT INTO vacations
(
 HotelID,
 StartV,
 EndV,
 Program,
 BasicCost,
 NumberOfRooms,
 NumberOfFloors
)
VALUES
(
 1,
 '2026-09-01',
 '2026-09-06',
 'Full Integration Test',
 1000,
 12,
 4
);


----------------------------------------------------
-- ROOMS
-- הכנסת סדר אקראי בכוונה
----------------------------------------------------

INSERT INTO rooms
(
 RoomNumber,
 Floor,
 HotelID,
 NumberOfBeds
)
VALUES

('302',3,1,2),
('101',1,1,2),
('401',4,1,4),
('203',2,1,3),
('104',1,1,1),
('301',3,1,4),
('402',4,1,2),
('201',2,1,4),
('102',1,1,3),
('303',3,1,1),
('202',2,1,2),
('403',4,1,1);


----------------------------------------------------
-- ROOM PREFERENCES
----------------------------------------------------

DECLARE @Room101 INT;
DECLARE @Room301 INT;
DECLARE @Room401 INT;
DECLARE @Room203 INT;


SELECT @Room101 = RoomID
FROM rooms
WHERE RoomNumber='101';

SELECT @Room301 = RoomID
FROM rooms
WHERE RoomNumber='301';

SELECT @Room401 = RoomID
FROM rooms
WHERE RoomNumber='401';

SELECT @Room203 = RoomID
FROM rooms
WHERE RoomNumber='203';


INSERT INTO room_preferences
(
 RoomID,
 IDPreferences
)
VALUES

(@Room101,@Sea),
(@Room301,@Sea),
(@Room301,@High),
(@Room401,@Balcony),
(@Room203,@High);


SELECT *
FROM rooms;

----------------------------------------------------
-- USERS
-- הכנסת משתמשים בסדר אקראי בכוונה
----------------------------------------------------

INSERT INTO users
(
 Name,
 Phone,
 Email,
 Credit
)
VALUES

('Single B','0500000016','singleb@test.com',0),

('Group C - Member 2','0500000010','gc2@test.com',0),

('Group A - Member 3','0500000003','ga3@test.com',0),

('Group D - Member 5','0500000015','gd5@test.com',0),

('Group B - Member 2','0500000006','gb2@test.com',0),

('Single D','0500000018','singled@test.com',0),

('Group A - Member 1','0500000001','ga1@test.com',0),

('Group D - Member 2','0500000012','gd2@test.com',0),

('Group C - Member 1','0500000009','gc1@test.com',0),

('Group B - Member 3','0500000007','gb3@test.com',0),

('Group D - Member 1','0500000011','gd1@test.com',0),

('Group A - Member 4','0500000004','ga4@test.com',0),

('Single A','0500000017','singlea@test.com',0),

('Group B - Member 1','0500000005','gb1@test.com',0),

('Group D - Member 3','0500000013','gd3@test.com',0),

('Group A - Member 2','0500000002','ga2@test.com',0),

('Single C','0500000019','singlec@test.com',0),

('Group D - Member 4','0500000014','gd4@test.com',0);



----------------------------------------------------
-- GET USER IDS
----------------------------------------------------

DECLARE @GA1 INT;
DECLARE @GA2 INT;
DECLARE @GA3 INT;
DECLARE @GA4 INT;

DECLARE @GB1 INT;
DECLARE @GB2 INT;
DECLARE @GB3 INT;

DECLARE @GC1 INT;
DECLARE @GC2 INT;

DECLARE @GD1 INT;
DECLARE @GD2 INT;
DECLARE @GD3 INT;
DECLARE @GD4 INT;
DECLARE @GD5 INT;

DECLARE @SingleA INT;
DECLARE @SingleB INT;
DECLARE @SingleC INT;
DECLARE @SingleD INT;


SELECT @GA1=UserID FROM users WHERE Email='ga1@test.com';
SELECT @GA2=UserID FROM users WHERE Email='ga2@test.com';
SELECT @GA3=UserID FROM users WHERE Email='ga3@test.com';
SELECT @GA4=UserID FROM users WHERE Email='ga4@test.com';


SELECT @GB1=UserID FROM users WHERE Email='gb1@test.com';
SELECT @GB2=UserID FROM users WHERE Email='gb2@test.com';
SELECT @GB3=UserID FROM users WHERE Email='gb3@test.com';


SELECT @GC1=UserID FROM users WHERE Email='gc1@test.com';
SELECT @GC2=UserID FROM users WHERE Email='gc2@test.com';


SELECT @GD1=UserID FROM users WHERE Email='gd1@test.com';
SELECT @GD2=UserID FROM users WHERE Email='gd2@test.com';
SELECT @GD3=UserID FROM users WHERE Email='gd3@test.com';
SELECT @GD4=UserID FROM users WHERE Email='gd4@test.com';
SELECT @GD5=UserID FROM users WHERE Email='gd5@test.com';


SELECT @SingleA=UserID FROM users WHERE Email='singlea@test.com';
SELECT @SingleB=UserID FROM users WHERE Email='singleb@test.com';
SELECT @SingleC=UserID FROM users WHERE Email='singlec@test.com';
SELECT @SingleD=UserID FROM users WHERE Email='singled@test.com';



----------------------------------------------------
-- VACATION CUSTOMERS
-- תאריכי רישום שונים לבדיקת Priority
----------------------------------------------------

INSERT INTO vacationers_customers
(
 UserID,
 VacationID,
 UpdateDate,
 GroupMemberNumber
)
VALUES

-- Group A ראשון
(@GA1,1,'2026-01-01',1),
(@GA2,1,'2026-01-02',2),
(@GA3,1,'2026-01-03',3),
(@GA4,1,'2026-01-04',4),


-- Group B
(@GB1,1,'2026-02-01',1),
(@GB2,1,'2026-02-02',2),
(@GB3,1,'2026-02-03',3),


-- Group C
(@GC1,1,'2026-03-01',1),
(@GC2,1,'2026-03-02',2),


-- Group D
(@GD1,1,'2026-04-01',1),
(@GD2,1,'2026-04-02',2),
(@GD3,1,'2026-04-03',3),
(@GD4,1,'2026-04-04',4),
(@GD5,1,'2026-04-05',5),


-- Singles
(@SingleA,1,'2026-05-01',NULL),
(@SingleB,1,'2026-05-10',NULL),
(@SingleC,1,'2026-06-01',NULL),
(@SingleD,1,'2026-06-15',NULL);



----------------------------------------------------
-- GROUPS
----------------------------------------------------

INSERT INTO groups
(
 UserID,
 GroupName,
 NumberofParticipants,
 VacationID
)
VALUES

(@GA1,'Group A',4,1),
(@GB1,'Group B',3,1),
(@GC1,'Group C',2,1),
(@GD1,'Group D',5,1);



----------------------------------------------------
-- GET GROUP IDS
----------------------------------------------------

DECLARE @GroupA INT;
DECLARE @GroupB INT;
DECLARE @GroupC INT;
DECLARE @GroupD INT;


SELECT @GroupA=GroupID
FROM groups
WHERE GroupName='Group A';


SELECT @GroupB=GroupID
FROM groups
WHERE GroupName='Group B';


SELECT @GroupC=GroupID
FROM groups
WHERE GroupName='Group C';


SELECT @GroupD=GroupID
FROM groups
WHERE GroupName='Group D';



----------------------------------------------------
-- GROUP MEMBERS
----------------------------------------------------

INSERT INTO group_members
(
 GroupID,
 Telephone
)
VALUES

(@GroupA,'0500000601'),
(@GroupA,'0500000602'),
(@GroupA,'0500000603'),

(@GroupB,'0500000604'),
(@GroupB,'0500000605'),

(@GroupC,'0500000606'),

(@GroupD,'0500000607'),
(@GroupD,'0500000608'),
(@GroupD,'0500000609'),
(@GroupD,'0500000610');



----------------------------------------------------
-- DEBUG
----------------------------------------------------

SELECT *
FROM users
ORDER BY UserID;


SELECT *
FROM vacationers_customers;


SELECT *
FROM groups;

----------------------------------------------------
-- CUSTOMER PREFERENCES
-- חלק משולב לסקריפט מלא
-- משתנים עם שמות ייחודיים
----------------------------------------------------

DECLARE @Main_Pref_SeaView INT;
DECLARE @Main_Pref_Quiet INT;
DECLARE @Main_Pref_HighFloor INT;
DECLARE @Main_Pref_Balcony INT;


SELECT @Main_Pref_SeaView = PreferencesID
FROM preferences
WHERE PreferenceType = 'Sea View';


SELECT @Main_Pref_Quiet = PreferencesID
FROM preferences
WHERE PreferenceType = 'Quiet';


SELECT @Main_Pref_HighFloor = PreferencesID
FROM preferences
WHERE PreferenceType = 'High Floor';


SELECT @Main_Pref_Balcony = PreferencesID
FROM preferences
WHERE PreferenceType = 'Balcony';



----------------------------------------------------
-- GROUP A
-- Sea View + Balcony
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

(5,7 ,@Main_Pref_SeaView,1),
(5,16,@Main_Pref_SeaView,1),
(5,3 ,@Main_Pref_SeaView,1),
(5,12,@Main_Pref_SeaView,1),

(5,7 ,@Main_Pref_Balcony,1),
(5,16,@Main_Pref_Balcony,1),
(5,3 ,@Main_Pref_Balcony,1),
(5,12,@Main_Pref_Balcony,1);



----------------------------------------------------
-- GROUP B
-- Quiet
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

(5,14,@Main_Pref_Quiet,1),
(5,5 ,@Main_Pref_Quiet,1),
(5,10,@Main_Pref_Quiet,1);



----------------------------------------------------
-- GROUP C
-- High Floor
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

(5,9,@Main_Pref_HighFloor,1),
(5,2,@Main_Pref_HighFloor,1);



----------------------------------------------------
-- GROUP D
-- Sea View
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

(5,11,@Main_Pref_SeaView,1),
(5,8 ,@Main_Pref_SeaView,1),
(5,15,@Main_Pref_SeaView,1),
(5,18,@Main_Pref_SeaView,1),
(5,4 ,@Main_Pref_SeaView,1);



----------------------------------------------------
-- SINGLE USERS
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

-- Single A
(5,13,@Main_Pref_SeaView,1),

-- Single B
(5,1,@Main_Pref_Quiet,1),

-- Single C
(5,17,@Main_Pref_Balcony,1),

-- Single D
(5,6,@Main_Pref_HighFloor,1);



----------------------------------------------------
-- PARTNER REQUESTS
----------------------------------------------------

INSERT INTO partner_requests
(
UserIDMember1,
UserIDMember2,
VacationID
)
VALUES

-- Group B
(14,5,1),

-- Group D
(11,15,1),

-- Singles
(13,1,1);



----------------------------------------------------
-- DEBUG
----------------------------------------------------

SELECT *
FROM customer_preferences
ORDER BY UserID, PreferencesID;


SELECT *
FROM partner_requests;

----------------------------------------------------
-- COMPETITIVE SCENARIO
-- קבוצות ויחידים מתחרים על חדרים
----------------------------------------------------


----------------------------------------------------
-- USERS
-- הכנסה בסדר אקראי
----------------------------------------------------

INSERT INTO users
(
Name,
Phone,
Email,
Credit
)
VALUES

('Late Priority Group Member 2','0500000902','priority2@test.com',0),
('Single Sea User','0500000905','singlesea@test.com',0),
('Second Group Member 1','0500000903','secondgroup1@test.com',0),
('Priority Group Member 1','0500000901','priority1@test.com',0),
('Single Normal User','0500000906','singlenormal@test.com',0),
('Second Group Member 2','0500000904','secondgroup2@test.com',0);



----------------------------------------------------
-- שליפת מזהים
----------------------------------------------------

DECLARE @Comp_Priority1 INT;
DECLARE @Comp_Priority2 INT;

DECLARE @Comp_Second1 INT;
DECLARE @Comp_Second2 INT;

DECLARE @Comp_SingleSea INT;
DECLARE @Comp_SingleNormal INT;


SELECT @Comp_Priority1 = UserID
FROM users
WHERE Email='priority1@test.com';


SELECT @Comp_Priority2 = UserID
FROM users
WHERE Email='priority2@test.com';


SELECT @Comp_Second1 = UserID
FROM users
WHERE Email='secondgroup1@test.com';


SELECT @Comp_Second2 = UserID
FROM users
WHERE Email='secondgroup2@test.com';


SELECT @Comp_SingleSea = UserID
FROM users
WHERE Email='singlesea@test.com';


SELECT @Comp_SingleNormal = UserID
FROM users
WHERE Email='singlenormal@test.com';



----------------------------------------------------
-- VACATION CUSTOMERS
-- בכוונה סדר הכנסת משתמשים לא לפי תאריך
----------------------------------------------------

INSERT INTO vacationers_customers
(
UserID,
VacationID,
UpdateDate,
GroupMemberNumber
)
VALUES

(@Comp_Second1,1,'2026-05-01',1),
(@Comp_Priority1,1,'2026-01-01',1),

(@Comp_SingleSea,1,'2026-03-01',NULL),

(@Comp_Priority2,1,'2026-01-02',2),

(@Comp_Second2,1,'2026-05-02',2),

(@Comp_SingleNormal,1,'2026-06-01',NULL);



----------------------------------------------------
-- GROUPS
----------------------------------------------------

INSERT INTO groups
(
UserID,
GroupName,
NumberofParticipants,
VacationID
)
VALUES

(
@Comp_Priority1,
'Priority Competition Group',
2,
1
),

(
@Comp_Second1,
'Second Competition Group',
2,
1
);



----------------------------------------------------
-- PARTNER REQUESTS
-- חברי קבוצות מבקשים יחד
----------------------------------------------------

INSERT INTO partner_requests
(
UserIDMember1,
UserIDMember2,
VacationID
)
VALUES

(
@Comp_Priority1,
@Comp_Priority2,
1
),

(
@Comp_Second1,
@Comp_Second2,
1
);



----------------------------------------------------
-- CUSTOMER PREFERENCES
----------------------------------------------------

DECLARE @Comp_Sea INT;
DECLARE @Comp_Quiet INT;


SELECT @Comp_Sea = PreferencesID
FROM preferences
WHERE PreferenceType='Sea View';


SELECT @Comp_Quiet = PreferencesID
FROM preferences
WHERE PreferenceType='Quiet';



INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

-- קבוצה ראשונה רוצה ים
(5,@Comp_Priority1,@Comp_Sea,1),
(5,@Comp_Priority2,@Comp_Sea,1),

-- קבוצה שניה רוצה שקט
(5,@Comp_Second1,@Comp_Quiet,1),
(5,@Comp_Second2,@Comp_Quiet,1),

-- יחיד מתחרה על ים
(5,@Comp_SingleSea,@Comp_Sea,1),

-- יחיד ללא עדיפות חזקה
(1,@Comp_SingleNormal,@Comp_Quiet,1);



----------------------------------------------------
-- DEBUG
----------------------------------------------------

SELECT *
FROM vacationers_customers
WHERE UserID IN
(
@Comp_Priority1,
@Comp_Priority2,
@Comp_Second1,
@Comp_Second2,
@Comp_SingleSea,
@Comp_SingleNormal
);


SELECT *
FROM partner_requests;


SELECT *
FROM customer_preferences
WHERE UserID IN
(
@Comp_Priority1,
@Comp_Priority2,
@Comp_Second1,
@Comp_Second2,
@Comp_SingleSea,
@Comp_SingleNormal
);

----------------------------------------------------
-- GROUP MEMBERS
-- השלמת חברי קבוצות
----------------------------------------------------

DECLARE @Comp_GroupPriority INT;
DECLARE @Comp_GroupSecond INT;


SELECT @Comp_GroupPriority = GroupID
FROM groups
WHERE GroupName = 'Priority Competition Group';


SELECT @Comp_GroupSecond = GroupID
FROM groups
WHERE GroupName = 'Second Competition Group';



----------------------------------------------------
-- הכנסת חברי קבוצה
-- Telephone בלבד לפי מבנה הטבלה
----------------------------------------------------

INSERT INTO group_members
(
GroupID,
Telephone
)
VALUES

-- Priority Competition Group

(@Comp_GroupPriority,'0500000901'),
(@Comp_GroupPriority,'0500000902'),


-- Second Competition Group

(@Comp_GroupSecond,'0500000903'),
(@Comp_GroupSecond,'0500000904');



----------------------------------------------------
-- DEBUG GROUPS
----------------------------------------------------

SELECT
g.GroupID,
g.GroupName,
g.NumberofParticipants,
gm.Telephone
FROM groups g
LEFT JOIN group_members gm
ON gm.GroupID = g.GroupID
WHERE g.GroupName IN
(
'Priority Competition Group',
'Second Competition Group'
);



----------------------------------------------------
-- בדיקת כל הנתונים לפני הרצה
----------------------------------------------------
----------------------------------------------------
-- FINAL VALIDATION FIXED
----------------------------------------------------


----------------------------------------------------
-- 1. כל השיבוצים
----------------------------------------------------

SELECT

p.PlacementID,
p.RoomID,
r.RoomNumber,
r.Floor,

p.VacationersCustomersID,

vc.UserID,
u.Name,
vc.UpdateDate

FROM placements p

LEFT JOIN vacationers_customers vc
ON vc.VacationIDForCustomers = p.VacationersCustomersID

LEFT JOIN users u
ON u.UserID = vc.UserID

LEFT JOIN rooms r
ON r.RoomID = p.RoomID

ORDER BY
p.PlacementID;



----------------------------------------------------
-- 2. בדיקת קבוצות
----------------------------------------------------

SELECT

g.GroupName,

u.Name,

r.RoomNumber

FROM groups g

JOIN vacationers_customers vc
ON vc.UserID = g.UserID
AND vc.VacationID = g.VacationID

JOIN users u
ON u.UserID = vc.UserID

LEFT JOIN placements p
ON p.VacationersCustomersID =
vc.VacationIDForCustomers

LEFT JOIN rooms r
ON r.RoomID = p.RoomID

ORDER BY
g.GroupName,
u.Name;



----------------------------------------------------
-- 3. בדיקת בקשות שותפים
----------------------------------------------------

SELECT

u1.Name AS User1,
u2.Name AS User2,

r1.RoomNumber AS Room1,
r2.RoomNumber AS Room2,

CASE
WHEN r1.RoomID = r2.RoomID
THEN 'MATCH'
ELSE 'NO MATCH'
END AS Result


FROM partner_requests pr


JOIN users u1
ON u1.UserID = pr.UserIDMember1


JOIN users u2
ON u2.UserID = pr.UserIDMember2


LEFT JOIN vacationers_customers vc1
ON vc1.UserID = pr.UserIDMember1
AND vc1.VacationID = pr.VacationID


LEFT JOIN vacationers_customers vc2
ON vc2.UserID = pr.UserIDMember2
AND vc2.VacationID = pr.VacationID


LEFT JOIN placements p1
ON p1.VacationersCustomersID =
vc1.VacationIDForCustomers


LEFT JOIN placements p2
ON p2.VacationersCustomersID =
vc2.VacationIDForCustomers


LEFT JOIN rooms r1
ON r1.RoomID = p1.RoomID


LEFT JOIN rooms r2
ON r2.RoomID = p2.RoomID;



----------------------------------------------------
-- 4. התאמת העדפות
----------------------------------------------------

SELECT

u.Name,

r.RoomNumber,

pref.PreferenceType


FROM placements p


JOIN vacationers_customers vc
ON vc.VacationIDForCustomers =
p.VacationersCustomersID


JOIN users u
ON u.UserID = vc.UserID


JOIN rooms r
ON r.RoomID = p.RoomID


LEFT JOIN customer_preferences cp
ON cp.UserID = u.UserID
AND cp.VacationID = vc.VacationID


LEFT JOIN preferences pref
ON pref.PreferencesID =
cp.PreferencesID

ORDER BY
u.Name;



----------------------------------------------------
-- 5. סיכום שיבוץ
----------------------------------------------------

SELECT

COUNT(*) AS Placements,

COUNT(DISTINCT VacationersCustomersID)
AS AssignedCustomers,

COUNT(DISTINCT RoomID)
AS UsedRooms

FROM placements;



-----------------
----------------------
------------------------------
---------------------------------------
------------------------------------------------
-------------------------------------------------------------
----------------------------------------------------------------------------
----------------------------------------------------------------------------------------


USE smart_stay;
GO

DELETE FROM placements;

DELETE FROM partner_requests;

DELETE FROM customer_preferences;

DELETE FROM group_members;

DELETE FROM groups;

DELETE FROM vacationers_customers;

DELETE FROM room_preferences;

DELETE FROM hotel_preferences;

DELETE FROM rooms;

DELETE FROM vacations;

DELETE FROM users;

DELETE FROM hotels;

DELETE FROM preferences;

GO

----------------------------------------------------
-- RESET IDENTITIES
----------------------------------------------------
DBCC CHECKIDENT ('placements', RESEED, 0);
DBCC CHECKIDENT ('partner_requests', RESEED, 0);
DBCC CHECKIDENT ('customer_preferences', RESEED, 0);
DBCC CHECKIDENT ('group_members', RESEED, 0);
DBCC CHECKIDENT ('groups', RESEED, 0);
DBCC CHECKIDENT ('vacationers_customers', RESEED, 0);
DBCC CHECKIDENT ('rooms', RESEED, 0);
DBCC CHECKIDENT ('vacations', RESEED, 0);
DBCC CHECKIDENT ('users', RESEED, 0);
DBCC CHECKIDENT ('hotels', RESEED, 0);
DBCC CHECKIDENT ('preferences', RESEED, 0);
GO

----------------------------------------------------
-- SYSTEM PREFERENCES
----------------------------------------------------

INSERT INTO preferences
(
    PreferenceType
)
VALUES
('Sea View'),
('Quiet'),
('High Floor'),
('Balcony');

DECLARE @Sea INT;
DECLARE @Quiet INT;
DECLARE @High INT;
DECLARE @Balcony INT;

SELECT @Sea = PreferencesID
FROM preferences
WHERE PreferenceType = 'Sea View';

SELECT @Quiet = PreferencesID
FROM preferences
WHERE PreferenceType = 'Quiet';

SELECT @High = PreferencesID
FROM preferences
WHERE PreferenceType = 'High Floor';

SELECT @Balcony = PreferencesID
FROM preferences
WHERE PreferenceType = 'Balcony';

----------------------------------------------------
-- HOTEL
----------------------------------------------------

INSERT INTO hotels
(
    Name,
    Address,
    Kosher,
    ContactPerson
)
VALUES
(
    'Integration Test Hotel',
    'Test City',
    1,
    'Manager'
);

----------------------------------------------------
-- VACATION
----------------------------------------------------

INSERT INTO vacations
(
    HotelID,
    StartV,
    EndV,
    Program,
    BasicCost,
    NumberOfRooms,
    NumberOfFloors
)
VALUES
(
    1,
    '2026-09-01',
    '2026-09-06',
    'Full Integration Test',
    1000,
    6,
    3
);

----------------------------------------------------
-- ROOMS
----------------------------------------------------

INSERT INTO rooms
(
    RoomNumber,
    Floor,
    HotelID,
    NumberOfBeds
)

VALUES
('101',1,1,2),   -- Sea View
('102',1,1,2),   -- Sea View
('201',2,1,4),   -- Quiet
('202',2,1,4),   -- Normal
('301',3,1,4),   -- Balcony + High Floor
('302',3,1,2),   -- Normal
('303',3,1,4);

----------------------------------------------------
-- ROOM IDS
----------------------------------------------------

DECLARE @Room101 INT;
DECLARE @Room102 INT;
DECLARE @Room201 INT;
DECLARE @Room301 INT;

SELECT @Room101 = RoomID
FROM rooms
WHERE RoomNumber = '101';

SELECT @Room102 = RoomID
FROM rooms
WHERE RoomNumber = '102';

SELECT @Room201 = RoomID
FROM rooms
WHERE RoomNumber = '201';

SELECT @Room301 = RoomID
FROM rooms
WHERE RoomNumber = '301';

----------------------------------------------------
-- ROOM PREFERENCES
----------------------------------------------------

INSERT INTO room_preferences
(
    RoomID,
    IDPreferences
)
VALUES
(@Room101,@Sea),
(@Room102,@Sea),
(@Room201,@Quiet),
(@Room301,@High),
(@Room301,@Balcony);

----------------------------------------------------
-- DEBUG
----------------------------------------------------

SELECT
    r.RoomID,
    r.RoomNumber,
    r.Floor,
    r.NumberOfBeds,
    p.PreferenceType
FROM rooms r
LEFT JOIN room_preferences rp
    ON rp.RoomID = r.RoomID
LEFT JOIN preferences p
    ON p.PreferencesID = rp.IDPreferences
ORDER BY
    r.RoomNumber;

	----------------------------------------------------
-- USERS
----------------------------------------------------

INSERT INTO users
(
    Name,
    Phone,
    Email,
    Credit
)
VALUES

-- Group A (נרשמו מוקדם)
('Group A Member 1','0500001001','ga1@test.com',0),
('Group A Member 2','0500001002','ga2@test.com',0),
('Group A Member 3','0500001003','ga3@test.com',0),
('Group A Member 4','0500001004','ga4@test.com',0),

-- Group B (נרשמו מאוחר יותר)
('Group B Member 1','0500002001','gb1@test.com',0),
('Group B Member 2','0500002002','gb2@test.com',0),
('Group B Member 3','0500002003','gb3@test.com',0),
('Group B Member 4','0500002004','gb4@test.com',0),

-- Singles
('Single Early Sea','0500003001','single1@test.com',0),
('Single Late Sea','0500003002','single2@test.com',0),

-- Partner external
('Partner User 1','0500004001','partner1@test.com',0),
('Partner User 2','0500004002','partner2@test.com',0);


----------------------------------------------------
-- USER IDS
----------------------------------------------------

DECLARE @GA1 INT;
DECLARE @GA2 INT;
DECLARE @GA3 INT;
DECLARE @GA4 INT;

DECLARE @GB1 INT;
DECLARE @GB2 INT;
DECLARE @GB3 INT;
DECLARE @GB4 INT;

DECLARE @SingleEarly INT;
DECLARE @SingleLate INT;

DECLARE @Partner1 INT;
DECLARE @Partner2 INT;


SELECT @GA1=UserID FROM users WHERE Email='ga1@test.com';
SELECT @GA2=UserID FROM users WHERE Email='ga2@test.com';
SELECT @GA3=UserID FROM users WHERE Email='ga3@test.com';
SELECT @GA4=UserID FROM users WHERE Email='ga4@test.com';


SELECT @GB1=UserID FROM users WHERE Email='gb1@test.com';
SELECT @GB2=UserID FROM users WHERE Email='gb2@test.com';
SELECT @GB3=UserID FROM users WHERE Email='gb3@test.com';
SELECT @GB4=UserID FROM users WHERE Email='gb4@test.com';


SELECT @SingleEarly=UserID
FROM users
WHERE Email='single1@test.com';


SELECT @SingleLate=UserID
FROM users
WHERE Email='single2@test.com';


SELECT @Partner1=UserID
FROM users
WHERE Email='partner1@test.com';


SELECT @Partner2=UserID
FROM users
WHERE Email='partner2@test.com';


----------------------------------------------------
-- VACATION CUSTOMERS
-- UpdateDate בודק קדימות הרשמה
----------------------------------------------------

INSERT INTO vacationers_customers
(
    UserID,
    VacationID,
    UpdateDate,
    GroupMemberNumber
)
VALUES

-- Group A ראשון
(@GA1,1,'2026-01-01',1),
(@GA2,1,'2026-01-02',2),
(@GA3,1,'2026-01-03',3),
(@GA4,1,'2026-01-04',4),


-- Group B אחרון
(@GB1,1,'2026-03-01',1),
(@GB2,1,'2026-03-02',2),
(@GB3,1,'2026-03-03',3),
(@GB4,1,'2026-03-04',4),


-- יחידים
(@SingleEarly,1,'2026-02-01',NULL),
(@SingleLate,1,'2026-06-01',NULL),


-- Partner
(@Partner1,1,'2026-04-01',NULL),
(@Partner2,1,'2026-04-02',NULL);


----------------------------------------------------
-- DEBUG USERS
----------------------------------------------------

SELECT
u.UserID,
u.Name,
vc.UpdateDate,
vc.GroupMemberNumber

FROM users u

JOIN vacationers_customers vc
ON vc.UserID=u.UserID

ORDER BY
vc.UpdateDate;


----------------------------------------------------
-- 04_USERS.sql
----------------------------------------------------
INSERT INTO users
(
Name,
Phone,
Email,
Credit
)
VALUES

('Priority Group Member 1','0500991001','priority1@test.com',0),
('Priority Group Member 2','0500991002','priority2@test.com',0),

('Second Group Member 1','0500992001','second1@test.com',0),
('Second Group Member 2','0500992002','second2@test.com',0),

('Sea Preference User','0500993001','sea@test.com',0),

('Quiet Preference User','0500994001','quiet@test.com',0),

('High Floor User','0500995001','high@test.com',0),

('Normal User 1','0500996001','normal1@test.com',0),
('Normal User 2','0500996002','normal2@test.com',0);

----------------------------------------------------
-- USER IDS
----------------------------------------------------

DECLARE @Priority1 INT;
DECLARE @Priority2 INT;

DECLARE @Second1 INT;
DECLARE @Second2 INT;

DECLARE @SeaUser INT;
DECLARE @QuietUser INT;
DECLARE @HighUser INT;

DECLARE @Normal1 INT;
DECLARE @Normal2 INT;


SELECT @Priority1=UserID
FROM users
WHERE Email='priority1@test.com';

SELECT @Priority2=UserID
FROM users
WHERE Email='priority2@test.com';


SELECT @Second1=UserID
FROM users
WHERE Email='second1@test.com';

SELECT @Second2=UserID
FROM users
WHERE Email='second2@test.com';


SELECT @SeaUser=UserID
FROM users
WHERE Email='sea@test.com';


SELECT @QuietUser=UserID
FROM users
WHERE Email='quiet@test.com';


SELECT @HighUser=UserID
FROM users
WHERE Email='high@test.com';


SELECT @Normal1=UserID
FROM users
WHERE Email='normal1@test.com';

SELECT @Normal2=UserID
FROM users
WHERE Email='normal2@test.com';


----------------------------------------------------
-- VACATION CUSTOMERS
-- תאריכים שונים לבדיקת עדיפות הרשמה
----------------------------------------------------

INSERT INTO vacationers_customers
(
UserID,
VacationID,
UpdateDate,
GroupMemberNumber
)
VALUES

(@Priority1,1,'2026-01-01',1),
(@Priority2,1,'2026-01-02',2),

(@Second1,1,'2026-02-01',1),
(@Second2,1,'2026-02-02',2),

(@SeaUser,1,'2026-03-01',NULL),

(@QuietUser,1,'2026-04-01',NULL),

(@HighUser,1,'2026-05-01',NULL),

(@Normal1,1,'2026-06-01',NULL),
(@Normal2,1,'2026-06-02',NULL);



----------------------------------------------------
-- 05_GROUPS.sql
----------------------------------------------------

DECLARE @GroupPriority INT;
DECLARE @GroupSecond INT;


INSERT INTO groups
(
UserID,
GroupName,
NumberofParticipants,
VacationID
)
VALUES

(
@Priority1,
'Priority Group',
2,
1
),

(
@Second1,
'Second Group',
2,
1
);


SELECT @GroupPriority=GroupID
FROM groups
WHERE GroupName='Priority Group';


SELECT @GroupSecond=GroupID
FROM groups
WHERE GroupName='Second Group';



----------------------------------------------------
-- GROUP MEMBERS
-- לפי מבנה הטבלה:
-- Telephone בלבד
----------------------------------------------------
INSERT INTO group_members
(
GroupID,
Telephone
)
VALUES

(@GroupPriority,'0500991001'),
(@GroupPriority,'0500991002'),

(@GroupSecond,'0500992001'),
(@GroupSecond,'0500992002');

----------------------------------------------------
-- 06_PREFERENCES_USERS.sql
----------------------------------------------------

INSERT INTO customer_preferences
(
Rating,
UserID,
PreferencesID,
VacationID
)
VALUES

-- Priority Group רוצה ים
(5,@Priority1,@Sea,1),
(5,@Priority2,@Sea,1),


-- Second Group רוצה שקט
(5,@Second1,@Quiet,1),
(5,@Second2,@Quiet,1),


-- יחידים
(5,@SeaUser,@Sea,1),
(5,@QuietUser,@Quiet,1),
(5,@HighUser,@High,1),


-- עדיפות נמוכה
(1,@Normal1,@Quiet,1),
(1,@Normal2,@High,1);



----------------------------------------------------
-- 07_PARTNER_REQUESTS.sql
----------------------------------------------------

INSERT INTO partner_requests
(
UserIDMember1,
UserIDMember2,
VacationID
)
VALUES

(@Priority1,@Priority2,1),

(@Second1,@Second2,1);



----------------------------------------------------
-- CLEAN PLACEMENTS BEFORE RUN
----------------------------------------------------

DELETE FROM placements;



----------------------------------------------------
-- DATA CHECK BEFORE SWAGGER
----------------------------------------------------

SELECT *
FROM users
ORDER BY UserID;


SELECT *
FROM vacationers_customers
ORDER BY UpdateDate;


SELECT *
FROM groups;


SELECT *
FROM group_members;


SELECT *
FROM partner_requests;


SELECT *
FROM customer_preferences;

SELECT 
    u.UserID,
    u.Name,
    vc.VacationIDForCustomers,
    vc.UpdateDate
FROM vacationers_customers vc
JOIN users u
ON u.UserID = vc.UserID
WHERE vc.VacationID = 1
ORDER BY vc.UpdateDate;

SELECT
    SUM(NumberOfBeds) AS TotalBeds
FROM rooms;
# Smart Stay - Room Assignment Optimization Engine

## 📋 Overview

Smart Stay is a sophisticated room assignment system for vacation resorts that uses **SAT-CP (SAT-based Constraint Programming)** to optimize room assignments based on guest preferences and constraints.

The system implements a 6-stage optimization pipeline:
1. **Stage 1**: Load data and create CP-SAT variables
2. **Stage 2**: Build domains and apply constraints
3. **Stage 3**: Run CP-SAT solver with MRV heuristic
4. **Stage 4**: Analyze solution and conflicts
5. **Stage 5**: Build optimization objective (maximize satisfaction)
6. **Stage 6**: Extract solution and save placements

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create database tables (first run)
python create_tables.py
```

### Running the API

```bash
# Start FastAPI server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Running Assignment Pipeline

```bash
# Run assignment for a vacation
python assignment/run_assignment.py
```

---

## 📁 Project Structure

```
.
├── assignment/                          # Core assignment engine
│   ├── assignment_engine.py            # Main orchestrator
│   ├── run_assignment.py               # Standalone runner
│   ├── stage_1_variables_domains/      # Load data, create variables
│   ├── stage_2_propagation/            # Build domains, apply constraints
│   ├── stage_3_search/                 # CP-SAT solver execution
│   ├── stage_4_conflict_analysis/      # Analyze solution quality
│   ├── stage_5_optimization/           # Maximize satisfaction scores
│   └── stage_6_solution/               # Extract & save placements
├── controllers/                         # FastAPI route handlers
├── models/                              # SQLAlchemy ORM models
├── services/                            # Business logic & repositories
├── database/                            # Databasection & setup
├── dtos/                                # Data transfer objects
├── main.py                              # FastAPI app entry point
├── create_tables.py                     # Database initialization
├── requirements.txt                     # Python dependencies
└── pytest.ini                           # Test configuration
```

---

## 🏗️ Architecture

### Tech Stack
- **Framework**: FastAPI + SQLAlchemy (ORM)
- **Solver**: Google OR-Tools CP-SAT v9.15.6755
- **Database**: SQL Server (via pyodbc) or SQLite
- **Language**: Python 3.10+

### Database Models
- **Vacation**: Group of guests in a hotel
- **User**: Individual guest
- **Room**: Hotel room with preferences
- **Placement**: Final assignment (user → room)
- **Preferences**: User/Room preference tags
- **Group**: Group membership (for constraints)
- **PartnerRequests**: Special room requests

### API Endpoints

#### Assignment Management
- `POST /assignments/run` - Run assignment pipeline
- `GET /assignments/{vacation_id}` - Get placements for vacation

#### CRUD Endpoints
- `/users/`, `/hotels/`, `/rooms/`, `/vacations/`
- `/placements/`, `/preferences/`, `/groups/`, etc.

---

## 🎯 How the Solver Works

### Stage 1: Variables & Domains
```
For each (user, room) pair:
  - Create binary variable x[user_id, room_id]
  - Initialize model with OR-Tools CP-SAT
  - Load vacation data (users, rooms, preferences)
```

### Stage 2: Constraint Propagation
```
Build user domains:
  user_domain[user_i] = {room_j | user_i can be assigned to room_j}

Apply constraints:
  1. Each user assigned exactly 1 room
  2. Room capacity: sum(assignments to room_k) ≤ capacity_k
  3. Domain enforcement: x[user_i, room_j] = 0 for invalid pairs
```

### Stage 3: Search
```
Configure solver:
  - Search workers: 8
  - Timeout: 300 seconds
  - Heuristic: MRV (Most Restricted Variable first)

Execute solver.Solve(model)
```

### Stage 4: Conflict Analysis
```
Extract solver statistics:
  - Branches searched
  - Conflicts encountered
  - Wall time

Detect infeasibility & build report
```

### Stage 5: Optimization
```
Calculate satisfaction scores for each (user, room) assignment
Apply soft bonuses for partner requests and group proximity
Prefer placing larger registered groups together on adjacent floors
Greedy group placement selects the smallest contiguous floor segment that fits a group,
minimizing unused bed capacity and reserving that floor capacity before assigning the next group
Fall back to the largest available cluster only when no contiguous segment can fit the full group
Build objective: Maximize(Σ satisfaction_score * x[user_id, room_id] + group_adjacency_bonus)
```

### Stage 6: Solution
```
Extract assignments from solved model
Build Placement objects
Save to database
Export Excel report
```

---

## 🔧 Configuration

### Environment Variables (optional)
```bash
# SQL Server (if not using SQLite)
DATABASE_URL=mssql+pyodbc://user:password@server/SMART_STAY?driver=ODBC Driver 17 for SQL Server

# Or individual settings:
DB_SERVER=localhost
DB_NAME=SMART_STAY
DB_USER=admin
DB_PASSWORD=password
DB_DRIVER=ODBC Driver 17 for SQL Server
```

If no environment variables are set, the system defaults to SQLite (`smart_stay.db`).

---

## ✅ Testing

```bash
# Run smoke tests
pytest test_api_smoke.py -v

# Test database connection
python test_connection.py

# Test specific module
pytest test_api.py::TestAssignment -v
```

---

## 📝 Example Usage

### Via FastAPI
```bash
curl -X POST http://localhost:8000/assignments/run \
  -H "Content-Type: application/json" \
  -d '{"vacation_id": 1, "hotel_id": 5}'
```

### Via Python Script
```python
from database.connection import SessionLocal
from assignment.assignment_engine import AssignmentEngine

session = SessionLocal()
engine = AssignmentEngine(session)
result = engine.run(vacation_id=1, hotel_id=5)

print(f"Placements created: {len(result['placements'])}")
print(f"Satisfaction score: {result['report'].get('avg_satisfaction')}")
session.close()
```

---

## 🐛 Troubleshooting

### Import Errors
```
ModuleNotFoundError: No module named 'ortools'
→ Run: pip install -r requirements.txt
```

### Database Errors
```
sqlalchemy.exc.OperationalError: Connection refused
→ Check DATABASE_URL environment variable
→ Run: python create_tables.py to initialize
```

### No Vacation Found
```
ValueError: Vacation 1 not found
→ Add test data: INSERT INTO Vacations VALUES (1, 'Test', ...);
```

---

## 📊 Performance

Typical assignment for 100 users → 20 rooms:
- **Stage 1**: ~50ms (data loading)
- **Stage 2**: ~100ms (constraint building)
- **Stage 3**: 1-30s (solver search)
- **Stage 4**: ~10ms (analysis)
- **Stage 5**: ~50ms (objective building)
- **Stage 6**: ~100ms (solution extraction & saving)

**Total**: 1-35 seconds (depends on constraint tightness)

---

## 📚 References

- [Google OR-Tools CP-SAT Documentation](https://developers.google.com/optimization/cp/cp_solver)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

## 👤 Author

Developed for Smart Stay Vacation Resort System

---

## 📄 License

Proprietary - All rights reserved

---

## **כללי השיבוץ (חובה ומומלץ)**

- **חוקי חובה (Hard constraints):**
  - כל משתמש חייב להיות משובץ בדיוק לחדר אחד בתוך אותה חופשה (`שיבוץ חובה`).
  - אסור לעבור את קיבולת המיטות של החדר: סכום המשתתפים בחדר ≤ קיבולת החדר.
  - בקשות שותפים (partner requests) הן חוק חובה: אם שני משתמשים ביקשו להיות יחד — חייבים לשבץ אותם באותו חדר, אלא אם כן קיימת סתירה בלתי ניתנת לפתרון.
  - חדר אחד יכול להכיל רק אנשים מאותה חופשה (vacation_id זהה) — אין ערבוב בין חופשות שונות באותו חדר.
  - חוסר התאמה לדרישות בטיחות או מגבלות (למשל גיל/נגישות) מבטלת התאמה לחדר מסוים (domain reduction).

- **חוקי עדיפות (Soft constraints / Objectives):**
  - יש עדיפות למימוש העדפות המשתמשים (preferences) לפי דירוג (Rating).
  - משתמש עם דירוג גבוה מקבל עדיפות יחסית ב-breaking-ties ובמילוי חדרים (e.g. דירוג 5 מקבל עדיפות על דירוג 2).
  - רצפים של העדפות: התאמות של פריטים מרובים מצטברות לפי משקולות (או סכימה של הרייטינג).
  - שמירה על חדרים מלאים היא מטרה משנית (לצמצם חדרים חלקיים), אך לא על חשבון חוקים מחייבים.

- **חוקים עסקיים נוספים (ניתנים להתאמה):**
  - האם חבורות (groups) צריכות להישמר יחד כפי שמוגדר ב-Group? ניתן להגדיר כ-Hard או כ-Soft.
  - האם יש הגבלה לחציונים מגדריים או ל-only-same-gender rooms — חוקים ניתנים להוספה.

## **פונקציית ציון ואיך מוגדר "שיבוץ אופטימלי"**

מטרה עיקרית: למקסם את שביעות הרצון הכוללת של המשתתפים תוך שמירה על כל החוקים החייבים.

- **מבנה בסיסי של פונקציית ציון (דוגמה פשוטה):**
  - לכל התאמת העדפה (preference match) שמתוייגת כ-Rating N, מקבלים N נקודות. לדוגמה: Rating 5 → +5 נקודות.
  - התאמת מספר העדפות מצטבר: אם למשתמש יש 3 העדפות שהתקיימו (5,4,3) → +12 נקודות.
  - בקשות שותפים: תנאי חובה (אם לא ניתן למלא — פתרון נחשב כבלתי תקין) או חלופה: טרום-דרוג גבוה מאוד (ולא ניתן לפסול בקלות).
  - בונוסים אפשריים: לשבץ משתמשים עם דירוג גבוה יחד (או להעניק בונוס אם כל חברי קבוצה מקבלים את העדפותיהם).
  - עונשים אפשריים: שימוש בחדר נוסף מעבר למינימום עלול לגרור -P נקודות (כדי לעודד מילוי מלא).

- **דוגמאת פונקציית מטרה לינארית (משוקללת):**
  Maximize Σ_{user,room} (Σ preference_rating(user,room) * x[user,room])
  - ניתן להוסיף טרמיות (lexicographic) עם סדר עדיפויות לבחירה (ראו סעיף הבא).

- **דוגמת סדר עדיפויות (Lexicographic / Multi-objective):**
  1. מימוש בקשות שותפים (Hard/Top-priority)
  2. מקסום התאמת העדפות (sum of ratings)
  3. מילוי חדרים בצורה מלאה (להקטין חדרים חלקיים)
  4. צמצום מספר החדרים בשימוש (minimize rooms)
 5. העדפת משתמשים בעלי דירוג גבוה בעת שוויון

- **Tie-breakers:**
  - במידה ויש מספר פתרונות עם אותו ניקוד: לבחור את הפתרון שמממש את העדפות המשתמשים בעלי הדירוג הגבוה ביותר.
  - אפשרות נוספת: להעדיף פתרון שממזער מרחקים לוגיסטיים (floor, building) אם הנתונים קיימים.

## **מטריקות ודוחות (Reports)**
- ציון כולל (Total Satisfaction)
- ממוצע ציון למשתתף (Avg satisfaction)
- אחוז משתמשים שקיבלו את כל ההעדפות המדורגות גבוה (e.g., % users with at least one Rating 5 matched)
- סטאטוס חוקי חובה (Hard constraints violated? — צריך להיות 0)

## **מקרי קצה ובדיקות מוצעות (Test Cases)**

1. יחיד בחופשה: משתמש אחד, חדר אחד — ישובץ נכון.
2. חדר קטן מאוד: בקשת שותפים שמבקשים לשבץ 3 אנשים בחדר עם 2 מיטות — בדוק שדווח על קונפליקט ותוצאה איננה משבצת לא תקינה.
3. בקשות שותפים סותרות: A מבקש להיות עם B; B מבקש להיות עם C; אך A ו-C סוררים — בדוק טיפול במחזוריות/סתירות.
4. משתמשים מחופשות שונות: ודא שאין ערבוב בין חופשות בחדר אחד.
5. העדפות בלתי מתאימות לכל חדר: כל ההעדפות של משתמש אינן ניתנות למימוש — ודא שהמערכת משבצת לפי חוקי חובה או מדווחת על כשל.
6. סינון לפי מגבלות נגישות/גיל: משתמש עם דרישה לנגישות לא ישבץ בחדר שאינו נגיש.
7. עדיפות לפי דירוג: משתמש דירוג 5 ו-2 מתחרים על המקום האחרון — ודא ש-5 מקבל עדיפות.
8. טייס עומס (Stress test): 1000 משתמשים, 200 חדרים — בדיקת ביצועים וזמני ריצה.
9. שוויון בניקוד: שני פתרונות עם אותו ניקוד — בדוק שנבחר tie-breaker תקין (לדוגמה, מעניקים עדיפות לדירוג גבוה יותר).
10. בקשות קבוצתיות (Group together): קבוצה של 4 מבקשת להישאר יחד; האם החוק Hard או Soft? בדוק את שני המצבים.
11. בקשות ליחיד בחדר (single-room request): ודא שמי שביקש חדר יחיד מקבל אותו או שדווח על חוסר זמינות.
12. בדיקת עקביות DB: לאחר שמירה, ודא שכל `Placement` מקושר ל-`Vacation` ול-`User` נכון.
13. גרסאות שדה חסרות: משתמש ללא דירוג/העדפות — ברירת מחדל ללא העדפות, אך חייב להיות משובץ.
14. בקשת שותף לא קיימת במערכת: בקשת שותף שמצביעה על user_id לא קיים — דווח שגיאה.
15. קונפליקט בין בקשת שותפים להעדפות: שותפים רוצים ביחד אך העדפות לחדרים נוגדות — האם עדיפות השותפים גוברת? בדוק התנהגות.

כל מקרה בדיקה צריך לכלול: קלט (מאגר/fixtures), ציפייה מדויקת (החל מהחוקים החייבים ועד לציון), ותוצאה בפועל (placements + דוח ציון).

## **איך המערכת פועלת — כללים בסיסיים לזרימת השיבוץ**

1. טעינת נתונים: מושך את כל המשתתפים, החדרים, ההעדפות ובקשות השותפים עבור `vacation_id` נתון.
2. בניית דומיינים: לכל משתמש מחשבים את קבוצת החדרים האפשרית לפי מגבלות (capabilities, accessibility, room type).
3. החלת חוקים מחייבים: מסירים זוגות (user,room) שאינם חוקיים.
4. בניית פונקציית המטרה: מחשבים את הניקוד לכל (user,room) לפי העדפות ומשקולות.
5. פתרון בעזרת CP-SAT (או אלגוריתם חלופי): מקסימיזציה תחת אילוצים.
6. ניתוח תוצר: וידוא חוקים, חישוב דוחות, בניית אובייקטי `Placement`.
7. במקרה של אי-אפשרות לפתור (infeasible): הפקת דוח קונפליקטים עם סיבות ופעולות מוצעות (הורדת דרישות, שחרור בקשות Soft).

## **המלצות פרקטיות ליישום ופיתוח**

- להגדיר במפורש אילו חוקים הם Hard ואילו Soft בקונפיגורציה (קובץ/DB) כדי לאפשר ריצות ניסוי שונות.
- לבנות מערך fixtures לבדיקות יחידה לכל מקרה קצה ברשימה לעיל.
- לשמור לוגים ודוחות של הפתרון: סטטיסטיקות solver, time, branch count.
- להתאים משקולות (weights) בפונקציית המטרה באמצעות ניסויים כדי למצוא תמהיל המייצג את מדיניות העסק.
- לשקול אלגוריתמי preflow / matching במקרה של מגבלות ספציפיות (כמו pairing-heavy scenarios).

---



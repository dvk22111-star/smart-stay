# Assignment Mechanism for Smart Stay

## Overview

המנגנון משתמש ב-OR-Tools CP-SAT כדי לפתור את בעיית השיבוץ של משתמשים לחדרים. המטרה היא:

- לשבץ כל משתמש בדיוק לחדר אחד
- לכבד קיבולות חדרים
- לכבד אילוצים ספציפיים של משתמשים
- לכבד בקשות שותפים
- למקסם את שביעות הרצון של המשתמשים על בסיס העדפות
- לשמור על שיבוץ מלא לכל המשתמשים (בהנחה שאין יותר משתמשים ממיטות)

## שלבי המנגנון

### שלב 1 - Stage1: משתנים ותחומי ערכים

קובץ: `assignment/stage_1_variables_domains/stage_1_service.py`

1. טוען את המשתמשים (`users`) שנמצאים בנופש.
2. טוען את החדרים (`rooms`) הזמינים במלון.
3. טוען את העדפות הלקוחות, העדפות החדרים, בקשות שותפים וקבוצות.
4. יוצר מודל `cp_model.CpModel()` של OR-Tools.
5. יוצר משתני בוליאן עבור כל צירוף משתמש × חדר.
   - `x[(user_id, room_id)] = 1` אם המשתמש שובץ בחדר
   - `x[(user_id, room_id)] = 0` אחרת

הפעולה הזו נעשית על ידי `assignment/stage_1_variables_domains/variables_builder.py`.

### שלב 2 - Stage2: אילוצים

קובץ: `assignment/stage_2_propagation/constraints_builder.py`

השלב בונה את האילוצים הבסיסיים של המודל:

1. `AddExactlyOne(user_vars)` עבור כל משתמש:
   - כל משתמש מקבל בדיוק חדר אחד.
   - זה מבטיח שיבוץ מלא (בהנחה שמספר המיטות מספיק).

2. `sum(room_vars) <= capacity` עבור כל חדר:
   - מכבד את קיבולת החדר.
   - `room_capacities` או `room.NumberOfBeds` משמשים להגדרת מגבלה זו.

3. אילוצי משתמש פרטניים:
   - אם למשתמש יש רשימת חדרים מותרת, כל משתנה לחדר מחוץ לרשימה מקבל ערך 0.
   - כך נמנעים חדרים לא רצויים מבחינת המשתמש.

4. בקשות שותפים:
   - עבור כל בקשת שותפות, מוחל `x[(u1, room)] == x[(u2, room)]` לכל חדר.
   - כלומר, שני המשתמשים חייבים להשתבץ באותו חדר או לא להשתבץ בכלל.
   - בגרסה הנוכחית אין שינוי מפורש ל"להישאר ללא שיבוץ" כי יש אילוץ `ExactlyOne`, ולכן ההנחה היא שהמשתמשים עדיין יכולים להשתבץ יחד בחדר אחד.

### שלב 5 - Stage5: בניית המטרה

קובץ: `assignment/stage_5_optimization/stage_5_service.py`

השלב הזה בונה את פונקציית המטרה שממקסמת את שביעות הרצון של השיבוץ.

#### איך מחושבים הציונים?

- `SatisfactionScoreCalculator.calculate_score(rating)`
  - ממיר דירוג העדפה למספר.
  - ההמרה נועדה להיות לוקסיקוגרפית:
    - `1 -> 1_000_000`
    - `2 -> 10_000`
    - `3 -> 100`
    - `4 -> 10`
    - `5 -> 1`
  - כלומר, עדיפות 1 גוברת על כל ההבדלים של עדיפות 2 ומטה.

- `RoomScoreCalculator.calculate(user_preferences, room_preferences, score_calculator)`
  - עבור כל העדפה של המשתמש, אם החדר תואם את ההעדפה, מוסיף את הציון המתאים.
  - העדפת משתמש מתחברת רק לחדרים שמצוינים ב-`room_preferences`.

#### בונוס רישום

המערכת מוסיפה "בונוס רישום" קטן כדי להשתמש ברישום כבורר שוויון בלבד:

- משתמשים שמאוחסנים קודם מקבלים בונוס גבוה במקצת.
- זה לא מבטל העדפות רלוונטיות, אלא רק מסייע לבחור בין פתרונות עם ציון מקסימלי זהה.

### בניית פיזור המטרה

קובץ: `assignment/stage_5_optimization/objective_builder.py`

- בונים רשימת מונחים `x[(user_id, room_id)] * score` לכל צירוף.
- לוקחים את סכום כל המונחים.
- מודל מקסימיזציה (`model.Maximize(sum(objective_terms))`).

## שלב 3 - Stage3: חיפוש פתרון

קובץ: `assignment/stage_3_search/stage_3_service.py`

1. קובעת אסטרטגיית חיפוש באמצעות `SearchStrategyBuilder`.
2. מגדירה את תצורת ה-CP-SAT באמצעות `SolverConfiguration`.
3. מריצה `solver.Solve(context.model)`.
4. מחזירה את ה-solver והסטטוס של הפתרון.

השלב הזה מבצע את החיפוש בפועל במרחב האפשרויות של המשתנים והאילוצים.

## שלב 4 - Stage4: ניתוח קונפליקטים

קבצים:
- `assignment/stage_4_conflict_analysis/stage_4_service.py`
- `assignment/stage_4_conflict_analysis/conflict_report_builder.py`
- `assignment/stage_4_conflict_analysis/infeasibility_detector.py`
- `assignment/stage_4_conflict_analysis/solver_statistics.py`

בשלב זה בודקים את תוצאת ה-solver:

- האם הפתרון הינו תקין?
- האם יש בעיות אי-פרשיות (infeasibility)?
- האם נדרש דוח קונפליקטים או סטטיסטיקה להמשך.

## שלב 6 - Stage6: חילוץ ושמירה

קובץ: `assignment/stage_6_solution/stage_6_service.py`

1. `extract_solution(model_vars, solver)`
   - מחלץ את צירופי המשתמש-חדר שהתבררו כ־True.
2. `build_placements(assignments, vacation_id, price_lookup, vacation_customers)`
   - בונה ישויות `Placement` על סמך השיבוץ.
3. `save_placements(placements, db_session)`
   - שומר את תוצאות השיבוץ למסד הנתונים.
4. `export_to_excel(assignments, db_session)`
   - מייצא את השיבוץ לקובץ Excel.
5. `build_report(assignments, total_users)`
   - בונה דוח מסכם על היקף השיבוץ.

## הערות חשובות

- המנגנון מניח שיש מספיק מקום לכל המשתמשים, ולכן משתמש ב-`AddExactlyOne` לכל משתמש.
- ההתאמה בין משתמש לחדר אינה נעשית לפי "העדפה ראשונה בלבד" בלבד, אלא על ידי צבירת ציון העדפות.
- משקלות הציונים מעוצבים כך שעדיפות 1 תמיד גוברת על כל כל ציון של עדיפות 2.
- במידה ויש שימוש בבקשות שותפים, שתי המשויך חייבים להשתבץ באותו חדר.

## זרימת קריאה ברורה

1. `assignment/assignment_engine.py` קורא את כל השלבים.
2. `Stage1VariablesAndDomainsService.execute()` מייצר את הקלט והמשתנים.
3. `Stage2PropagationService.execute()` מיישם את האילוצים.
4. `Stage5OptimizationService.execute()` בונה את פונקציית המטרה.
5. `Stage3SearchService.execute()` מריץ את הסולבר.
6. `Stage4Service.execute()` מנתח את תוצאת הסולבר.
7. `run_stage_6(...)` מחלץ, שומר ומייצא את התוצאה.

## קבצים עיקריים לעיון

- `assignment/assignment_engine.py`
- `assignment/stage_1_variables_domains/stage_1_service.py`
- `assignment/stage_1_variables_domains/variables_builder.py`
- `assignment/stage_2_propagation/constraints_builder.py`
- `assignment/stage_5_optimization/stage_5_service.py`
- `assignment/stage_5_optimization/room_score_calculator.py`
- `assignment/stage_5_optimization/satisfaction_score_calculator.py`
- `assignment/stage_5_optimization/objective_builder.py`
- `assignment/stage_3_search/stage_3_service.py`
- `assignment/stage_6_solution/stage_6_service.py`

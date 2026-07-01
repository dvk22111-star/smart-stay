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
Build objective: Maximize(Σ satisfaction_score * x[user_id, room_id])
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

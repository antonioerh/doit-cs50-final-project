CREATE table IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

CREATE table IF NOT EXISTS muscles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT OR IGNORE INTO muscles (name) VALUES
('Abdominals'), ('Chest'), ('Shoulders'), ('Biceps'), ('Triceps'), 
('Forearms'), ('Upper Back'), ('Lower Back'), ('Lats'), ('Traps'), ('Glutes'), 
('Quadriceps'), ('Hamstrings'), ('Calves'), ('Abductors'), ('Adductors'), ('Neck'), ('Core'), ('Full Body');

CREATE table IF NOT EXISTS equipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT OR IGNORE INTO equipments (name) VALUES
('Bodyweight'), ('Dumbbell'), ('Barbell'), ('Machine'), ('Cable'), 
('Kettlebell'), ('Resistance Band'), ('Smith Machine'), ('Trap Bar'), ('Bench'), ('EZ Bar'), 
('Medicine Ball'), ('Stability Ball'), ('Foam Roller');

CREATE table IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    muscle_id INTEGER,
    equipment_id INTEGER,

    FOREIGN KEY (muscle_id) REFERENCES muscles(id),
    FOREIGN KEY (equipment_id) REFERENCES equipments(id)
);

CREATE TABLE IF NOT EXISTS routines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS routine_exercises (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  routine_id INTEGER NOT NULL,
  exercise_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  notes TEXT,
  UNIQUE (routine_id, position),
  FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE,
  FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);

CREATE TABLE IF NOT EXISTS routine_sets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  routine_exercise_id INTEGER NOT NULL,
  set_index INTEGER NOT NULL,
  reps INTEGER,
  weight REAL,
  rir INTEGER,
  rest_seconds INTEGER,
  is_warmup INTEGER NOT NULL DEFAULT 0,
  UNIQUE (routine_exercise_id, set_index),
  FOREIGN KEY (routine_exercise_id) REFERENCES routine_exercises(id) ON DELETE CASCADE
);



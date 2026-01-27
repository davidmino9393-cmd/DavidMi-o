import sqlite3
import os

DB_PATH = "db/wot.db"

# Crear carpeta db si no existe
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS player_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    period TEXT, -- '1d', '7d', '30d', '90d'
    battles INTEGER,
    wn8 REAL,
    avg_damage REAL,
    avg_frags REAL,
    avg_spot REAL,
    win_rate REAL,
    survival_rate REAL,
    created_at DATETIME
);""")

# Tabla de snapshots por tanque
cur.execute("""
CREATE TABLE IF NOT EXISTS tank_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    tank_id INTEGER NOT NULL,
    battles INTEGER,
    wins INTEGER,
    damage_dealt INTEGER,
    frags INTEGER,
    spotted INTEGER,
    defense_points INTEGER,
    created_at DATETIME
);
""")

# Tabla de expected values (WN8)
cur.execute("""
CREATE TABLE IF NOT EXISTS expected_values (
    tank_id INTEGER PRIMARY KEY,
    exp_damage REAL,
    exp_frags REAL,
    exp_spot REAL,
    exp_def REAL,
    exp_win REAL
);
""")

# Tabla de calculo WN8
cur.execute("""
CREATE TABLE IF NOT EXISTS wn8_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    wn8 REAL,
    battles INTEGER,
    created_at DATETIME
);
""")

conn.commit()
conn.close()

print("Base de datos inicializada correctamente")

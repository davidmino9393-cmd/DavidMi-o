import sqlite3
import numpy as np
import logging
from datetime import datetime

def calculate_wn8(db_path: str, player_id: int, days=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Traer snapshots del período
    if days:
        cur.execute("""
            SELECT *
            FROM tank_snapshot
            WHERE player_id = ?
              AND created_at >= datetime('now', ?)
            ORDER BY tank_id, created_at
        """, (player_id, f"-{days} days"))
    else:
        cur.execute("""
            SELECT *
            FROM tank_snapshot
            WHERE player_id = ?
            ORDER BY tank_id, created_at
        """, (player_id,))

    snapshots = cur.fetchall()

    if len(snapshots) < 2:
        logging.info(f"No hay suficientes snapshots para {days} días")
        return

    # 2. Agrupar por tanque
    tanks = {}
    for row in snapshots:
        tank_id = row[2]
        tanks.setdefault(tank_id, []).append(row)

    # 3. Leer expected values
    cur.execute("""
        SELECT tank_id, exp_damage, exp_frags, exp_spot, exp_def, exp_win
        FROM expected_values
    """)
    expected = {r[0]: r[1:] for r in cur.fetchall()}

    total_battles = 0
    rDAMAGE, rFRAG, rSPOT, rDEF, rWIN = [], [], [], [], []

    # 4. Calcular por tanque
    for tank_id, snaps in tanks.items():
        if tank_id not in expected or len(snaps) < 2:
            continue

        old = snaps[0]
        new = snaps[-1]

        battles = new[3] - old[3]
        wins    = new[4] - old[4]
        dmg     = new[5] - old[5]
        frags   = new[6] - old[6]
        spot    = new[7] - old[7]
        defense = new[8] - old[8]

        if battles <= 0:
            continue

        exp_dmg, exp_frags, exp_spot, exp_def, exp_win = expected[tank_id]
        total_battles += battles

        rDAMAGE.append(dmg / (battles * exp_dmg))
        rFRAG.append(frags / (battles * exp_frags))
        rSPOT.append(spot / (battles * exp_spot))
        rDEF.append(defense / (battles * exp_def))
        rWIN.append(wins / (battles * exp_win))

    if total_battles == 0:
        print("No hay batallas válidas para calcular WN8")
        return

    # 5. Fórmula WN8
    rDAMAGE = np.mean(rDAMAGE)
    rFRAG   = np.mean(rFRAG)
    rSPOT   = np.mean(rSPOT)
    rDEF    = np.mean(rDEF)
    rWIN    = np.mean(rWIN)

    rWINc    = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc   = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc   = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc    = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))

    wn8 = (
        980 * rDAMAGEc +
        210 * rDAMAGEc * rFRAGc +
        155 * rFRAGc * rSPOTc +
        75  * rDEFc * rFRAGc +
        145 * min(1.8, rWINc)
    )

    # 6. Guardar snapshot
    cur.execute("""
        INSERT INTO wn8_snapshot (player_id, wn8, battles, created_at)
        VALUES (?, ?, ?, ?)
    """, (player_id, wn8, total_battles, datetime.utcnow()))

    conn.commit()
    conn.close()

    label = f"{days} días" if days else "histórico"
    print(f"WN8 ({label}): {wn8:.2f} | Batallas: {total_battles}")

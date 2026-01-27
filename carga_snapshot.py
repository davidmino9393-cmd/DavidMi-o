import sqlite3
from wot_api_extract import extract_tank_stats

def save_tank_snapshots(db_path, application_id, account_id, access_token):
    data = extract_tank_stats(application_id, account_id, access_token)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for tank in data:
        stats = tank.get("statistics", {}).get("all", {})

        battles = stats.get("battles", 0)
        if battles == 0:
            continue

        cur.execute("""
            INSERT INTO tank_snapshot (
                player_id,
                tank_id,
                battles,
                wins,
                damage_dealt,
                frags,
                spotted,
                defense_points,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            account_id,
            tank["tank_id"],
            battles,
            stats.get("wins", 0),
            stats.get("damage_dealt", 0),
            stats.get("frags", 0),
            stats.get("spotted", 0),
            stats.get("dropped_capture_points", 0)
        ))

    conn.commit()
    conn.close()

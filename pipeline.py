import logging
import os
from config import DB_PATH, APPLICATION_ID, ACCESS_TOKEN
from carga_snapshot import save_tank_snapshots
from calculo_wn8 import calculate_wn8

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/wot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def run_pipeline(account_id: int):
    logging.info(f"Inicio pipeline | account_id={account_id}")

    save_tank_snapshots(
        DB_PATH,
        APPLICATION_ID,
        account_id,
        ACCESS_TOKEN
    )

    for days in [1, 7, 30, 90, None]:
        calculate_wn8(DB_PATH, account_id, days=days)

    logging.info("Fin pipeline")

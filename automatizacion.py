import time
import logging
import schedule

from pipeline import run_pipeline
from wot_api_extract import get_account_id_by_nickname

NICKNAME = "YoArGenTiNo"

logging.basicConfig(
    filename="logs/wot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def job():
    try:
        account_id = get_account_id_by_nickname(APPLICATION_ID, NICKNAME)
        run_pipeline(account_id)
    except Exception as e:
        logging.error(f"Error en job: {e}")

# horarios
schedule.every(6).hours.do(job)        # snapshots cada 6h
schedule.every().day.at("03:00").do(job)  # cálculo diario fijo

logging.info("Scheduler iniciado")

while True:
    schedule.run_pending()
    time.sleep(60)

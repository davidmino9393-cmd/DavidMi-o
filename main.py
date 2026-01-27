from carga_snapshot import save_tank_snapshots
from calculo_wn8 import calculate_wn8
from wot_api_extract import get_account_id_by_nickname
from pipeline import run_pipeline
from config import APPLICATION_ID

DB_PATH = "db/wot.db"
APPLICATION_ID = "8cf0ba0b173e205dc88f634cba40497b"
NICKNAME = "YoArGenTiNo"

def main():
    nickname = input("Ingresá el nickname de WoT: ").strip()

    account_id = get_account_id_by_nickname(APPLICATION_ID, nickname)
    if not account_id:
        print("No se encontró el jugador")
        return

    run_pipeline(account_id)

if __name__ == "__main__":
    main()

# Obtener account_id desde el nickname
ACCOUNT_ID = get_account_id_by_nickname(APPLICATION_ID, NICKNAME)

# Para stats públicas NO se usa access_token
ACCESS_TOKEN = None

# Guardar snapshot
save_tank_snapshots(
    DB_PATH,
    APPLICATION_ID,
    ACCOUNT_ID,
    ACCESS_TOKEN
)

# Calcular WN8 por períodos
calculate_wn8(DB_PATH, ACCOUNT_ID, days=1)
calculate_wn8(DB_PATH, ACCOUNT_ID, days=7)
calculate_wn8(DB_PATH, ACCOUNT_ID, days=30)
calculate_wn8(DB_PATH, ACCOUNT_ID, days=90)
calculate_wn8(DB_PATH, ACCOUNT_ID)   
calculate_wn8(DB_PATH, ACCOUNT_ID, days=180)
calculate_wn8(DB_PATH, ACCOUNT_ID, days=365)
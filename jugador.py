from wot_api_extract import get_account_id_by_nickname
from pipeline import run_pipeline
from config import APPLICATION_ID

def main():
    nickname = input("Ingresá tu nickname de World of Tanks: ").strip()

    if not nickname:
        print("Pone un nickname broh")
        return

    try:
        account_id = get_account_id_by_nickname(APPLICATION_ID, nickname)
    except Exception as e:
        print(f"Error buscando jugador: {e}")
        return

    print(f"Jugador encontrado | account_id={account_id}")
    run_pipeline(account_id)

if __name__ == "__main__":
    main()

import requests
import time
import logging

API_BASE_URL = "https://api.worldoftanks.com/wot"
MAX_RETRIES = 5
BACKOFF_FACTOR = 2


def get_account_id_by_nickname(application_id: str, nickname: str, exact: bool = True):
    """
    Obtiene el account_id a partir del nickname del jugador.
    """
    endpoint = f"{API_BASE_URL}/account/list/"
    params = {
        "application_id": application_id,
        "search": nickname,
        "limit": 5
    }

    r = requests.get(endpoint, params=params, timeout=10)
    data = r.json()

    if data.get("status") != "ok":
        raise Exception(f"API error: {data.get('error')}")

    results = data.get("data", [])

    if not results:
        raise Exception(f"No se encontró el jugador '{nickname}'")

    if exact:
        for r in results:
            if r["nickname"].lower() == nickname.lower():
                return r["account_id"]

        raise Exception(f"No se encontró coincidencia exacta para '{nickname}'")

    return results[0]["account_id"]


def extract_tank_stats(application_id, account_id, access_token, fields=None, extra=None, in_garage=None, session=None):
    """
    Extrae estadísticas por tanque para un jugador usando la API oficial de WoT.
    Maneja errores, rate limiting y logging.
    """
    endpoint = f"{API_BASE_URL}/tanks/stats/"
    params = {
        "application_id": application_id,
        "account_id": account_id,
       # "access_token": access_token
    }
    if fields:
        params["fields"] = fields
    if extra:
        params["extra"] = extra
    if in_garage is not None:
        params["in_garage"] = str(int(bool(in_garage)))

    s = session or requests.Session()
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = s.get(endpoint, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    return data["data"][str(account_id)]
                else:
                    logging.error(f"API error: {data.get('error', {}).get('message')}")
                    raise Exception(f"API error: {data.get('error', {}).get('message')}")
            elif response.status_code == 429:
                # Rate limit: backoff exponencial con jitter
                wait = BACKOFF_FACTOR ** retries + (0.1 * BACKOFF_FACTOR * retries * time.time() % 1)
                logging.warning(f"Rate limit reached. Waiting {wait:.2f}s before retrying...")
                time.sleep(wait)
                retries += 1
            else:
                logging.error(f"HTTP error {response.status_code}: {response.text}")
                response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Network error: {e}")
            time.sleep(BACKOFF_FACTOR ** retries)
            retries += 1
    raise Exception("Max retries exceeded for extract_tank_stats")
from pathlib import Path
from faststream import Logger
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from google_subs.config import settings
from google_subs.shemas.google_shemas import GoogleAccessAnswer, GoogleAccess

SERVICE_ACCOUNT_FILE = settings.SERVICE_ACCOUNT_FILE
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

BASE_DIR = Path(__file__).parent.parent

credentials = ServiceAccountCredentials.from_json_keyfile_name(BASE_DIR / SERVICE_ACCOUNT_FILE, SCOPES)
client = gspread.authorize(credentials)


def create_google_access(google_credentials: GoogleAccess, status: str, access: bool) -> GoogleAccessAnswer:
    return GoogleAccessAnswer(
        table_id=google_credentials.table_id,
        bot_msg_id=google_credentials.bot_msg_id,
        request_id=google_credentials.request_id,
        user=google_credentials.user,
        status=status,
        access=access,
    )


async def verify_google_sheet_access(google_credentials: GoogleAccess, log: Logger) -> GoogleAccessAnswer:
    table_id = google_credentials.table_id
    try:
        log.info("Starting google sheet verification")
        spreadsheet = client.open_by_key(table_id)
        try:
            spreadsheet.sheet1.get_values('A1')
            log.info(f"Успешный доступ к таблице f{table_id}")
            return create_google_access(google_credentials,
                                        f"Успешный доступ к таблице: f{table_id}",
                                        access=True)
        except gspread.exceptions.APIError as read_error:
            if "PERMISSION_DENIED" in str(read_error):
                log.error(f"Нет прав на чтение таблицы {table_id}")

                return create_google_access(google_credentials,
                                            f"Нет прав на чтение таблицы {table_id}",
                                            access=False)
            raise

    except PermissionError:
        log.error(f"Сервисному аккаунту запрещен доступ к таблице {table_id}")
        return create_google_access(google_credentials,
                                    f"Сервисному аккаунту запрещен доступ к таблице {table_id}",
                                    access=False)

    except gspread.exceptions.APIError as e:
        error_msg = str(e).lower()

        if "permission_denied" in error_msg:
            msg = f"Отказано в доступе к таблице {table_id}"
            log.error(msg)
        elif "not_found" in error_msg:
            msg = f"Таблица {table_id} не найдена"
            log.error(msg)
        else:
            msg = f"Ошибка Google Sheets API: {e}"
            log.error(msg)
        return create_google_access(google_credentials,
                                    msg,
                                    access=False)

    except gspread.exceptions.SpreadsheetNotFound:
        msg = f'Таблица {table_id} не существует'
        log.error(msg)
        return create_google_access(google_credentials,
                                    msg,
                                    access=False)

    except Exception as e:
        log.critical(f"Критическая ошибка при проверке доступа: {type(e).__name__}: {e}")
        return create_google_access(google_credentials,
                                    'Ошибка при проверке доступа',
                                    access=False)

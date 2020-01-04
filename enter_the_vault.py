import subprocess
import os

from console_functions.check_vault_health import check_vault_health
from console_functions.get_vault_password import get_vault_password
from crypto_files.encode_vault import decode_vault, encode_vault


os.system("title Vault Doors")
salt = get_vault_password()
healthy = check_vault_health(salt)
decode_vault(salt)
subprocess.call(f'start /wait py -m vault.vault_console {healthy}', shell=True)
encode_vault(salt)

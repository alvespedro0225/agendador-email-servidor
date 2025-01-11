from pathlib import Path
from configparser import ConfigParser

path = Path(__file__).parent / "config/config.ini"
config = ConfigParser()
config["SERVER"] = {
    # o ip do servidor que vai ser usado: e.g. "127.0.0.1"
    "host": "",
    # qual o port usar, so nao usar um ja reservado
    "port": "10_000",
}

config["EMAIL"] = {
    # qual email vai ser usado pra mandar os lembretes
    "email": "",
    # a palavra-passe de apps pro email
    # no caso de gmail: https://support.google.com/mail/answer/185833?hl=pt
    "pw": "",
    # o provedor do serviço smtp
    # google = smtp.gmail.com
    # microsoft = smtp-mail.outlook.com
    # se for usar outro procura "provedor smtp {empresa}"
    "host": "",
    # qual o port usado pela empresa
    "port": "587",
}

with open(path, "w") as file:
    config.write(file)

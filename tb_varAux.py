# varAux.py


import os
import sys
import subprocess
import time
import argparse
import argcomplete
import re


# ----- Enviroment ----- #
CORE = False  # Para limitar o uso das funcionalidades ao contexto
GNB = True  # Para limitar o uso das funcionalidades ao contexto
UE = False  # Para limitar o uso das funcionalidades ao contexto
CLI = True  # Para limitar o uso das funcionalidades ao contexto
WEBUI = False  # Para limitar o uso das funcionalidades ao contexto

# ----- Colors ----- #
BLACK = "\033[30m"  # Pouco usado para texto
RED = "\033[31m"  # Erros, alertas
GREEN = "\033[32m"  # Sucesso, informação geral
YELLOW = "\033[33m"  # Avisos, destaque leve
BLUE = "\033[34m"  # Títulos, links
MAGENTA = "\033[35m"  # Destaque secundário
CYAN = "\033[36m"  # Informações, comandos
WHITE = "\033[37m"  # Texto normal, pouco usado
RESET = "\033[0m"  # Voltar ao estilo padrão
BOLD = "\033[1m"  # Texto em negrito
UNDERLINE = "\033[4m"  # Sublinhado, bom para títulos
INVERT = "\033[7m"  # Inverte cores do fundo e texto

# ----- ANSI ----- #
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

# ----- FUNCTION & LOG FILE ----- #
FUNC_FILE = {
    # Componentes CORE
    "nrf": "open5gs/install/var/log/open5gs/nrf.log",
    "scp": "open5gs/install/var/log/open5gs/scp.log",
    "udm": "open5gs/install/var/log/open5gs/udm.log",
    "udr": "open5gs/install/var/log/open5gs/udr.log",
    "ausf": "open5gs/install/var/log/open5gs/ausf.log",
    "pcf": "open5gs/install/var/log/open5gs/pcf.log",
    "nssf": "open5gs/install/var/log/open5gs/nssf.log",
    "amf": "open5gs/install/var/log/open5gs/amf.log",
    "smf": "open5gs/install/var/log/open5gs/smf.log",
    "upf": "open5gs/install/var/log/open5gs/upf.log",
    "bsf": "open5gs/install/var/log/open5gs/bsf.log",
    # Componentes GNB
    "gnb": "UERANSIM/log/gnb.log",
    # Componentes UE
    "ue": "UERANSIM/log/ue.log",
}

# ----- LOG TYPE & COLOR ----- #
TYPE_COLOR = {
    "info": GREEN,
    "debug": CYAN,
    "warning": YELLOW,
    "error": RED,
    "fatal": MAGENTA
}

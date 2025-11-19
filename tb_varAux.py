# varAux.py
"""
### Módulo: tb_varAux.py
Módulo responsável por disponibilizar ao *script* principal\\
as **variáveis** auxiliares necessárias ao funcionamento.
"""

import os
import sys
import subprocess
import time
import argparse
import argcomplete
import re
import yaml
from pathlib import Path

# ----- Enviroment ----- #
CORE = False  # Para limitar o uso das funcionalidades ao contexto
GNB = True  # Para limitar o uso das funcionalidades ao contexto
UE = False  # Para limitar o uso das funcionalidades ao contexto

CLI = GNB or UE  # Para limitar o uso das funcionalidades ao contexto
WEBUI = CORE  # Para limitar o uso das funcionalidades ao contexto
LOG = CORE or GNB or UE  # Para limitar o uso das funcionalidades ao contexto
DIFF = CORE or GNB or UE  # Para limitar o uso das funcionalidades ao contexto

SLEEP_BETWEEN_COMMANDS = 0.5 # Tempo de intervalo entre dois comandos consecutivos


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


# ----- NETWORK CONFIG PATH and FILES for CORE, GNB and UE ----- #
NETCONFDIR = "networkConfig"
NETCONFFILES = None

if os.path.isdir(NETCONFDIR):
    NETCONFFILES = [f for f in os.listdir(NETCONFDIR)
                    if os.path.isfile(os.path.join(NETCONFDIR, f))]


# ----- LOG PATH for CORE, GNB and UE ----- #
LOGDIR = None

if CORE:
    LOGDIR = "open5gs/install/var/log/open5gs"
elif GNB:
    LOGDIR = "UERANSIM/log"
elif UE:
    LOGDIR = "UERANSIM/log"


# ----- LOG FILE ----- #
LOGFILES = None

if os.path.isdir(LOGDIR):
    if CORE:
        LOGFILES = [f for f in os.listdir(LOGDIR)
                    if os.path.isfile(os.path.join(LOGDIR, f))]
    elif GNB:
        LOGFILES = [f for f in os.listdir(LOGDIR)
                    if os.path.isfile(os.path.join(LOGDIR, f))
                    and "gnb" in f
                    and ("open5gs" in f or "o5gs" in f)]
    elif UE:
        LOGFILES = [f for f in os.listdir(LOGDIR)
                    if os.path.isfile(os.path.join(LOGDIR, f))
                    and "ue" in f
                    and ("open5gs" in f or "o5gs" in f)]


# ----- LOG TYPE & COLOR ----- #
TYPE_COLOR = {
    "info": GREEN,
    "debug": CYAN,
    "trace": BLUE,
    "warning": YELLOW,
    "error": RED,
    "fatal": MAGENTA
}


# ----- CONFIG PATH for CORE, GNB and UE ----- #
CONFIGDIR = None

if CORE:
    CONFIGDIR = "open5gs/install/etc/open5gs"
elif GNB:
    CONFIGDIR = "UERANSIM/config"
elif UE:
    CONFIGDIR = "UERANSIM/config"


# ----- CONFIGFILES for GNB or UE ----- #
CONFIGFILES = None

if os.path.isdir(CONFIGDIR):
    if CORE:
        CONFIGFILES = [f for f in os.listdir(CONFIGDIR)
                       if os.path.isfile(os.path.join(CONFIGDIR, f))
                       and not f.startswith("_")]
    elif GNB:
        CONFIGFILES = [f for f in os.listdir(CONFIGDIR)
                       if os.path.isfile(os.path.join(CONFIGDIR, f))
                       and "gnb" in f
                       and ("open5gs" in f or "o5gs" in f)]
    elif UE:
        CONFIGFILES = [f for f in os.listdir(CONFIGDIR)
                       if os.path.isfile(os.path.join(CONFIGDIR, f))
                       and "ue" in f
                       and ("open5gs" in f or "o5gs" in f)]


# ----- RUN PATH for CORE, GNB and UE ----- #
RUNDIR = None

if CORE:
    RUNDIR = "open5gs/install/bin"
elif GNB:
    RUNDIR = "UERANSIM/build"
elif UE:
    RUNDIR = "UERANSIM/build"


# ----- NETWORK and RAN FUNCTIONS and EXECUTABLES PATH ----- #
FUNCT_EXEC = None
FUNCT_TYPES = None

if CORE:
    FUNCT_EXEC = {
        "nrf": f"./{RUNDIR}/open5gs-nrfd",
        "scp": f"./{RUNDIR}/open5gs-scpd",
        "udm": f"./{RUNDIR}/open5gs-udmd",
        "udr": f"./{RUNDIR}/open5gs-udrd",
        "ausf": f"./{RUNDIR}/open5gs-ausfd",
        "pcf": f"./{RUNDIR}/open5gs-pcfd",
        "nssf": f"./{RUNDIR}/open5gs-nssfd",
        "amf": f"./{RUNDIR}/open5gs-amfd",   # depende dos anteriores
        "smf": f"./{RUNDIR}/open5gs-smfd",
        "upf": f"./{RUNDIR}/open5gs-upfd",
        "bsf": f"./{RUNDIR}/open5gs-bsfd"
    }
    FUNCT_TYPES = ["NRF", "SCP", "UDM", "UDR", "AUSF",
                   "PCF", "NSSF", "AMF", "SMF", "UPF", "BSF"]
elif GNB:
    FUNCT_EXEC = {
        "gnb": f"{RUNDIR}/nr-gnb"
    }
    FUNCT_TYPES = ["gNB"]
elif UE:
    FUNCT_EXEC = {
        "ue": f"sudo {RUNDIR}/nr-ue"
    }
    FUNCT_TYPES = ["UE"]

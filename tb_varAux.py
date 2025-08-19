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


# ----- LOG FILE ----- #
LOGFILES = None

LOGDIR_CORE = "open5gs/install/var/log/open5gs"  # caminho absoluto na VM CORE
LOGDIR_GNB_UE = "UERANSIM/log"  # caminho absoluto na VM GNB/UE

if os.path.isdir(LOGDIR_CORE):
    if CORE:
        LOGFILES = [f for f in os.listdir(LOGDIR_CORE)
                    if os.path.isfile(os.path.join(LOGDIR_CORE, f))]

if os.path.isdir(LOGDIR_GNB_UE):
    if GNB:
        LOGFILES = [f for f in os.listdir(LOGDIR_GNB_UE)
                    if os.path.isfile(os.path.join(LOGDIR_GNB_UE, f))
                    and "gnb" in f
                    and ("open5gs" in f or "o5gs" in f)]
    elif UE:
        LOGFILES = [f for f in os.listdir(LOGDIR_GNB_UE)
                    if os.path.isfile(os.path.join(LOGDIR_GNB_UE, f))
                    and "ue" in f
                    and ("open5gs" in f or "o5gs" in f)]


# ----- LOG TYPE & COLOR ----- #
TYPE_COLOR = {
    "info": GREEN,
    "debug": CYAN,
    "warning": YELLOW,
    "error": RED,
    "fatal": MAGENTA
}


# ----- CONFIGFILES for GNB or UE ----- #
CONFIGFILES = None

CONFIGDIR = "UERANSIM/config"  # caminho absoluto na VM GNB/UE

if os.path.isdir(CONFIGDIR):
    if CORE:
        CONFIGFILES = None
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


# ----- CONFIGFILES for GNB or UE ----- #
RUNDIR = None

if CORE:
    RUNDIR = "open5gs/install/bin"
elif GNB:
    RUNDIR = "UERANSIM/build"
elif UE:
    RUNDIR = "UERANSIM/build"

# tb_envAux.py
"""
### Módulo: tb_envAux.py
Módulo responsável por disponibilizar ao *script* principal\\
as **variáveis de ambiente** e os **imports** necessários ao funcionamento.
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
from typing import Literal


# ----- Enviroment ----- #
CORE = False  # Para limitar o uso das funcionalidades ao contexto
GNB = True  # Para limitar o uso das funcionalidades ao contexto
UE = False  # Para limitar o uso das funcionalidades ao contexto

CLI = GNB or UE  # Para limitar o uso das funcionalidades ao contexto
WEBUI = CORE  # Para limitar o uso das funcionalidades ao contexto
LOG = CORE or GNB or UE  # Para limitar o uso das funcionalidades ao contexto
DIFF = CORE or GNB or UE  # Para limitar o uso das funcionalidades ao contexto

SLEEP_BETWEEN_COMMANDS = 0.5  # Tempo de intervalo entre dois comandos consecutivos

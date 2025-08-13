# varAux.py

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

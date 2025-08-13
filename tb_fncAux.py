# fncAux.py

import re
import argparse
from tb_varAux import *


def _protect_ansi(text):
    """Substitui seqs ANSI por placeholders e devolve (novo_texto, lista_de_matches)."""
    matches = ANSI_RE.findall(text)
    if not matches:
        return text, []
    out = text
    placeholders = []
    for i, m in enumerate(matches):
        token = f"__ANSI_PLACEHOLDER_{i}__"
        out = out.replace(m, token, 1)
        placeholders.append(m)
    return out, placeholders


def _restore_ansi(text, placeholders):
    """Restaura placeholders pelas seqs ANSI originais."""
    out = text
    for i, m in enumerate(placeholders):
        token = f"__ANSI_PLACEHOLDER_{i}__"
        out = out.replace(token, m, 1)
    return out


def _safe_substitute(text, pattern, repl):
    """Protege sequências ANSI, aplica re.sub, restaura."""
    text_prot, placeholders = _protect_ansi(text)
    text_sub = re.sub(pattern, repl, text_prot)
    return _restore_ansi(text_sub, placeholders)


def color_usage(text):
    # Protege sequências ANSI para evitar conflito
    text_prot, placeholders = _protect_ansi(text)

    # Função para substituir conforme grupo encontrado
    def replacer(m):
        s = m.group(0)
        if s.startswith('./'):  # nome do programa
            return f"{BOLD}{WHITE}{s}{RESET}"
        elif s.startswith('<') and s.endswith('>'):  # <metavars>
            return f"{MAGENTA}{s}{RESET}"
        elif s.startswith('-'):  # -op --opções
            return f"{CYAN}{s}{RESET}"
        else:  # posicionais
            return f"{YELLOW}{s}{RESET}"

    # Regex que apanha todos em grupos numa só passada:
    # ou metavars (<...>), ou opções (-x, --xx), ou posicionais (palavras)
    pattern = r'(\./[^\s]+)|(<[^>]*>)|(-{1,2}[A-Za-z0-9][\w-]*)|(\b(?!-)(?!<)[A-Za-z0-9_-]+\b)'

    text_colored = re.sub(pattern, replacer, text_prot)

    # Restaura as sequências ANSI originais
    return _restore_ansi(text_colored, placeholders)


class ColorHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        super().start_section(f"{BOLD}{GREEN}{heading}{RESET}")

    def _format_action_invocation(self, action):
        if not action.option_strings:
            # Positional argument
            metavar = self._metavar_formatter(action, action.dest)(1)[0]
            return f"{YELLOW}{metavar}{RESET}"
        else:
            options = ', '.join(action.option_strings)
            if action.nargs != 0:
                metavar = self._metavar_formatter(action, action.dest)(1)[0]
                return f"\n{CYAN}{options}{RESET} {MAGENTA}{metavar}{RESET}"
            else:
                return f"\n{CYAN}{options}{RESET}"

    def format_usage(self, usage, actions, groups, prefix=None):
        raw = super().format_usage(usage, actions, groups, prefix)
        raw = raw.replace('usage:', f"{BOLD}{GREEN}usage:{RESET}", 1)
        raw = color_usage(raw)
        return raw

    def format_help(self):
        help_text = super().format_help()
        help_text = help_text.replace(
            'usage:', f"{BOLD}{GREEN}usage:{RESET}", 1)

        lines = help_text.splitlines(True)
        if not lines:
            return help_text

        lines[0] = color_usage(lines[0])
        return ''.join(lines)

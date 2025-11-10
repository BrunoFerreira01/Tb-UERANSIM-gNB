# fncAux.py
"""
### Módulo: tb_fncAux.py
Módulo responsável por disponibilizar ao *script* principal \\
as **funções** auxiliares necessárias ao funcionamento.
"""

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


def splitLineFields(line):

    if CORE:
        padrao = r"^(\d{2}/\d{2}) (\d{2}:\d{2}:\d{2}\.\d+): \[([^\]]+)\] (\w+): (.*)$"
    elif GNB or UE:
        padrao = r"^\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d+)\] \[(.*?)\] \[(.*?)\] (.*)$"

    match = re.match(padrao, line.strip())

    if match:
        data, hora, componente, tipo, mensagem = match.groups()

        return data.lower(), hora.lower(), componente.lower(), tipo.lower(), mensagem

    else:
        return None, None, None, None, None


def colorLine(line, marcador):

    if marcador in line or not line.strip():  # a linha do marcador da nova simulação nem as linhas vazias
        return line

    data, hora, componente, tipo, mensagem = splitLineFields(line)

    # linhas que não tenham feito match
    if all(v is None for v in (data, hora, componente, tipo, mensagem)):
        return line

    COLOR = TYPE_COLOR.get(tipo, RESET)  # default: sem cor

    lineColored = f"[{GREEN}{data} {hora}{RESET}] "
    lineColored += f"[{BOLD}{YELLOW}{componente}{RESET}] "
    lineColored += f"[{COLOR}{tipo}{RESET}] "
    lineColored += f"{RESET}{mensagem}\n"

    return lineColored


def findLastMark(caminho_ficheiro, marcador, bloco=4096):

    tamanho = os.path.getsize(caminho_ficheiro)

    with open(caminho_ficheiro, "rb") as f:

        pos = tamanho
        buffer = b""

        while pos > 0:

            leitura = min(bloco, pos)
            pos -= leitura
            f.seek(pos)
            buffer = f.read(leitura) + buffer

            if marcador.encode() in buffer:
                # Encontrou — determinar a última posição exata
                ultima_pos = buffer.rfind(marcador.encode())
                return pos + ultima_pos

    return 0  # não encontrado, começa do início


def tailLogFile(caminho_ficheiro, marcador, intervalo=0.5):

    start_pos = findLastMark(caminho_ficheiro, marcador)

    with open(caminho_ficheiro, "r") as f:

        f.seek(start_pos)  # posiciona no marcador encontrado

        print()

        try:
            while True:

                linha = f.readline()

                if not linha:
                    time.sleep(intervalo)
                    continue

                print(colorLine(linha, marcador), end="")

        except KeyboardInterrupt:
            print(
                f"\n{YELLOW}{BOLD}Ctrl+C detetado. Leitura do log terminada pelo utilizador.{RESET}\n")
            sys.exit(1)


def coreOptions():
    options = f"{GREEN}{BOLD}options{RESET}:\n"
    options += f"  {CYAN}-c {MAGENTA}<filename>    {RESET}: set configuration file\n"
    options += f"  {CYAN}-l {MAGENTA}<filename>    {RESET}: set logging file\n"
    options += f"  {CYAN}-e {MAGENTA}<level>       {RESET}: set global log-level (default:info)\n"
    options += f"  {CYAN}-m {MAGENTA}<domain>      {RESET}: set log-domain (e.g. mme:sgw:gtp)\n"
    options += f"  {CYAN}-d               {RESET}: print lots of debugging information\n"
    options += f"  {CYAN}-t               {RESET}: print tracing information for developer\n"
    options += f"  {CYAN}-D               {RESET}: start as a daemon\n"
    options += f"  {CYAN}-v               {RESET}: show version number and exit\n"
    options += f"  {CYAN}-h               {RESET}: show this message and exit\n"
    options += f"  {CYAN}-k               {RESET}: use <id> config section\n"

    return options

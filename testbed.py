#!/usr/bin/env python3

import subprocess
import sys

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

processos = []

def executar_comando(comando, cwd):
    try:
        print(f"\n{GREEN}{BOLD}A executar: {YELLOW}{comando}{RESET}\n")
        # subprocess.run(comando, shell=True, check=True, cwd=cwd)
        proc = subprocess.Popen(comando, shell=True, cwd=cwd)
        return proc

    except subprocess.CalledProcessError as e:

        print(f"\n{RED}Erro ao executar o comando: {e}{RESET}\n")
        sys.exit(1)


def printHelp():

    all = False
    core = False
    gnb = False
    ue = False
    cli = False

    if "all" in sys.argv[2:]:
        all = True
    else:
        if "core" in sys.argv[2:]:
            core = True
        if "gnb" in sys.argv[2:]:
            gnb = True
        if "ue" in sys.argv[2:]:
            ue = True
        if "cli" in sys.argv[2:]:
            cli = True

    print()

    print(f"{GREEN}Uso:{RESET}")
    print(
        f"  ./testbed.py {YELLOW}[OPÇÃO] {CYAN}[ARGUMENTOS] {MAGENTA}<VALORES>{RESET}\n")

    print(f"{GREEN}Opções:{RESET}")
    print(f"  {YELLOW}-h, --help{RESET}      Mostra esta ajuda e termina.")
    print(
        f"  {YELLOW}core{RESET}            Executa o 5G Core {BLUE}(Open5GS){RESET}.")

    if all or core:

        print()

    print(f"  {YELLOW}gnb{RESET}             Executa o 5G RAN - gNodeB {BLUE}(UERANSIM){RESET}.")

    if all or gnb:

        print(
            f"    {CYAN}-c, --config {MAGENTA}<config-file>{RESET}  Use specified configuration file for gNB")
        print(
            f"    {CYAN}-l, --disable-cmd{RESET}           Disable command line functionality for this instance")
        print(
            f"    {CYAN}-h, --help{RESET}                  Show this help message and exit")
        print(
            f"    {CYAN}-v, --version{RESET}               Show version information and exit")

        print()

    print(
        f"  {YELLOW}ue{RESET}              Executa o 5G RAN - UE {BLUE}(UERANSIM){RESET}.")

    if all or ue:

        print(
            f"    {CYAN}-c, --config {MAGENTA}<config-file>{RESET}  Use specified configuration file for UE")
        print(
            f"    {CYAN}-i, --imsi {MAGENTA}<imsi>{RESET}           Use specified IMSI number instead of provided one")
        print(f"    {CYAN}-n, --num-of-UE {MAGENTA}<num>{RESET}       Generate specified number of UEs starting from the given IMSI")
        print(
            f"    {CYAN}-t, --tempo {MAGENTA}<tempo>{RESET}         Starting delay in milliseconds for each of the UEs")
        print(
            f"    {CYAN}-l, --disable-cmd{RESET}           Disable command line functionality for this instance")
        print(
            f"    {CYAN}-r, --no-routing-config{RESET}     Do not auto configure routing for UE TUN interface")
        print(
            f"    {CYAN}-h, --help{RESET}                  Show this help message and exit")
        print(
            f"    {CYAN}-v, --version{RESET}               Show version information and exit")

        print()

    print(f"  {YELLOW}cli {MAGENTA}<node-name>{RESET} Executa a CLI para o Node especificado {BLUE}(UERANSIM){RESET}.")

    if all or cli:

        print(
            f"    {CYAN}-d, --dump{RESET}            List all UE and gNBs in the environment")
        print(f"    {CYAN}-e, --exec {MAGENTA}<command>{RESET}  Execute the given command directly without an interactive shell")
        print(
            f"    {CYAN}-h, --help{RESET}            Show this help message and exit")
        print(
            f"    {CYAN}-v, --version{RESET}         Show version information and exit")

        print()

    print(
        f"  {YELLOW}webui{RESET}           Executa o Web UI {BLUE}(Open5GS){RESET}.")
    print(f"  {YELLOW}multi {MAGENTA}<num>{RESET}     Abre o número especificado de terminais na mesma pasta.")

    print()


def processar_opcoes(opcao):

    comando = None
    cwd = None
    num = 1

    if opcao == "core":
        # comando = "./open5gs/build/tests/app/5gc"
        comandos_core = [
            "./open5gs/install/bin/open5gs-nrfd",
            "./open5gs/install/bin/open5gs-scpd",
            "./open5gs/install/bin/open5gs-amfd",
            "./open5gs/install/bin/open5gs-smfd",
            "./open5gs/install/bin/open5gs-ausfd",
            "./open5gs/install/bin/open5gs-udmd",
            "./open5gs/install/bin/open5gs-udrd",
            "./open5gs/install/bin/open5gs-pcfd",
            "./open5gs/install/bin/open5gs-nssfd",
            "./open5gs/install/bin/open5gs-bsfd",
            "./open5gs/install/bin/open5gs-upfd"
        ]
        return comandos_core, cwd, num

    elif opcao == "gnb":
        comando = "UERANSIM/build/nr-gnb -c UERANSIM/config/open5gs-gnb.yaml"

    elif opcao == "ue":
        comando = "UERANSIM/build/nr-ue -c UERANSIM/config/open5gs-ue.yaml"

    elif opcao == "cli":
        comando = "UERANSIM/build/nr-cli"

    elif opcao == "webui":
        comando = "npm run dev"
        cwd = "open5gs/webui"

    elif opcao == "multi":
        comando = "gnome-terminal"

        if len(sys.argv) > 2:

            try:
                num = int(sys.argv[2])

            except ValueError:
                print(
                    f"\n{MAGENTA}{sys.argv[2]} {RED}não é um número válido.{RESET}")
                printHelp()

                sys.exit(1)
        else:
            print(f"\n{RED}Falta argumento {MAGENTA}<num>{RED}.{RESET}")
            printHelp()

            sys.exit(1)

    else:
        print(f"\n{RED}Opção inválida: {CYAN}{opcao}{RED}.{RESET}")
        printHelp()

        sys.exit(1)

    if opcao in ["gnb", "ue", "cli"]:

        if len(sys.argv) > 2:

            comando = ' '.join(comando.split() + sys.argv[2:])

    return [comando], cwd, num


def main():

    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        printHelp()

        sys.exit(1)

    opcao = sys.argv[1]

    comandos, cwd, num = processar_opcoes(opcao)

    for i in range(num):
        for comando in comandos:
            proc = executar_comando(comando, cwd)
            if proc:
                processos.append(proc)

    print(f"\n{CYAN}{BOLD}Total de processos iniciados: {len(processos)}{RESET}\n")

    try:
        # Espera por todos os processos — bloqueia até que sejam terminados
        for proc in processos:
            proc.wait()

    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}Ctrl+C detetado. A terminar os processos...{RESET}\n")

        for proc in processos:
            proc.terminate()
            
        print(f"\n{GREEN}{BOLD}Todos os processos foram terminados com sucesso.{RESET}\n")


if __name__ == "__main__":
    main()

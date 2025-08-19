#!/usr/bin/env python3


from tb_varAux import *
from tb_fncAux import *


# echo 'eval "$(register-python-argcomplete ./testbed.py)"' >> ~/.bashrc


processos = []


def processArgs():

    parser = argparse.ArgumentParser(prog=f"./{os.path.basename(sys.argv[0])}",
                                     formatter_class=ColorHelpFormatter)

    parser.add_argument('-nt', '--newterm',
                        metavar='<num>', type=int, default=1,
                        help='Número de novos terminais a abrir adicionalmente.')

    # Argumento Principal
    subparsers = parser.add_subparsers(dest="command")

    if CORE:  # Sub Argumentos CORE

        core_parser = subparsers.add_parser(name="core",
                                            help=f"Executa o 5G Core {BLUE}(Open5GS){RESET}.",
                                            formatter_class=ColorHelpFormatter)
        core_parser.add_argument('-nt', '--newterm',
                                 action='store_true',
                                 help='Abre um novo terminal depois de executar a instrução principal.')

    if GNB:  # Sub Argumentos GNB

        gnb_parser = subparsers.add_parser(name="gnb",
                                           help=f"Executa o 5G RAN - gNodeB {BLUE}(UERANSIM){RESET}.",
                                           formatter_class=ColorHelpFormatter)
        gnb_parser.add_argument('-c', '--config',
                                metavar='<config-file>', type=str, default='open5gs-gnb.yaml', choices=CONFIGFILES,
                                help='Use specified configuration file for gNB')
        gnb_parser.add_argument('-l', '--disable-cmd',
                                action='store_true',
                                help='Disable command line functionality for this instance')
        gnb_parser.add_argument('-v', '--version',
                                action='store_true',
                                help='Show version information and exit')
        gnb_parser.add_argument('-nt', '--newterm',
                                action='store_true',
                                help='Abre um novo terminal depois de executar a instrução principal.')

    if UE:  # Sub Argumentos UE

        ue_parser = subparsers.add_parser("ue",
                                          help=f"Executa o 5G RAN - UE {BLUE}(UERANSIM){RESET}.",
                                          formatter_class=ColorHelpFormatter)
        ue_parser.add_argument('-c', '--config',
                               metavar='<config-file>', type=str, default='open5gs-ue.yaml', choices=CONFIGFILES,
                               help='Use specified configuration file for UE')
        ue_parser.add_argument('-i', '--imsi',
                               metavar='<imsi>', type=str,
                               help='Use specified IMSI number instead of provided one')
        ue_parser.add_argument('-n', '--num-of-UE',
                               metavar='<num>', type=int,
                               help='Generate specified number of UEs starting from the given IMSI')
        ue_parser.add_argument('-t', '--tempo',
                               metavar='<tempo>', type=int,
                               help='Starting delay in milliseconds for each of the UEs')
        ue_parser.add_argument('-l', '--disable-cmd',
                               action='store_true',
                               help='Disable command line functionality for this instance')
        ue_parser.add_argument('-r', '--no-routing-config',
                               action='store_true',
                               help='Do not auto configure routing for UE TUN interface')
        ue_parser.add_argument('-v', '--version',
                               action='store_true',
                               help='Show version information and exit')
        ue_parser.add_argument('-nt', '--newterm',
                               action='store_true',
                               help='Abre um novo terminal depois de executar a instrução principal.')

    if CLI:  # Sub Argumentos CLI

        cli_parser = subparsers.add_parser(name="cli",
                                           help=f"Executa a CLI para o Node especificado {BLUE}(UERANSIM){RESET}.",
                                           formatter_class=ColorHelpFormatter)
        cli_parser.add_argument('-nn', '--node-name',
                                metavar='<node-name>', type=str,
                                help='Nome do node para executar CLI')
        cli_parser.add_argument('-d', '--dump',
                                action='store_true',
                                help='List all UE and gNBs in the environment')
        cli_parser.add_argument('-e', '--exec',
                                metavar='<command>', type=str,
                                help='Execute the given command directly without an interactive shell')
        cli_parser.add_argument('-v', '--version',
                                action='store_true',
                                help='Show version information and exit')
        cli_parser.add_argument('-nt', '--newterm',
                                action='store_true',
                                help='Abre um novo terminal depois de executar a instrução principal.')

    if WEBUI:  # Sub Argumentos WEBUI

        webui_parser = subparsers.add_parser(name="webui",
                                             help=f"Executa o Web UI {BLUE}(Open5GS){RESET}.",
                                             formatter_class=ColorHelpFormatter)
        webui_parser.add_argument('-nt', '--newterm',
                                  action='store_true',
                                  help='Abre um novo terminal depois de executar a instrução principal.')

    if LOG:  # Sub Argumentos LOG

        log_parser = subparsers.add_parser(name="log",
                                           help=f"Mostra logs de um componente{RESET}.",
                                           formatter_class=ColorHelpFormatter)
        log_parser.add_argument('file',
                                metavar='<file>', type=str, choices=LOGFILES,
                                help='Fichiro cujo log vai ser mostrado.')
        log_parser.add_argument('-nt', '--newterm',
                                action='store_true',
                                help='Abre um novo terminal depois de executar a instrução principal.')

    argcomplete.autocomplete(parser)

    return parser.parse_args()


def execCommand(comando, cwd):
    try:
        print(f"\n{GREEN}{BOLD}A executar: {YELLOW}{comando}{RESET}\n")
        # subprocess.run(comando, shell=True, check=True, cwd=cwd)
        proc = subprocess.Popen(comando, shell=True,
                                cwd=cwd, executable="/bin/bash")
        return proc

    except subprocess.CalledProcessError as e:

        print(f"\n{RED}Erro ao executar o comando: {e}{RESET}\n")
        sys.exit(1)


def processOptions(args):

    comando = None
    cwd = None

    if args.command == "core":

        if CORE:  # Estou no ambiente CORE

            comando = [
                f"./{RUNDIR}/open5gs-nrfd",
                f"./{RUNDIR}/open5gs-scpd",
                f"./{RUNDIR}/open5gs-udmd",
                f"./{RUNDIR}/open5gs-udrd",
                f"./{RUNDIR}/open5gs-ausfd",
                f"./{RUNDIR}/open5gs-pcfd",
                f"./{RUNDIR}/open5gs-nssfd",
                f"./{RUNDIR}/open5gs-amfd",       # só depois dos anteriores
                f"./{RUNDIR}/open5gs-smfd",
                f"./{RUNDIR}/open5gs-upfd",
                f"./{RUNDIR}/open5gs-bsfd"
            ]

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "gnb":

        if GNB:  # Estou no ambiente GNB

            comando = f"{RUNDIR}/nr-gnb"

            if args.config is not None:  # -c, --config <config-file>
                comando += f" -c {CONFIGDIR}/{args.config}"

            if args.disable_cmd:  # -l, --disable-cmd
                comando += f" -l"

            if args.version:  # -v, --version
                comando += f" -v"

            log_path = f"{LOGDIR_GNB_UE}/{args.config.replace('.yaml', '.log')}"

            with open(log_path, "a") as log_file:
                log_file.write("\n")

            comando += f" | tee -a {log_path}"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}GNB={GNB}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "ue":

        if UE:  # Estou no ambiente UE

            comando = f"sudo {RUNDIR}/nr-ue"

            if args.config is not None:  # -c, --config <config-file>
                comando += f" -c {CONFIGDIR}/{args.config}"

            if args.imsi is not None:  # -i, --imsi <imsi>
                comando += f" -i {args.imsi}"

            if args.num_of_UE is not None:  # -n, --num-of-UE <num>
                comando += f" -n {args.num_of_UE}"

            if args.tempo is not None:  # -t, --tempo <tempo>
                comando += f" -t {args.tempo}"

            if args.disable_cmd:  # -l, --disable-cmd
                comando += f" -l"

            if args.no_routing_config:  # -r, --no-routing-config
                comando += f" -r"

            if args.version:  # -v, --version
                comando += f" -v"

            log_path = f"{LOGDIR_GNB_UE}/{args.config.replace('.yaml', '.log')}"

            with open(log_path, "a") as log_file:
                log_file.write("\n")

            comando += f" | tee -a {log_path}"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}UE={UE}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "cli":

        if CLI:  # Estou no ambiente CLI

            comando = f"{RUNDIR}/nr-cli"

            if args.node_name is not None:  # -nn, --node-name <node-name>
                comando += f" {args.node_name}"

            if args.dump:  # -d, --dump
                comando += f" -d"

            if args.exec is not None:  # -e, --exec <command>
                comando += f" -e {args.exec}"

            if args.version:  # -v, --version
                comando += f" -v"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}CLI={CLI}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "webui":

        if WEBUI:  # Estou no ambiente WEBUI

            comando = "npm run dev"
            cwd = "open5gs/webui"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}WEBUI={WEBUI}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "log":

        file = None
        marcador = None

        if CORE:  # Estou no ambiente CORE

            file = f"{LOGDIR_CORE}/{args.file}"
            marcador = "Open5GS daemon v"

        elif GNB:  # Estou no ambiente GNB

            file = f"{LOGDIR_GNB_UE}/{args.file}"
            marcador = "UERANSIM v"

        elif UE:  # Estou no ambiente UE

            file = f"{LOGDIR_GNB_UE}/{args.file}"
            marcador = "UERANSIM v"

        for i in range(args.newterm):  # Se a opção de abrir novos terminais tenha sido ativada
            execCommand("gnome-terminal", None)

        # Processar para a leitura do ficheiro
        tailLogFile(file, marcador)

    # Se não for lista de comandos, porque o CORE são vários
    if not isinstance(comando, list):
        comando = [comando]

    return comando, cwd


def main():

    args = processArgs()

    # print(f"Comando selecionado: {args.command}")
    # print(args)

    comandos, cwd = processOptions(args)

    print(comandos)

    if comandos != [None]:  # Se exisitir uma lista de comandos

        for comando in comandos:

            proc = execCommand(comando, cwd)

            if proc:
                processos.append(proc)

    for i in range(args.newterm):  # Se a opção de abrir novos terminais tenha sido ativada
        execCommand("gnome-terminal", None)

    print(f"\n{CYAN}{BOLD}Total de processos iniciados: {len(processos)}{RESET}\n")

    try:
        # Espera por todos os processos — bloqueia até que sejam terminados
        for proc in processos:
            proc.wait()

    except KeyboardInterrupt:
        print(
            f"\n{YELLOW}{BOLD}Ctrl+C detetado. A terminar os processos...{RESET}\n")

        for proc in processos:
            proc.terminate()

        print(
            f"\n{GREEN}{BOLD}Todos os processos foram terminados com sucesso.{RESET}\n")


if __name__ == "__main__":
    main()

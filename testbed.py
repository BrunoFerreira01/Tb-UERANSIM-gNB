#!/usr/bin/env python3


from tb_varAux import *
from tb_fncAux import *


# echo 'eval "$(register-python-argcomplete ./testbed.py)"' >> ~/.bashrc


processos = []


def processArgs():

    parser = argparse.ArgumentParser(prog=f"./{os.path.basename(sys.argv[0])}",
                                     formatter_class=ColorHelpFormatter)

    # Argumento Principal
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub Argumentos CORE
    core_parser = subparsers.add_parser(name="core",
                                        help=f"Executa o 5G Core {BLUE}(Open5GS){RESET}.",
                                        formatter_class=ColorHelpFormatter)

    # Sub Argumentos GNB
    gnb_parser = subparsers.add_parser(name="gnb",
                                       help=f"Executa o 5G RAN - gNodeB {BLUE}(UERANSIM){RESET}.",
                                       formatter_class=ColorHelpFormatter)
    gnb_parser.add_argument('-c', '--config',
                            metavar='<config-file>', type=str, default='open5gs-gnb.yaml',
                            help='Use specified configuration file for gNB')
    gnb_parser.add_argument('-l', '--disable-cmd',
                            action='store_true',
                            help='Disable command line functionality for this instance')
    gnb_parser.add_argument('-v', '--version',
                            action='store_true',
                            help='Show version information and exit')

    # Sub Argumentos UE
    ue_parser = subparsers.add_parser("ue",
                                      help=f"Executa o 5G RAN - UE {BLUE}(UERANSIM){RESET}.",
                                      formatter_class=ColorHelpFormatter)
    ue_parser.add_argument('-c', '--config',
                           metavar='<config-file>', type=str, default='open5gs-ue.yaml',
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

    # Sub Argumentos CLI
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

    # Sub Argumentos WEBUI
    webui_parser = subparsers.add_parser(name="webui",
                                         help=f"Executa o Web UI {BLUE}(Open5GS){RESET}.",
                                         formatter_class=ColorHelpFormatter)

    # Sub Argumentos MULTI
    multi_parser = subparsers.add_parser(name="multi",
                                         help=f"Executa o Web UI {BLUE}(Open5GS){RESET}.",
                                         formatter_class=ColorHelpFormatter)
    multi_parser.add_argument('num_terms',
                              metavar='<num>', type=int,
                              help='Número de terminais a abrir')

    # Sub Argumentos LOG
    log_parser = subparsers.add_parser(name="log",
                                       help=f"Mostra logs de um componente{RESET}.",
                                       formatter_class=ColorHelpFormatter)
    log_parser.add_argument('func',
                            metavar='<func>', type=str, choices=list(FUNC_FILE.keys()),
                            help='Componente cujos logs vão ser mostrados.')

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
    num = 1

    if args.command == "core":

        if CORE:  # Estou no ambiente CORE

            # comando = "./open5gs/build/tests/app/5gc"

            comando = [
                "./open5gs/install/bin/open5gs-nrfd",
                "./open5gs/install/bin/open5gs-scpd",
                "./open5gs/install/bin/open5gs-udmd",
                "./open5gs/install/bin/open5gs-udrd",
                "./open5gs/install/bin/open5gs-ausfd",
                "./open5gs/install/bin/open5gs-pcfd",
                "./open5gs/install/bin/open5gs-nssfd",
                "./open5gs/install/bin/open5gs-amfd",       # só depois dos anteriores
                "./open5gs/install/bin/open5gs-smfd",
                "./open5gs/install/bin/open5gs-upfd",
                "./open5gs/install/bin/open5gs-bsfd"
            ]

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "gnb":

        if GNB:  # Estou no ambiente GNB

            log_path = "UERANSIM/log/gnb.log"

            with open(log_path, "a") as log_file:
                log_file.write("\n")

            comando = "UERANSIM/build/nr-gnb"

            if args.config is not None:  # -c, --config <config-file>
                comando += f" -c UERANSIM/config/{args.config}"

            if args.disable_cmd:  # -l, --disable-cmd
                comando += f" -l"

            if args.version:  # -v, --version
                comando += f" -v"

            comando += f" | tee -a {log_path}"

            # comando = "UERANSIM/build/nr-gnb -c UERANSIM/config/open5gs-gnb.yaml"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}GNB={GNB}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "ue":

        if UE:  # Estou no ambiente UE

            log_path = "UERANSIM/log/ue.log"

            with open(log_path, "a") as log_file:
                log_file.write("\n")

            comando = "sudo UERANSIM/build/nr-ue"

            if args.config is not None:  # -c, --config <config-file>
                comando += f" -c UERANSIM/config/{args.config}"

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

            comando += f" | tee -a {log_path}"

            # comando = "sudo UERANSIM/build/nr-ue -c UERANSIM/config/open5gs-ue.yaml"

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}UE={UE}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "cli":

        if CLI:  # Estou no ambiente CLI

            comando = "UERANSIM/build/nr-cli"

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

    elif args.command == "multi":
        comando = "gnome-terminal"

        num = int(args.num_terms)

    elif args.command == "log":

        func = list(FUNC_FILE.keys())
        file = None
        marcador = None

        if CORE:  # Estou no ambiente CORE

            if args.func in func[:-2]:
                file = FUNC_FILE[args.func]
                marcador = "Open5GS daemon v"

            else:
                print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

                sys.exit(1)

        elif GNB:  # Estou no ambiente GNB

            if args.func in func[-2]:
                file = FUNC_FILE[args.func]
                marcador = "UERANSIM v"

            else:
                print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

                sys.exit(1)

        elif UE:  # Estou no ambiente UE

            if args.func in func[-1]:
                file = FUNC_FILE[args.func]
                marcador = "UERANSIM v"

            else:
                print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

                sys.exit(1)

        # Processar para a leitura do ficheiro
        tailLogFile(file, marcador)

    # Se não for lista de comandos, porque o CORE são vários
    if not isinstance(comando, list):
        comando = [comando]

    return comando, cwd, num


def main():

    args = processArgs()

    # print(f"Comando selecionado: {args.command}")
    # print(args)

    comandos, cwd, num = processOptions(args)

    for i in range(num):
        for comando in comandos:
            proc = execCommand(comando, cwd)
            if proc:
                processos.append(proc)

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

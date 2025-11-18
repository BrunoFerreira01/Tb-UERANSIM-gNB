#!/usr/bin/env python3


from tb_varAux import *
from tb_fncAux import *
from tb_clsAux import *


# echo 'eval "$(register-python-argcomplete ./testbed.py)"' >> ~/.bashrc


processos = []


def processArgs():

    parser = argparse.ArgumentParser(prog=f"./{os.path.basename(sys.argv[0])}",
                                     formatter_class=ColorHelpFormatter)

    parser.add_argument('-nt', '--newterm',
                        metavar='<num>', type=int, default=0, nargs='?', const=1,
                        help='Número de novos terminais a abrir adicionalmente.')

    # Argumento Principal
    subparsers = parser.add_subparsers(dest="command")

    if CORE:  # Sub Argumentos CORE

        core_parser = subparsers.add_parser(name="core",
                                            help=f"Executa o 5G Core {BLUE}(Open5GS){RESET}.",
                                            formatter_class=ColorHelpFormatter)
        core_parser.add_argument('netConfigFile',
                                 metavar='<file>', type=str, choices=NETCONFFILES,
                                 help='Fichiro de configuração da rede.')
        core_parser.add_argument('-nt', '--newterm',
                                 metavar='<num>', type=int, default=0, nargs='?', const=1,
                                 help='Abre um novo terminal depois de executar a instrução principal.')

    if GNB:  # Sub Argumentos GNB

        gnb_parser = subparsers.add_parser(name="gnb",
                                           help=f"Executa o 5G RAN - gNodeB {BLUE}(UERANSIM){RESET}.",
                                           formatter_class=ColorHelpFormatter)
        gnb_parser.add_argument('netConfigFile',
                                metavar='<file>', type=str, choices=NETCONFFILES,
                                help='Fichiro de configuração da rede.')
        gnb_parser.add_argument('-nt', '--newterm',
                                metavar='<num>', type=int, default=0, nargs='?', const=1,
                                help='Abre um novo terminal depois de executar a instrução principal.')

    if UE:  # Sub Argumentos UE

        ue_parser = subparsers.add_parser("ue",
                                          help=f"Executa o 5G RAN - UE {BLUE}(UERANSIM){RESET}.",
                                          formatter_class=ColorHelpFormatter)
        ue_parser.add_argument('netConfigFile',
                               metavar='<file>', type=str, choices=NETCONFFILES,
                               help='Fichiro de configuração da rede.')
        ue_parser.add_argument('-nt', '--newterm',
                               metavar='<num>', type=int, default=0, nargs='?', const=1,
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
                                metavar='<num>', type=int, default=0, nargs='?', const=1,
                                help='Abre um novo terminal depois de executar a instrução principal.')

    if WEBUI:  # Sub Argumentos WEBUI

        webui_parser = subparsers.add_parser(name="webui",
                                             help=f"Executa o Web UI {BLUE}(Open5GS){RESET}.",
                                             formatter_class=ColorHelpFormatter)
        webui_parser.add_argument('-nt', '--newterm',
                                  metavar='<num>', type=int, default=0, nargs='?', const=1,
                                  help='Abre um novo terminal depois de executar a instrução principal.')

    if LOG:  # Sub Argumentos LOG

        log_parser = subparsers.add_parser(name="log",
                                           help=f"Mostra logs de um componente{RESET}.",
                                           formatter_class=ColorHelpFormatter)
        log_parser.add_argument('file',
                                metavar='<file>', type=str, choices=LOGFILES,
                                help='Fichiro cujo log vai ser mostrado.')
        log_parser.add_argument('-nt', '--newterm',
                                metavar='<num>', type=int, default=0, nargs='?', const=1,
                                help='Abre um novo terminal depois de executar a instrução principal.')

    if DIFF:  # Sub Argumentos DIFF

        diffnetworkconf_parser = subparsers.add_parser(name="diffnetworkconf",
                                                       help=f"Mostra as diferenças entre dois ficheiros de configuração da rede{RESET}.",
                                                       formatter_class=ColorHelpFormatter)
        diffnetworkconf_parser.add_argument('file1',
                                            metavar='<file1>', type=str, choices=NETCONFFILES,
                                            help='Fichiro original a ser comparado.')
        diffnetworkconf_parser.add_argument('file2',
                                            metavar='<file2>', type=str, choices=NETCONFFILES,
                                            help='Fichiro editado a ser comparado.')
        diffnetworkconf_parser.add_argument('-nt', '--newterm',
                                            metavar='<num>', type=int, default=0, nargs='?', const=1,
                                            help='Abre um novo terminal depois de executar a instrução principal.')

        diffinstanceconf_parser = subparsers.add_parser(name="diffinstanceconf",
                                                        help=f"Mostra as diferenças entre dois ficheiros de configuração de instância{RESET}.",
                                                        formatter_class=ColorHelpFormatter)
        diffinstanceconf_parser.add_argument('file1',
                                             metavar='<file1>', type=str, choices=CONFIGFILES,
                                             help='Fichiro original a ser comparado.')
        diffinstanceconf_parser.add_argument('file2',
                                             metavar='<file2>', type=str, choices=CONFIGFILES,
                                             help='Fichiro editado a ser comparado.')
        diffinstanceconf_parser.add_argument('-nt', '--newterm',
                                             metavar='<num>', type=int, default=0, nargs='?', const=1,
                                             help='Abre um novo terminal depois de executar a instrução principal.')

    argcomplete.autocomplete(parser)

    return parser.parse_args()


def execCommand(comando, cwd):
    try:
        print(f"\n{GREEN}{BOLD}A executar: {YELLOW}{cleanString(comando)}{RESET}\n")
        # subprocess.run(comando, shell=True, check=True, cwd=cwd)
        proc = subprocess.Popen(comando, shell=True,
                                cwd=cwd, executable="/bin/bash")
        return proc

    except subprocess.CalledProcessError as e:

        print(f"\n{RED}Erro ao executar o comando: {e}{RESET}\n")
        sys.exit(1)


def processOptions(args, system: SystemConfig):

    comando = []
    cwd = None

    if args.command == "core":

        if CORE:  # Estou no ambiente CORE

            for nf_type, nf in system.core.network_functions.items():

                for inst in nf.instances.values():

                    if inst.active:

                        inst: NetworkFunctionInstance

                        cmd = f"{FUNCT_EXEC[nf_type.lower()]} {inst.get_command()}"

                        if inst.new_terminal:
                            title = f"echo -e \"\n{BOLD}{BLUE}=== {CYAN}Function: {YELLOW}{nf_type.upper()} {BLUE}|{MAGENTA} Instance Name: {YELLOW}{inst.name}{BLUE} ==={RESET}\n\""
                            cmd = f"gnome-terminal -- bash -c '{title}; {cmd}; exec bash'"

                        comando.append(cmd)

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}CORE={CORE}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "gnb":

        if GNB:  # Estou no ambiente GNB

            for nf_type, nf in system.ran.network_functions.items():

                for inst in nf.instances.values():

                    if inst.active and nf_type == "gNB":

                        inst: gNBInstance

                        log_path = f"{LOGDIR}/{inst.config_file.replace('.yaml', '.log')}"

                        with open(log_path, "a") as log_file:
                            log_file.write("\n")

                        cmd = f"{FUNCT_EXEC[nf_type.lower()]} {inst.get_command()} | tee -a {log_path}"

                        if inst.new_terminal:
                            title = f"echo -e \"\n{BOLD}{BLUE}=== {CYAN}Function: {YELLOW}{nf_type.upper()} {BLUE}|{MAGENTA} Instance Name: {YELLOW}{inst.name}{BLUE} ==={RESET}\n\""
                            cmd = f"gnome-terminal -- bash -c '{title}; {cmd}; exec bash'"

                        comando.append(cmd)

        else:
            print(f"\n{RED}Ambiente errado: {CYAN}GNB={GNB}{RED}.\n{RESET}")

            sys.exit(1)

    elif args.command == "ue":

        if UE:  # Estou no ambiente UE

            for nf_type, nf in system.ran.network_functions.items():

                for inst in nf.instances.values():

                    if inst.active and nf_type == "UE":

                        inst: UEInstance

                        log_path = f"{LOGDIR}/{inst.config_file.replace('.yaml', '.log')}"

                        with open(log_path, "a") as log_file:
                            log_file.write("\n")

                        cmd = f"{FUNCT_EXEC[nf_type.lower()]} {inst.get_command()} | tee -a {log_path}"

                        if inst.new_terminal:
                            title = f"echo -e \"\n{BOLD}{BLUE}=== {CYAN}Function: {YELLOW}{nf_type.upper()} {BLUE}|{MAGENTA} Instance Name: {YELLOW}{inst.name}{BLUE} ==={RESET}\n\""
                            cmd = f"gnome-terminal -- bash -c '{title}; {cmd}; exec bash'"

                        comando.append(cmd)

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

        file = f"{LOGDIR}/{args.file}"
        marcador = None

        if CORE:  # Estou no ambiente CORE
            marcador = "Open5GS daemon v"

        elif GNB:  # Estou no ambiente GNB
            marcador = "UERANSIM v"

        elif UE:  # Estou no ambiente UE
            marcador = "UERANSIM v"

        for i in range(args.newterm):  # Se a opção de abrir novos terminais tenha sido ativada
            execCommand("gnome-terminal", None)

        # Processar para a leitura do ficheiro
        tailLogFile(file, marcador)

    elif args.command == "diffnetworkconf":

        comando = f"diff -u --color=always {NETCONFDIR}/{args.file1} {NETCONFDIR}/{args.file2}"

    elif args.command == "diffinstanceconf":

        comando = f"diff -u --color=always {CONFIGDIR}/{args.file1} {CONFIGDIR}/{args.file2}"

    # Se não for lista de comandos, porque o CORE, GNB e UE são vários
    if not isinstance(comando, list):
        comando = [comando]

    return comando, cwd


def main():

    args = processArgs()

    # print(f"Comando selecionado: {args.command}")
    # print(args)

    system = SystemConfig.load_yaml(f"{NETCONFDIR}/{args.netConfigFile}") if args.command in [
        "core", "gnb", "ue"] else None

    print(system)

    comandos, cwd = processOptions(args, system)

    # for cmd in comandos:
    #     print(cmd)

    # system.save_yaml(f"{NETCONFDIR}/{args.netConfigFile}")

    if comandos != [None]:  # Se exisitir uma lista de comandos

        for comando in comandos:

            proc = execCommand(comando, cwd)

            time.sleep(0.5)

            if proc:
                processos.append(proc)

    for i in range(args.newterm):  # Se a opção de abrir novos terminais tenha sido ativada
        execCommand("gnome-terminal", None)

    print(f"\n{CYAN}{BOLD}Total de processos iniciados: {len(processos)}{RESET}\n")

    try:
        # Espera por todos os processos: bloqueia até que sejam terminados
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

# clsAux.py
"""
### Módulo: tb_clsAux.py
Módulo responsável por disponibilizar ao *script* principal\\
as **classes** auxiliares necessárias ao funcionamento.
"""
from tb_varAux import *

# === MODELOS DE DADOS ===


class NetworkFunctionInstance:
    def __init__(self,
                 name: str | None = None,
                 active: bool = False,
                 new_terminal: bool = False,
                 config_file: str | None = None,
                 log_file: str | None = None,
                 log_level: str | None = None,
                 log_domain: str | None = None,
                 debug: bool = False,
                 trace: bool = False,
                 daemon: bool = False,
                 version: bool = False,
                 help_flag: bool = False
                 ):
        self.name = name
        self.active = active
        self.new_terminal = new_terminal
        # -c file    : set configuration file
        self.config_file = config_file
        # -l file    : set logging fil
        self.log_file = log_file
        # -e level   : set global log-level (def:info)
        self.log_level = log_level
        # -m domain  : set log-domain (e.g. mme:sgw:gtp)
        self.log_domain = log_domain
        # -d         : print lots of debugging information
        self.debug = debug
        # -t         : print tracing information for developer
        self.trace = trace
        # -D         : start as a daemon
        self.daemon = daemon
        # -v         : show version number and exit
        self.version = version
        # -h         : show this message and exit
        self.help_flag = help_flag

    def __str__(self):
        instance = f"{BOLD}{MAGENTA}Instance Name:{RESET} {BOLD}{YELLOW}{self.name}{RESET}\n"
        lines = []
        lines.append(
            f"  {WHITE}Active:{RESET}      {BOLD}{GREEN if self.active else RED}{self.active}{RESET}")
        lines.append(
            f"  {WHITE}New Terminal:{RESET}{GREEN if self.new_terminal else RED}{self.new_terminal}{RESET}")
        lines.append(
            f"  {WHITE}Config File:{RESET} {YELLOW}{self.config_file}{RESET}")
        if self.log_file:
            lines.append(
                f"  {WHITE}Log File:{RESET}    {YELLOW}{self.log_file}{RESET}")
        if self.log_level:
            lines.append(
                f"  {WHITE}Log Level:{RESET}   {YELLOW}{self.log_level}{RESET}")
        if self.log_domain:
            lines.append(
                f"  {WHITE}Log Domain:{RESET}  {YELLOW}{self.log_domain}{RESET}")
        if self.debug:
            lines.append(
                f"  {WHITE}Debug:{RESET}       {GREEN}{self.debug}{RESET}")
        if self.trace:
            lines.append(
                f"  {WHITE}Trace:{RESET}       {GREEN}{self.trace}{RESET}")
        if self.daemon:
            lines.append(
                f"  {WHITE}Daemon:{RESET}      {GREEN}{self.daemon}{RESET}")
        if self.version:
            lines.append(
                f"  {WHITE}Version:{RESET}     {GREEN}{self.version}{RESET}")
        if self.help_flag:
            lines.append(
                f"  {WHITE}Help:{RESET}        {GREEN}{self.help_flag}{RESET}")

        return instance + "\n".join(lines)

    # --- Métodos genéricos ---
    def get_command(self):
        """Gera o comando CLI para executar esta instância."""
        cmd = []

        if self.config_file:
            cmd += ["-c", f"{CONFIGDIR}/{self.config_file}"]
        if self.log_file:
            cmd += ["-l", f"{LOGDIR}/{self.log_file}"]
        if self.log_level:
            cmd += ["-e", self.log_level]
        if self.log_domain:
            cmd += ["-m", self.log_domain]
        if self.debug:
            cmd.append("-d")
        if self.trace:
            cmd.append("-t")
        if self.daemon:
            cmd.append("-D")
        if self.version:
            cmd.append("-v")
        if self.help_flag:
            cmd.append("-h")

        return " ".join(cmd)

    def set_attr(self, attr, value):
        """Define dinamicamente o valor de um atributo existente."""
        if not hasattr(self, attr):
            raise AttributeError(f"Atributo '{attr}' não existe.")
        setattr(self, attr, value)
        print(f"[OK] {attr} definido como: {value}")

    def reset_attr(self, attr):
        """Reinicia um atributo para o seu valor padrão."""
        defaults = {
            "active": False,
            "new_terminal": False,
            "config_file": None,
            "log_file": None,
            "log_level": None,
            "log_domain": None,
            "debug": False,
            "trace": False,
            "daemon": False,
            "version": False,
            "help_flag": False
        }
        if attr not in defaults:
            raise AttributeError(f"Não é possível resetar '{attr}'.")
        setattr(self, attr, defaults[attr])
        print(
            f"[OK] {attr} foi reiniciado para o valor padrão: {defaults[attr]}")

    def to_dict(self):
        """Retorna apenas os atributos cujo valor difere dos valores por defeito."""
        default = type(self)()  # cria nova instância com valores default
        result = {}
        for key, value in vars(self).items():
            if getattr(default, key) != value:
                result[key] = value

        result["name"] = self.name
        result["active"] = self.active
        result["new_terminal"] = self.new_terminal
        result["config_file"] = self.config_file

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            active=data.get("active", False),
            new_terminal=data.get("new_terminal", False),
            config_file=data.get("config_file", None),
            log_file=data.get("log_file", None),
            log_level=data.get("log_level", None),
            log_domain=data.get("log_domain", None),
            debug=data.get("debug", False),
            trace=data.get("trace", False),
            daemon=data.get("daemon", False),
            version=data.get("version", False),
            help_flag=data.get("help_flag", False)
        )


class NetworkFunction:
    def __init__(self, nf_type):
        self.nf_type = nf_type
        self.instances = {}  # nome -> NetworkFunctionInstance

    def __str__(self):
        header = f"{BOLD}{CYAN}{self.nf_type}:{RESET}"
        lines = [header]
        if not self.instances:
            lines.append(f"  {MAGENTA}<no instances>{RESET}")
        else:
            for inst in self.instances.values():
                # indentamos cada instância
                inst_str = str(inst).replace("\n", "\n  ")
                lines.append(f"  {inst_str}")
        return "\n".join(lines)

    def add_instance(self, name, config_file=None):
        if name in self.instances:
            raise ValueError(
                f"A instância '{name}' já existe em {self.nf_type}")
        self.instances[name] = NetworkFunctionInstance(name, config_file)

    def remove_instance(self, name):
        self.instances.pop(name, None)

    def to_dict(self):
        return {
            nf.name: nf.to_dict()
            for nf in self.instances.values()
        }

    @classmethod
    def from_dict(cls, nf_type, data):
        nf = cls(nf_type)
        for name, inst_data in data.items():
            nf.instances[name] = NetworkFunctionInstance.from_dict(inst_data)
        return nf


class CoreConfig:

    def __init__(self):
        self.network_functions = {t: NetworkFunction(t) for t in FUNCT_TYPES}

    def __str__(self):
        header = f"{BOLD}{CYAN}Core Configuration:{RESET}"
        lines = [header]
        for nf_type, nf in self.network_functions.items():
            nf_str = str(nf).replace("\n", "\n  ")
            lines.append(f"  {nf_str}")
        return "\n".join(lines)

    def add_instance(self, nf_type, name, config_file=None):
        self.network_functions[nf_type].add_instance(name, config_file)

    def remove_instance(self, nf_type, name):
        self.network_functions[nf_type].remove_instance(name)

    def to_dict(self):
        return {
            nf_type: nf.to_dict()
            for nf_type, nf in self.network_functions.items()
        }

    @classmethod
    def from_dict(cls, data):
        core = cls()
        for nf_type, nf_data in data.items():
            core.network_functions[nf_type] = NetworkFunction.from_dict(
                nf_type, nf_data)
        return core


class gNBInstance:
    def __init__(self,
                 name: str | None = None,
                 active: bool = False,
                 new_terminal: bool = False,
                 config_file: str | None = None,
                 disable_cmd: bool = False,
                 version: bool = False,
                 help_flag: bool = False
                 ):
        self.name = name
        self.active = active
        self.new_terminal = new_terminal
        # -c file   : Use specified configuration file for gNB
        self.config_file = config_file
        # -l        : Disable command line functionality for this instance
        self.disable_cmd = disable_cmd
        # -v        : show version number and exit
        self.version = version
        # -h        : show this message and exit
        self.help_flag = help_flag

    def __str__(self):
        instance = f"{BOLD}{MAGENTA}Instance Name:{RESET} {BOLD}{YELLOW}{self.name}{RESET}\n"
        lines = []
        lines.append(
            f"  Active:{RESET}      {BOLD}{GREEN if self.active else RED}{self.active}{RESET}")
        lines.append(
            f"  New Terminal:{RESET}{GREEN if self.new_terminal else RED}{self.new_terminal}{RESET}")
        lines.append(
            f"  Config File:{RESET} {YELLOW}{self.config_file}{RESET}")
        if self.disable_cmd:
            lines.append(
                f"  Disable cmd:{RESET} {GREEN}{self.disable_cmd}{RESET}")
        if self.version:
            lines.append(f"  Version:{RESET}     {GREEN}{self.version}{RESET}")
        if self.help_flag:
            lines.append(
                f"  Help:{RESET}        {GREEN}{self.help_flag}{RESET}")

        return instance + "\n".join(lines)

    # --- Métodos genéricos ---
    def get_command(self):
        """Gera o comando CLI para executar esta instância."""
        cmd = []

        if self.config_file:
            cmd += ["-c", f"{CONFIGDIR}/{self.config_file}"]
        if self.disable_cmd:
            cmd.append("-l")
        if self.version:
            cmd.append("-v")
        if self.help_flag:
            cmd.append("-h")

        return " ".join(cmd)

    def set_attr(self, attr, value):
        """Define dinamicamente o valor de um atributo existente."""
        if not hasattr(self, attr):
            raise AttributeError(f"Atributo '{attr}' não existe.")
        setattr(self, attr, value)
        print(f"[OK] {attr} definido como: {value}")

    def reset_attr(self, attr):
        """Reinicia um atributo para o seu valor padrão."""
        defaults = {
            "active": False,
            "new_terminal": False,
            "config_file": None,
            "disable_cmd": False,
            "version": False,
            "help_flag": False
        }
        if attr not in defaults:
            raise AttributeError(f"Não é possível resetar '{attr}'.")
        setattr(self, attr, defaults[attr])
        print(
            f"[OK] {attr} foi reiniciado para o valor padrão: {defaults[attr]}")

    def to_dict(self):
        """Retorna apenas os atributos cujo valor difere dos valores por defeito."""
        default = type(self)()  # cria nova instância com valores default
        result = {}
        for key, value in vars(self).items():
            if getattr(default, key) != value:
                result[key] = value

        result["name"] = self.name
        result["active"] = self.active
        result["new_terminal"] = self.new_terminal
        result["config_file"] = self.config_file

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            active=data.get("active", False),
            new_terminal=data.get("new_terminal", False),
            config_file=data.get("config_file", None),
            disable_cmd=data.get("disable_cmd", False),
            version=data.get("version", False),
            help_flag=data.get("help_flag", False)
        )


class UEInstance:
    def __init__(self,
                 name: str | None = None,
                 active: bool = False,
                 new_terminal: bool = False,
                 config_file: str | None = None,
                 imsi: str | None = None,
                 num_of_ue: int | None = None,
                 tempo: int | None = None,
                 disable_cmd: bool = False,
                 no_routing_config: bool = False,
                 version: bool = False,
                 help_flag: bool = False
                 ):
        self.name = name
        self.active = active
        self.new_terminal = new_terminal
        # -c file   : Use specified configuration file for UE
        self.config_file = config_file
        # -i imsi   : Use specified IMSI number instead of provided one
        self.imsi = imsi
        # -n num    : Generate specified number of UEs starting from the given IMSI
        self.num_of_ue = num_of_ue
        # -t tempo  : Starting delay in milliseconds for each of the UEs
        self.tempo = tempo
        # -l        : Disable command line functionality for this instance
        self.disable_cmd = disable_cmd
        # -r        : Do not auto configure routing for UE TUN interface
        self.no_routing_config = no_routing_config
        # -v        : show version number and exit
        self.version = version
        # -h        : show this message and exit
        self.help_flag = help_flag

    def __str__(self):
        instance = f"{BOLD}{MAGENTA}Instance Name:{RESET} {BOLD}{YELLOW}{self.name}{RESET}\n"
        lines = []
        lines.append(
            f"  {WHITE}Active:{RESET}      {BOLD}{GREEN if self.active else RED}{self.active}{RESET}")
        lines.append(
            f"  {WHITE}New Terminal:{RESET}{GREEN if self.new_terminal else RED}{self.new_terminal}{RESET}")
        lines.append(
            f"  {WHITE}Config File:{RESET} {YELLOW}{self.config_file}{RESET}")
        if self.imsi:
            lines.append(
                f"  {WHITE}IMSI:{RESET}        {YELLOW}{self.imsi}{RESET}")
        if self.num_of_ue:
            lines.append(
                f"  {WHITE}Number UEs:{RESET}  {YELLOW}{self.num_of_ue}{RESET}")
        if self.tempo:
            lines.append(
                f"  {WHITE}Tempo:{RESET}       {YELLOW}{self.tempo}{RESET} ms")
        if self.disable_cmd:
            lines.append(
                f"  {WHITE}Disable cmd:{RESET} {GREEN}{self.disable_cmd}{RESET}")
        if self.no_routing_config:
            lines.append(
                f"  {WHITE}No Rou Conf:{RESET} {GREEN}{self.no_routing_config}{RESET}")
        if self.version:
            lines.append(
                f"  {WHITE}Version:{RESET}     {GREEN}{self.version}{RESET}")
        if self.help_flag:
            lines.append(
                f"  {WHITE}Help:{RESET}        {GREEN}{self.help_flag}{RESET}")

        return instance + "\n".join(lines)

    # --- Métodos genéricos ---
    def get_command(self):
        """Gera o comando CLI para executar esta instância."""
        cmd = []

        if self.config_file:
            cmd += ["-c", f"{CONFIGDIR}/{self.config_file}"]
        if self.imsi:
            cmd += ["-i", f"{self.imsi}"]
        if self.num_of_ue:
            cmd += ["-n", f"{self.num_of_ue}"]
        if self.tempo:
            cmd += ["-t", f"{self.tempo}"]
        if self.disable_cmd:
            cmd.append("-l")
        if self.no_routing_config:
            cmd.append("-r")
        if self.version:
            cmd.append("-v")
        if self.help_flag:
            cmd.append("-h")

        return " ".join(cmd)

    def set_attr(self, attr, value):
        """Define dinamicamente o valor de um atributo existente."""
        if not hasattr(self, attr):
            raise AttributeError(f"Atributo '{attr}' não existe.")
        setattr(self, attr, value)
        print(f"[OK] {attr} definido como: {value}")

    def reset_attr(self, attr):
        """Reinicia um atributo para o seu valor padrão."""
        defaults = {
            "active": False,
            "new_terminal": False,
            "config_file": None,
            "imsi": None,
            "num_of_ue": None,
            "tempo": None,
            "disable_cmd": False,
            "no_routing_config": False,
            "version": False,
            "help_flag": False
        }
        if attr not in defaults:
            raise AttributeError(f"Não é possível resetar '{attr}'.")
        setattr(self, attr, defaults[attr])
        print(
            f"[OK] {attr} foi reiniciado para o valor padrão: {defaults[attr]}")

    def to_dict(self):
        """Retorna apenas os atributos cujo valor difere dos valores por defeito."""
        default = type(self)()  # cria nova instância com valores default
        result = {}
        for key, value in vars(self).items():
            if getattr(default, key) != value:
                result[key] = value

        result["name"] = self.name
        result["active"] = self.active
        result["new_terminal"] = self.new_terminal
        result["config_file"] = self.config_file

        return result

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            active=data.get("active", False),
            new_terminal=data.get("new_terminal", False),
            config_file=data.get("config_file", None),
            imsi=data.get("imsi", None),
            num_of_ue=data.get("num_of_ue", None),
            tempo=data.get("tempo", None),
            disable_cmd=data.get("disable_cmd", False),
            no_routing_config=data.get("no_routing_config", False),
            version=data.get("version", False),
            help_flag=data.get("help_flag", False)
        )


class RANFunction:
    def __init__(self, func_type):
        self.func_type = func_type
        self.instances = {}  # nome -> gNBInstance ou UEInstance

    def __str__(self):
        header = f"{BOLD}{CYAN}{self.func_type}:{RESET}"
        lines = [header]
        if not self.instances:
            lines.append(f"  {MAGENTA}<no instances>{RESET}")
        else:
            for inst in self.instances.values():
                inst_str = str(inst).replace("\n", "\n  ")
                lines.append(f"  {inst_str}")
        return "\n".join(lines)

    def add_instance(self, name, config_file=None):
        if name in self.instances:
            raise ValueError(
                f"A instância '{name}' já existe em {self.func_type}")

        if self.func_type == "gNB":
            self.instances[name] = gNBInstance(name, config_file=config_file)
        elif self.func_type == "UE":
            self.instances[name] = UEInstance(name, config_file=config_file)

    def remove_instance(self, name):
        self.instances.pop(name, None)

    def to_dict(self):
        return {
            nf.name: nf.to_dict()
            for nf in self.instances.values()
        }

    @classmethod
    def from_dict(cls, func_type, data):
        func = cls(func_type)
        for name, inst_data in data.items():
            if func_type == "gNB":
                func.instances[name] = gNBInstance.from_dict(inst_data)
            elif func_type == "UE":
                func.instances[name] = UEInstance.from_dict(inst_data)
        return func


class RANConfig:

    def __init__(self):
        self.network_functions = {t: RANFunction(t) for t in FUNCT_TYPES}

    def __str__(self):
        header = f"{BOLD}{CYAN}RAN Configuration:{RESET}"
        lines = [header]
        for func_type, func in self.network_functions.items():
            func_str = str(func).replace("\n", "\n  ")
            lines.append(f"  {func_str}")
        return "\n".join(lines)

    def add_instance(self, nf_type, name, config_file=None):
        self.network_functions[nf_type].add_instance(name, config_file)

    def remove_instance(self, nf_type, name):
        self.network_functions[nf_type].remove_instance(name)

    def to_dict(self):
        return {nf_type: nf.to_dict() for nf_type, nf in self.network_functions.items()}

    @classmethod
    def from_dict(cls, data):
        ran = cls()
        for nf_type, nf_data in data.items():
            ran.network_functions[nf_type] = RANFunction.from_dict(
                nf_type, nf_data)
        return ran


class SystemConfig:
    """Camada de topo que agrupa as configurações do Core e outras futuras."""

    def __init__(self, core=None, ran=None, other_configs=None):

        self.core = core or CoreConfig()
        self.ran = ran or RANConfig()
        self.other_configs = other_configs or {}

    def __str__(self):
        header = f"{BOLD}{BLUE}=== System Configuration ==={RESET}"
        lines = [header]
        if CORE:
            lines.append(str(self.core))
        elif GNB:
            lines.append(str(self.ran.network_functions["gNB"]))
        elif UE:
            lines.append(str(self.ran.network_functions["UE"]))
        else:
            # fallback: mostrar tudo
            lines.append(str(self.core))
            lines.append(str(self.ran))
        if self.other_configs:
            lines.append(f"{BOLD}{CYAN}Other Configurations:{RESET}")
            lines.append(str(self.other_configs))
        return "\n".join(lines)

    def to_dict(self):
        """Converte apenas as partes relevantes consoante o contexto."""
        data = {}
        if CORE:
            data["Core"] = self.core.to_dict()
        elif GNB:
            data["RAN"] = {"gNB": self.ran.network_functions["gNB"].to_dict()}
        elif UE:
            data["RAN"] = {"UE": self.ran.network_functions["UE"].to_dict()}
        else:
            data = {
                "Core": self.core.to_dict(),
                "RAN": self.ran.to_dict()
            }
        if self.other_configs:
            data["OtherConfigs"] = self.other_configs
        return data

    @classmethod
    def from_dict(cls, data):
        """Carrega apenas as partes relevantes consoante o contexto."""
        core = CoreConfig.from_dict(
            data.get("Core", {})) if CORE else CoreConfig()
        ran_data = data.get("RAN", {})
        if GNB:
            ran = RANConfig.from_dict({"gNB": ran_data.get("gNB", {})})
        elif UE:
            ran = RANConfig.from_dict({"UE": ran_data.get("UE", {})})
        else:
            ran = RANConfig.from_dict(ran_data)
        other = data.get("OtherConfigs", {})
        return cls(core=core, ran=ran, other_configs=other)

    def save_yaml(self, filename):
        """Guarda apenas as partes relevantes consoante o contexto."""
        with open(filename, "w") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False,
                           allow_unicode=True)

    @classmethod
    def load_yaml(cls, filename):
        """Carrega apenas as partes relevantes consoante o contexto."""
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(f"Ficheiro '{filename}' não encontrado.")
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls.from_dict(data)

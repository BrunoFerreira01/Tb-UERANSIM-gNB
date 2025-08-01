# Instalação do Wireshark

Começar por atualizar os repositórios e instalar o Wireshark.

```bash
$ sudo apt update
$ sudo apt install wireshark -y
```

Confirmar opção "Sim", no "pop-up", para que todos os users possam capturar pacotes.

Adicionar o utilizador ao grupo `wireshark`

```bash
$ sudo usermod -aG wireshark $USER
```

Reiniciar a sessão na Virtual Machine.

Verifiar a instalação ou abrir o programa.

```bash
$ wireshark --version # Consultar a versão
$ wireshark # Executar o wireshark
```
import os
import sys

def check_firewalld():
    with open("/etc/os-release", "r") as file:
        for line in file:
            if line.startswith("NAME="):
                distro_id = line.split("=")[1].strip().strip('"')

    if distro_id == "ubuntu":
        install_firewalld = input("O firewall-cmd não está instalado. Deseja instalar o firewalld? (S/N): ").lower()
        if install_firewalld == "s":
            os.system("sudo apt install firewalld -y")  
            os.system("sudo systemctl start firewalld")  
            os.system("sudo systemctl enable firewalld")  
            print("Firewalld instalado e iniciado com sucesso.")
        else:
            print("Firewalld não instalado. Algumas funcionalidades podem não estar disponíveis.")
    elif distro_id == "centos" or distro_id == "rhel":
        install_firewalld = input("O firewall-cmd não está instalado. Deseja instalar o firewalld? (S/N): ").lower()
        if install_firewalld == "s":
            os.system("sudo yum install firewalld -y")  
            os.system("sudo systemctl start firewalld")  
            os.system("sudo systemctl enable firewalld")  
            print("Firewalld instalado e iniciado com sucesso.")
        else:
            print("Firewalld não instalado. Algumas funcionalidades podem não estar disponíveis.")
    else:
        print("Distribuição não suportada.")

def show_options(options):
    for i, option in enumerate(options, start=1):
        if i == len(options):  
            print("[0]", option)
        else:
            print(f"[{i}] {option}")

def select_option(prompt, options):
    while True:
        try:
            choice = input(prompt)
            if choice == '0':
                return None  
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except KeyboardInterrupt:
            print('Ctrl+C')

def show_list(title, items):
    print(f"{title}:")
    show_options(items)

def configure_zone_manually(selected_zone, selected_interface):
    print("\nConfiguração manual para a zona:")
    show_list("Opções", ["Configurar icmp-block-inversion (yes/no)", "Configurar forward (yes/no)", "Configurar masquerade (yes/no)", "Configurar interfaces", "Desativar zona", "Voltar ao menu principal"])

    while True:
        choice = input("Escolha uma opção: ")

        if choice == "1":
            icmp_choice = input("Deseja bloquear icmp? (yes/no): ").lower()
            if icmp_choice == 'yes':
                icmp_type = input("Digite o tipo de ICMP a ser bloqueado: ")
                os.system(f"firewall-cmd --zone={selected_zone} --add-icmp-block={icmp_type}")
                print(f"ICMP tipo {icmp_type} bloqueado.")
            elif icmp_choice == 'no':
                print("Configuração de ICMP não alterada.")
            else:
                print("Escolha inválida. Tente novamente.")

        elif choice == "2":
            forward_choice = input("Deseja configurar forward? (yes/no): ").lower()
            if forward_choice == 'yes':
                forward_value = input("Digite 'yes' ou 'no' para forward: ")
                os.system(f"firewall-cmd --zone={selected_zone} --add-option=forward --value={forward_value}")
                print(f"Forward configurado para {forward_value}.")
            elif forward_choice == 'no':
                print("Configuração de forward não alterada.")
            else:
                print("Escolha inválida. Tente novamente.")

        elif choice == "3":
            masquerade_choice = input("Deseja configurar masquerade? (yes/no): ").lower()
            if masquerade_choice == 'yes':
                masquerade_value = input("Digite 'yes' ou 'no' para masquerade: ")
                os.system(f"firewall-cmd --zone={selected_zone} --add-option=masquerade --value={masquerade_value}")
                print(f"Masquerade configurado para {masquerade_value}.")
            elif masquerade_choice == 'no':
                print("Configuração de masquerade não alterada.")
            else:
                print("Escolha inválida. Tente novamente.")

        elif choice == "4":
            os.system(f"firewall-cmd --zone={selected_zone} --remove-interface={selected_interface}")
            os.system(f"firewall-cmd --zone={selected_zone} --permanent --remove-interface={selected_interface}")

            interfaces = show_interfaces()
            selected_interface = select_option("Escolha a interface (número): ", interfaces)

            os.system(f"firewall-cmd --zone={selected_zone} --add-interface={selected_interface}")
            os.system(f"firewall-cmd --zone={selected_zone} --permanent --add-interface={selected_interface}")
            print(f"Interface alterada para {selected_interface} na zona {selected_zone}.")

        elif choice == "5":
            if selected_zone == "public":
                print("A zona 'public' é uma zona integrada e não pode ser desativada.")
            else:
                os.system(f"firewall-cmd --permanent --zone={selected_zone} --remove-interface={selected_interface}")
                os.system(f"firewall-cmd --zone={selected_zone} --remove-interface={selected_interface}")
                print(f"Zona {selected_zone} desativada.")

        elif choice == "6":
            break
        elif choice == "0":
            return 
        else:
            print("Escolha inválida. Tente novamente.")


def apply_firewall_settings(selected_interface, selected_zone, selected_service, selected_port, blocked_ips):
    try:
        if selected_interface:
            print(f"Configurando interface: {selected_interface}")
            os.system(f"firewall-cmd --zone={selected_zone} --change-interface={selected_interface}")
            os.system("firewall-cmd --reload")
            print("Configurações da interface aplicadas.")

        if selected_zone:
            print(f"Configurando zona: {selected_zone}")
            if selected_service and selected_service != "Voltar ao Menu":
                os.system(f"firewall-cmd --zone={selected_zone} --add-service={selected_service}")
                os.system(f"firewall-cmd --zone={selected_zone} --permanent --add-service={selected_service}")
            if selected_port:
                os.system(f"firewall-cmd --permanent --zone={selected_zone} --add-port={selected_port}/tcp")
            configure_zone_manually(selected_zone, selected_interface)
            os.system("firewall-cmd --reload")
            print("Configurações da zona aplicadas.")

        if selected_service and selected_service != "Voltar ao Menu":
            print(f"Configurando serviço: {selected_service}")

        if selected_port:
            print(f"Configurando porta: {selected_port}")

        for blocked_ip in blocked_ips:
            print(f"Bloqueando IP: {blocked_ip}")

        os.system('firewall-cmd --list-all')    
        print("Configurações aplicadas com sucesso.")
    except Exception as e:
        print(f"Erro ao aplicar configurações: {e}")

def show_interfaces():
    print("Interfaces disponíveis:")
    interfaces = os.listdir("/sys/class/net")
    show_list("Opções", interfaces + ["Voltar ao menu principal"])
    return interfaces

def show_zones():
    print("Zonas disponíveis:")
    zones = os.popen("firewall-cmd --get-zones").read().strip().split()
    show_list("Opções", zones + ["Voltar ao menu principal"])
    return zones

def show_running_services():
    print("Serviços rodando:")
    known_services = ["sshd", "httpd", "nginx", "mysql", "postgresql", "apache2", "vsftpd", "proftpd"] 
    running_services = os.popen("systemctl list-units --type=service --state=running --no-pager | awk '{print $1}'").read().strip().split()
    all_services = known_services + running_services
    all_services.append("Voltar ao Menu")
    show_list("Opções", all_services)
    return all_services

def show_interface_configuration(interface):
    try:
        print(f"\nConfiguração da interface {interface}:")
        os.system(f"firewall-cmd --zone=$(firewall-cmd --get-zone-of-interface={interface}) --list-all")
    except Exception as e:
        print(f"Erro ao obter configuração da interface {interface}: {e}")

def show_zone_configuration(zone):
    try:
        print(f"\nConfiguração da zona {zone}:")
        os.system(f"firewall-cmd --zone={zone} --list-all")
    except Exception as e:
        print(f"Erro ao obter configuração da zona {zone}: {e}")

def configure_firewall():
    check_firewalld()  
    blocked_ips = set()
    selected_interface = None
    selected_zone = None
    selected_service = None
    selected_port = None
    press = '(Pressione qualquer tecla para voltar ao menu inicial)'
    os.system('clear')

    while True:
        print('''
            ;                ..                              ..
          .DL               ;W,      ,##############Wf.     ;W,
  f.     :K#L     LWL      j##,       ........jW##Wt       j##,
  EW:   ;W##L   .E#f      G###,             tW##Kt        G###,
  E#t  t#KE#L  ,W#;     :E####,           tW##E;        :E####,
  E#t f#D.L#L t#K:     ;W#DG##,         tW##E;         ;W#DG##,
  E#jG#f  L#LL#G      j###DW##,      .fW##D,          j###DW##,
  E###;   L###j      G##i,,G##,    .f###D,           G##i,,G##,
  E#K:    L#W;     :K#K:   L##,  .f####Gffffffff;  :K#K:   L##,
  EG      LE.     ;##D.    L##, .fLLLLLLLLLLLLi   ;##D.    L##,
  ;       ;@      ,,,      .,,                    ,,,      .,, 
''')
        print("Opções:")
        show_options([
            f"Selecionar interface {'(Selecionado: ' + selected_interface + ')' if selected_interface else ''}",
            f"Selecionar zona {'(Selecionado: ' + selected_zone + ')' if selected_zone else ''}",
            f"Selecionar serviços {'(Selecionado: ' + selected_service + ')' if selected_service else ''}",
            f"Selecionar portas {'(Selecionado: ' + selected_port + ')' if selected_port else ''}",
            "Bloquear IP",
            "Bloquear Range de IPs por máscara",
            "Mostrar Configuração da Interface",
            "Mostrar Configuração da Zona",
            "Listar IPs bloqueados",
            "Aplicar Configurações",
            "Sair"
        ])

        choice = input("\nEscolha uma opção: ")

        if choice == "1":
            interfaces = show_interfaces()
            iface_choice = select_option("Escolha a interface (número): ", interfaces)
            selected_interface = iface_choice
            print(f"Interface escolhida: {selected_interface}")
            os.system('clear')

        elif choice == "2":
            zones = show_zones()
            zone_choice = select_option("Escolha a zona (número): ", zones)
            selected_zone = zone_choice
            print(f"Zona escolhida: {selected_zone}")
            os.system('clear')

        elif choice == "3":
            services = show_running_services()
            service_choice = select_option("Escolha o serviço (número): ", services)
            selected_service = service_choice
            print(f"Serviço escolhido: {selected_service}")
            input(press)
            os.system('clear')
        elif choice == "4":
            selected_port = input("Digite a porta desejada: ")
            print(f"Porta escolhida: {selected_port}")
            input(press)
            os.system('clear')
        elif choice == "5":
            ip_to_block = input("Digite o IP a ser bloqueado: ")
            blocked_ips.add(ip_to_block)
            print(f"IP {ip_to_block} bloqueado.")
            input(press)
            os.system('clear')
        elif choice == "6":
            range_to_block = input("Digite o range de IPs a ser bloqueado (ex: 192.168.0.0/24): ")
            blocked_ips.add(range_to_block)
            print(f"Range de IPs {range_to_block} bloqueado.")
            input(press)
            os.system('clear')
        elif choice == "7":
            if selected_interface:
                show_interface_configuration(selected_interface)
                input(press)
                os.system('clear')
            else:
                print("Nenhuma interface selecionada.")
                input(press)
                os.system('clear')
        elif choice == "8":
            if selected_zone:
                show_zone_configuration(selected_zone)
                input(press)
                os.system('clear')
            else:
                print("Nenhuma zona selecionada.")
                input(press)
                os.system('clear')
        elif choice == "9":
            print("Lista de IPs bloqueados:")
            show_list("IPs bloqueados", blocked_ips)
            input(press)
            os.system('clear')
        elif choice == "10":
            apply_firewall_settings(selected_interface, selected_zone, selected_service, selected_port, blocked_ips)
            input(press)
            os.system('clear')
        elif choice == "0":
            break
        else:
            print("Escolha inválida.")

if __name__ == "__main__":
    configure_firewall()

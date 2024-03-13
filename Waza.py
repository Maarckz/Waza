###################################
## DEFINIDA A VARIAVEL DA VERSÃO ##
###################################
version = '\033[7;32mv1.2dev\033[m'

import os

#############################################################
## VERIFICA A DISTRO LINUX, INSTALA E HABILITA O FIREWALLD ##
#############################################################
def verifica_distro_e_firewall():
    with open("/etc/os-release", "r") as arquivo: #
        
        for linha in arquivo:
           
            if linha.startswith("ID="):
                distro_id = linha.split("=")[1].strip().strip('"')
    
    ##############################
    ## DISTROS A SER VERIFICADA ##
    ##############################
    if distro_id in ["ubuntu", "oracle", "rhel"]:
        status = os.system("sudo systemctl status firewalld >/dev/null 2>&1")
      
        if status == 0:
            print("Firewalld está instalado e em execução.")
       
        else:
            intalar_firewalld = input(f"O firewalld não está instalado. Deseja instalar o firewalld no {distro_id}? (S/N): ").lower()
          
            if intalar_firewalld == "s":
                package_manager = "apt" if distro_id == "ubuntu" else "yum"

                #############################################
                ## INSTALA, INICIA, E HABILITA O FIREWALLD ##
                #############################################
                os.system(f"sudo {package_manager} install firewalld -y")
                os.system("sudo systemctl start firewalld")
                os.system("sudo systemctl enable firewalld")
                print("Firewalld instalado e iniciado com sucesso.")
           
            else:
                print("Firewalld não instalado. Instale manualmente e tente novamente!")
  
    else:
        print("Distribuição não suportada.")

#######################################
## FUNÇÃO PARA CONFIGURAR O FIREWALL ##
#######################################
def configure_firewall():
    verifica_distro_e_firewall()

    ##############################################################
    ## DEFINE UMA SEQUENCIA DE VARIÁVEIS PARA INTERAÇÃO DO MENU ##
    ############################################################## 
    seleciona_interface = None
    seleciona_zonas_str = None
    selected_services_str = None
    block_selected_services_str = None
    selected_ports_str = None
    block_selected_ports_str = None
    port_list = None
    press = '(Pressione qualquer tecla para voltar ao menu inicial)'
    
    os.system('clear')
   
    try:
        while True:
            ###########################
            ## BANNER PRA FICAR COOL ##
            ###########################
            print(f'''\033[1;91m
        .DL               ;W,      ,##############Wf.     ;W,
f.     :K#L     LWL      j##,       ........jW##Wt       j##,
EW:   ;W##L   .E#f      G###,             tW##Kt        G###,
E#t  t#KE#L  ,W#;     :E####,           tW##E;        :E####,
E#t f#D.L#L t#K:     ;W#DG##,         tW##E;         ;W#DG##,
E#jG#f  L#LL#G      j###DW##,      .fW##D,          j###DW##,
E###;   L###j      G##i,,G##,    .f###D,           G##i,,G##,
E#K:    L#W;     :K#K:   L##,  .f####Gffffffff;  :K#K:   L##,
EG      LE.     ;##D.    L##, .fLLLLLLLLLLLLi   ;##D.    L##,
                                                     \033[m{version}''')
            
            print("Opções:\n")

            #######################################################
            ## LISTAGEM DE OPÇÕES PARA FACILITAR O USUÁRIO.      ##
            ## A LÓGICA É FAZER O USUÁRIO SELECIONAR A INTERFACE ##
            ## E A ZONA E DEPOIS PENSAR EM CONFIGURAR.           ##
            ##                                                   ##
            ## NESTE TRECHO TAMBÉM HÁ ALGUMAS CONDICIONAIS PARA  ##
            ## EXIBIR FEEDBACK DO QUE ESTÁ ACONTECENDO APOS O    ##
            ## USUÁRIO FAZER A SELEÇÃO DAS CONFIGURAÇÕES         ##
            #######################################################
            print(f"\033[0;34m[1]\033[m - Selecionar interface {'(Selecionado: ' + seleciona_interface + ')' if seleciona_interface else ''}")
           
            if seleciona_zonas_str:
                print(f"\033[0;34m[2]\033[m - Selecionar zona (Selecionado:  {seleciona_zonas_str})")
           
            else:
                print(f"\033[0;34m[2]\033[m - Selecionar zona")
          
            if selected_services_str:
                print(f"\033[0;34m[3]\033[m - Liberar serviços (Selecionados: {selected_services_str})")
           
            else:
                print("\033[0;34m[3]\033[m - Liberar serviços")            
           
            if selected_ports_str:
                print(f"\033[0;34m[4]\033[m - Liberar portas (Selecionados: {selected_ports_str})")
           
            else:
                print("\033[0;34m[4]\033[m - Liberar portas ")
           
            if block_selected_services_str:
                print(f"\033[0;34m[5]\033[m - Bloquear serviços (Selecionados: {block_selected_services_str})")
          
            else:
                print("\033[0;34m[5]\033[m - Bloquear serviços")            
          
            if block_selected_ports_str:
                print(f"\033[0;34m[6]\033[m - Bloquear portas (Selecionados: {block_selected_ports_str})")
          
            else:
                print("\033[0;34m[6]\033[m - Bloquear portas ") 
            print(f"\033[0;34m[7]\033[m - Remover interface da Zona")
            print(f"\033[0;34m[8]\033[m - Bloquear IP")
            print(f"\033[0;34m[9]\033[m - Bloquear IPs por Máscara")
            print(f'\033[0;34m[10]\033[m- Listar todas as Zonas')
            print(f"\033[0;34m[11]\033[m- Mostrar Configuração da Zona")
            print(f"\033[0;34m[12]\033[m- Listar IPs bloqueados")
            print("\033[0;34m[13]\033[m- Aplicar Configurações")
            print("\033[0;34m[0]\033[m - Sair")


            opcao = input("\nEscolha uma opção: ")

            ###########################################################
            ## EXIBE UM MENU PARA SELEÇÃO DAS INTERFACES DISPONÍVEIS ##
            ###########################################################
            if opcao == "1":
                interfaces = os.popen("ls /sys/class/net/").read().strip().split()
                print("Interfaces disponíveis:")
              
                for i, iface in enumerate(interfaces, start=1):
                    print(f"[{i}] {iface}")
              
                try:
                    print("[0] Voltar ao Menu")
                    interface_index = int(input("Escolha a interface (número): "))
                 
                    if interface_index == 0:
                        seleciona_interface = None
                  
                    elif 1 <= interface_index <= len(interfaces):
                        seleciona_interface = interfaces[interface_index - 1]
               
                except (ValueError, IndexError):
                    print("Escolha inválida.")

            ######################################################### 
            ## EXIBE UM MENU PARA SELEÇÃO DAS ZONAS DISPONÍVEIS    ##
            ## AQUI ELE PERMITE MULTISELEÇÃO DAS ZONAS DISPONÍVEIS ##
            #########################################################                  
            elif opcao == "2": 
                    zonas = os.popen("firewall-cmd --get-zones").read().strip().split()
                    print("Zonas disponíveis:")
                   
                    for i, zone in enumerate(zonas, start=1):
                        print(f"[{i}] {zone}")
                   
                    try:
                        print("[0] Voltar ao Menu")
                        seleciona_zonas = []
                      
                        while True:
                            zone_index = int(input("Escolha a zona (número): "))
                           
                            if zone_index == 0:
                                break
                          
                            elif 1 <= zone_index <= len(zonas):
                                seleciona_zona = zonas[zone_index - 1]
                                seleciona_zonas.append(seleciona_zona)  
                           
                            else:
                                print("Escolha inválida.")
                            seleciona_zonas_str = ', '.join(seleciona_zonas)
                   
                    except (ValueError, IndexError):
                        print("Escolha inválida.")

            #########################################################
            ## EXIBE UM MENU PARA SELEÇÃO DOS SERVIÇOS DISPONÍVEIS ##
            ## AQUI ELE PERMITE MULTISELEÇÃO DOS SERVIÇOS          ##
            #########################################################                        
            elif opcao == "3": 
                if seleciona_zona and seleciona_interface:
                    services = os.popen("""firewall-cmd --get-services""").read().strip().split()
                    services = [service.strip() for service in services if service.strip()]
                    print("Escolha os Serviços:")
                  
                    for i, service in enumerate(services, start=1):
                        print(f"[{i}] {service}")
                    try:
                        print("[0] Voltar ao Menu")
                        selected_services = []
                        
                        while True:
                            service_index = int(input("Escolha o serviço (número): "))
                          
                            if service_index == 0:
                                break
                           
                            elif 1 <= service_index <= len(services):
                                selected_service = services[service_index - 1]
                                selected_services.append(selected_service)
                            
                            else:
                                print("Escolha inválida.")
                        selected_services_str = ', '.join(selected_services)
                    
                    except (ValueError, IndexError):
                        print("Escolha inválida.")
               
                else:
                    print("Zona ou serviço não selecionado.")
        
            ###########################################################
            ## PEDE UMA ENTRADA DAS PORTAS QUE DESEJA PERMITIR.      ##
            ## AS PORTAS SÃO SEPARADAS POR "," E SENDO ENVIADAS PARA ##
            ## UMA LISTA QUE SERÁ CONFIGURADA MAIS PARA FRENTE       ##
            ###########################################################         
            elif opcao == "4":
                if seleciona_zona:
                    ports = input("Digite a(s) porta(s) desejada(s) separada(s) por vírgula: ")
                    port_list = ports.split(',')
                   
                    for index, port in enumerate(port_list):
                        try:
                            port_list[index] = port.strip()
                        except ValueError:
                            print(f"Entrada inválida para a porta: {port}")
                    selected_ports_str = ', '.join(port_list)
                
                else:
                    print("Zona ou serviço não selecionado.")

            #########################################################
            ## EXIBE UM MENU PARA SELEÇÃO DOS SERVIÇOS DISPONÍVEIS ##
            ## AQUI ELE PERMITE MULTISELEÇÃO DOS SERVIÇOS          ##
            #########################################################              
            elif opcao == "5":
                if seleciona_zona:
                    block_services = os.popen("""firewall-cmd --get-services""").read().strip().split()
                    block_services = [block_service.strip() for block_service in block_services if block_service.strip()]
                    print("Escolha os Serviços:")
                   
                    for i, block_service in enumerate(block_services, start=1):
                        print(f"[{i}] {block_service}")
                    try:
                        print("[0] Voltar ao Menu")
                        block_selected_services = []
                      
                        while True:
                            block_service_index = int(input("Escolha o serviço (número): "))
                         
                            if block_service_index == 0:
                                break
                         
                            elif 1 <= block_service_index <= len(block_services):
                                block_selected_service = block_services[block_service_index - 1]
                                block_selected_services.append(block_selected_service)
                        
                            else:
                                print("Escolha inválida.")
                        block_selected_services_str = ', '.join(block_selected_services)
                   
                    except (ValueError, IndexError):
                        print("Escolha inválida.")
              
                else:
                    print("Zona ou serviço não selecionado.")
            
            ##############################################################
            ## A OPÇÃO 6 SERÁ O PROCESSO INVERSO DA PERMISSÃO DE PORTAS ##
            ##############################################################
            elif opcao == '6':
                pass
            
            #################################################################
            ## PERMITE REMOVER DA ZONA SELECIONADA A INTERFACE SELECIONADA ##
            #################################################################
            elif opcao == "7": 
                if seleciona_zona and seleciona_interface:
                    sit_remove = input(f"Deseja remover a interface {seleciona_interface} da zona {seleciona_zona}. (S/N) ")
                    
                    if sit_remove.lower() == 's':
                        os.system(f"firewall-cmd --zone={seleciona_zona} --permanent --remove-interface={seleciona_interface}")
                        os.system("firewall-cmd --reload")
                        print(f"Interface {seleciona_interface}removida da zona {seleciona_zona}.")
               
                else:
                    print("Selecione a Interface a ser removida e a Zona a ser configurada.")

            ############################################################################
            ## PERMITE BLOQUEAR IP INDIVIDUALMENTE, AINDA NÃO TEM TRATAMENTO COM "RE" ##
            ############################################################################        
            elif opcao == "8":
                bloquear_ip = input("Digite o IP a ser bloqueado: ")
                os.system(f"firewall-cmd --permanent --zone={seleciona_zona} --add-rich-rule='rule family=ipv4 source address={bloquear_ip} drop'")
                print(f"IP {bloquear_ip} bloqueado.")
                input(press)

            ########################################
            ##   PERMITE BLOQUEAR A FAIXA DE IP   ##
            ########################################
            elif opcao == "9":
                ip_mask = input("Digite a faixa de IP a ser bloqueado: ")
                os.system(f"firewall-cmd --permanent --zone={seleciona_zona} --add-rich-rule='rule family=ipv4 source address={ip_mask} drop'")
                print(f"Range de IPs {ip_mask} bloqueado.")
                input(press)

            ##########################
            ## LISTA TODAS AS ZONAS ##
            ##########################
            elif opcao == "10":
                os.system('firewall-cmd --list-all-zones')
                input(press)

            ##############################################
            ## LISTA A CONFIGURAÇÃO DA ZONA SELECIONADA ##
            ##############################################
            elif opcao == "11":
                try:
                    os.system(f'firewall-cmd --zone={seleciona_zona} --list-all')
                    input(press)
                except UnboundLocalError:
                    print('Selecione uma zona.')
                    input(press)
            
            #############################
            ## LISTA OS IPS BLOQUEADOS ##
            #############################
            elif opcao == "12":
                os.system('sudo iptables -L -n')
                input(press)

            ##################################################################################################
            ## A MAGICA ACONTECE AQUI! AQUI ESTÁ A CONFIGURAÇÃO FINAL DE TUDO QUE FOI SELECIONADO NO SCRIPT ##
            ##################################################################################################    
            ## ESTA OPÇÃO CONFIRMA AS ALTERAÇÕES SELECIONADAS, E FAZ ABRE POSSIBILIDADE DE NOVOS AJUSTES ##
            ###############################################################################################
            elif opcao == "13":
                try:
                    ########################################################
                    ## FAZ A ALTERAÇÃO DA INTERFACE PARA ZONA SELECIONADA ##
                    ########################################################
                    if seleciona_zona and seleciona_interface:
                        cfg_iface = os.popen(f"firewall-cmd --zone={seleciona_zona} --change-interface={seleciona_interface} --permanent").read()
                        print(f'Configuração da INTERFACE e ZONA: {cfg_iface}')
                        
                        ##############################################################
                        ## SE O SERVIÇO ESTIVER SELECIONADO, ELE FAZ A CONFIGURAÇÃO ##
                        ##############################################################
                        if selected_services_str != None:
                            selected_services_list = selected_services_str.split(', ')
                        
                            for service in selected_services_list:
                                cfg_service = os.popen(f"firewall-cmd --add-service={service} --permanent --zone={seleciona_zona}").read()
                                print(f'Permissão do serviço {service}: {cfg_service}')
                        
                        ############################################################
                        ## SE A PORTA ESTIVER SELECIONADA, ELE FAZ A CONFIGURAÇÃO ##
                        ############################################################
                        if selected_ports_str != None:
                            selected_ports_str = selected_ports_str.split(',')
                           
                            for port in selected_ports_str:
                                
                                if port != 0 or port != '':
                                    tcp_port = os.popen(f"firewall-cmd --add-port={port}/tcp --permanent --zone={seleciona_zona}").read()
                                    print(f'Porta {port}/tcp liberada: {tcp_port}')
                                    udp_port = os.popen(f"firewall-cmd --add-port={port}/udp --permanent --zone={seleciona_zona}").read()
                                    print(f'Porta {port}/udp liberada: {udp_port}')
                        
                        ##########################################################################
                        ## SE O BLOQUEIO DE SERVIÇO ESTIVER SELECIONADO, ELE FAZ A CONFIGURAÇÃO ##
                        ##########################################################################
                        if block_selected_services_str != None:
                            block_selected_services_list = block_selected_services_str.split(', ')
                            
                            for block_service in block_selected_services_list:
                                block_cfg_service = os.popen(f"firewall-cmd --remove-service={block_service} --permanent --zone={seleciona_zona}").read()
                                print(f'Bloqueio do serviço {block_service}: {block_cfg_service}')
                       
                        ##########################################################################
                        ## SE O BLOQUEIO DE SERVIÇO ESTIVER SELECIONADO, ELE FAZ A CONFIGURAÇÃO ##
                        ##########################################################################
                        '''
                        if block_selected_ports_str != None:
                            block_selected_ports_str = block_selected_ports_str.split(',')
                           
                            for block_port in block_selected_ports_str:
                                
                                if block_port != 0 or block_port != '':
                                    block_tcp_port = os.popen(f"firewall-cmd --remove-port={block_port}/tcp --permanent --zone={seleciona_zona}").read()
                                    print(f'Porta {block_port}/tcp bloqueada: {block_tcp_port}')
                                    block_udp_port = os.popen(f"firewall-cmd --remove-port={block_port}/udp --permanent --zone={seleciona_zona}").read()
                                    print(f'Porta {block_port}/udp bloqueada: {block_udp_port}')
                        '''
                        #########################################
                        ## ABRE O MENU DE CONFIGURAÇÕES EXTRAS ##
                        #########################################
                        try:
                            while True:
                                print("Configuração manual para a zona:")
                                print('[1] Defina o Target')
                                print("[2] Bloquear ICMP")
                                print("[3] Configurar forward")
                                print("[4] Configurar masquerade")
                                print("[0] Concluir")
                                choice = input("Escolha uma opção: ")
                                
                                ############################################
                                ## ABRE O MENU DE CONFIGURÇÃO DE "TARGET" ##
                                ############################################
                                if choice == "1":
                                    print('[1] Default')
                                    print("[2] ACCEPT")
                                    print("[3] REJECT")
                                    print("[4] DROP")
                                    print("[0] Concluir")
                                    target = int(input('Escolha a opção do Target: '))
                                    
                                    if target == 1:
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --set-target=default")
                                   
                                    if target == 2:
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --set-target=ACCEPT")
                                  
                                    if target == 3:
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --set-target=REJECT")  
                                 
                                    if target == 4:
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --set-target=DROP")
                                  
                                    if target == 0:
                                        pass
                                  
                                    else:
                                        print('Digite uma opção válida')
                              
                                if choice == "2":
                                    icmp_options = {
                                        "Echo-Request": "echo-request",
                                        "Echo-Reply": "echo-reply",
                                        "Destination Unreachable": "destination-unreachable",
                                        "Source Quench": "source-quench",
                                        "Redirect": "redirect",
                                        "Time Exceeded": "time-exceeded",
                                        "Parameter Problem": "parameter-problem",
                                        "Timestamp Request/Reply": "timestamp-request",
                                        "Address Mask Request/Reply": "address-mask-request",
                                        "Router Solicitation/Advertisement": "router-solicitation",
                                        "Traceroute": "traceroute"
                                    }
                                    print("\nOpções de bloqueio ICMP:")
                                    
                                    for num, option in enumerate(icmp_options.keys(), start=1):
                                        print(f"{num}. {option}")
                                   
                                    try:
                                        option_num = int(input("Digite o número correspondente à opção de ICMP a ser bloqueada: "))
                                      
                                        if 1 <= option_num <= len(icmp_options):
                                            selected_icmp = list(icmp_options.keys())[option_num - 1]
                                            icmp_type = icmp_options[selected_icmp]
                                            os.system(f"firewall-cmd --zone={seleciona_zona} --add-icmp-block={icmp_type}")
                                            os.system("firewall-cmd --reload")
                                            print(f"Comando executado: firewall-cmd --zone={seleciona_zona} --add-icmp-block={icmp_type}")
                                            print(f"ICMP tipo '{selected_icmp}' bloqueado.")
                                    
                                        else:
                                            print("Número de opção inválido.")
                                    except ValueError:
                                        print("Entrada inválida. O número da opção deve ser um número inteiro.")
                               
                                elif choice == "3":
                                    forward_value = input("Deseja habilitar o Forward? (S/N) ")
                                  
                                    if forward_value.lower() =='s':
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --add-forward")
                                        print(f"Forward configurado para {forward_value}.")
                                  
                                    elif forward_value.lower() =='n':
                                        os.system(f"firewall-cmd --zone={seleciona_zona} --remove-forward")
                                        print(f"Forward configurado para {forward_value}.")
                                    os.system("firewall-cmd --reload")

                                elif choice == "4":
                                    masquerade_value = input("Deseja habilitar o Masquerade? (S/N) ")
                                    os.system(f"firewall-cmd --zone={seleciona_zona} --add-option=masquerade --value={masquerade_value}")
                                    os.system("firewall-cmd --reload")
                                    print(f"Comando executado: firewall-cmd --zone={seleciona_zona} --add-option=masquerade --value={masquerade_value}")
                                    print(f"Masquerade configurado para {masquerade_value}.")

                                elif choice == "0":
                                    break

                                else:
                                    print("Escolha inválida. Tente novamente.")

                        except KeyboardInterrupt:
                            print("\nPrograma encerrado.")
                            os.system('clear')
                        
                        os.system("firewall-cmd --reload")

                    else:
                        print("Zona ou serviço não selecionado.")

                except UnboundLocalError:
                    print("Zona ou serviço não selecionado.")

            elif opcao == "0":
                print("Até a próxima! (ツ)")
                break

            else:
                print("Opção inválida. Tente novamente.")
            os.system('clear')

    except KeyboardInterrupt:
        print("\nPrograma encerrado.")


configure_firewall()

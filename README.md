Esta é uma ferramenta de linha de comando para configurar o firewall em sistemas Linux que usam o serviço firewalld (firewall-cmd). A ferramenta é projetada para fornecer uma interface simplificada , útil para administradores de sistemas que desejam configurar rapidamente o firewall em seus servidores Linux, garantindo a segurança da rede e dos serviços executados neles. A ferramenta oferece suporte para sistemas Linux com firewalld, como Ubuntu, CentOS e RHEL.


Funcionalidades:


Verifica se o firewalld está instalado e o instala caso não esteja.

Permite configurar interfaces e zonas.

Libera serviços e portas específicas.

Bloqueia serviços e portas específicas.

Permite bloquear IPs individualmente ou por máscara.

Mostra a lista de todas as zonas.

Mostra a configuração da zona selecionada.

Lista os IPs bloqueados.

Aplica as configurações.

Requisitos:


Sistema operacional Linux.

Firewalld instalado.

Como usar:


Clone este repositório:

git clone https://github.com/seu-usuario/gerenciador-firewall.git

Acesse o diretório do script:

cd gerenciador-firewall

Execute o script com permissões de root:

sudo ./gerenciador-firewall.sh

Siga as instruções na tela para gerenciar o firewalld.

Observações:


Este script é apenas para fins educacionais e não deve ser usado em ambientes de produção sem antes ser testado e validado.

É recomendável fazer backup da sua configuração do firewalld antes de usar este script.

O script está em constante desenvolvimento e novas funcionalidades podem ser adicionadas no futuro.

Contribuições:


Sinta-se à vontade para contribuir para este projeto.

Para contribuir, faça um fork do repositório e envie um pull request com suas alterações.

Agradecimentos:


Agradeço a todos que contribuíram para este projeto.

Contato:


Se você tiver alguma dúvida ou sugestão, entre em contato comigo através do GitHub.

Licença:


Este script é licenciado sob a licença MIT.

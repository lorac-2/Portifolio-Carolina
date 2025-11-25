Monitor e Solucionador de Vulnerabilidades de Rede
Python Scapy

💻 Sobre o Projeto
Este projeto é uma ferramenta de monitoramento e remediação de vulnerabilidades de rede desenvolvida em Python. O objetivo é ajudar administradores de sistemas e entusiastas de segurança a auditar o tráfego de rede e a aplicar medidas de segurança de forma proativa.

O programa combina a análise de pacotes de dados em tempo real com a capacidade de interagir com o sistema operacional para resolver problemas de segurança. Ele identifica tráfego suspeito, como conexões a portas incomuns ou de IPs não confiáveis, e oferece a opção de bloquear essas conexões diretamente no firewall do sistema.

Por Que Este Projeto É Útil?
Em ambientes empresariais, o tráfego de rede pode ser vasto e difícil de monitorar manualmente. Uma única conexão maliciosa pode ser a porta de entrada para um ataque de ransomware, roubo de dados ou interrupção de serviço. Este programa é útil porque:

Automação: Ele automatiza o processo de detecção de anomalias, liberando a equipe de segurança para se concentrar em ameaças mais complexas.
Proatividade: Em vez de apenas registrar um alerta, ele oferece uma solução imediata, como o bloqueio de um IP ou porta, minimizando o tempo de exposição a ameaças.
Visibilidade: Fornece um relatório detalhado que pode ser usado para auditorias de segurança, análise forense e para entender o comportamento normal da rede.
⚙️ Funcionalidades
Análise de Pacotes: Captura e inspeciona pacotes de rede em busca de atividade maliciosa.
Detecção de Anomalias: Sinaliza automaticamente tráfego suspeito com base em portas não autorizadas e IPs não confiáveis.
Remediação de Vulnerabilidades: Permite que o usuário bloqueie IPs maliciosos diretamente no firewall do sistema.
Geração de Relatórios: Cria um relatório completo, detalhando todas as ameaças identificadas e as ações tomadas.
Configurável: As configurações de portas e IPs confiáveis podem ser facilmente ajustadas via arquivo config.json.
🛠️ Como Utilizar
1. Pré-requisitos
Python 3.x
Sistemas Operacionais: O programa foi testado em sistemas Linux (Ubuntu) e pode ser adaptado para Windows e macOS. A remediação de vulnerabilidades via firewall depende do sistema. No Linux, ele utiliza o comando iptables. No Windows, será necessário usar comandos equivalentes (ex: netsh advfirewall).
Permissões: Para capturar pacotes e manipular o firewall, você precisará executar o script com permissões de administrador.
2. Instalação e Configuração
Clone o repositório:
git clone [https://github.com/lorac-2/meu-portifolio.git](https://github.com/lorac-2/meu-portifolio.git)
cd meu-portifolio
cd monitor-de-rede-python
Instale as dependências:
pip install -r requirements.txt
Ajuste as configurações: Abra o arquivo config.json e defina as portas a serem monitoradas e os IPs que você considera seguros.
Execute o programa: Execute o script com privilégios de administrador.
# No Linux/macOS
sudo python3 monitor_rede.py 

# No Windows (Executar o CMD como Administrador)
python monitor_rede.py
3. Modo de Uso
Quando uma atividade suspeita for detectada, o programa imprimirá um alerta. Você terá a opção de bloquear o IP de origem.

ALERTA: Conexão de IP não confiável | Origem: 192.168.1.5 | Porta: 22
Deseja bloquear este IP no firewall? (s/n):
Digite s para bloquear o IP. O programa executará o comando de firewall apropriado.

Digite n para ignorar a ação.

O programa continuará monitorando até que você o interrompa com Ctrl + C, momento em que o relatório final será gerado.

🤝 Contribuição e Feedback
Este projeto é uma demonstração de conceito, e sua segurança pode ser aprimorada de várias maneiras. Se você clonar este repositório, fizer melhorias no código ou encontrar bugs, por favor, me dê um feedback! Seu contributo é valioso para o aprimoramento contínuo deste projeto.

Feito com ❤️ por lorac-2

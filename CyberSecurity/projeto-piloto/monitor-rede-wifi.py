
import sys
import datetime
import json
import os
from scapy.all import sniff, IP, TCP, UDP

# --- Carregando Configurações do Arquivo ---
def carregar_configuracoes():
    """Carrega as configurações do arquivo config.json."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'config.json' não encontrado. Crie o arquivo e configure o programa.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Erro: O arquivo 'config.json' está mal formatado. Verifique a sintaxe JSON.")
        sys.exit(1)

config = carregar_configuracoes()

# --- Variáveis Globais de Monitoramento ---
pacotes_analisados = 0
trafego_total_bytes = 0
ips_com_alerta = set()
pacotes_suspeitos = []
ips_bloqueados = set()

# --- Função de Remediação de Vulnerabilidade ---
def bloquear_ip(ip):
    """
    Bloqueia um IP suspeito usando o firewall do sistema.
    A implementação padrão usa iptables para Linux.
    """
    try:
        if sys.platform.startswith('linux'):
            os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
            print(f"IP {ip} bloqueado com sucesso no firewall (iptables).")
            ips_bloqueados.add(ip)
        else:
            print("Remediação de firewall não implementada para este sistema operacional.")
    except Exception as e:
        print(f"Erro ao tentar bloquear o IP {ip}: {e}")

# --- Função de Análise de Pacote ---
def analisar_pacote(pacote):
    """
    Função principal que analisa cada pacote de rede capturado.
    Verifica se o pacote é IP, extrai informações e detecta ameaças.
    """
    global pacotes_analisados, trafego_total_bytes

    pacotes_analisados += 1
    
    # --- Verificando o Protocolo IP ---
    if IP in pacote:
        ip_origem = pacote[IP].src
        ip_destino = pacote[IP].dst
        trafego_total_bytes += len(pacote)

        # --- Verificando Protocolos de Transporte ---
        protocolo = "Outro"
        porta_destino = None

        if TCP in pacote:
            protocolo = "TCP"
            porta_destino = pacote[TCP].dport
        elif UDP in pacote:
            protocolo = "UDP"
            porta_destino = pacote[UDP].dport
        
        # --- Verificação de Ameaças e Alertas ---
        if porta_destino:
            alerta_detectado = False
            alerta_tipo = ""

            # Alerta 1: Porta de destino não monitorada
            if porta_destino not in config['portas_monitoradas']:
                alerta_tipo = "Porta Não Monitorada"
                alerta_detectado = True
            
            # Alerta 2: Conexão de IP não confiável
            elif ip_origem not in config['ips_confiados']:
                if porta_destino in config['portas_monitoradas']:
                    alerta_tipo = "IP Não Confiável"
                    alerta_detectado = True
            
            if alerta_detectado:
                print(f"ALERTA: {alerta_tipo} | Origem: {ip_origem} -> Destino: {ip_destino} | Porta: {porta_destino}")
                ips_com_alerta.add(ip_origem)
                pacotes_suspeitos.append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tipo": alerta_tipo,
                    "origem": ip_origem,
                    "destino": ip_destino,
                    "porta": porta_destino,
                    "protocolo": protocolo
                })

                if ip_origem not in ips_bloqueados:
                    resposta = input(f"Deseja bloquear o IP {ip_origem} no firewall? (s/n): ").lower()
                    if resposta == 's':
                        bloquear_ip(ip_origem)
                    elif resposta == 'n':
                        print(f"IP {ip_origem} não bloqueado.")


# --- Geração de Relatórios e Resumo ---
def gerar_relatorio():
    """Gera um relatório final com base nos dados coletados."""
    nome_arquivo = config.get('relatorio_output', 'relatorio_monitoramento.txt')

    with open(nome_arquivo, "w") as f:
        f.write("--- Relatório de Monitoramento de Rede ---\n")
        f.write(f"Data e Hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("--- Resumo Geral ---\n")
        f.write(f"Total de pacotes analisados: {pacotes_analisados}\n")
        f.write(f"Tráfego total (aproximado): {trafego_total_bytes / 1024 / 1024:.2f} MB\n\n")

        f.write("--- IPs Bloqueados ---\n")
        if ips_bloqueados:
            for ip in ips_bloqueados:
                f.write(f"  - {ip}\n")
        else:
            f.write("Nenhum IP foi bloqueado durante a sessão.\n")
        f.write("\n")

        f.write("--- Atividade Suspeita Detectada ---\n")
        if pacotes_suspeitos:
            f.write(f"Total de alertas: {len(pacotes_suspeitos)}\n")
            f.write("IPs com alertas:\n")
            for ip in ips_com_alerta:
                f.write(f"  - {ip}\n")
            f.write("\nDetalhes dos Alertas:\n")
            for p in pacotes_suspeitos:
                f.write(f"  - [{p['timestamp']}] Tipo: {p['tipo']} | Origem: {p['origem']} -> Destino: {p['destino']} | Porta: {p['porta']} | Protocolo: {p['protocolo']}\n")
        else:
            f.write("Nenhuma atividade suspeita detectada.\n")
    
    print(f"\nRelatório salvo em: {nome_arquivo}")

# --- Execução Principal ---
if __name__ == "__main__":
    print("Iniciando o monitoramento de rede (pressione Ctrl+C para parar)...")
    print("Aguardando pacotes...")
    
    try:
        sniff(prn=analisar_pacote, count=0)
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Verifique se o script foi executado com permissões de administrador.")
    
    gerar_relatorio()

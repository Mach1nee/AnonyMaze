#!/bin/bash

# Arte ASCII - adicione sua arte abaixo
ASCII_ART="
# Aqui vai sua arte ASCII
# Exemplo:
#   _.----._     _.---.
#         .-'        `-.-'      `.
#       .'                 .:''':.`.
#     .'        .:'''':. .' .----.  `.
# .-./        .' .----.    /  .-. \   `.
#/.-.           /  .-. \   \ ' O ' |    \
#||        `.   | ' O '/    \ `-' /     |
#|| (        \   \ `-'/      `-.__     / `.
# \`-'        )   .-'  --         )        `.
#  `-'     _.'   (            _.-'    _/\    \
#     `.       /\_ `-.____..-'     .-' _/    /
#       `.     \_ `-._         _.-'_.-'   .'
#         `--.._ `-._ `-.__..-'_.-'     .'
#       .-'     `-._ `--.__..-'  _.----'`.
#      /            `---.......-' _     \ \
#     /                          ( `-._.-` )
#    /  /     _                  .-    _.-'
#   (  `-._.-' )                (_   .'    \
#    `-._      -.               (_.-'       |
#        `.     _)                   __..---'
#       |  `-._) ''...__ .-. __...'''__..---'
#        \      '''...__((=))__...'''      /
#         |              `-'             .'
#         \                             /
#          |                           |
#          \     \    \      /    /   /
#           `. \               /     /
#               `--.._   ` '  _.--'
#                      [====]
#                       )  (
#                    .-'    '-.
#                   |          |
#                   | .------. |
#                   | |      | |
#                   | '------' |
#                   |          | 
#                   '----------'
"

# Exibe a arte ASCII
echo "$ASCII_ART"

# Intervalo padrão em segundos (3 minutos)
INTERVALO=180 # 180 segundos = 3 minutos

# Para mudar o intervalo, altere o valor da variável INTERVALO
# INTERVALO=120 # 120 segundos = 2 minutos
# INTERVALO=240 # 240 segundos = 4 minutos

# Instala o Tor
echo "Instalando o Tor..."
sudo apt update
sudo apt install -y tor

# Habilita o Tor para iniciar automaticamente
echo "Habilitando o Tor para iniciar automaticamente..."
sudo systemctl enable tor

# Configura o Tor
echo "Configurando o Tor..."
sudo bash -c 'echo "SocksPort 9050" >> /etc/tor/torrc'

# Configura iptables
USERNAME=$(whoami)
echo "Configurando regras do iptables..."
sudo bash -c "cat <<EOL > /etc/iptables/iptables.rules
*nat
:OUTPUT ACCEPT
-A OUTPUT -m owner --uid-owner $USERNAME -p tcp -j REDIRECT --to-port 9050
COMMIT
EOL"

# Cria script para restaurar regras do iptables na inicialização
echo "Criando script de restauração do iptables..."
sudo bash -c 'cat <<EOL > /etc/network/if-up.d/iptables
#!/bin/sh
iptables-restore < /etc/iptables/iptables.rules
EOL'
sudo chmod +x /etc/network/if-up.d/iptables

# Reinicia o Tor
echo "Reiniciando o Tor..."
sudo systemctl restart tor

# Loop para mudar o IP a cada intervalo
echo "Mudando o IP a cada $INTERVALO segundos (3 minutos por padrão)."
while true; do
    echo "Mudando IP..."
    curl --socks5-hostname localhost:9050 https://check.torproject.org > /dev/null 2>&1
    sleep $INTERVALO
done

echo "Configuração concluída. O Tor está configurado para iniciar automaticamente e as regras do iptables estão aplicadas."

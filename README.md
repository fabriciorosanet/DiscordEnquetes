# DiscordEnquetes

Este projeto é um bot para Discord que permite a criação de enquetes interativas. Os usuários podem votar em opções apresentadas, e as respostas são armazenadas em um arquivo CSV para análise posterior.

## Funcionalidades

- Envio automático de enquetes em canais específicos.
- Respostas dos usuários são registradas com data e hora.
- Opção de salvar as respostas em um arquivo CSV.
- Interface amigável com botões para interação.

## Tecnologias Utilizadas

- **Discord.py**: Biblioteca para interação com a API do Discord.
- **Pandas**: Para manipulação de dados e geração de arquivos CSV.
- **Python-dotenv**: Para carregar variáveis de ambiente a partir de um arquivo `.env`.

## Como Usar

1. Clone o repositório:
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
Instale as dependências:
pip install -r requirements.txt
DISCORD_TOKEN=seu_token_aqui

Execute o bot:
python bot.py

Comando para ser usando no Discord !salvar_respostas no canal para salvar as respostas em um arquivo CSV.

Contribuição
Sinta-se à vontade para enviar pull requests ou abrir issues para melhorias e sugestões.
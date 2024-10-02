import discord
from discord.ext import commands
import pandas as pd
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Obtém a token do bot a partir da variável de ambiente

intents = discord.Intents.all()  # Habilita todas as permissões que o bot pode ter
bot = commands.Bot(command_prefix='!', intents=intents)  # Cria uma instância do bot

responses_data = []  # Lista que armazena as respostas das enquetes
saopaulo_tz = timezone('America/Sao_Paulo')  # Define o fuso horário de São Paulo

# Estrutura para as enquetes e botões
class PollButton(discord.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Registra a resposta do usuário quando o botão for clicado
        responses_data.append({
            "User": interaction.user.name,
            "Response": self.label,
            "Poll Datetime": datetime.now().astimezone(saopaulo_tz)
        })
        await interaction.response.send_message(f'Você votou: {self.label}', ephemeral=True)

class PollView(discord.ui.View):
    def __init__(self, options, timeout=None):
        super().__init__(timeout=timeout)
        for i, option in enumerate(options):
            self.add_item(PollButton(label=option, custom_id=f"poll_option_{i+1}"))

    async def on_timeout(self):
        # Quando a enquete expirar, desativa todos os botões
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)  # Atualiza a mensagem no Discord para refletir os botões desativados
        print("Enquete encerrada.")

# Evento quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print("Bot pronto para enviar enquetes!")
    
    # Envia uma enquete automática ao canal especificado com validade
    channel_id = 1113194119825735750  # Substitua pelo ID do canal de destino
    channel = bot.get_channel(channel_id)
    
    if channel:
        question = " Como você avalia o seu perfil no LinkedIn?"
        options = [
            "Excelente – Perfil completo e atrativo",
            "Bom – Perfil sólido, espaço para melhorias",
            "Regular – Precisa de algumas atualizações",
            "Precisa de Melhorias – Várias melhorias necessárias",
            "Não Tenho LinkedIn"]

        # Define o tempo de validade (em segundos) - neste caso, 60 segundos (1 minuto)
        poll_duration = 1000
        view = PollView(options, timeout=poll_duration)
        
        # Envia a enquete para o canal
        view.message = await channel.send(f"**{question}**", view=view)
        
        # Inicia um temporizador para encerrar a enquete após o tempo definido
        await asyncio.sleep(poll_duration)
        
        # Após o tempo expirar, desativa os botões (feito automaticamente pelo método `on_timeout`)
        print(f"Enquete de {poll_duration} segundos encerrada.")
    else:
        print("Canal não encontrado. Verifique o ID.")

# Comando para salvar as respostas no CSV
@bot.command(name="salvar_respostas")
async def save_responses(ctx):
    if responses_data:
        df = pd.DataFrame(responses_data)
        df.sort_values(by="Poll Datetime", ascending=False, inplace=True)
        df.to_csv('respostas_enquete.csv', sep='§', encoding='utf-8', index=False)
        await ctx.send("Respostas salvas no arquivo 'respostas_enquete.csv'.")
    else:
        await ctx.send("Nenhuma resposta registrada ainda.")

bot.run(DISCORD_TOKEN)

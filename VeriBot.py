import discord
from discord.ext import commands
from discord.ui import Button, View
import os

# ===== CONFIGURAÇÕES (edite com seus dados) =====
TOKEN = os.getenv("TOKEN")
ROLE_ID = 1387838255717683371  # ID do cargo a ser atribuído
GUILD_ID = 400756362851647489  # ID do servidor
CHANNEL_ID = 1387841854594351205 # ID do canal onde o bot envia a mensagem

# ===== INTENTS E INSTÂNCIA DO BOT =====
intents = discord.Intents.default()
intents.members = True  # Necessário para gerenciar cargos
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== VIEW COM BOTÃO DE VERIFICAÇÃO =====
class VerificacaoView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Mantém o botão ativo permanentemente

    @discord.ui.button(label="✅ Verificar", style=discord.ButtonStyle.success, custom_id="verificar_botao")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)
        if role in interaction.user.roles:
            await interaction.response.send_message("Você já está verificado!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Você foi verificado com sucesso!", ephemeral=True)

# ===== EVENTO ON_READY (ENVIA A MENSAGEM UMA VEZ) =====
@bot.event
async def on_ready():
    print(f"✅ VeriBot online como {bot.user}.")

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    
    # Evita enviar múltiplas vezes se já estiver no canal
    if channel:
        view = VerificacaoView()
        await channel.send("👋 Bem-vindo! Clique no botão abaixo para se verificar e receber acesso ao servidor:", view=view)

# ===== INICIAR O BOT =====
bot.run(TOKEN)

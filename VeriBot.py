import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerificacaoView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verificar", style=discord.ButtonStyle.success, custom_id="verificar_botao")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)
        if role in interaction.user.roles:
            await interaction.response.send_message("Você já está verificado!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Verificado com sucesso!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ VeriBot online como {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("👋 Clique abaixo para se verificar:", view=VerificacaoView())

# Manter vivo com webserver
keep_alive()

# Iniciar o bot
bot.run(TOKEN)

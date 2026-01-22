"""Comando para consultar saldo."""

import discord
from discord import app_commands
from discord.ext import commands
from bot.database.manager import DatabaseManager
from bot.utils.errors import BankingError


class SaldoCommand(commands.Cog):
    """Cog para o comando de saldo."""
    
    def __init__(self, bot: commands.Bot, db: DatabaseManager):
        self.bot = bot
        self.db = db
    
    @app_commands.command(name="saldo", description="Consulta seu saldo atual")
    async def saldo(self, interaction: discord.Interaction):
        """Comando para consultar o saldo do usuário."""
        try:
            user_id = str(interaction.user.id)
            balance = self.db.get_balance(user_id)
            
            embed = discord.Embed(
                title="💰 Saldo",
                description=f"**{interaction.user.display_name}**, seu saldo atual é:",
                color=discord.Color.green()
            )
            embed.add_field(
                name="💵 Moedas",
                value=f"**{balance:.2f}** moedas",
                inline=False
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            
            await interaction.response.send_message(embed=embed)
        
        except BankingError as e:
            await interaction.response.send_message(embed=e.to_embed(), ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erro Inesperado",
                description=f"Ocorreu um erro ao consultar seu saldo. Por favor, tente novamente.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

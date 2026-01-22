"""Comando para transferir moedas entre usuários."""

import discord
from discord import app_commands
from discord.ext import commands
from bot.database.manager import DatabaseManager
from bot.utils.errors import (
    BankingError,
    InsufficientBalanceError,
    InvalidAmountError,
    SelfTransferError,
    UserNotFoundError
)


class TransferirCommand(commands.Cog):
    """Cog para o comando de transferência."""
    
    def __init__(self, bot: commands.Bot, db: DatabaseManager):
        self.bot = bot
        self.db = db
    
    @app_commands.command(name="transferir", description="Transfere moedas para outro usuário")
    @app_commands.describe(
        usuario="O usuário que receberá as moedas",
        valor="A quantidade de moedas a transferir"
    )
    async def transferir(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        valor: str
    ):
        """Comando para transferir moedas entre usuários."""
        try:
            # Validações básicas
            from_user_id = str(interaction.user.id)
            to_user_id = str(usuario.id)
            
            # Impede transferência para si mesmo
            if from_user_id == to_user_id:
                raise SelfTransferError()
            
            # Valida e converte o valor
            try:
                amount = float(valor)
            except ValueError:
                raise InvalidAmountError("O valor deve ser um número válido.")
            
            # Valida se o valor é positivo
            if amount <= 0:
                raise InvalidAmountError("O valor deve ser maior que zero.")
            
            # Verifica saldo suficiente
            current_balance = self.db.get_balance(from_user_id)
            if current_balance < amount:
                raise InsufficientBalanceError(current_balance)
            
            # Realiza a transferência
            self.db.transfer(from_user_id, to_user_id, amount)
            
            # Cria embed de sucesso
            embed = discord.Embed(
                title="✅ Transferência Realizada",
                description=f"Transferência de **{amount:.2f}** moedas realizada com sucesso!",
                color=discord.Color.green()
            )
            embed.add_field(
                name="👤 De",
                value=interaction.user.mention,
                inline=True
            )
            embed.add_field(
                name="👤 Para",
                value=usuario.mention,
                inline=True
            )
            embed.add_field(
                name="💰 Novo Saldo",
                value=f"**{self.db.get_balance(from_user_id):.2f}** moedas",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed)
        
        except BankingError as e:
            await interaction.response.send_message(embed=e.to_embed(), ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erro Inesperado",
                description=f"Ocorreu um erro ao processar a transferência. Por favor, tente novamente.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

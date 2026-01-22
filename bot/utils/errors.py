"""Sistema de tratamento de erros customizados."""

import discord
from typing import Optional


class BankingError(Exception):
    """Classe base para erros do sistema bancário."""
    
    def __init__(self, message: str, title: str = "❌ Erro"):
        self.message = message
        self.title = title
        super().__init__(self.message)
    
    def to_embed(self) -> discord.Embed:
        """Converte o erro em um Embed do Discord."""
        embed = discord.Embed(
            title=self.title,
            description=self.message,
            color=discord.Color.red()
        )
        return embed


class InsufficientBalanceError(BankingError):
    """Erro quando o saldo é insuficiente."""
    
    def __init__(self, current_balance: float):
        super().__init__(
            f"Saldo insuficiente! Você possui **{current_balance:.2f}** moedas.",
            "💰 Saldo Insuficiente"
        )


class InvalidAmountError(BankingError):
    """Erro quando o valor é inválido."""
    
    def __init__(self, reason: str = "O valor deve ser um número positivo maior que zero."):
        super().__init__(
            reason,
            "❌ Valor Inválido"
        )


class SelfTransferError(BankingError):
    """Erro quando tenta transferir para si mesmo."""
    
    def __init__(self):
        super().__init__(
            "Você não pode transferir moedas para si mesmo!",
            "🚫 Transferência Inválida"
        )


class UserNotFoundError(BankingError):
    """Erro quando o usuário não é encontrado."""
    
    def __init__(self):
        super().__init__(
            "Usuário não encontrado. Certifique-se de mencionar o usuário corretamente.",
            "👤 Usuário Não Encontrado"
        )


class DatabaseError(BankingError):
    """Erro relacionado ao banco de dados."""
    
    def __init__(self, message: str = "Erro ao acessar o banco de dados."):
        super().__init__(
            message,
            "💾 Erro no Banco de Dados"
        )

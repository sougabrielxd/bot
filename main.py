"""Bot Discord - Sistema Bancário Meia-Noite."""

import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.database.manager import DatabaseManager
from bot.commands.saldo import SaldoCommand
from bot.commands.transferir import TransferirCommand


# Carrega variáveis de ambiente
load_dotenv()

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX", "/")

if not DISCORD_TOKEN:
    print("ERRO: DISCORD_TOKEN não encontrado no arquivo .env")
    print("Por favor, crie um arquivo .env com: DISCORD_TOKEN=seu_token_aqui")
    sys.exit(1)


class BankingBot(commands.Bot):
    """Bot principal do sistema bancário."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=DISCORD_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.db = DatabaseManager()
    
    async def setup_hook(self):
        """Configuração inicial do bot."""
        # Adiciona os cogs
        await self.add_cog(SaldoCommand(self, self.db))
        await self.add_cog(TransferirCommand(self, self.db))
        
        # Sincroniza comandos slash
        try:
            synced = await self.tree.sync()
            print(f"Sincronizados {len(synced)} comandos slash.")
        except Exception as e:
            print(f"Erro ao sincronizar comandos: {e}")
    
    async def on_ready(self):
        """Evento quando o bot está pronto."""
        print(f"{self.user} está online!")
        print(f"Bot está em {len(self.guilds)} servidor(es)")
        print(f"Prefixo: {DISCORD_PREFIX}")


def main():
    """Função principal para iniciar o bot."""
    bot = BankingBot()
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()

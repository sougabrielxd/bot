"""Gerenciador de persistência de dados usando JSON."""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from bot.utils.errors import DatabaseError


class DatabaseManager:
    """Gerencia a persistência dos dados dos usuários."""
    
    def __init__(self, data_file: str = "data/users.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, float] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Carrega os dados do arquivo JSON."""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            else:
                self._data = {}
                self._save_data()
        except (json.JSONDecodeError, IOError) as e:
            raise DatabaseError(f"Erro ao carregar dados: {str(e)}")
    
    def _save_data(self) -> None:
        """Salva os dados no arquivo JSON."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise DatabaseError(f"Erro ao salvar dados: {str(e)}")
    
    def get_balance(self, user_id: str) -> float:
        """
        Retorna o saldo do usuário.
        Se o usuário não existir, cria com saldo inicial de 100 moedas.
        """
        if user_id not in self._data:
            self._data[user_id] = 100.0
            self._save_data()
        return self._data[user_id]
    
    def set_balance(self, user_id: str, balance: float) -> None:
        """Define o saldo do usuário."""
        self._data[user_id] = balance
        self._save_data()
    
    def add_balance(self, user_id: str, amount: float) -> None:
        """Adiciona moedas ao saldo do usuário."""
        current_balance = self.get_balance(user_id)
        self.set_balance(user_id, current_balance + amount)
    
    def subtract_balance(self, user_id: str, amount: float) -> None:
        """Subtrai moedas do saldo do usuário."""
        current_balance = self.get_balance(user_id)
        self.set_balance(user_id, current_balance - amount)
    
    def user_exists(self, user_id: str) -> bool:
        """Verifica se o usuário existe no banco de dados."""
        return user_id in self._data
    
    def transfer(self, from_user_id: str, to_user_id: str, amount: float) -> None:
        """
        Realiza uma transferência entre dois usuários.
        Não valida saldo ou valores - isso deve ser feito antes de chamar este método.
        """
        self.subtract_balance(from_user_id, amount)
        self.add_balance(to_user_id, amount)

import random
from typing import List, Any

class VpnBalancing:
    """
    Classe para gerenciar o balanceamento de seleções de VPN.
    """
    
    def __init__(self, items: List[Any]) -> None:
        """
        Inicializa a instância com uma lista de itens e um contador.

        :param items: Lista de itens a serem balanceados.
        """
        self.items = items
        self.counter = [0] * len(items)

    def selecionar(self) -> Any:
        """
        Seleciona um item da lista com base no balanceamento.

        :return: O item selecionado.
        """
        min_count = min(self.counter)
        candidatos = [i for i, count in enumerate(self.counter) if count == min_count]
        selecionado = random.choice(candidatos)
        self.counter[selecionado] += 1
        return self.items[selecionado
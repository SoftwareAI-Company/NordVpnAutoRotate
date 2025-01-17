import random
class vpn_balancing:
    def __init__(self, items):
        self.items = items
        self.counter = [0] * len(items)

    def selecionar(self):
        min_count = min(self.counter)
        candidatos = [i for i, count in enumerate(self.counter) if count == min_count]
        selecionado = random.choice(candidatos)
        self.counter[selecionado] += 1
        return self.items[selecionado]
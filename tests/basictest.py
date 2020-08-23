from gameservice.util.poker import evaluate52
from gameservice.sequential.poker import PokerPlayer

print(evaluate52(["Ah", "Ad", "As", "Ac", "Ks", "Kc", "Jh"]))

player = PokerPlayer(0)

print(player.info(False))
print(player.info(True))

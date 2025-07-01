# game/skill_effects.py
import random
from game.status_effects import Radiacion, Mojado, Mareado, Veneno

# ───────────────────────── Helpers con daño variable ─────────────────────────
def deal_damage(min_dmg: int, max_dmg: int):
    def effect(attacker, defender):
        amount = random.randint(min_dmg, max_dmg)
        defender.take_damage(amount)
        return f"{defender.name} recibió {amount} puntos de daño."
    return effect


def steal_health(min_dmg: int, max_dmg: int):
    def effect(attacker, defender):
        amount = random.randint(min_dmg, max_dmg)
        defender.take_damage(amount)
        healed = attacker.heal(amount)
        return (f"{defender.name} sufrió {amount} de daño. "
                f"{attacker.name} recuperó {healed} puntos de vida.")
    return effect

# energía y curación se mantienen fijas
def steal_energy(amount: int):
    def effect(attacker, defender):
        stolen = min(defender.energy, amount)
        defender.energy -= stolen
        return f"{attacker.name} le robó {stolen} de energía a {defender.name}."
    return effect


def drain_energy(amount: int):
    def effect(attacker, defender):
        stolen = min(defender.energy, amount)
        defender.energy -= stolen
        attacker.energy = min(attacker.energy + stolen, attacker.max_energy)
        return f"{attacker.name} drenó {stolen} de energía de {defender.name}."
    return effect


def heal(amount: int):
    def effect(attacker, defender):
        healed = attacker.heal(amount)
        return f"{attacker.name} recuperó {healed} puntos de vida."
    return effect


def restore_energy(amount: int):
    def effect(attacker, defender):
        before = attacker.energy
        attacker.energy = min(attacker.energy + amount, attacker.max_energy)
        gained = attacker.energy - before
        return f"{attacker.name} recuperó {gained} de energía."
    return effect


def skip_turn():
    def effect(attacker, defender):
        defender.skip_turn_flag = True
        return f"{defender.name} perderá su próximo turno."
    return effect

# ───────────────────── Helpers con estados persistentes ──────────────────────
_STATUS_MAP = {
    Radiacion.__name__: Radiacion,
    Mojado.__name__:    Mojado,
    Mareado.__name__:   Mareado,
    Veneno.__name__:    Veneno
}


def deal_damage_with_status(min_dmg: int, max_dmg: int, status_cls):
    def effect(attacker, defender):
        amount = random.randint(min_dmg, max_dmg)
        defender.take_damage(amount)
        if not any(isinstance(s, status_cls) for s in defender.status_effects):
            defender.add_status(status_cls())
            return (f"{defender.name} recibió {amount} puntos de daño. "
                    f"¡Ahora está en estado {status_cls.__name__}!")
        return f"{defender.name} recibió {amount} puntos de daño."
    return effect


def deal_damage_with_status_both(min_dmg: int, max_dmg: int, status_cls):
    def effect(attacker, defender):
        amount = random.randint(min_dmg, max_dmg)
        defender.take_damage(amount)
        if not any(isinstance(s, status_cls) for s in defender.status_effects):
            defender.add_status(status_cls())
        if not any(isinstance(s, status_cls) for s in attacker.status_effects):
            attacker.add_status(status_cls())
        return (f"{defender.name} recibió {amount} puntos de daño. "
                f"¡Ambos brainrots están en estado {status_cls.__name__}!")
    return effect

# ──────────────────── Helpers para efectos NO persistentes ───────────────────
def weaken_next_attack(mult: float):
    def effect(attacker, defender):
        defender.next_attack_mult = mult
        pct = int(mult * 100)
        return (f"{defender.name} quedó debilitado. "
                f"Su próximo ataque causará apenas {pct}% del daño.")
    return effect


def raise_defense_nullify():
    def effect(attacker, defender):
        defender.nullify_next_attack = True
        return (f"{defender.name} quedó completamente bloqueado. "
                f"Su próximo ataque será anulado.")
    return effect


def extra_energy_cost(factor: float):
    def effect(attacker, defender):
        defender.next_energy_mult = factor
        extra = int((factor - 1) * 100)
        return (f"{defender.name} gastará {extra}% de energía "
                f"adicional en su próximo movimiento.")
    return effect


def self_damage(amount: int):
    def effect(attacker, defender):
        attacker.take_damage(amount)
        return f"{attacker.name} se dañó a sí mismo en {amount} PV."
    return effect


def reflect_damage_if_direct(min_dmg: int, max_dmg: int):
    def effect(attacker, defender):
        attacker.reflect_damage_range = (min_dmg, max_dmg)
        return (f"{attacker.name} se preparó para reflejar entre "
                f"{min_dmg} y {max_dmg} PV si recibe un ataque directo.")
    return effect
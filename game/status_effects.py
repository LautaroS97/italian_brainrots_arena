import random

# ──────────────────────────── BASE EFFECTS ────────────────────────────
class StatusEffect:
    def __init__(self, name, icon_path, cure_chance=0.5):
        self.name = name
        self.icon_path = icon_path
        self.cure_chance = cure_chance
        self.cured = False

    # hook - por defecto no altera nada
    def on_damage_calc(self, dmg):   return dmg
    def on_energy_calc(self, cost):  return cost

    # hooks para lógica por turno
    def apply_effect(self, target):  pass
    def tick_effect(self, target):   pass

    def try_cure(self):
        if random.random() < self.cure_chance:
            self.cured = True


# ─────────────────────────── EFECTOS PERSISTENTES ──────────────────────────
class Radiacion(StatusEffect):
    def __init__(self):
        super().__init__("Radiación", "assets/icons/radiacion.png", 0.5)

    def tick_effect(self, target):
        target.hp = max(0, target.hp - 5)


class Mojado(StatusEffect):
    def __init__(self):
        super().__init__("Mojado", "assets/icons/mojado.png", 0.5)

    def apply_effect(self, target):
        if not hasattr(target, "pp_multiplier"):
            target.pp_multiplier = 1.0
        target.pp_multiplier *= 1.05


class Mareado(StatusEffect):
    def __init__(self):
        super().__init__("Mareado", "assets/icons/mareado.png", 0.5)

    def apply_effect(self, target):
        if not hasattr(target, "damage_multiplier"):
            target.damage_multiplier = 1.0
        target.damage_multiplier *= 0.4


class Veneno(StatusEffect):
    def __init__(self):
        super().__init__("Veneno", "assets/icons/veneno.png", 0.5)

    def tick_effect(self, target):
        target.hp = max(0, target.hp - 10)
        target.energy = max(0, target.energy - 5)
        if not hasattr(target, "damage_multiplier"):
            target.damage_multiplier = 1.0
        if not hasattr(target, "pp_multiplier"):
            target.pp_multiplier = 1.0
        target.damage_multiplier *= 0.9
        target.pp_multiplier *= 1.1


# ──────────────────────── EFECTOS TEMPORALES (1 TURNO) ─────────────────────
class _TempStatus(StatusEffect):
    """Se autodescarta tras modificar el primer cálculo relevante."""
    def __init__(self, name, icon_path):
        super().__init__(name, icon_path, cure_chance=1.0)  # se cura sola
    def _auto_cure(self):
        self.cured = True


class Debilitado20(_TempStatus):
    def __init__(self):
        super().__init__("Debilitado 20%", "assets/icons/debilitado20.png")
    def on_damage_calc(self, dmg):
        self._auto_cure()
        return int(dmg * 0.8)


class Debilitado50(_TempStatus):
    def __init__(self):
        super().__init__("Debilitado 50%", "assets/icons/debilitado50.png")
    def on_damage_calc(self, dmg):
        self._auto_cure()
        return int(dmg * 0.5)


class Debilitado75(_TempStatus):
    def __init__(self):
        super().__init__("Debilitado 75%", "assets/icons/debilitado75.png")
    def on_damage_calc(self, dmg):
        self._auto_cure()
        return int(dmg * 0.25)


class EnergyUp25(_TempStatus):
    def __init__(self):
        super().__init__("PP +25%", "assets/icons/energyup25.png")
    def on_energy_calc(self, cost):
        self._auto_cure()
        return int(cost * 1.25)


class NullifyNextAttack(_TempStatus):
    def __init__(self):
        super().__init__("Anulado", "assets/icons/nullify.png")
    def on_damage_calc(self, dmg):
        self._auto_cure()
        return 0
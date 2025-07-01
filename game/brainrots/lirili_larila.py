from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    weaken_next_attack,
    extra_energy_cost
)


def _arenas_movedizas_effect():
    wk = weaken_next_attack(0.5)       # 50 % menos daño
    ec = extra_energy_cost(1.25)       # +25 % de PP
    def effect(att, riv):
        return f"{wk(att, riv)} {ec(att, riv)}"
    return effect


def _volver_al_pasado_effect():
    def effect(att, riv):
        before = att.energy
        att.energy = att.max_energy
        gained = att.energy - before
        return f"{att.name} retrocedió en el tiempo y recuperó {gained} PP."
    return effect


def get_brainrot():
    base = "assets/animations/Lirili_Larila"

    return Brainrot(
        name="Lirili Larila",
        max_hp=100,
        max_energy=100,
        lore_text="Una criatura melódica que encanta con su canto y aturde con su ritmo.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={
            "file_root": f"{base}/idle",
            "fps": 5
        },
        skills=[
            # ───────── Ataque básico ─────────
            Skill(
                name="Patadón",
                description="Ataque físico básico que causa entre 5 y 10 PV de daño.",
                energy_cost=5,
                execute=deal_damage(5, 10),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/patadon",
                    "fps": 8,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),
            # ───────── Defensa ─────────
            Skill(
                name="Arenas Movedizas",
                description="Reduce 50 % el daño del próximo ataque rival y le aumenta su costo en 25 %.",
                energy_cost=20,
                execute=_arenas_movedizas_effect(),
                priority=True,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/arenas_movedizas",
                    "fps": 6,
                    "freeze": True,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Ataque fuerte ─────────
            Skill(
                name="Bomba de Espinas",
                description="Bomba cactus que explota causando entre 20 y 25 PV de daño.",
                energy_cost=15,
                execute=deal_damage(20, 25),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/bomba_de_espinas",
                    "fps": 7,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),
            # ───────── Poder especial ─────────
            Skill(
                name="Volver al Pasado",
                description="Recupera toda la energía perdida por el último ataque del rival.",
                energy_cost=30,
                execute=_volver_al_pasado_effect(),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/volver_al_pasado",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            )
        ]
    )
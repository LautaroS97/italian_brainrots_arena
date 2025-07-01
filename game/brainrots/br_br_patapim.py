from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    weaken_next_attack,
    raise_defense_nullify,
    drain_energy
)

# ───────── Helpers específicos ─────────
def _patapum_effect():
    dmg = deal_damage(15, 20)          # daño variable
    wk  = weaken_next_attack(0.8)      # 20 % menos daño rival
    def effect(att, riv):
        return f"{dmg(att, riv)} {wk(att, riv)}"
    return effect


def get_brainrot():
    base = "assets/animations/Br_Br_Patapim"

    return Brainrot(
        name="Br Br Patapim",
        max_hp=100,
        max_energy=100,
        lore_text="Destructor de ritmos y tamborines, trae caos con cada golpe.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={
            "file_root": f"{base}/idle",
            "fps": 6
        },
        skills=[
            # ───────── Ataque básico ─────────
            Skill(
                name="Patapimba",
                description="Ataque físico básico que causa entre 10 y 15 PV de daño.",
                energy_cost=15,
                execute=deal_damage(10, 15),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/patapimba",
                    "fps": 8,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),

            # ───────── Defensa ─────────
            Skill(
                name="Arbustote",
                description="Muralla de musgo: anula por completo el próximo ataque rival.",
                energy_cost=25,
                execute=raise_defense_nullify(),
                priority=True,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/arbustote",
                    "fps": 5,
                    "freeze": True,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),

            # ───────── Ataque fuerte ─────────
            Skill(
                name="Patapum",
                description="Ataque fuerte (15-20 PV) que reduce 20 % el daño del próximo ataque rival.",
                energy_cost=20,
                execute=_patapum_effect(),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/patapum",
                    "fps": 7,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),

            # ───────── Poder especial ─────────
            Skill(
                name="Drenaje Vital",
                description="Le roba 10 PP al rival y los añade al usuario.",
                energy_cost=0,
                execute=drain_energy(10),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/drenaje_vital",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            )
        ]
    )
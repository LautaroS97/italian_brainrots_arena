from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    deal_damage_with_status_both,
    weaken_next_attack,
    extra_energy_cost
)
from game.status_effects import Radiacion


def _ventarron_effect():
    wk = weaken_next_attack(0.5)   # 50 % menos daño
    ec = extra_energy_cost(1.25)   # +25 % de PP
    def effect(att, riv):
        return f"{wk(att, riv)} {ec(att, riv)}"
    return effect


def get_brainrot():
    base = "assets/animations/Bombardino_Crocodilo"

    return Brainrot(
        name="Bombardino Crocodilo",
        max_hp=100,
        max_energy=100,
        lore_text="Una bestia anfibia con un gusto musical explosivo.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={
            "file_root": f"{base}/idle",
            "fps": 5
        },
        skills=[
            # ───────── Ataque básico ─────────
            Skill(
                name="Masticada",
                description="Mordida básica que causa entre 5 y 15 PV de daño.",
                energy_cost=5,
                execute=deal_damage(5, 15),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/masticada",
                    "fps": 8,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),

            # ───────── Defensa ─────────
            Skill(
                name="Ventarrón",
                description="Pantalla de viento: reduce 50 % el daño entrante y hace que el rival gaste 25 % más de PP.",
                energy_cost=15,
                execute=_ventarron_effect(),
                priority=True,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/ventarron",
                    "fps": 6,
                    "freeze": True,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),

            # ───────── Ataque fuerte ─────────
            Skill(
                name="Bombazo",
                description="Misil guiado que causa entre 15 y 25 PV de daño.",
                energy_cost=10,
                execute=deal_damage(15, 25),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/bombazo",
                    "fps": 6,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),

            # ───────── Poder especial ─────────
            Skill(
                name="Crocomisil",
                description="Impacto devastador (40-50 PV) que deja a ambos en estado 'Radiación'.",
                energy_cost=25,
                execute=deal_damage_with_status_both(40, 50, Radiacion),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/crocomisil",
                    "fps": 7,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            )
        ]
    )
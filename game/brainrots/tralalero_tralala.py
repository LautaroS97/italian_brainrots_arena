from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    deal_damage_with_status,
    weaken_next_attack
)
from game.status_effects import Mojado


def get_brainrot():
    base = "assets/animations/Tralalero_Tralala"

    return Brainrot(
        name="Tralalero Tralala",
        max_hp=100,
        max_energy=100,
        lore_text="Híbrido entre cantante de ópera y surfista de cloacas.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={
            "file_root": f"{base}/idle",
            "fps": 5
        },
        skills=[
            # ───────── Ataque básico ─────────
            Skill(
                name="Altas Llantas",
                description="Ataque físico básico que causa entre 5 y 10 PV de daño.",
                energy_cost=5,
                execute=deal_damage(5, 10),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/altas_llantas",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Defensa ─────────
            Skill(
                name="Piel de Tiburón",
                description="Endurece la piel: el próximo ataque rival causará solo un 25 % de su daño.",
                energy_cost=20,
                execute=weaken_next_attack(0.25),
                priority=True,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/piel_de_tiburon",
                    "fps": 6,
                    "freeze": True,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Ataque fuerte ─────────
            Skill(
                name="Chupetón",
                description="Mordida de tiburón que inflige entre 10 y 20 PV de daño.",
                energy_cost=10,
                execute=deal_damage(10, 20),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/chupeton",
                    "fps": 7,
                    "freeze": False,
                    "movement": False,
                    "collision": True,
                    "sound": False
                }
            ),
            # ───────── Poder especial ─────────
            Skill(
                name="Manguerazo",
                description="Inflige 10-20 PV de daño y aplica el estado 'Mojado'.",
                energy_cost=25,
                execute=deal_damage_with_status(10, 20, Mojado),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/manguerazo",
                    "fps": 8,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            )
        ]
    )
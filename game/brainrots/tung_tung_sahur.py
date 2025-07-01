from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    deal_damage_with_status,
    raise_defense_nullify,
    reflect_damage_if_direct,
    self_damage
)
from game.status_effects import Veneno


def _palo_borracho_effect():
    nul = raise_defense_nullify()
    ref = reflect_damage_if_direct(2, 5)
    def effect(att, riv):
        return f"{nul(att, riv)} {ref(att, riv)}"
    return effect


def _cabezazo_effect():
    dmg = deal_damage(10, 20)
    auto = self_damage(2)
    def effect(att, riv):
        return f"{dmg(att, riv)} {auto(att, riv)}"
    return effect


def get_brainrot():
    base = "assets/animations/Tung_Tung_Sahur"

    return Brainrot(
        name="Tung Tung Sahur",
        max_hp=100,
        max_energy=100,
        lore_text="Forjado entre fábricas, humo y lucha de clases.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={
            "file_root": f"{base}/idle",
            "fps": 6
        },
        skills=[
            # ───────── Ataque básico ─────────
            Skill(
                name="Palazo",
                description="Ataque físico básico que causa entre 4 y 8 PV de daño.",
                energy_cost=3,
                execute=deal_damage(4, 8),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/palazo",
                    "fps": 5,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Defensa ─────────
            Skill(
                name="Palo Borracho",
                description="Bloquea por completo el ataque rival y refleja 2-5 PV si fue directo.",
                energy_cost=15,
                execute=_palo_borracho_effect(),
                priority=True,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/palo_borracho",
                    "fps": 7,
                    "freeze": True,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Ataque fuerte ─────────
            Skill(
                name="Cabezazo",
                description="Golpe potente (10-20 PV) que le resta 2 PV al usuario.",
                energy_cost=8,
                execute=_cabezazo_effect(),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/cabezazo",
                    "fps": 8,
                    "freeze": False,
                    "movement": True,
                    "collision": True,
                    "sound": False
                }
            ),
            # ───────── Poder especial ─────────
            Skill(
                name="Palo Santo",
                description="Inflige 5-10 PV de daño y aplica el estado 'Veneno'.",
                energy_cost=25,
                execute=deal_damage_with_status(5, 10, Veneno),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/palo_santo",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            )
        ]
    )
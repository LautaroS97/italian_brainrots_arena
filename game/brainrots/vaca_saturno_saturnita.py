from game.brainrot import Brainrot
from game.skill import Skill
from game.skill_effects import (
    deal_damage,
    self_damage,
    deal_damage_with_status
)
from game.status_effects import Mareado


def _anillo_proteccion_effect():
    def effect(att, riv):
        lost_hp   = att.max_hp   - att.hp
        lost_pp   = att.max_energy - att.energy
        heal_amt  = int(lost_hp * 0.5)
        pp_gain   = int(lost_pp * 0.5)
        att.heal(heal_amt)
        att.restore_energy(pp_gain)
        return (f"{att.name} recuperó {heal_amt} PV y {pp_gain} PP.")
    return effect


def _disco_acrecion_effect():
    dmg = deal_damage(25, 30)
    auto = self_damage(6)
    def effect(att, riv):
        return f"{dmg(att, riv)} {auto(att, riv)}"
    return effect


def get_brainrot():
    base = "assets/animations/Vaca_Saturno_Saturnita"

    return Brainrot(
        name="Vaca Saturno Saturnita",
        max_hp=100,
        max_energy=100,
        lore_text="Una entidad cósmica de cuatro estómagos y una misión intergaláctica.",
        portrait_img=f"{base}/portrait.png",
        idle_anim={"file_root": f"{base}/idle", "fps": 4},
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
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Defensa ─────────
            Skill(
                name="Anillo de Protección",
                description="Recupera 50 % de la vida y energía perdidas por el último ataque recibido.",
                energy_cost=10,
                execute=_anillo_proteccion_effect(),
                priority=False,          # se usa tras recibir el golpe
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/anillo_de_proteccion",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Ataque fuerte ─────────
            Skill(
                name="Disco de Acreción",
                description="Bumerán poderoso (25-30 PV) que quita 6 PV al usuario.",
                energy_cost=18,
                execute=_disco_acrecion_effect(),
                priority=False,
                is_direct_attack=True,
                render_behind_rival=True,
                animation={
                    "file_root": f"{base}/disco_de_acrecion",
                    "fps": 5,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            ),
            # ───────── Poder especial ─────────
            Skill(
                name="Polvo Estelar",
                description="Causa daño (6-18 PV) y aplica el estado 'Mareado'.",
                energy_cost=25,
                execute=deal_damage_with_status(6, 18, Mareado),
                priority=False,
                is_direct_attack=False,
                render_behind_rival=False,
                animation={
                    "file_root": f"{base}/polvo_estelar",
                    "fps": 6,
                    "freeze": False,
                    "movement": False,
                    "collision": False,
                    "sound": False
                }
            )
        ]
    )
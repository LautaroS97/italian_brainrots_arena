import random
import pygame
from typing import List
from game.sound_manager import SoundManager
from game.skill import Skill
from game.brainrot import Brainrot


class _MsgProxy:
    def __init__(self, sink: list[str]):
        self._sink = sink
    def show_message(self, text: str):
        if text:
            self._sink.append(text)


class BattleManager:
    def __init__(
        self,
        player1: Brainrot,
        player2: Brainrot,
        sound_manager: SoundManager | None = None,
    ):
        self.player1 = player1
        self.player2 = player2
        self.turn = 1
        self.status_messages: List[str] = [
            f"¡{self.get_active_player().name} comienza el combate!"
        ]
        self.game_over = False
        self.winner: str | None = None
        self.sound_manager = sound_manager
        self.pending_victory_type: str | None = None

    # ───────────────────────── utilidades ─────────────────────────
    def get_active_player(self) -> Brainrot:
        return self.player1 if self.turn == 1 else self.player2

    def get_enemy_player(self) -> Brainrot:
        return self.player2 if self.turn == 1 else self.player1

    # ───────────────────────── turno de acción ────────────────────
    def apply_action(self, skill: Skill):
        if self.game_over:
            self.status_messages = ["El combate ya ha terminado."]
            return

        attacker = self.get_active_player()
        defender = self.get_enemy_player()
        messages: List[str] = []

        # costo real de energía
        cost = skill.energy_cost
        for st in attacker.status_effects:
            cost = getattr(st, "on_energy_calc", lambda c: c)(cost)
        cost = int(cost * getattr(attacker, "next_energy_mult", 1.0))
        attacker.next_energy_mult = 1.0

        # efectos de estado
        proxy = _MsgProxy(messages)
        attacker.process_statuses(proxy)
        defender.process_statuses(proxy)
        if self._check_immediate_death(attacker, defender, messages):
            self.status_messages = messages
            return

        if attacker.skip_turn_flag:
            attacker.skip_turn_flag = False
            attacker.consume_energy(cost)
            messages.append(f"{attacker.name} perdió su turno (−{cost} PP).")
        else:
            if defender.nullify_next_attack:
                defender.nullify_next_attack = False
                attacker.consume_energy(cost)
                messages.append(
                    f"{attacker.name} usó {skill.name} (−{cost} PP)! "
                    f"¡Pero el ataque fue anulado!"
                )
            else:
                skill._override_cost = cost
                attacker.start_skill_animation(skill, defender, self.sound_manager)
                result_text = skill.execute(attacker, defender)
                delattr(skill, "_override_cost")
                messages.append(result_text)

                # reflejo de daño
                if skill.is_direct_attack and getattr(defender, "reflect_damage_range", None):
                    lo, hi = defender.reflect_damage_range
                    reflected = random.randint(lo, hi)
                    attacker.take_damage(reflected)
                    defender.reflect_damage_range = None
                    messages.append(f"¡{defender.name} reflejó {reflected} puntos de daño!")

        # victoria / turno
        self._check_post_action(attacker, defender, messages)
        if not self.game_over:
            self.turn = 2 if self.turn == 1 else 1
            messages.append(f"Turno de {self.get_active_player().name}.")

        self.status_messages = messages

    # ─────────────────── helpers de victoria ─────────────────────
    def _check_immediate_death(
        self, attacker: Brainrot, defender: Brainrot, msg_list: list[str]
    ) -> bool:
        if attacker.is_dead():
            self._set_winner(
                defender, "health", msg_list,
                f"{attacker.name} fue derrotado. {defender.name} gana el combate."
            )
            return True
        if defender.is_dead():
            self._set_winner(
                attacker, "health", msg_list,
                f"{defender.name} fue derrotado. {attacker.name} gana el combate."
            )
            return True
        return False

    def _check_post_action(
        self, attacker: Brainrot, defender: Brainrot, msg_list: list[str]
    ):
        if attacker.is_dead():
            self._set_winner(
                defender, "health", msg_list,
                f"{attacker.name} fue derrotado. {defender.name} gana el combate."
            )
        elif attacker.energy <= 0:
            self._set_winner(
                defender, "energy", msg_list,
                f"{attacker.name} se quedó sin energía. {defender.name} gana el combate."
            )
        elif defender.is_dead():
            self._set_winner(
                attacker, "health", msg_list,
                f"{defender.name} fue derrotado. {attacker.name} gana el combate."
            )
        elif defender.energy <= 0:
            self._set_winner(
                attacker, "energy", msg_list,
                f"{defender.name} se quedó sin energía. {attacker.name} gana el combate."
            )

    def _set_winner(
        self,
        winner_brainrot: Brainrot,
        victory_type: str,
        msg_list: List[str],
        final_msg: str,
    ):
        self.game_over = True
        self.winner = winner_brainrot.name
        self.pending_victory_type = victory_type
        msg_list.append(final_msg)

    # ─────────────── sonido de victoria ───────────────
    def play_victory_sound(self):
        if not self.game_over or not self.sound_manager:
            return
        winner = self.winner
        loser = self.player1.name if self.player1.name != winner else self.player2.name
        if self.pending_victory_type == "health":
            self.sound_manager.play_victory_health(loser, winner)
        elif self.pending_victory_type == "energy":
            self.sound_manager.play_victory_energy(loser, winner)
        self.pending_victory_type = None

    # ───────────────────────── getters ─────────────────────────
    def is_game_over(self) -> bool:
        return self.game_over

    def get_status_messages(self) -> List[str]:
        return self.status_messages

    def start_intro_sequence(self):
        if self.sound_manager:
            self.sound_manager.play_intro_sequence(
                self.player1.name, self.player2.name
            )
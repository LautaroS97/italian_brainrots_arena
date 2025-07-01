class Skill:

    def __init__(
        self,
        name: str,
        description: str,
        energy_cost: int,
        execute,                       # función (attacker, defender [, energy]) -> str
        animation: dict | None = None,
        priority: bool = False,
        is_direct_attack: bool = True,
        render_behind_rival: bool = False,
        extra_message=None            # str o callable(op1, op2) -> str
    ):
        self.name = name
        self.description = description
        self.energy_cost = energy_cost
        self.execute_effect = execute
        self.animation = animation or {}
        self.priority = priority
        self.is_direct_attack = is_direct_attack
        self.render_behind_rival = render_behind_rival
        self.extra_message = extra_message

    def execute(self, attacker, defender):
        attacker.consume_energy(self.energy_cost)

        try:
            result = self.execute_effect(attacker, defender, self.energy_cost)
        except TypeError:
            result = self.execute_effect(attacker, defender)

        msg = f"{attacker.name} usó {self.name} (−{self.energy_cost} PP)! {result}"

        if self.extra_message:
            extra = self.extra_message(attacker, defender) if callable(self.extra_message) else self.extra_message
            if extra:
                msg += f" {extra}"

        return msg
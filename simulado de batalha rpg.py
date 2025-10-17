from abc import ABC, abstractmethod
import random


class RPG(ABC):
    def __init__(self, name, rpg_class, health, strength, intelligence, dexterity):
        self.name = name
        self.rpg_class = rpg_class
        self.health = health
        self.max_health = health
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity

    # Método abstrato: todas as subclasses devem implementar
    @abstractmethod
    def stack(self):
        pass

    # Método abstrato de ataque (será sobrescrito nas subclasses)
    @abstractmethod
    def attack(self, target):
        pass

    def base_level(self):
        return (self.health + self.strength + self.intelligence + self.dexterity) // 10

    def level(self):
        return self.base_level()

    def defend(self):
        return self.dexterity + random.randint(0, 3)

    def __str__(self):
        return f"{self.name} ({self.rpg_class}) - Nível: {self.level()} - HP: {self.health}/{self.max_health}"



class Warrior(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, kills):
        super().__init__(name, "Guerreiro", health, strength, intelligence, dexterity)
        self.kills = kills

    # Sobrescrita do método level
    def level(self):
        return super().level() + self.kills // 2

    def stack(self):
        return f"Guerreiro {self.name} acumulou {self.kills} kills!"

    # Sobrescrita (override) de attack
    def attack(self, enemy):
        base_damage = self.strength + random.randint(0, 5)
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} atacou {enemy.name} com espada: Dano bruto = {base_damage}, Defesa = {defense}, Dano real = {damage}")
        return damage


class Archer(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, precision):
        super().__init__(name, "Arqueiro", health, strength, intelligence, dexterity)
        self.precision = precision

    def level(self):
        return super().level() + self.precision // 5

    def stack(self):
        return f"Arqueiro {self.name} tem precisão de {self.precision}!"

    def attack(self, enemy):
        base_damage = self.strength + self.precision // 2 + random.randint(0, 5)
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} disparou uma flecha em {enemy.name}: Dano bruto = {base_damage}, Defesa = {defense}, Dano real = {damage}")
        return damage


class Healer(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, assists):
        super().__init__(name, "Clérigo", health, strength, intelligence, dexterity)
        self.assists = assists

    def level(self):
        return super().level() + self.assists // 3

    def stack(self):
        return f"Clérigo {self.name} ajudou {self.assists} vezes!"

    # Sobrescreve o método attack para curar ou causar dano mágico leve
    def attack(self, enemy):
        # Healer também pode causar dano leve com magia
        base_damage = self.intelligence // 2 + random.randint(0, 3)
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} lançou um feitiço de luz em {enemy.name}: Dano real = {damage}")
        return damage

    def heal(self, ally):
        heal_amount = self.intelligence + random.randint(0, 5)
        ally.health = min(ally.max_health, ally.health + heal_amount)
        print(f"{self.name} curou {ally.name} em {heal_amount} HP!")
        return heal_amount


class Villain(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, evilness):
        super().__init__(name, "Vilão", health, strength, intelligence, dexterity)
        self.evilness = evilness

    def level(self):
        return super().level() + self.evilness // 2

    def stack(self):
        return f"Vilão {self.name} está causando caos com malícia {self.evilness}!"

    def attack(self, hero):
        base_damage = self.strength + self.evilness // 2 + random.randint(0, 5)
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} atacou {hero.name}: Dano bruto = {base_damage}, Defesa = {defense}, Dano real = {damage}")
        return damage


class Minion(Villain):
    # Sobrescrita de stack
    def stack(self):
        return f"Minion {self.name} apenas segue ordens com malícia {self.evilness}."

    # Sobrescrita de attack
    def attack(self, hero):
        base_damage = self.strength // 2 + random.randint(0, 4)
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} (Minion) atacou timidamente {hero.name}: Dano real = {damage}")
        return damage


class Boss(Villain):
    # Sobrescrita de attack
    def attack(self, hero):
        base_damage = self.strength + self.evilness + random.randint(5, 10)
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} (Boss) devastou {hero.name}: Dano bruto = {base_damage}, Defesa = {defense}, Dano real = {damage}")
        return damage

    def __str__(self):
        return f"{self.name} (Boss) - Malícia: {self.evilness} - HP: {self.health}/{self.max_health}"



warrior = Warrior("Naruto", 40, 10, 8, 11, kills=30)
archer = Archer("Hunte", 35, 12, 10, 16, precision=30)
healer = Healer("Killua", 30, 9, 17, 9, assists=30)
heroes = [warrior, archer, healer]

villain1 = Minion("Illumi", 30, 8, 6, 10, evilness=30)
villain2 = Boss("Boruto", 50, 14, 15, 12, evilness=30)
villain3 = Boss("Feitan", 50, 14, 15, 12, evilness=30)
villain4 = Boss("Goku", 50, 30, 50, 23, evilness=30)
villains = [villain1, villain2, villain3, villain4]



def battle(heroes, villains):
    turn = 1
    max_turns = 10

    while turn <= max_turns:
        print(f"\n--- Turno {turn} ---")

        # Turno dos heróis
        for hero in heroes:
            if hero.health <= 0:
                continue
            if isinstance(hero, Healer) and random.random() < 0.5:
                ally = random.choice([h for h in heroes if h.health > 0])
                hero.heal(ally)
            else:
                targets = [v for v in villains if v.health > 0]
                if targets:
                    target = random.choice(targets)
                    hero.attack(target)

        # Turno dos vilões
        for villain in villains:
            if villain.health <= 0:
                continue
            targets = [h for h in heroes if h.health > 0]
            if targets:
                target = random.choice(targets)
                villain.attack(target)

        print("\nEstado após o turno:")
        for h in heroes:
            print(h)
        for v in villains:
            print(v)

        turn += 1

    print("\n------ FIM DA BATALHA -------------")
    total_hp_heroes = sum(h.health for h in heroes if h.health > 0)
    total_hp_villains = sum(v.health for v in villains if v.health > 0)

    print(f"HP restante - Heróis: {total_hp_heroes} | Vilões: {total_hp_villains}")
    if total_hp_heroes > total_hp_villains:
        print("Vitória dos heróis!")
    elif total_hp_villains > total_hp_heroes:
        print("Vitória dos vilões!")
    else:
        print("Empate técnico!")


# ======================
# EXECUÇÃO
# ======================
battle(heroes, villains)



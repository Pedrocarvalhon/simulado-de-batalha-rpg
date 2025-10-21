from abc import ABC, abstractmethod
import random



# classe base  rpg
class RPG(ABC):
    def __init__(self, name, rpg_class, health, strength, intelligence, dexterity):
        self.name = name
        self.rpg_class = rpg_class
        self.health = health
        self.max_health = health
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity

    @abstractmethod
    def stack(self):
        pass

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



# CLASSES DOS HERÓIS

class Warrior(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, kills):
        super().__init__(name, "Guerreiro", health, strength, intelligence, dexterity)
        self.kills = kills

    def level(self):
        return super().level() + self.kills // 2

    def stack(self):
        return f"Guerreiro {self.name} acumulou {self.kills} kills!"

    def attack(self, enemy):
        base_damage = self.strength + random.randint(0, 5)
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name}!")
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} atacou {enemy.name} ⚔️: Dano bruto={base_damage}, Defesa={defense}, Dano real={damage}")
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
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name}!")
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} disparou uma flecha 🏹 em {enemy.name}: Dano bruto={base_damage}, Defesa={defense}, Dano real={damage}")
        return damage


class Healer(RPG):
    def __init__(self, name, health, strength, intelligence, dexterity, assists):
        super().__init__(name, "Clérigo", health, strength, intelligence, dexterity)
        self.assists = assists

    def level(self):
        return super().level() + self.assists // 3

    def stack(self):
        return f"Clérigo {self.name} ajudou {self.assists} vezes!"

    def attack(self, enemy):
        base_damage = self.intelligence // 2 + random.randint(0, 3)
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name}!")
        defense = enemy.defend()
        damage = max(0, base_damage - defense)
        enemy.health -= damage
        print(f"{self.name} lançou um feitiço de luz ✨ em {enemy.name}: Dano real={damage}")
        return damage

    def heal(self, ally):
        heal_amount = self.intelligence + random.randint(0, 5)
        ally.health = min(ally.max_health, ally.health + heal_amount)
        print(f"{self.name} curou {ally.name} em {heal_amount} HP !")
        return heal_amount
    
# CLASSES DOS VILÕES
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
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name}!")
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} atacou {hero.name} : Dano bruto={base_damage}, Defesa={defense}, Dano real={damage}")
        return damage


class Minion(Villain):
    def stack(self):
        return f"Minion {self.name} apenas segue ordens com malícia {self.evilness}."

    def attack(self, hero):
        base_damage = self.strength // 2 + random.randint(0, 4)
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name}!")
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} (Minion) atacou {hero.name}: Dano real={damage}")
        return damage


class Boss(Villain):
    def attack(self, hero):
        base_damage = self.strength + self.evilness + random.randint(5, 10)
        if random.random() < 0.1:
            base_damage *= 2
            print(f" ATAQUE CRÍTICO de {self.name} (Boss)!")
        defense = hero.defend()
        damage = max(0, base_damage - defense)
        hero.health -= damage
        print(f"{self.name} (Boss) devastou {hero.name} 💀: Dano bruto={base_damage}, Defesa={defense}, Dano real={damage}")
        return damage


# CRIAÇÃO DOS PERSONAGENS
warrior = Warrior("Naruto", 30, 12, 8, 11, kills=20)
archer = Archer("Hunte", 30, 12, 8, 11, precision=20)
healer = Healer("Killua", 30, 12, 8, 11, assists=20)
heroes = [warrior, archer, healer]

villain1 = Minion("Illumi", 30, 14, 6, 12, evilness=20)
villain2 = Boss("Boruto", 30, 14, 15, 12, evilness=20)
villain3 = Boss("Feitan", 30, 14, 15, 16, evilness=20)
villain4 = Boss("Goku", 30, 14, 23, 16, evilness=20)
villains = [villain1, villain2, villain3, villain4]


# FUNÇÃO DE BATALHA
def battle(heroes, villains):
    turn = 1
    max_turns = 5
    regen_percent = 0.2

    current_heroes = list(heroes)
    current_villains = list(villains)

    while turn <= max_turns:
        print(f"\n===  Turno {turn} ===")

        # Regeneração
        for char in current_heroes + current_villains:
            if char.health > 0:
                regen = int(char.max_health * regen_percent)
                char.health = min(char.max_health, char.health + regen)
                print(f"{char.name} regenerou {regen} HP !")

        # Heróis atacam
        for hero in current_heroes:
            if hero.health <= 0:
                continue
            living_villains = [v for v in current_villains if v.health > 0]
            if not living_villains:
                continue
            if isinstance(hero, Healer) and random.random() < 0.5:
                low_allies = [h for h in current_heroes if h.health > 0 and h.health < h.max_health]
                if low_allies:
                    hero.heal(random.choice(low_allies))
                else:
                    hero.attack(random.choice(living_villains))
            else:
                hero.attack(random.choice(living_villains))

        # Vilões atacam
        for villain in current_villains:
            if villain.health <= 0:
                continue
            living_heroes = [h for h in current_heroes if h.health > 0]
            if not living_heroes:
                continue
            villain.attack(random.choice(living_heroes))

        # Mostrar estado
        print("\n Estado após o turno:")
        for h in current_heroes:
            print(h)
        for v in current_villains:
            print(v)

        turn += 1

    # Resultado final
    print("\n------ 🏁 FIM DA BATALHA -------------")
    total_hp_heroes = sum(h.health for h in current_heroes if h.health > 0)
    total_hp_villains = sum(v.health for v in current_villains if v.health > 0)
    print(f" HP Heróis: {total_hp_heroes} |  HP Vilões: {total_hp_villains}")

    if total_hp_heroes > total_hp_villains:
        print("🎖️ Vitória dos Heróis!")
    elif total_hp_villains > total_hp_heroes:
        print(" Vitória dos Vilões!")
    else:
        print("⚖️ Empate técnico!")



# EXECUÇÃO

battle(heroes, villains)

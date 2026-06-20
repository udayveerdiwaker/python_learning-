# ==============================================================================
# challenge.py - RPG Character Manager and Battle Simulator
# ==============================================================================
# CHALLENGE TASK: Complete the Player class methods and run this simulator.
# Once it runs, play with it, study the logic, and try the extension exercises!

class Player:
    """
    Represents a player in a game, holding their stats and inventory.
    """
    def __init__(self, name, max_health=100):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.inventory = []  # Starts with an empty inventory list
        self.max_inventory_slots = 5  # Maximum items a player can carry

    def display_status(self):
        """
        Prints the current player name, health, and their inventory.
        """
        print(f"\n--- {self.name}'s Status ---")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Inventory ({len(self.inventory)}/{self.max_inventory_slots}): {self.inventory}")
        print("-" * 25)

    def add_item(self, item):
        """
        Adds an item to the player's inventory if slots are available.
        Returns True if successful, False if inventory is full.
        """
        # Check if the player has space in their inventory
        if len(self.inventory) < self.max_inventory_slots:
            self.inventory.append(item)
            print(f"Added {item} to your inventory!")
            return True
        else:
            print("Your inventory is full! Discard an item first.")
            return False

    def consume_item(self, item):
        """
        Uses an item from the inventory.
        If it's a "Potion", it restores 30 health (up to max_health).
        If it's a "Mega Potion", it restores 60 health.
        If it's anything else, it just prints that it can't be consumed.
        The item must be removed from the inventory after consumption.
        """
        # Check if the item is actually in the inventory
        if item in self.inventory:
            if item == "Potion":
                self.health = min(self.max_health, self.health + 30)
                print(f"Consumed Potion. Restored 30 health. Current Health: {self.health}")
                self.inventory.remove(item)
            elif item == "Mega Potion":
                self.health = min(self.max_health, self.health + 60)
                print(f"Consumed Mega Potion. Restored 60 health. Current Health: {self.health}")
                self.inventory.remove(item)
            else:
                print(f"You cannot eat or drink a {item}!")
        else:
            print(f"You don't have a {item} in your inventory!")

    def take_damage(self, amount):
        """
        Reduces health by the specified amount.
        Health cannot go below 0.
        """
        self.health = max(0, self.health - amount)
        print(f"{self.name} takes {amount} damage! Health is now: {self.health}")
        if self.health == 0:
            print(f"💀 {self.name} has fallen in battle!")


# ==============================================================================
# MAIN SIMULATOR INTERFACE (CLI)
# ==============================================================================
if __name__ == "__main__":
    print("Welcome to the Python Practice RPG Character Simulator!")
    player_name = input("Enter your hero's name: ").strip()
    if not player_name:
        player_name = "Nameless Hero"
        
    hero = Player(player_name)
    # Give the hero some initial items
    hero.add_item("Sword")
    hero.add_item("Potion")

    while True:
        hero.display_status()
        print("Choose an action:")
        print("1. Gather food/loot (Add random item)")
        print("2. Consume Potion")
        print("3. Fight a Monster (Take damage)")
        print("4. Exit game")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            import random
            loot_pool = ["Potion", "Mega Potion", "Shield", "Golden Key", "Apple"]
            found_item = random.choice(loot_pool)
            print(f"\nYou found a {found_item} lying on the ground!")
            hero.add_item(found_item)
            
        elif choice == "2":
            # Let the user choose what to consume (Potion or Mega Potion)
            print("\nWhich potion do you want to drink?")
            print("Options: Potion, Mega Potion")
            potion_choice = input("Type potion name: ").strip()
            hero.consume_item(potion_choice)
            
        elif choice == "3":
            import random
            damage = random.randint(15, 45)
            print(f"\nA wild Goblin attacks!")
            hero.take_damage(damage)
            if hero.health == 0:
                print("\nGame Over! Restarting your health to try again.")
                hero.health = hero.max_health
                
        elif choice == "4":
            print(f"\nThanks for playing, {hero.name}! Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select from options 1 to 4.")

# ------------------------------------------------------------------------------
# 🏆 Extension Challenges for You:
# 1. Modify the `take_damage` function: If the player has a "Shield" in their inventory,
#    reduce the incoming damage by 10 points and print "Your shield blocked 10 damage!".
# 2. Add a new action "Discard Item": Let the player select and drop any item from
#    their inventory to free up space.
# ------------------------------------------------------------------------------

"""
Required sections

- Data_enter
- Confirming_Program

- Combat_Program_Initiator
- Combat_Program
    - Attack_Roller + Attack_damage
    - Battle_end
    - Battle_loop
    - Battle_Repeat
        - Same_battle
        - Different_battle

Required Data Points
- Round_Tracker
- Hits_Tracker
- Graze_Tracker
- Miss_Tracker

- Health
- Flinch
- Armour
- Mitigation
"""

import random
import time

print("Loading...")
time.sleep(0.5)

positive_response = ("Y", "y", "Yes", "yes")
negative_response = ("N", "n", "No", "no")

data_enter = True
data_process = False
confirm_program = False
battle_processor = False
battle_loop = False
battle_end = False
monster_turn = False
player_turn = False

while data_enter:
    data_prompt = input("\nDo you want to use custom data? (Y/N): ")
    #Custom enters

    entity_values = {
        "Player Health": None,
        "Player Flinch": None,
        "Player Armour": None,
        "Player Mitigation": None,
        "Monster Health": None,
        "Monster Flinch": None,
        "Monster Armour": None,
        "Monster Mitigation": None

    }
    if data_prompt in positive_response:
        for stat in entity_values:
            while True:
                user_enter = (input(f"Enter {stat}: "))

                if not user_enter.isdigit():
                    print("Error. Please enter a positive integer")
                elif int(user_enter) < 0:
                    print("Error. Please enter a positive integer.")
                else:
                    entity_values[stat] = int(user_enter)
                    break

        data_enter = False
        data_process = True

    # Default data
    elif data_prompt in negative_response:
        entity_values["Player Health"] = 10
        entity_values["Player Flinch"] = 10
        entity_values["Player Armour"] = 10
        entity_values["Player Mitigation"] = 10

        entity_values["Monster Health"] = 10
        entity_values["Monster Flinch"] = 10
        entity_values["Monster Armour"] = 10
        entity_values["Monster Mitigation"] = 10
        data_enter = False
        data_process = True

    else:
        data_enter = True
        data_process = False
        print("\nInvalid response, please enter Y or N ")

    #data processing
    while data_process:
        action_points = {
            "Player AP": 2,
            "Monster AP": 2
        }

        player_health = entity_values["Player Health"]
        player_flinch = entity_values["Player Flinch"]
        player_armour = entity_values["Player Armour"]
        player_mitigation = entity_values["Player Mitigation"]
        player_action = action_points["Player AP"]

        monster_health = entity_values["Monster Health"]
        monster_flinch = entity_values["Monster Flinch"]
        monster_armour = entity_values["Monster Armour"]
        monster_mitigation = entity_values["Monster Mitigation"]
        monster_action = action_points["Monster AP"]

        print(f"\nPlayer has {player_health} HP, {player_flinch} Flinch, {player_armour} Armour, and {player_mitigation} Mitigation")
        print(f"Monster has {monster_health} HP, {monster_flinch} Flinch, {monster_armour} Armour, and {monster_mitigation} Mitigation\n ")

        confirm_prompt = str(input("Are you ready to proceed? (Y/N): "))
        if confirm_prompt in positive_response:
            data_process = False
            battle_processor = True
            print("\nLoading...\n")
            time.sleep(0.5)
        elif confirm_prompt in negative_response:
            print(f"\nPlease repeat selection")
            data_process = False
            data_enter = True
        else:
            print("Invalid response, please enter Y or N\n ")

        while battle_processor:
            counters = {
            "Monster Hit": None,
            "Monster Graze": None,
            "Monster Miss": None,
            "Player Hit": None,
            "Player Graze": None,
            "Player Miss": None,
            "Round Counter": None,
            }

            for number in counters:
                counters[number] = 0

            initiate_prompt = str(input("Initiate combat?(Y/N): "))
            if initiate_prompt in positive_response:
                print("")
                battle_processor = False
                battle_loop = True

                turn_order = random.randint(1, 2)
                if turn_order == 1:
                    monster_turn = True
                    print(f"Monster Starts!\n ")
                else:
                    player_turn = True
                    print(f"Player Starts!\n ")
            elif initiate_prompt in negative_response:
                battle_loop = False
                battle_processor = False
                data_input = True
            else:
                print(f"Invalid response, please enter Y or N.\n ")

            while battle_loop:
                counters["Round Counter"] += 1
                while monster_turn:
                    if monster_health <= 0 or player_health <= 0:
                        monster_turn = False
                        battle_end = True
                        battle_loop = False
                    else:
                        if monster_action == 0:
                            monster_turn = False
                            player_turn = True
                            monster_action = action_points["Monster AP"]
                        else:
                            monster_action -= 1
                            # Monster Attacking Data
                            monster_accuracy = random.randrange(1, 20)
                            monster_damage = random.randrange(1, 8)
                            monster_graze = monster_damage - player_mitigation
                            time.sleep(0.6)
                            if monster_action == 1:
                                print("Monster makes their first attack!")
                            else:
                                print("Monster makes their second attack!")
                            if monster_accuracy >= player_armour and monster_accuracy >= player_flinch:
                                player_health -= monster_damage
                                counters["Monster Hit"] += 1
                                print(
                                    f"Monster hit the Player directly, dealing {monster_damage} damage. Player is now at {player_health} HP!")
                            elif player_armour >= monster_accuracy >= player_flinch:
                                counters["Monster Graze"] += 1
                                if monster_graze <= 1:
                                    monster_graze = 1
                                    player_health -= monster_graze
                                    print(f"Monster barely grazed the Player, dealing 1 damage. Player is now at {player_health} HP!")
                                else:
                                    player_health -= monster_graze
                                    print(f"Monster grazed the Player, dealing {monster_graze} damage. Player is now at {player_health} HP!")
                            else:
                                counters["Monster Miss"] += 1
                                print(f"Monster missed the Player completely dealing no damage!")
                            print("")

                while player_turn:
                    if monster_health <= 0 or player_health <= 0:
                        player_turn = False
                        battle_end = True
                        battle_loop = False
                    else:
                        if player_action == 0:
                            player_turn = False
                            monster_turn = True
                            player_action = action_points["Player AP"]
                        else:
                            player_action -= 1
                            # Player Attacking Data
                            player_damage = random.randrange(1, 6) + 3
                            player_accuracy = random.randrange(3, 18) + 5
                            player_graze = player_damage - monster_mitigation

                            time.sleep(0.6)
                            if player_action == 1:
                                print("Player makes their first attack!")
                            else:
                                print("Player makes their second attack!")
                            if player_accuracy >= monster_armour and player_accuracy >= monster_flinch:
                                monster_health -= player_damage
                                counters["Player Hit"] += 1
                                print(f"Player hit the Monster directly, dealing {player_damage} damage. Monster is now at {monster_health} HP!")
                                player_damage = random.randrange(1, 6) + 3
                            elif monster_armour >= player_accuracy >= monster_flinch:
                                counters["Player Graze"] += 1
                                if player_graze <= 1:
                                    player_graze = 1
                                    monster_health -= player_graze
                                    print(f"Player barely grazed the Monster, dealing 1 damage. Monster is now at {monster_health} HP!")
                                else:
                                    monster_health -= player_graze
                                    print(
                                        f"Player grazed the Monster, dealing {player_graze} damage. Monster is now at {monster_health} HP!")
                                player_damage = random.randrange(1, 6) + 3
                            else:
                                counters["Player Hit"] += 1
                                print(f"Player missed the Monster completely dealing no damage!")
                            print("")

                while battle_end:
                    if player_health >= 1:
                        print(f"Player survives with {player_health} HP\n")
                    elif monster_health >= 1:
                        print(f"Monster survives with {monster_health} HP!\n")
                    else:
                        print(f"Unknown outcome.")
                    print(f"This combat took {counters["Round Counter"]} rounds!\n")
                    print(f"The monster landed {counters["Monster Hit"]} attacks!\nThe monster grazed {counters["Monster Graze"]} attacks.\nThe monster missed {counters["Monster Miss"]} attacks.\n")
                    print(f"The player landed {counters["Player Hit"]} attacks!\nThe player grazed {counters["Player Graze"]} attacks.\nThe player missed {counters["Player Miss"]} attacks.\n")
                    adjust_program = True
                    while adjust_program:
                        adjust_prompt = str(input("Would you like to repeat? (Y/N): "))
                        if adjust_prompt in positive_response:
                            while adjust_prompt in positive_response:
                                repeat_prompt = str(input(f" \nDo you want to\n1) Repeat the Battle?\n2) Restart the Program?\nResponse: "))
                                if repeat_prompt == "1":
                                    adjust_prompt = ""
                                    adjust_program = False
                                    battle_end = False

                                    player_health = entity_values["Player Health"]
                                    player_flinch = entity_values["Player Flinch"]
                                    player_armour = entity_values["Player Armour"]
                                    player_mitigation = entity_values["Player Mitigation"]
                                    player_action = action_points["Player AP"]

                                    monster_health = entity_values["Monster Health"]
                                    monster_flinch = entity_values["Monster Flinch"]
                                    monster_armour = entity_values["Monster Armour"]
                                    monster_mitigation = entity_values["Monster Mitigation"]
                                    monster_action = action_points["Monster AP"]

                                    print("\nLoading...\n")
                                    time.sleep(0.5)
                                    battle_processor = True


                                elif repeat_prompt == "2":
                                    adjust_prompt = ""
                                    adjust_program = False
                                    battle_end = False

                                    print("\nLoading...")
                                    time.sleep(0.5)
                                    data_enter = True
                                else:
                                    print(f"\nInvalid response, please enter 1 or 2. ")
                        elif adjust_prompt in negative_response:
                            print(f"\nThank you for simulating!\n ")
                            combat_program = False
                            adjust_program = False
                            battle_end = False

                        else:
                            print(f"\nInvalid response, please enter Y or N.\n ")

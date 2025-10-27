'''
australia.py

A program that simulates the relocation of Australian animals across states.

Each animal has a known threat to avoid. The goal is to relocate as many 
animals as possible while ensuring that no animal ends up near its threat — 
and no two animals share the same state.

This program involves reading animal data from a file, building objects to
represent each animal, and implementing relocation logic to ensure animals
are placed safely.
'''

# A mapping of which states are adjacent to which.
# Used to determine whether an animal’s threat is in a neighboring area.
ADJACENT_STATES = {
    'NSW': ['QLD', 'VIC', 'SA'],
    'QLD': ['NSW', 'NT', 'SA'],
    'VIC': ['NSW', 'SA'],
    'TAS': [],  # Tasmania is isolated, so no adjacent states
    'SA': ['WA', 'NT', 'QLD', 'NSW', 'VIC'],
    'NT': ['WA', 'QLD', 'SA'],
    'WA': ['NT', 'SA']
}

# List of all valid states where animals can be placed.
VALID_STATES = ['NSW', 'QLD', 'VIC', 'TAS', 'SA', 'NT', 'WA']

import os  # used for checking whether animals.csv exists


# ------------------------------
# Class Definition
# ------------------------------

class FictionalAnimal:
    '''
    Represents a fictional Australian animal used in the relocation simulation.

    Each animal has a name, habitat, threat, and current state.
    '''

    def __init__(self, name: str, habitat: str, threat: str):
        '''
        Initialises a new FictionalAnimal with the given name, habitat, and threat.
        Sets the starting state to 'ACT' by default (meaning not yet relocated).
        '''
        self.name = name.strip()     # animal name, trimmed of extra spaces
        self.habitat = habitat.strip()  # preferred habitat
        self.threat = threat.strip()    # animal that threatens this one
        self.state = 'ACT'              # all animals start in ACT (unplaced)


    def get_state(self) -> str:
        '''Returns the current state where this animal is located.'''
        return self.state


    def set_state(self, state: str):
        '''
        Updates the animal's state if the new state is valid.

        A valid state must exist in the list VALID_STATES.
        If not valid, the state remains unchanged.
        '''
        if state in VALID_STATES:
            self.state = state


    def __str__(self) -> str:
        '''
        Returns a formatted string showing all details of the animal.
        Example output:
        Kangaroo
           Habitat : Grassland
           Threat  : Dingo
           State   : NSW
        '''
        return (f"{self.name}\n"
                f"   Habitat : {self.habitat}\n"
                f"   Threat  : {self.threat}\n"
                f"   State   : {self.state}")


    @staticmethod
    def load_dataset() -> list['FictionalAnimal']:
        '''
        Loads animal data from animals.csv and returns a list of FictionalAnimal objects.

        Expected line format: <name>,<habitat>,<threat>
        - Lines missing fields or with extra fields are skipped.
        - If the file does not exist, return an empty list.
        '''
        animals = []  # store created animal objects

        # if the file doesn’t exist, return empty list immediately
        if not os.path.exists('animals.csv'):
            return animals

        # open the CSV file and read each line
        with open('animals.csv', 'r', encoding='utf-8') as f:
            for line in f:
                # Split the line by commas (CSV format)
                parts = line.strip().split(',')
                # Skip if not exactly 3 parts (invalid line)
                if len(parts) != 3:
                    continue
                name, habitat, threat = parts
                # create new FictionalAnimal object and add to list
                animals.append(FictionalAnimal(name, habitat, threat))
        return animals  # return all valid animal objects


# ------------------------------
# Relocation Logic
# ------------------------------

def relocate_animals(animals: list[FictionalAnimal]):
    '''
    Relocate animals safely across Australian states.

    Each state can host at most one animal.
    Animals must not be placed next to their threats
    (based on adjacency in ADJACENT_STATES).
    '''
    occupied_states = {}  # dictionary: state -> animal placed there
    placed_animals = set()  # track animals already relocated

    # Loop over each valid state to try to place animals there
    for state in VALID_STATES:
        for animal in animals:
            # Skip if animal already placed in a previous state
            if animal.name in placed_animals:
                continue

            # Skip this state if it already contains an animal
            if state in occupied_states:
                break

            # get all neighboring states for conflict checks
            adjacent = ADJACENT_STATES[state]
            conflict = False  # assume safe until proven otherwise

            # 1️. Check if this animal’s threat is already in an adjacent state
            for adj in adjacent:
                if adj in occupied_states:
                    if occupied_states[adj].name == animal.threat:
                        conflict = True  # can’t place here
                        break
            if conflict:
                continue  # try next animal or next state

            # 2️. Check if any neighbor’s threat is THIS animal (reverse threat)
            for adj in adjacent:
                if adj in occupied_states:
                    other_animal = occupied_states[adj]
                    if other_animal.threat == animal.name:
                        conflict = True
                        break
            if conflict:
                continue

            # If no conflicts → place the animal here
            animal.set_state(state)          # update its internal state
            occupied_states[state] = animal  # mark state as occupied
            placed_animals.add(animal.name)  # record that it’s placed
            break  # move on to the next state in VALID_STATES


# ------------------------------
# Main Function
# ------------------------------

def main():
    '''
    Runs the full relocation simulation from start to finish.

    Steps:
    1. Load animals from animals.csv.
    2. Print their details before relocation.
    3. Run relocate_animals() to distribute them safely.
    4. Print the summary of where each animal ended up.
    '''
    print(">> READING IN ANIMALS.")
    animals = FictionalAnimal.load_dataset()  # load data
    print(f"Loaded {len(animals)} animals from animals.csv.\n")

    # Display animal data before relocation
    print(">> BEFORE RELOCATION.")
    for a in animals:
        print(a)      # __str__() defines the display format
        print()       # blank line for readability

    print(">> RELOCATING ANIMALS.")
    relocate_animals(animals)  # perform relocation

    # Count how many were actually moved (state != 'ACT')
    relocated = sum(1 for a in animals if a.get_state() != 'ACT')
    print(f"Animals relocated: {relocated}/{len(animals)}\n")

    # Print final summary: each animal + its assigned state
    print(">> SUMMARY.")
    for a in animals:
        print(f"{a.name}: {a.get_state()}")


# ------------------------------
# Program Entry Point
# ------------------------------

# This ensures the program runs only when executed directly
# (not when imported as a module in another script)
if __name__ == '__main__':
    main()

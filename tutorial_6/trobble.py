class Trobble:
    """Trobbles: simplified digital pets.

    Data Attributes:
    name -- the Trobble's name.
    sex -- 'male' or 'female'.
    age -- a non-negative integer
    health -- an integer between 0 (dead) and 10 (full health) inclusive
    hunger -- a non-negative integer (0 is not hungry)
    """
    
    def __init__(self, name, sex) -> None:
        self.name = name
        self.sex = sex
        self.health = 10
        self.age = 0
        self.hunger = 0

    def __str__(self) -> str:
        """
        returns string in this format '_name_: _sex_, health _health_, hunger _hunger_, age _age_'
        """
        return f"{self.name}: {self.sex}, health {self.health}, hunger {self.hunger}, age {self.age}"

    def next_turn(self):
        """End the turn for the instance and recompute the attribute values
        for the next turn.
        """
        if self.is_alive():
            self.age += 1
            self.hunger += self.age
            self.health -= self.hunger // 20
            self.health = max(0, self.health)

    def feed(self, food_value=25):
        """Feed the Trobble instance to decrease the hunger by 25
        with a minimum value of 0.
        """
        self.hunger = max(0, self.hunger - food_value)
    
    def cure(self, cure_value=5):
        """Increase the health of the instance by 5 up to the maximum of 10.
        """
        self.health = min(10, self.health + cure_value)
    
    def party(self):
        """Increase the health of the instance by 2 up to the maximum of 10 
	    and increase the hunger by 4.
        """
        self.health = min(10, self.health + 2)
        self.hunger += 4

    def is_alive(self):
        """Return True if the health of the instance is positive,
        otherwise False.
        """
        return self.health > 0

    def is_birthday(self):
        """Return True if the age of the instance is a multiple of 10,
        otherwise False.
        """
        return self.age % 10 == 0 and self.age > 0

    def congratulate_with_the_birtday(self, food_value=5):
        """Print a congratulation message for the birthday.
        """
        print(f"Happy Birthday {self.name}!")
        self.feed(food_value)

# Playing with Trobbles

def get_name():
    return input('Please give your new Trobble a name: ')

def get_sex():
    sex = None
    while sex is None:
        prompt = 'Is your new Trobble male or female? Type "m" or "f" to choose: '
        choice = input(prompt)
        if choice == 'm':
            sex = 'male'
        elif choice == 'f':
            sex = 'female'
    return sex

def get_action(actions):
    while True:
        prompt = f"Type one of {', '.join(actions.keys())} to perform the action: "
        action_string = input(prompt)
        if action_string not in actions:
            print('Unknown action!')
        else:
            return actions[action_string]
        
def play():
    name = get_name()
    sex = get_sex()
    trobble = Trobble(name, sex)
    actions = {'feed': trobble.feed, 'cure': trobble.cure, 'party': trobble.party}
    while trobble.is_alive():
        if trobble.is_birthday():
            trobble.congratulate_with_the_birtday()
        print('You have one Trobble named ' + str(trobble))
        action = get_action(actions)
        action()
        trobble.next_turn()
    print(f'Unfortunately, your Trobble {trobble.name} has died at the age of {trobble.age}')


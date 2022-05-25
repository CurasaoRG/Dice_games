# from collections import Counter
import random


def main():
    players_num = 2
    game = YachtGame(players_num)
    game.play()


class YachtGame:
    COMBINATIONS = ("pair", "two pairs", "three", "full house", "four", "yacht",
                    "small straight", "big straight", "chance")

    def __init__(self, players_num=1):
        self.players = []
        self.score = {}
        for i in range(players_num):
            self.players.append(Player(i))
        self.win = 0
        self.winner = 1

    def show_table(self):
        print("Status")
        line = "Player id".ljust(15, " ")
        for player in self.players:
            line += f"{player.player_id}".ljust(5, " ")
        print(line)
        for key in YachtGame.COMBINATIONS:
            line = f"{key}".ljust(15, " ")
            for player in self.players:
                line = line + f"{player.combinations_dict.get(key, '-')}".ljust(5, " ")
            print(line)
        line = "total score".ljust(15, " ")
        for player in self.players:
            line += f"{sum(player.combinations_dict.values())}".ljust(5, " ")
        print(line)

    def play(self):
        for i in range(len(self.COMBINATIONS)):
            print(f"throw #{i + 1}")
            for player in self.players:
                player.throw()
                if player.points > self.win:
                    self.winner = player.player_id
                    self.win = player.points
            self.show_table()
        print(f"Winner is player #{self.winner}")


class Player:

    def __init__(self, player_id):
        self.combinations_dict = {}
        self.points = 0
        self.current_throw = []
        self.player_id = player_id + 1

    def empty_combinations(self):
        return set(YachtGame.COMBINATIONS) - set(self.combinations_dict.keys())

    def set_to_zero(self):
        print("which combination set to zero?")
        print(f"you haven't completed following: {self.empty_combinations()}")
        while True:
            question = input()
            if question in self.empty_combinations():
                self.combinations_dict[question] = 0
                break

    def accept_combination(self, combination, double=False):
        while True:
            question = input(f"accept combination as {combination}?(Y/N)").strip().upper()
            if question == "Y":
                self.combinations_dict[combination] = sum(self.current_throw) * (1 + double) + 50 * (
                            combination == "yacht")
                break
            elif question == "N":
                if "chance" not in self.combinations_dict.keys():
                    question = input(f'accept combination as "chance"?(Y/N)').strip().upper()
                    if question == "Y":
                        self.combinations_dict["chance"] = sum(self.current_throw)
                    else:
                        self.set_to_zero()
                else:
                    self.set_to_zero()
                break
        self.points += self.combinations_dict[combination]

    def check_combination(self, tryout):

        dice_dict = {}
        for dice in tryout:
            dice_dict[dice] = 1 + dice_dict.get(dice, 0)
        if 5 in dice_dict.values():
            combination = "yacht"
        elif 4 in dice_dict.values():
            combination = "four"
        elif 3 in dice_dict.values():
            if 2 in dice_dict.values():
                combination = "full house"
            else:
                combination = "three"
        elif 2 in dice_dict.values():
            if len(dice_dict.keys()) == 3:
                combination = "two pairs"
            else:
                combination = "pair"
        else:
            if 6 not in dice_dict.keys():
                combination = "small straight"
            elif 1 not in dice_dict.keys():
                combination = "big straight"
            else:
                combination = "chance"
        return combination

    def check_even(self, tryout):
        even, odd = True, True
        for num in tryout:
            even *= (num % 2 == 0)
            odd *= (num % 2 == 1)
        if even:
            return "even"
        elif odd:
            return "odd"
        else:
            return False

    def show_status(self):
        print("Status")
        dash = ""
        for key in YachtGame.COMBINATIONS:
            if key in self.combinations_dict.keys(): dash = "="
            print(f"{key} {dash} {self.combinations_dict.get(key, '-')}")
            dash = ""
        print(f"total points = {sum(self.combinations_dict.values())}")

    def throw(self):

        def try_keep(old, keep, dice_num):
            pass

        def roll_dice(old, keep, dice_num):
            new = [random.randrange(1, 7) for _ in range(dice_num)]
            if not keep:
                return new
            bold = []
            for i in keep:
                bold.append(old[int(i) - 1])
            bold.extend(new)
            return bold

        def list_input(input_text):
            rest = []
            while True:
                res = input(input_text)
                if res.strip() == '':
                    return rest
                for item in res.split(','):
                    item = item.strip()
                    if (len(item) > 1) or (item not in '12345'):
                        print("wrong number")
                        break
                    else:
                        rest.append(item)
                else:
                    break
            return rest

        print(f"player #{self.player_id} turn")
        throw_count = 1
        tryout = []
        keep = []
        while throw_count <= 3:
            dice_num = 5
            if keep:
                dice_num -= len(keep)
            tryout = roll_dice(tryout, keep, dice_num)
            combination = self.check_combination(tryout)
            if combination not in self.combinations_dict.keys():
                print(f"{tryout} => {combination}, sum = {sum(tryout)}")
            else:
                print(f"{tryout} => {combination} (completed with {self.combinations_dict[combination]} points), "
                    f"sum = {sum(tryout)}")
            if throw_count == 3: break
            while True:
                question = input("Keep combination (K) or Throw again (T)?").strip().upper()
                if question in ("K", "T"):
                    break
            if question == "K":
                break
            if question == "T":
                keep = list_input("which ones to keep? fill in numbers separated by comma: ")
                throw_count += 1
                continue
        self.current_throw = tryout[:]
        if combination == "chance":
            if "chance" in self.combinations_dict.keys():
                print("you already had a chance")
                self.set_to_zero()
            else:
                self.accept_combination("chance")
        elif combination not in self.combinations_dict.keys():
            print(f"Completed combination {combination}")
            self.accept_combination(combination, throw_count == 1)
        else:
            print("you already have this combination")
            if "chance" not in self.combinations_dict.keys():
                self.accept_combination("chance")
            else:
                self.set_to_zero()


if __name__ == "__main__":
    main()

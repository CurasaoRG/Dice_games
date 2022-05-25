import random


def main():

    pig = PigGame()
    pig.play()


class PigGame:

    def __init__(self):
        self.N_players=int(input("Set number of players "))
        self.points = {}
        for _ in range(1,self.N_players+1):
            self.points[_] = 0
        self.goal = 100

    def show_results(self):
        for i in range(1,self.N_players + 1):
            print(f"player # {i} have {self.points[i]}")

    def play(self):

        def dice_roll():
            num = random.randrange(1, 7)
            print(f"you have {num}")
            return num

        turn = 0
        max_points = 0
        winner = []
        while not winner:
            turn +=1
            print(f"turn # {turn}")
            self.show_results()
            for player in range(1,self.N_players+1):
                if winner:
                    print(f"this is last turn - player(s) #{','.join(map(str,winner))} have winning score")
                score = 0
                print(f"#{player} player turn. current score = {self.points[player]}")
                while True:
                    question = input("press R to roll, S to stop").strip().upper()
                    if question == "R":
                        dice = dice_roll()
                        if dice == 1:
                            print("your current points burned")
                            print(f"your score = {self.points[player]}\n")
                            score = 0
                            break
                        score += dice
                        print(f"current score {score+self.points[player]}")
                        if score+self.points[player] >= self.goal:
                            print(f"you have reached goal of {self.goal}")
                            self.points[player] += score
                            winner.append(player)
                            max_points = max(max_points, self.points[player])
                            break
                    elif question == "S":
                        print(f"current score of player # {player} is {score+self.points[player]}\n")
                        self.points[player] += score
                        break
                    else:
                        pass
        self.show_results()
        for w in winner:
            if self.points[w] == max_points:
                print(f"winner is player # {w}")


if __name__ == "__main__":
    main()
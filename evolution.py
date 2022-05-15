import copy
import random
import threading
import running_information
import player
from player import Player
import numpy as np


class Evolution:

    def __init__(self):

        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """

        players.sort(key=lambda x: x.fitness, reverse=True)

        running_information.high.append(players[0].fitness)
        running_information.low.append(players[len(players)-1].fitness)
        running_information.average.append(players[int(len(players)/2)].fitness)
        sorted_list = players[:num_players - 50]

        r_players = players[num_players - 51:]
        random.shuffle(r_players)
        random_list = r_players[:50]

        players_output = sorted_list + random_list
        # splits = np.array_split(players, num_players)
        # for arr in splits:
        #    l = list(arr)
        #    l.sort(key=lambda x:x.fitness,reverse=True )
        #    players_output.append(arr[0])
        # print(num_players,len(players))
        # players_output = []
        # random.shuffle(players)
        # counter=0
        # number=0
        # while counter<num_players-1:
        #    if players[number].fitness>players[number+1].fitness:
        #        players_output.append(players[number])
        #    else:
        #        players_output.append(players[number+1])

        #    counter+=1
        #    number+=2
        #    print(number,counter)

        # for
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)

        # TODO (Additional: Learning curve)
        # return players[: num_players]
        return players_output

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:

            childs = self.create_childs(prev_players)

            return childs

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    def recombination_mutation(self, parent1_input: player.Player, parent2_input: player.Player, mutation_percent):
        parent1 = self.clone_player(parent1_input)
        parent2 = self.clone_player(parent2_input)

        for i in range(0, len(parent1.nn.b1)):
            if random.randint(1, 10) % 2 == 0:
                temp = np.copy(parent1.nn.b1[i])
                parent1.nn.b1[i] = parent2.nn.b1[i]
                parent2.nn.b1[i] = temp

            parent1.nn.b1[i] = self.mutation(parent1.nn.b1[i], mutation_percent)
            parent2.nn.b1[i] = self.mutation(parent2.nn.b1[i], mutation_percent)

        for i in range(0, len(parent1.nn.b2)):
            if random.randint(1, 10) % 2 == 0:
                temp = np.copy(parent1.nn.b2[i])
                parent1.nn.b2[i] = parent2.nn.b2[i]
                parent2.nn.b2[i] = temp

            parent1.nn.b2[i] = self.mutation(parent1.nn.b2[i], mutation_percent)
            parent2.nn.b2[i] = self.mutation(parent2.nn.b2[i], mutation_percent)

        i = 0
        for row in parent1.nn.w1:
            for j in range(0, len(row)):
                if random.randint(1, 10) % 2 == 0:
                    temp = np.copy(parent1.nn.w1[i][j])
                    parent1.nn.w1[i][j] = parent2.nn.w1[i][j]
                    parent2.nn.w1[i][j] = temp

                parent1.nn.w1[i][j] = self.mutation(parent1.nn.w1[i][j], mutation_percent)
                parent2.nn.w1[i][j] = self.mutation(parent2.nn.w1[i][j], mutation_percent)

            i += 1

        i = 0
        for row in parent1.nn.w2:
            for j in range(0, len(row)):
                if random.randint(1, 10) % 2 == 0:
                    temp = np.copy(parent1.nn.w2[i][j])
                    parent1.nn.w2[i][j] = parent2.nn.w2[i][j]
                    parent2.nn.w2[i][j] = temp

                parent1.nn.w2[i][j] = self.mutation(parent1.nn.w2[i][j], mutation_percent)
                parent2.nn.w2[i][j] = self.mutation(parent2.nn.w2[i][j], mutation_percent)

            i += 1

        return parent1, parent2

    def mutation(self, w, mutation_percent):
        rand = random.randint(1, 100)
        if rand <= mutation_percent:
            if rand % 2 == 0:
                w += rand / 100
            else:
                w -= rand / 100

        return w

    def create_childs(self, prev_players):
        ch_list = []
        random.shuffle(prev_players)
        for i in range(0, len(prev_players) - 1,2):
            #t = threading.Thread(target=self.recombination_mutation2, args=(prev_players[i], prev_players[i + 1], 10))
            ch1,ch2 = self.recombination_mutation2(prev_players[i], prev_players[i + 1], mutation_percent=1)
            #t.start()
            #threads_list.append(t)
            ch_list.append(ch1)
            ch_list.append(ch2)

        #for t in threads_list:
        #    t.join()
        #print(ch_list)
        return ch_list

    def recombination_mutation2(self, parent1_input: player.Player, parent2_input: player.Player, mutation_percent):
        parent1 = self.clone_player(parent1_input)
        parent2 = self.clone_player(parent2_input)

        for i in range(0, len(parent1.nn.b1)):
            if i <= len(parent1.nn.b1) / 2:
                temp = np.copy(parent1.nn.b1[i])
                parent1.nn.b1[i] = parent2.nn.b1[i]
                parent2.nn.b1[i] = temp

            parent1.nn.b1[i] = self.mutation(parent1.nn.b1[i], mutation_percent)
            parent2.nn.b1[i] = self.mutation(parent2.nn.b1[i], mutation_percent)

        for i in range(0, len(parent1.nn.b2)):
            if i <= len(parent1.nn.b2) / 2:
                temp = np.copy(parent1.nn.b2[i])
                parent1.nn.b2[i] = parent2.nn.b2[i]
                parent2.nn.b2[i] = temp

            parent1.nn.b2[i] = self.mutation(parent1.nn.b2[i], mutation_percent)
            parent2.nn.b2[i] = self.mutation(parent2.nn.b2[i], mutation_percent)

        i = 0
        for row in parent1.nn.w1:
            if i <= len(parent1.nn.w1) / 2:
                temp = np.copy(parent1.nn.w1[i])
                parent1.nn.w1[i] = parent2.nn.w1[i]
                parent2.nn.w1[i] = temp

            for j in range(0, len(row) - 1):
                parent1.nn.w1[i][j] = self.mutation(parent1.nn.w1[i][j], mutation_percent)
                parent2.nn.w1[i][j] = self.mutation(parent2.nn.w1[i][j], mutation_percent)

            i += 1

        i = 0
        for row in parent1.nn.w2:
            if i <= len(parent1.nn.w2) / 2:
                temp = np.copy(parent1.nn.w2[i])
                parent1.nn.w2[i] = parent2.nn.w2[i]
                parent2.nn.w2[i] = temp

            for j in range(0, len(row) - 1):
                parent1.nn.w2[i][j] = self.mutation(parent1.nn.w2[i][j], mutation_percent)
                parent2.nn.w2[i][j] = self.mutation(parent2.nn.w2[i][j], mutation_percent)

            i += 1


        return parent1, parent2


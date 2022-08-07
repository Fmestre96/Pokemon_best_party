import json
from scipy.stats import gmean
import itertools

#create a function that opens a json file and returns the data
def open_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

#import "pokemons.json" and store it in a variable
pokemon_list = open_json("pokemon_full_stats.json")
pokemon_types = open_json("pokemon_types.json")

gyarados = 130 
rhydon = 112
Exeggutor = 103
Gengar = 94
Omastar = 139
Venomoth = 49

mew = 151
mewtwo = 150
moltres = 146
zapdos = 145
articuno = 144
dragonite = 149


def alpha_dom_beta(alpha, beta):
    alpha_types = [alpha["type1"], alpha["type2"]]
    alpha_types.sort()
    beta_types = [beta["type1"], beta["type2"]]
    beta_types.sort()


    if(alpha_types == beta_types):
        if(alpha["total"] > beta["total"]):
        #if(alpha["total"] > beta["total"] and alpha["hp"] >= beta["hp"] and alpha["attack"] >= beta["attack"] and alpha["defense"] >= beta["defense"] and alpha["special_attack"] >= beta["special_attack"] and alpha["special_defense"] >= beta["special_defense"] and alpha["speed"] >= beta["speed"]):
            #print(beta["name"] + " is dominated by " + alpha["name"])
            return True
    return False

def is_pareto_dominated(poke_checked):
    for pokemon in pokemon_list:
        if(alpha_dom_beta(pokemon, poke_checked)):
            return True
    return False




def attack_advantage(alpha, beta):
    alpha_type1 = alpha["type1"].upper()
    alpha_type2 = alpha["type2"].upper()
    beta_type1 = beta["type1"].upper()
    beta_type2 = beta["type2"].upper()

    try:
        attack_factor11 = pokemon_types[alpha_type1][beta_type1]
    except:
        #print("{} does not have an attack advantage against {}".format(alpha_type1, beta_type1))
        attack_factor11 = 0
    try:
        attack_factor12 = pokemon_types[alpha_type1][beta_type2]
    except:
        #print("{} does not have an attack advantage against {}".format(alpha_type1, beta_type2))
        attack_factor12 = 1
    try:
        attack_factor21 = pokemon_types[alpha_type2][beta_type1]
    except:
        #print("{} does not have an attack advantage against {}".format(alpha_type2, beta_type1))
        attack_factor21 = 0
    try:
        attack_factor22 = pokemon_types[alpha_type2][beta_type2]
    except:
        #print("{} does not have an attack advantage against {}".format(alpha_type2, beta_type2))
        attack_factor22 = 1

    # print(attack_factor11)
    # print(attack_factor12)
    # print(attack_factor21)
    # print(attack_factor22)

    return max(0.125, attack_factor11*attack_factor12, attack_factor21*attack_factor22)

def defense_advantage(alpha, beta):
    return 1/attack_advantage(beta, alpha)

def edge(alpha, beta):
    attack = attack_advantage(alpha, beta)
    defense = defense_advantage(alpha, beta)
    # print("{} attack advantage".format(attack))
    # print("{} defense advantage".format(defense))
    return attack * defense


def show_dominators():
    dominators = []
    dominateds = []
    for pokemon in pokemon_list:
        dominators.append(pokemon)
        is_dominated = is_pareto_dominated(pokemon)
        if(is_dominated):
            dominateds.append(pokemon)
            dominators.remove(pokemon)

    print("{} pokemon are dominated".format(len(dominateds)))
    print("{} pokemon are dominators".format(len(dominators)))



def attack_geo_mean(pokemon_check):
    all_attacks = []
    for pokemon in pokemon_list:
        attack = attack_advantage(pokemon_check, pokemon)
        #print(attack)
        all_attacks.append(attack)

    return gmean(all_attacks)

def defense_geo_mean(pokemon_check):
    all_defenses = []
    for pokemon in pokemon_list:
        defense = defense_advantage(pokemon_check, pokemon)
        #print(defense)
        all_defenses.append(defense)

    return gmean(all_defenses)
    

def edge_geo_mean(pokemon_check):
    all_edges = []
    for pokemon in pokemon_list:
        poke_edge = edge(pokemon_check, pokemon)
        #print(edge)
        all_edges.append(poke_edge)

    return gmean(all_edges)


def print_pokemon_edges(pokemon):
    print(attack_geo_mean(pokemon)) 
    print(defense_geo_mean(pokemon))
    print(edge_geo_mean(pokemon))


def party_best_edge(party):
    best_edge = []
    #for each index in the pokemon_list, select the max edge of the party
    for i in range(len(pokemon_list)):
        party_index_edge = []
        for pokemon in party:
            party_index_edge.append(pokemon['edges'][i])
        best_edge.append(max(party_index_edge))

    return gmean(best_edge)


def show_party(party):
    for pokemon in party:
        print(pokemon["name"])
    print("Edge of the party: {}".format(party_best_edge(party)))

def best_pokemon_to_add_to_party(party):
    #print("Current party Edge is: {}".format(party_best_edge(party)))
    max_party_edge = -1
    max_pokemon = pokemon_list[0]

    for pokemon in pokemon_list:
        party.append(pokemon)
        party_edge = party_best_edge(party)
        if((party_edge > max_party_edge) or (party_edge == max_party_edge and pokemon["total"] > max_pokemon['total'])):
            max_party_edge = party_edge
            max_pokemon = pokemon
            # print("Max party edge: {} with pokemon {}".format(party_edge, pokemon["name"]))
            # show_party(party)
            # print('----------------------------------------------------')
        party.remove(pokemon)
    
    #print(max_party_edge)
    return max_pokemon


def greedy_approach():
    party=[]
    while(len(party) < 6):
        pokemon = best_pokemon_to_add_to_party(party)
        party.append(pokemon)

    return party


def best_party_combinations(available_pokemon_list):
    party = []
    max_party_edge = -1
    best_party = []

    possible_parties = list(itertools.combinations(available_pokemon_list, 6))
    for party in possible_parties:
        party_edge = party_best_edge(party)
        if((party_edge >= max_party_edge)):
            max_party_edge = party_edge
            best_party = party


    return best_party

def naive_approach():
    return best_party_combinations(pokemon_list)

def pareto_combinations_approach():
    dominators = []
    for pokemon in pokemon_list:
        dominators.append(pokemon)
        is_dominated = is_pareto_dominated(pokemon)
        if(is_dominated):
            dominators.remove(pokemon)    
    return best_party_combinations(dominators)

def save_full_stats():
    for pokemon1 in pokemon_list:
        pokemon1['attack_advantages']=[]
        pokemon1['defense_advantages']=[]
        pokemon1['edges']=[]
        for pokemon2 in pokemon_list:
            poke_attack_advantage = attack_advantage(pokemon1, pokemon2)
            poke_defense_advantage = defense_advantage(pokemon1, pokemon2)
            poke_edge = edge(pokemon1, pokemon2)
            pokemon1['attack_advantages'].append(poke_attack_advantage)
            pokemon1['defense_advantages'].append(poke_defense_advantage)
            pokemon1['edges'].append(poke_edge)
        pokemon1["attack_geo_mean"] = gmean(pokemon1['attack_advantages'])
        pokemon1["defense_geo_mean"] = gmean(pokemon1['defense_advantages'])
        pokemon1["edge_geo_mean"] = gmean(pokemon1['edges'])

    #save file to json
    with open('pokemon_full_stats.json', 'w') as outfile:
        json.dump(pokemon_list, outfile)

#main function
if __name__ == "__main__":

    #show_dominators()
    #print(attack_advantage(pokemon_list[mew-1], pokemon_list[mew-1]))
    #print_pokemon_edges(pokemon_list[rhydon-1])

    # pokemon_edges =[]
    # for pokemon in pokemon_list:
    #     pokemon_edges.append(edge_geo_mean(pokemon))
    
    # max_edge = max(pokemon_edges)
    # max_edge_index = pokemon_edges.index(max_edge)
    # print(pokemon_list[max_edge_index]['name'])


    # best_party_greedy = greedy_approach()
    # show_party(best_party_greedy)

    # best_party_naive = naive_approach()
    # show_party(best_party_naive)

    best_party_pareto = pareto_combinations_approach()
    show_party(best_party_pareto)

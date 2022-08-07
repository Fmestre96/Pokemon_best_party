import json
from scipy.stats import gmean

#create a function that opens a json file and returns the data
def open_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

#import "pokemons.json" and store it in a variable
pokemon_data = open_json("pokemon_stats.json")
pokemon_types = open_json("pokemon_types.json")



def alpha_dom_beta(alpha, beta):
    alpha_types = [alpha["type1"], alpha["type2"]]
    alpha_types.sort()
    beta_types = [beta["type1"], beta["type2"]]
    beta_types.sort()


    if(alpha_types == beta_types):
        if(alpha["total"] > beta["total"]):
        #if(alpha["total"] > beta["total"] and alpha["hp"] >= beta["hp"] and alpha["attack"] >= beta["attack"] and alpha["defense"] >= beta["defense"] and alpha["special_attack"] >= beta["special_attack"] and alpha["special_defense"] >= beta["special_defense"] and alpha["speed"] >= beta["speed"]):
            print(beta["name"] + " is dominated by " + alpha["name"])
            return True
    return False

def is_pareto_dominated(poke_checked, pokemon_list):
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
        attack_factor11 = 1
    try:
        attack_factor12 = pokemon_types[alpha_type1][beta_type2]
    except:
        attack_factor12 = 1
    try:
        attack_factor21 = pokemon_types[alpha_type2][beta_type1]
    except:
        attack_factor21 = 1
    try:
        attack_factor22 = pokemon_types[alpha_type2][beta_type2]
    except:
        attack_factor22 = 1

    # attack_factor11 = (pokemon_types.get(alpha_type1) or {}).get(beta_type1) or 1
    # attack_factor12 = (pokemon_types.get(alpha_type1) or {}).get(beta_type2) or 1
    # attack_factor21 = (pokemon_types.get(alpha_type2) or {}).get(beta_type1) or 1
    # attack_factor22 = (pokemon_types.get(alpha_type2) or {}).get(beta_type2) or 1

    # print(attack_factor11)
    # print(attack_factor12)
    # print(attack_factor21)
    # print(attack_factor22)

    return max(0.25, attack_factor11*attack_factor12, attack_factor21*attack_factor22)

def defense_advantage(alpha, beta):
    return attack_advantage(beta, alpha)

def edge(alpha, beta):
    attack = attack_advantage(alpha, beta)
    defense = defense_advantage(alpha, beta)
    # print("{} attack advantage".format(attack))
    # print("{} defense advantage".format(defense))
    return attack / defense


def show_dominators():
    dominators = []
    dominateds = []
    for pokemon in pokemon_data:
        dominators.append(pokemon)
        is_dominated = is_pareto_dominated(pokemon, pokemon_data)
        if(is_dominated):
            dominateds.append(pokemon)
            dominators.remove(pokemon)

    print("{} pokemon are dominated".format(len(dominateds)))
    print("{} pokemon are dominators".format(len(dominators)))



def attack_geo_mean(pokemon_check, pokemon_list):
    all_attacks = []
    for pokemon in pokemon_list:
        attack = attack_advantage(pokemon_check, pokemon)
        #print(attack)
        all_attacks.append(attack)

    return gmean(all_attacks)

def defense_geo_mean(pokemon_check, pokemon_list):
    all_defenses = []
    for pokemon in pokemon_list:
        defense = defense_advantage(pokemon_check, pokemon)
        #print(defense)
        all_defenses.append(defense)

    return gmean(all_defenses)
    

def edge_geo_mean(pokemon_check, pokemon_list):
    all_edges = []
    for pokemon in pokemon_list:
        poke_edge = edge(pokemon_check, pokemon)
        #print(edge)
        all_edges.append(poke_edge)

    return gmean(all_edges)



#main function
if __name__ == "__main__":
    #show_dominators()
    #print(attack_advantage(pokemon_data[0], pokemon_data[3]))
    print(attack_geo_mean(pokemon_data[129], pokemon_data)) 
    print(defense_geo_mean(pokemon_data[129], pokemon_data))
    print(edge_geo_mean(pokemon_data[129], pokemon_data))

    


# for pokemon in dominators:
#     print(pokemon["name"])

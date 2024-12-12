"""
Inizializza la rete definendo i nodi e i collegamenti.
Mappa la rete come un dizionario, dove le chiavi sono i nodi
e i valori sono dizionari che rappresentano i vicini e i costi dei collegamenti.
"""
def initialize_network():
    network = {
        "A": {"C": 4, "B": 2},
        "B": {"A": 2, "C": 7, "E": 1},
        "C": {"B": 7, "A": 4},
        "D": {"E": 4},
        "E": {"B": 1, "D": 4},
    }
    return network

"""
Inizializza le tabelle di routing per tutti i nodi della rete.
Questo consiste nell'impostare la distanza da sé stesso a 0 e
aggiungire i vari vicini con le proprie distanze.
Le informazioni sui vicini e le rispettive distanze vengono prese
dalla network. 
"""
def initialize_routing_tables(network):
    routing_tables = {}

    for node in network:
        # ogni nodo conosce sé stesso con distanza 0
        routing_tables[node] = {node: (0, node)}

        for neighbor, cost in network[node].items():
            # inizializza i vicini diretti con i rispettivi costi
            routing_tables[node][neighbor] = (cost, neighbor)

    return routing_tables

"""
Aggiorna la tabella di routing di un nodo utilizzando le tabelle dei vicini.
Questo viene fatto attraverso l'algoritmo di Bellman-Ford che confronta
i percorsi attuali con quelli che passano attraverso i vicini. In caso
venga trovato un percos più corto la tabella di routing viene aggiornata.
"""
def bellman_ford(node, neighbors, routing_tables):
    updated = False

    for neighbor, cost_to_neighbor in neighbors.items():
        # tabella di routing del vicino
        neighbor_table = routing_tables[neighbor]

        for destination, (neighbor_distance, neighbor_to_cross) in neighbor_table.items():
            # calcola la distanza passando attraverso il vicino
            new_distance = cost_to_neighbor + neighbor_distance

            if (destination not in routing_tables[node] or new_distance < routing_tables[node][destination][0]):
                # mostra il cambiamento di distanza
                old_value = routing_tables[node].get(destination, (float('inf'), None))
                print(f"Updating {node} -> {destination}: {old_value[0]} -> {new_distance}")
                routing_tables[node][destination] = (new_distance, neighbor)

                # indica che è avvenuto un aggiornamento
                updated = True

    return updated

"""
Stampa le tabelle di routing di tutti i nodi.
Vengono evidenziate le varie distanze e i prossimi salti.
"""
def print_routing_tables(routing_tables):
    print("\nRouting Tables:")

    for node, table in routing_tables.items():
        print(f"Node {node}:")

        for destination, (distance, next_hop) in table.items():
            print(f"  {destination}: {distance} via {next_hop}")

        print()

"""
Simula il protocollo di routing basato sull'algoritmo di Bellman-Ford.
Si occupa di inizializzare le tabelle di routing di ogni nodo e aggiorna
le tabelle fino alla convergenza dell'algoritmo.
Ad ogni aggiornamento visualizza i percorsi modificati.
"""
def main(network):
    routing_tables = initialize_routing_tables(network)

    print("Initial Routing Tables:")
    print_routing_tables(routing_tables)

    # tiene traccia se avviene un cambiamento
    updated = True  
    iteration = 0

    while updated:
        print(f"\nIteration {iteration + 1}:")
        updated = False

        for node, neighbors in network.items():

            if bellman_ford(node, neighbors, routing_tables):
                # convergenza non ancora raggiunta se è stato verficato un cambiamento
                updated = True

        print_routing_tables(routing_tables) 
        iteration += 1

    # mostra le tabelle finali
    print("\nFinal Routing Tables:")
    print_routing_tables(routing_tables)
    print(f"Convergence after {iteration} iterations")


# configurazione della rete
network = initialize_network()

main(network)

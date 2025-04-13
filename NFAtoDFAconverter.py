import pandas as pd
from itertools import chain, combinations
import graphviz

def visualizeNFA(nfa, nfaFinalStates, filename='nfa'):
    dot = graphviz.Digraph('NFA', comment='NFA Visualization')
    dot.attr(rankdir='LR')
    
    # add states
    for state in nfa:
        if state in nfaFinalStates:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')
    
    # add transitions
    for state in nfa:
        for symbol, nextStates in nfa[state].items():
            for nextState in nextStates:
                dot.edge(state, nextState, label=symbol)
    
    # save and render
    dot.render(filename, format='png', cleanup=True)
    print(f"\nNFA visualization saved as {filename}.png")

def visualizeDFA(dfa, dfaStartState, dfaFinalStates, inputSymbols, filename='dfa'):
    dot = graphviz.Digraph('DFA', comment='DFA Visualization')
    dot.attr(rankdir='LR')
    
    # add states
    for state in dfa:
        state_name = '∅' if not state else ','.join(sorted(state))
        if state == dfaStartState:
            dot.node(state_name, shape='circle', style='bold')
        elif state in dfaFinalStates:
            dot.node(state_name, shape='doublecircle')
        else:
            dot.node(state_name, shape='circle')
    
    # add transitions
    for state in dfa:
        state_name = '∅' if not state else ','.join(sorted(state))
        for symbol in inputSymbols:
            nextState = dfa[state][symbol]
            nextState_name = '∅' if not nextState else ','.join(sorted(nextState))
            dot.edge(state_name, nextState_name, label=symbol)
    
    # save and render
    dot.render(filename, format='png', cleanup=True)
    print(f"\nDFA visualization saved as {filename}.png")

def computeEpsilonClosure(nfa, states):
    closure = set(states)
    stack = list(states)
    
    while stack:
        currentState = stack.pop()

        # check if current state has epsilon transitions
        if currentState in nfa and "ε" in nfa[currentState]:
            for nextState in nfa[currentState]["ε"]:
                if nextState not in closure:
                    closure.add(nextState)
                    stack.append(nextState)
    
    return closure

def computeTransition(nfa, states, symbol):
    # first get the epsilon closure of the input states
    startStates = computeEpsilonClosure(nfa, states)
    
    # find all states reachable on the given symbol
    reachableStates = set()
    for state in startStates:
        if state in nfa and symbol in nfa[state]:
            reachableStates.update(nfa[state][symbol])
    
    # return the epsilon closure of the reachableStates
    return computeEpsilonClosure(nfa, reachableStates)

def powerset(iterable):
    # generate alll possibles subsets
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def createDFA(nfa, inputSymbols, nfaFinalStates):
    # create DFA using powerset method "subset construction"
    # get all NFA states
    nfaStates = list(nfa.keys())
    
    # initialize DFA
    dfa = {}
    dfaFinalStates = set()
    
    # get the start state of DFA (epsilon closure of NFA start state)
    dfaStartState = frozenset(computeEpsilonClosure(nfa, {nfaStates[0]}))
    
    # initialize queue for processing DFA states
    queue = [dfaStartState]
    processed = set()
    
    # add dead state (empty set)
    deadState = frozenset()
    dfa[deadState] = {}
    for symbol in inputSymbols:
        dfa[deadState][symbol] = deadState
    
    while queue:
        currentState = queue.pop(0)
        if currentState in processed:
            continue
            
        processed.add(currentState)
        dfa[currentState] = {}
        
        # check if this DFA state contains any NFA final states
        if any(state in nfaFinalStates for state in currentState):
            dfaFinalStates.add(currentState)
        
        # compute transitions for each input symbol
        for symbol in inputSymbols:
            nextState = frozenset(computeTransition(nfa, currentState, symbol))
            dfa[currentState][symbol] = nextState
            
            if nextState not in processed and nextState not in queue and nextState != deadState:
                queue.append(nextState)
    
    return dfa, dfaFinalStates, dfaStartState

# step 1: NFA Input/Parsing
nfa = {}
inputSymbols = set()  # track all input symbols except epsilon

n = int(input("No. of states: "))  
t = int(input("No. of transitions: "))  

for i in range(n):
    state = input("State name: ").strip()  
    nfa[state] = {}  
    
    for j in range(t):
        path = input("Input symbol (e.g., a, b, ε): ").strip().lower()  
        if path in ["ε", "e", "eps", "epsilon"]:  
            path = "ε"
        else:
            inputSymbols.add(path)
        
        reachingStates = input(f"Enter end state(s) from state {state} on input {path} (space-separated, or '∅' if none): ").split()  
        
        if reachingStates == ["∅"]:  
            reachingStates = []
        
        nfa[state].setdefault(path, []).extend(reachingStates)  

print("\nNFA Representation:\n", nfa)

nfaFinalStates = input("Enter final state(s) of NFA (space-separated): ").split()

# visualize NFA
visualizeNFA(nfa, nfaFinalStates)

# step 2: Epsilon and Transition Computation
print("\nEpsilon Closures:")
for state in nfa:
    closure = computeEpsilonClosure(nfa, {state})
    print(f"ε-closure({state}) = {sorted(closure)}")

print("\nTransitions (including ε-closure):")
for state in nfa:
    print(f"\nFrom state {state}:")
    for symbol in sorted(inputSymbols):
        transition = computeTransition(nfa, {state}, symbol)
        print(f"  On input {symbol}: {sorted(transition)}")

# step 3: Subset Construction Algorithm "DFA creation"
print("\nCreating DFA using subset construction!!")
dfa, dfaFinalStates, dfaStartState = createDFA(nfa, inputSymbols, nfaFinalStates)

print("\nDFA States:")
for state in dfa:
    print(f"State: {'∅' if not state else sorted(state)}")

print("\nDFA Transitions:")
for state in dfa:
    print(f"\nFrom state {'∅' if not state else sorted(state)}:")
    for symbol in sorted(inputSymbols):
        nextState = dfa[state][symbol]
        print(f"  On input {symbol}: {'∅' if not nextState else sorted(nextState)}")

print("\nDFA Start State:", sorted(dfaStartState))
print("DFA Final States:")
for state in dfaFinalStates:
    print(f"  {sorted(state)}")

# visualize DFA
visualizeDFA(dfa, dfaStartState, dfaFinalStates, inputSymbols)

# step 4: DFA Representation (Transition Table)
dfaTable = []
sortedInputSymbols = sorted(inputSymbols)

for state in dfa:
    row = {
        "State": "∅" if not state else ','.join(sorted(state)),
        "Is Start": "Yes" if state == dfaStartState else "",
        "Is Final": "Yes" if state in dfaFinalStates else "",
        "Is Dead": "Yes" if not state else ""
    }
    for symbol in sortedInputSymbols:
        nextState = dfa[state][symbol]
        row[symbol] = "∅" if not nextState else ','.join(sorted(nextState))
    dfaTable.append(row)

df = pd.DataFrame(dfaTable)
df = df.set_index("State")
print("\n--- DFA Transition Table ---\n")
print(df.to_string())

# save DFA representation to file
with open('DFArepresentation.txt', 'w') as f:
    f.write("--- DFA Transition Table ---\n\n")
    f.write(df.to_string())
    f.write("\n\nDFA States:\n")
    for state in dfa:
        f.write(f"State: {'∅' if not state else sorted(state)}\n")
    f.write("\nDFA Transitions:\n")
    for state in dfa:
        f.write(f"\nFrom state {'∅' if not state else sorted(state)}:\n")
        for symbol in sorted(inputSymbols):
            nextState = dfa[state][symbol]
            f.write(f"  On input {symbol}: {'∅' if not nextState else sorted(nextState)}\n")
    f.write(f"\nDFA Start State: {sorted(dfaStartState)}\n")
    f.write("DFA Final States:\n")
    for state in dfaFinalStates:
        f.write(f"  {sorted(state)}\n")
    f.write("\nDead State: ∅\n")

print("\nDFA representation has been saved to 'DFArepresentation.txt'")
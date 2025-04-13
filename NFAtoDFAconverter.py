import pandas as pd

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
        
        print(f"Enter end state(s) from state {state} on input {path} (space-separated, or '∅' if none): ")
        reaching_states = input().split()  
        
        if reaching_states == ["∅"]:  
            reaching_states = []
        
        nfa[state].setdefault(path, []).extend(reaching_states)  

print("\nNFA Representation:\n", nfa)

print("\nNFA Transition Table:")
nfaTable = pd.DataFrame(nfa).fillna('∅')  
print(nfaTable.transpose())

print("\nEnter final state(s) of NFA (space-separated): ")
nfaFinalStates = input().split()

print("\nFinal states of the NFA:", nfaFinalStates)

# compute and display epsilon closures for all states
print("\nEpsilon Closures:")
for state in nfa:
    closure = computeEpsilonClosure(nfa, {state})
    print(f"ε-closure({state}) = {sorted(closure)}")

# compute and display transitions for all states on all input symbols
print("\nTransitions (including ε-closure):")

for state in nfa:
    print(f"\nFrom state {state}:")
    
    for symbol in sorted(inputSymbols):
        transition = computeTransition(nfa, {state}, symbol)
        print(f"  On input {symbol}: {sorted(transition)}")

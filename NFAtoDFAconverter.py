import pandas as pd

def computeEpsilonClosure(nfa, states):
    closure = set(states)
    stack = list(states)
    
    while stack:
        current_state = stack.pop()

        # check if current state has epsilon transitions
        if current_state in nfa and "ε" in nfa[current_state]:
            for next_state in nfa[current_state]["ε"]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    
    return closure

nfa = {}

n = int(input("No. of states: "))  
t = int(input("No. of transitions: "))  

for i in range(n):
    state = input("State name: ").strip()  
    nfa[state] = {}  
    
    for j in range(t):
        path = input("Input symbol (e.g., a, b, ε): ").strip().lower()  
        if path in ["ε", "e", "eps", "epsilon"]:  
            path = "ε"
        
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

# Compute and display epsilon closures for all states
print("\nEpsilon Closures:")
for state in nfa:
    closure = computeEpsilonClosure(nfa, {state})
    print(f"ε-closure({state}) = {sorted(closure)}")

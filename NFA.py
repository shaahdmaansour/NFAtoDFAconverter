import pandas as pd

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
nfa_table = pd.DataFrame(nfa).fillna('∅')  
print(nfa_table.transpose())

print("\nEnter final state(s) of NFA (space-separated): ")
nfa_final_states = input().split()

print("\nFinal states of the NFA:", nfa_final_states)

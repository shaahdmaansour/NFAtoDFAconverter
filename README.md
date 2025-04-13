# NFA to DFA Converter

## 📌 Overview

This project implements a **Non-deterministic Finite Automaton (NFA)** to **Deterministic Finite Automaton (DFA)** Converter. Given an **NFA** as input, the program constructs an equivalent **DFA** by following the **subset construction (powerset)** algorithm.

## ⚙️ How It Works

1. **Reads the NFA input** from a text file or user input.
2. **Applies the subset construction algorithm** to generate an **equivalent DFA**.
3. **Minimizes** the DFA. (extra)
4. **Outputs the DFA** in a structured format.
5. **Visualizes** the DFA.

## 🛠 Features

- Converts any given NFA to an equivalent DFA.
- Supports ε (epsilon) transitions in the input.
- Minimizes the DFA for optimized state reduction.
- Accepts multiple input formats (text, JSON, CSV). (extra)
- Visualizes both the NFA and DFA using Graphviz.
- Command-line interface for easy interaction.

## 🚀 How to Run the Project [editable]

1. **clone this repository**
```sh
git clone git@github.com:shaahdmaansour/NFAtoDFAconverter.git
```

2. **Install dependencies (if applicable)**
```sh
pip install -r requirements.txt
```

3. **Run the program**
```sh
python NFAtoDFAconverter.py
```

## 📷 Sample Output

- ![image](https://github.com/user-attachments/assets/63376597-6e0d-478d-b0f2-07f8599d7692)


## 🤝 Contributers

- [**Shahd El-Kazzaz**](https://github.com/shaahdmaansour)  
- [**Omar Bassam**](https://github.com/OmarBassamTawfik)
- [**Radwa Ahmed**](https://github.com/RadwaAhmed1)
- [**Mariam Abdulbary**](https://github.com/mariiamalaa)
- [**Moslim Eldawi**](https://github.com/eldawi)

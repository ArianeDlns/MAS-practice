# Argument-Based Negociation Interaction

Imagine that a car manufacturer wants to launch a new car on the market. For this, a crucial choice is the one of the engines that should meet some technical requirements but at the same time be attractive for the customers (economic, robust, ecological, etc.). Several types of engines exist and thus provide a large offer of cars models: essence or diesel Internal Combustion Engine (ICE), Compressed Natural GAS (CNG), Electric Battery (EB), Fuel Cell (FC), etc. The company decides to take into account different criteria to evaluate them: Consumption, environmental impact (CO2, clean fuel, NOX1...), cost, durability, weight, targeted maximum speed, etc. To establish the best offer/choice among a large set of options, they decide to simulate a negotiation process where agents, with different opinions and preferences (even different knowledge and expertise), discuss the issue to end up with the best offer. The simulation will allow the company to simulate several typologies of agent behaviors (expertise, role, preferences, . . . ) at a lower cost within a reasonable time.  
The practical sessions in this Multi-Agent System Course will be devoted to the programming of a negotiation & argumentation simulation. Agents representing human engineering will need to negotiate with each other to make a joint decision regarding choosing the best engine. The negotiation comes when the agents have different preferences on the criteria, and the argumentation will help them decide which item to select. Moreover, the arguments supporting the best choice will help build the justification supporting it, an essential element for the company to develop its marketing campaign.

Les agents ont la même liste de critères et la même liste d'items. 

### Running the code 

Running `pw_argumentation.py` 
```
cd mesa_preference/mesa/
python3 pw_argumentation.py 
```

To run tests 
```
python3 -m communication.preferences.Preferences
```

### 


<p align="center"> <img src="https://github.com/ArianeDlns/MAS-practive/blob/main/Proj2_ABNI/img/argumentation.png" width="700" alt="argumentation"/> 

### Consignes: 

Nous attendons de vous que vous rédigiez un petit rapport (5 pages max) sur votre modèle de négociation (surtout si vous avez opté pour des choix différents que ceux mentionnés dans le cours/TP). Mettez quelques  captures d'écran des sorties de votre implémentation. Calculez quelques statistiques sur les résultats  en fonction des paramètres de simulation (nombre d'agents, nombre d'items, ...). Vous devez clairement identifier les paramètres et les valeurs observées.

Préparez un zip de votre code. La qualité du code (modularité, propreté, commentaires...) sera prise en compte.

### Date limite
:calendar: 15 avril 2022 

## To do list
- [x] read .csv
# Argument-Based Negociation Interaction

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![Open in Visual Studio Code](https://img.shields.io/badge/Editor-VSCode-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://github.dev/ArianeDlns/MAS-practice/tree/master/Proj2_ABNI) [![GitHub commit](https://badgen.net/github/last-commit/ArianeDlns/MAS-practice/master)](https://GitHub.com/ArianeDlns/MAS-practice/commits/master) [![Report](https://img.shields.io/badge/Report-1.2-green?style=square&logo=overleaf&logoColor=white)](https://fr.overleaf.com/read/zcjpxdzwdbnk)

## Problème 

Imaginons qu'un constructeur automobile veuille lancer une nouvelle voiture sur le marché. Pour cela, un choix crucial est celui du moteur qui doit répondre à certaines exigences techniques tout en étant attractif pour les clients (économique, robuste, écologique, etc.). Plusieurs types de moteurs existent et fournissent ainsi une large offre de modèles de voitures : moteur à combustion interne (ICE) essence ou diesel, gaz naturel comprimé (GNC), batterie électrique (EB), pile à combustible (FC), etc. L'entreprise décide de prendre en compte différents critères pour les évaluer : Consommation, impact environnemental (CO2, carburant propre, NOX1...), coût, durabilité, poids, vitesse maximale visée, etc. Pour établir la meilleure offre/le meilleur choix parmi un large ensemble d'options, ils décident de simuler un processus de négociation où des agents, avec des opinions et des préférences différentes (voire des connaissances et une expertise différentes), discutent du problème pour aboutir à la meilleure offre. La simulation permettra à l'entreprise de simuler plusieurs typologies de comportements d'agents (expertise, rôle, préférences, . . .) à moindre coût et dans un délai raisonnable.  
Les sessions pratiques de ce cours sur les systèmes multi-agents seront consacrées à la programmation d'une simulation de négociation et d'argumentation. Les agents représentant le génie humain devront négocier entre eux pour prendre une décision commune concernant le choix du meilleur moteur. La négociation intervient lorsque les agents ont des préférences différentes sur les critères, et l'argumentation les aidera à décider quel élément choisir. De plus, les arguments soutenant le meilleur choix aideront à construire la justification de celui-ci, un élément essentiel pour que l'entreprise puisse développer sa campagne de marketing.

Les agents ont la même liste de critères et la même liste d'items. 

## Consignes

Nous attendons de vous que vous rédigiez un petit rapport (5 pages max) sur votre modèle de négociation (surtout si vous avez opté pour des choix différents que ceux mentionnés dans le cours/TP). Mettez quelques  captures d'écran des sorties de votre implémentation. Calculez quelques statistiques sur les résultats  en fonction des paramètres de simulation (nombre d'agents, nombre d'items, ...). Vous devez clairement identifier les paramètres et les valeurs observées.

Préparez un zip de votre code. La qualité du code (modularité, propreté, commentaires...) sera prise en compte.

## Running the code 

running `pw_argumentation.py` 
``` bash
cd mesa_preference/mesa/ # change directory to the mesa folder
pip install -r requirements.txt # install all the requirements
python3 pw_argumentation.py # run the code
```

run tests 
``` bash
python3 -m communication.preferences.Preferences # run the tests
```

## Résultats 

### Résumé des résultats
<p align="center"> <img src="https://github.com/ArianeDlns/MAS-practice/blob/master/Proj2_ABNI/img/argumentation_CSV.png" width="700" alt="argumentation"/> 

Nous voyons ici les résultats pour le cas d'une argumentation à deux agents avec deux items. Les préférences sont celles issues du [preferences.csv](https://github.com/ArianeDlns/MAS-practice/blob/master/Proj2_ABNI/mesa_preference/mesa/preferences.csv) qui correspond au sujet du projet. On voit ainsi que chacun des agents parle à son tour et propose ou argumente sur les critères.

<p align="center"> <img src="https://github.com/ArianeDlns/MAS-practice/blob/master/Proj2_ABNI/img/argumentation_3_items.png" width="700" alt="argumentation"/> 

Nous avons ensuite étendu notre étude à trois items. On voit ainsi que les agents ont maintenant trois choix différents pour argumenter. Leur préférences ont été générées aléatoirement.

## Choix techniques
### Algorithme de négociation
<p align="center"> <img src="https://github.com/ArianeDlns/MAS-practice/blob/master/Proj2_ABNI/img/algorithm.png" width="700" alt="algorithm"/> 

### Paramètres du système et choix des agents
- Nous avons délibérément choisi de limiter notre étude à deux agents, tout en rendant notre code modulable pour en implémenter plus, dans tous les cas un argumentation ne peut se faire qu'en présence de deux agents qui argumentent l'un avec l'autre. 
- Pour éviter de retomber sur les mêmes arguments/items, une fois discutés ceux-ci sont retirés de la boucle de négociation.

### Structure 

```bash
.
├── MAS_Course6.pdf # Course materials
├── PW4_engine.pdf # Course materials
├── README.md
├── img
│   ├── argumentation_3_items.png
│   └── argumentation_CSV.png
└── mesa_preference
    └── mesa
        ├── communication
        │   ├── __init__.py
        │   ├── agent
        │   │   ├── CommunicatingAgent.py
        │   │   └── __init__.py
        │   ├── arguments
        │   │   ├── Argument.py
        │   │   ├── Comparison.py
        │   │   ├── CoupleValue.py
        │   │   └── __init__.py
        │   ├── mailbox
        │   │   ├── Mailbox.py
        │   │   └── __init__.py
        │   ├── message
        │   │   ├── Message.py
        │   │   ├── MessagePerformative.py
        │   │   ├── MessageService.py
        │   │   └── __init__.py
        │   ├── preferences
        │   │   ├── CriterionName.py
        │   │   ├── CriterionValue.py
        │   │   ├── Item.py
        │   │   ├── Preferences.py # preferences script
        │   │   ├── Value.py
        │   │   └── __init__.py
        │   ├── requirements.txt
        │   └── runtests.py
        ├── preferences.csv # file with the preferences
        ├── preferences_project.csv # (optional) file with the preferences for the project
        ├── pw_argumentation.py # main script
        ├── requirements.txt # requirements
        └── runtests.py # (optional) run tests
```

Le coeur du code implémenté se trouve dans: 
- **pw_argumentation.py** : le script principal avec la classe ``ArgumentAgent``
- **Preferences.py** : le script qui génère les préférences des agents

Quelques autres modifications ont pu être faites à d'autres endroits du code comme pour coloriser les actions ou rajouter de représentation sous forme de chaîne de caractères afin d'améliorer la lisibilité des outputs.

### Pour aller plus loin ...
Nous avons pensé à quelques amélioration concernant ce projet: 
- l'implémentation de plusieurs agents négociant en parallèle 
- la possibilité de faire des tests sur des préférences différentes
- une complexification du système d'argumentation afin de pouvoir renégocier d'anciens items ou d'anciennes préférences
- la possibilité d'avoir des ordre de préférence différents pour chaque agent

### Date limite
:calendar: 15 avril 2022 

## To do list
- [x] read .csv
- [x] explain algorithm implemented
- [x] color les agents/items/propositions

## References:
[Kazil et al.(2020)] Jackie Kazil, David Masad, and Andrew Crooks. Utilizing python for agent-based mo-
deling : The mesa framework. In Robert Thomson, Halil Bisgin, Christopher Dancy, Ayaz Hyder, and
Muhammad Hussain, editors, Social, Cultural, and Behavioral Modeling, pages 308–317, Cham, 2020.
Springer International Publishing  

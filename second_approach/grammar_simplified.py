# CFG = {
#     "S": [["NP", "VP"]],
#     "NP": [["Det", "N"], ["Pron"], ["Det", "Adj", "N"]],
#     "VP": [["V", "Adv"], ["V", "NP"], ["V", "NP", "PP"]],
#     "PP": [["Prep", "NP"]]
# }

CFG = {
    "S": [["NP", "VP"]],
    "NP": [["Det", "N"], ["Pron"]],
    "VP": [["V", "Adv"], ["V", "NP"]],
    "PP": [["Prep", "NP"]]
}

adj = {
    "00": "nieuwe",
    "01": "oude",
    "10": "grote",
    "11": "mooie",
}

n = {
    "00": "kerk",
    "01": "bibliotheek",
    "10": "school",
    "11": "bioscoop"
}

v = {
    "00": "loopt",
    "01": "sluipt",
    "10": "rent",
    "11": "springt"
}

adv = {
    "00": "snel",
    "01": "dichtbij",
    "10": "vaak",
    "11": "graag"
}

pron = {
    "00": "hij",
    "01": "zij",
    "10": "Jan",
    "11": "Emma"
}

det = {
    "00": "de",
    "01": "een",
    "10": "de",
    "11": "een"
}

prep = {
    "00": "naar",
    "01": "naast",
    "10": "op",
    "11": "in"
}

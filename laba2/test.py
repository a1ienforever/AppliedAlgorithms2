transitions = {
    ("q0", "0"): {"q1"},
    ("q1", "1"): {"q2"},
    ("q2", "1"): {"q3"},
    ("q3", "0"): {"q4"},
    ("q3", "1"): {"q5"},
    ("q4", "e"): {"q6"},
    ("q5", "e"): {"q7"},
    ("q6", "0"): {"q3"},
    ("q7", "1"): {"q6"},
}
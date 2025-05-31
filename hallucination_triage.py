import re

# List of common hallucinations
HALLUCINATION_KEYWORDS = [
    "i don’t know",
    "as an ai language model",
    "cannot provide",
    "unable to",
    "no information",
    "not sure",
    "sorry",
    "error",
    "gibberish",
    "???"
]

def detect_hallucination(text):
    if not text or len(text.strip()) < 10:
        return True, "Output too short or empty"

    lowered = text.lower()

    for i in HALLUCINATION_KEYWORDS:
        if i in lowered:
            return True, f"Contains hallucination phrase: '{i}'"

    return False, ""

if __name__ == "__main__":
    samples = [
        "I don’t know the answer to that.",
        "This is a perfect valid answer with no issues.",
        "",
        "!!!@@@###$$$",
        "Sorry, I cannot provide that information."
    ]

    for s in samples:
        flag, reason = detect_hallucination(s)
        print(f"Text: {s}\nHallucination? {flag}, Reason: {reason}\n")

#!/usr/bin/env python3
"""
One-time content migration: convert freestanding bold-markdown callouts
(`**NOTE**: ...`, `**Hint**: ...`, `**Recall**: ...` with no surrounding
markup) into the same `<div class="alert alert-block alert-*">` boxes used
everywhere else in the course, so they get the colored-box CSS restored in
_static/custom.css. These were never boxed, even pre-migration - this is a
deliberate content change, not a v1->v2 regression fix.

Each entry is (path, cell_index, old, new): `old` must appear exactly once
in that cell's joined source; the script fails loudly if not, rather than
silently skipping or matching the wrong spot.
"""
import json

LABEL_CLASS = {
    "NOTE": "info",
    "RECALL": "info",
    "HINT": "success",
}


def box(label, body):
    cls = LABEL_CLASS[label]
    return f'<div class="alert alert-block alert-{cls}">\n<b>{label}</b>: {body}\n</div>'


REPLACEMENTS = [
    ("src/C00/C00-Bits-and-Bytes.ipynb", 4,
     "**NOTE**: The subscript 10 indicates that the number is in base 10.",
     box("NOTE", "The subscript 10 indicates that the number is in base 10.")),

    ("src/C02/C02-Hardware.ipynb", 2,
     "**NOTE**: A resistor should be added in series with the LED to limit the current and prevent damage.",
     box("NOTE", "A resistor should be added in series with the LED to limit the current and prevent damage.")),

    ("src/C02/C02-Hardware.ipynb", 3,
     "**NOTE**: There exist other types of transistors, which can be used to implement an AND gate.\n",
     box("NOTE", "There exist other types of transistors, which can be used to implement an AND gate.") + "\n"),

    ("src/C02/C02-Hardware.ipynb", 6,
     "**NOTE**: A resistor should be added in series with the LED to limit the current and prevent damage.",
     box("NOTE", "A resistor should be added in series with the LED to limit the current and prevent damage.")),

    ("src/C02/C02-Hardware.ipynb", 7,
     "**NOTE**: There exist other types of transistors, which can be used to implement an OR gate.\n",
     box("NOTE", "There exist other types of transistors, which can be used to implement an OR gate.") + "\n"),

    ("src/C02/C02-Hardware.ipynb", 11,
     "**NOTE**: We discovered that our output does not depend on the value of A! ",
     box("NOTE", "We discovered that our output does not depend on the value of A!")),

    ("src/C02/C02-Hardware.ipynb", 13,
     "**NOTE**: In this case, the formula was already minimal. In general, the tool will first perform a minimization of the formula, and then generate the circuit. The smaller the formula, the smaller the circuit; fewer gates, less area, less power, lower cost. ",
     box("NOTE", "In this case, the formula was already minimal. In general, the tool will first perform a minimization of the formula, and then generate the circuit. The smaller the formula, the smaller the circuit; fewer gates, less area, less power, lower cost.")),

    ("src/C02/C02-Hardware.ipynb", 28,
     "**NOTE**: someone has actually done it: see [here](https://www.youtube.com/watch?v=g_ZaioqF1B0&ab_channel=PauloConstantino) and [here](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU&ab_channel=BenEater).",
     box("NOTE", "someone has actually done it: see [here](https://www.youtube.com/watch?v=g_ZaioqF1B0&ab_channel=PauloConstantino) and [here](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU&ab_channel=BenEater).")),

    ("src/C03/C03-Software.ipynb", 16,
     "**NOTE**: As already pointed out, we cannot write an algorithm in our own natural language (e.g., English). To make an algorithm interpretable by a computer, we need to learn a **programming language**.",
     box("NOTE", "As already pointed out, we cannot write an algorithm in our own natural language (e.g., English). To make an algorithm interpretable by a computer, we need to learn a **programming language**.")),

    ("src/C03/C03-Software.ipynb", 29,
     "**NOTE**: If you have:\n"
     "- $1$ core without preemptive multitasking: up to $1$ applications executing in parallel\n"
     "- $1$ core with preemptive multitasking: illusion of parallel execution of an infinite number of apps\n"
     "- $k$ cores without preemptive multitasking: up to $k$ applications executing in parallel\n"
     "- $k$ cores with preemptive multitasking: illusion of parallel execution of an infinite number of applications, with up to $k$ actually executing in parallel at any given time\n",
     '<div class="alert alert-block alert-info">\n'
     "<b>NOTE</b>: If you have:\n"
     "- $1$ core without preemptive multitasking: up to $1$ applications executing in parallel\n"
     "- $1$ core with preemptive multitasking: illusion of parallel execution of an infinite number of apps\n"
     "- $k$ cores without preemptive multitasking: up to $k$ applications executing in parallel\n"
     "- $k$ cores with preemptive multitasking: illusion of parallel execution of an infinite number of applications, with up to $k$ actually executing in parallel at any given time\n"
     "</div>\n"),

    ("src/C04/C04-OS-Essentials.ipynb", 20,
     "\n**NOTE**: The PATH environment variable is crucial for program accessibility. When software is installed, it must add its directory to PATH; otherwise you can only run the program by typing its absolute path. This is why properly installed programs can be launched from any location in the terminal by simply typing their name.",
     "\n" + box("NOTE", "The PATH environment variable is crucial for program accessibility. When software is installed, it must add its directory to PATH; otherwise you can only run the program by typing its absolute path. This is why properly installed programs can be launched from any location in the terminal by simply typing their name.")),

    ("src/C04/C04-OS-Essentials.ipynb", 33,
     "\n**NOTE**: For users, containers typically means using Docker. Docker runs Linux-based applications, so on macOS and Windows, it requires a lightweight Linux-based VM. On Linux, Docker can run natively without an additional VM layer.",
     "\n" + box("NOTE", "For users, containers typically means using Docker. Docker runs Linux-based applications, so on macOS and Windows, it requires a lightweight Linux-based VM. On Linux, Docker can run natively without an additional VM layer.")),

    ("src/C05/C05-Computer-Network.ipynb", 11,
     "**NOTE**: The OSI model is **theoretical**. In practice, we use the **TCP/IP model**, simpler and more practical.",
     box("NOTE", "The OSI model is **theoretical**. In practice, we use the **TCP/IP model**, simpler and more practical.")),

    ("src/C05/C05-Computer-Network.ipynb", 47,
     "**Note**: This is simplified. In reality, modern web pages require dozens or hundreds of additional requests for resources (images, scripts, stylesheets, fonts, etc.), each following a similar process.",
     box("NOTE", "This is simplified. In reality, modern web pages require dozens or hundreds of additional requests for resources (images, scripts, stylesheets, fonts, etc.), each following a similar process.")),

    ("src/P00/P00-Python-Getting-Started.ipynb", 61,
     "    **NOTE**: The first time you create an environment, conda will ask to accept the terms of agreement **before asking to proceed**",
     '    <div class="alert alert-block alert-info">\n'
     "    <b>NOTE</b>: The first time you create an environment, conda will ask to accept the terms of agreement **before asking to proceed**\n"
     "    </div>"),

    ("src/H04/H04-Python-Recap-IV-{v}.ipynb", 282,
     "**Hint**: Remember that it is possible to use the common operators for comparison (e.g., `<`, `>`, `==`) on `date` objects.\n\n"
     "**Recall**: To use the `datetime` module in your code, please make sure to import it before the `def` of your function.",
     box("HINT", "Remember that it is possible to use the common operators for comparison (e.g., `<`, `>`, `==`) on `date` objects.")
     + "\n\n" +
     box("RECALL", "To use the `datetime` module in your code, please make sure to import it before the `def` of your function.")),
]

# E12: identical content across pseudocode/solution/student
E12_CELLS = {
    3: ("**NOTE**: do not use any buit-in function from Python to solve the exercise",
        box("NOTE", "do not use any buit-in function from Python to solve the exercise")),
    25: ("**NOTE**: The Fibonacci sequence is a series of numbers where each number is the sum of the two previous ones, starting with 0 and 1. To calculate it, you begin with 0 and 1, then add these to get the next number. Continue this process to generate the sequence. It goes 0, 1, 1, 2, 3, 5, 8, and so on.",
         box("NOTE", "The Fibonacci sequence is a series of numbers where each number is the sum of the two previous ones, starting with 0 and 1. To calculate it, you begin with 0 and 1, then add these to get the next number. Continue this process to generate the sequence. It goes 0, 1, 1, 2, 3, 5, 8, and so on.")),
    36: ("**NOTE**: The Collatz Conjecture is a mathematical problem that starts with any positive integer. The process involves two steps: if the number is even, divide it by 2; if it's odd, multiply it by 3 and add 1. Repeat this process with the resulting number. The conjecture suggests that, no matter what number you start with, you'll eventually reach the number 1.",
         box("NOTE", "The Collatz Conjecture is a mathematical problem that starts with any positive integer. The process involves two steps: if the number is even, divide it by 2; if it's odd, multiply it by 3 and add 1. Repeat this process with the resulting number. The conjecture suggests that, no matter what number you start with, you'll eventually reach the number 1.")),
    47: ("**NOTE**: Suppose that there is always only one number missing",
         box("NOTE", "Suppose that there is always only one number missing")),
    69: ("**NOTE**: A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (**ignoring spaces, punctuation, and capitalization**).",
         box("NOTE", "A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (**ignoring spaces, punctuation, and capitalization**).")),
}
for v in ("pseudocode", "solution", "student"):
    for idx, (old, new) in E12_CELLS.items():
        REPLACEMENTS.append((f"src/E12/E12-Python-Exercises-Loops-With-Strings-Lists-{v}.ipynb", idx, old, new))

# H01: identical content across pseudocode/solution/student
H01_CELLS = {
    175: ("**NOTE**:\n- count the word case-insensitive.\n- split `s` by space to obtain the words.",
          '<div class="alert alert-block alert-info">\n<b>NOTE</b>:\n- count the word case-insensitive.\n- split `s` by space to obtain the words.\n</div>'),
    222: ('**NOTE**: \n'
          "- ROT13 is a special case of the Caesar cipher, which is a simple substitution cipher where each letter in the plaintext is shifted a certain number of places down or up the alphabet. In the case of ROT13, the shift is 13 places.\n"
          '- Consider an alphabet of 26 letters: `"abcdefghijklmnopqrstuvwxyz"`\n'
          "- `ord(c)` returns an integer representing `c`.\n"
          "- `chr(x)` returns the character associated with integer `x`.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- ROT13 is a special case of the Caesar cipher, which is a simple substitution cipher where each letter in the plaintext is shifted a certain number of places down or up the alphabet. In the case of ROT13, the shift is 13 places.\n"
          '- Consider an alphabet of 26 letters: `"abcdefghijklmnopqrstuvwxyz"`\n'
          "- `ord(c)` returns an integer representing `c`.\n"
          "- `chr(x)` returns the character associated with integer `x`.\n"
          "</div>"),
    240: ("**NOTE**: The square root can be calculated using `math.sqrt()` from the math library.",
          box("NOTE", "The square root can be calculated using `math.sqrt()` from the math library.")),
    249: ("**NOTE**: The function should track both uppercase and lowercase characters as distinct.\n"
          "**NOTE**: Spaces and punctuation should also be tracked as characters.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- The function should track both uppercase and lowercase characters as distinct.\n"
          "- Spaces and punctuation should also be tracked as characters.\n"
          "</div>"),
    258: ("**NOTE**: The words should be grouped based on their sorted letter order.<br>\n"
          "**NOTE**: If no anagram pairs are found, each word should still appear in its own list.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- The words should be grouped based on their sorted letter order.\n"
          "- If no anagram pairs are found, each word should still appear in its own list.\n"
          "</div>"),
    276: ("**NOTE**: Ignore any non-alphabetic characters when forming the acronym.<br>\n"
          "**NOTE**: The acronym should be in uppercase.<br>\n"
          "**NOTE**: If the input string is empty, return `{'acronym': '', 'phrase': ''}`.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- Ignore any non-alphabetic characters when forming the acronym.\n"
          "- The acronym should be in uppercase.\n"
          "- If the input string is empty, return `{'acronym': '', 'phrase': ''}`.\n"
          "</div>"),
    285: ("**NOTE**: If a movie appears multiple times in the input list, all ratings should be included in the list for that movie.<br>\n"
          "**NOTE**: The order of the ratings in the lists should reflect the order they appear in the input list.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- If a movie appears multiple times in the input list, all ratings should be included in the list for that movie.\n"
          "- The order of the ratings in the lists should reflect the order they appear in the input list.\n"
          "</div>"),
    296: ("**NOTE**: If a contact appears multiple times in the input list, the last occurrence should be kept in the dictionary.<br>\n"
          "**NOTE**: The names in the dictionary should be in lowercase to maintain case insensitivity.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- If a contact appears multiple times in the input list, the last occurrence should be kept in the dictionary.\n"
          "- The names in the dictionary should be in lowercase to maintain case insensitivity.\n"
          "</div>"),
    307: ("**NOTE**:\n"
          "- If a user has multiple connections with the same friend, those should only be counted once.\n"
          '- The function should maintain case insensitivity for usernames (e.g., "Alice" and "alice" should be treated as the same user).\n'
          "- If a user has no friends, their value in the dictionary should be an empty set.",
          '<div class="alert alert-block alert-info">\n'
          "<b>NOTE</b>:\n"
          "- If a user has multiple connections with the same friend, those should only be counted once.\n"
          '- The function should maintain case insensitivity for usernames (e.g., "Alice" and "alice" should be treated as the same user).\n'
          "- If a user has no friends, their value in the dictionary should be an empty set.\n"
          "</div>"),
}
for v in ("pseudocode", "solution", "student"):
    for idx, (old, new) in H01_CELLS.items():
        REPLACEMENTS.append((f"src/H01/H01-Python-Recap-{v}.ipynb", idx, old, new))

# expand the H04 {v} template entry added above into 3 concrete file replacements
_expanded = []
for path, idx, old, new in REPLACEMENTS:
    if "{v}" in path:
        for v in ("pseudocode", "solution", "student"):
            _expanded.append((path.format(v=v), idx, old, new))
    else:
        _expanded.append((path, idx, old, new))
REPLACEMENTS = _expanded


def main():
    by_path = {}
    for path, idx, old, new in REPLACEMENTS:
        by_path.setdefault(path, []).append((idx, old, new))

    for path, edits in by_path.items():
        with open(path) as f:
            nb = json.load(f)
        for idx, old, new in edits:
            cell = nb["cells"][idx]
            src = "".join(cell["source"])
            if old not in src:
                raise SystemExit(f"NOT FOUND: {path} cell {idx}\n--- expected ---\n{old!r}\n--- actual ---\n{src!r}")
            new_src = src.replace(old, new, 1)
            cell["source"] = new_src.splitlines(keepends=True)
        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
            f.write("\n")
        print(f"Updated {len(edits)} cell(s) in {path}")


if __name__ == "__main__":
    main()

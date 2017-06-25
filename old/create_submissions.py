
import re
import csv

SILLY = [
    "Inspiration",
    "How we built it",
    "Challenges we ran into",
    "What it does",
    "How I built it",
    "Challenges I ran into",
    "Accomplishments that I'm proud of",
    "Accomplishments that we're proud of",
    "What I learned",
    "What we learned",
    ":"
]
SPACE_CHARS = "\n\\/".split()

def proc(description):
    for s in SILLY:
        description = description.replace(s, '')
    for s in SPACE_CHARS:
        description = description.replace(s, ' ')
    description = re.sub('[^A-Za-z ]+', '', description)
    description = re.sub('[ ]+', ' ', description)
    description = description.strip().lower()
    return description

with open('submissions-hackmit-2016.csv', 'r') as f:
    reader = csv.reader(f)

    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        title = proc(row[0])
        description = proc(row[2])
        print("%s %s" % (title, description))


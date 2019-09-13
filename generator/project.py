from model.project import Project
import random
import string
import os.path
import jsonpickle
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of progect", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n=5
f = "data/projects.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a

def random_string(prefix , maxlen):
    simbols = string.ascii_letters + string.digits + " "*4 + string.digits
    return prefix + "".join([random.choice(simbols) for i in range(random.randrange(maxlen))])

testdata = [
    Project(name=random_string("name", 5), description=random_string("description", 5))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent = 2)
    out.write(jsonpickle.encode(testdata))
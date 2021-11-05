from requests import get
from ast import literal_eval

identifer = "abcdef123"

def GlobalAPI():
    url = str('http://localhost:8000/api/results/') + identifer
    results = get(url).json()
    return results

def GoAPI():
    url = str('http://localhost:5000/api/results/') + identifer
    results = get(url).json()
    return results

if __name__ == "__main__":
    python = GlobalAPI()
    golang = GoAPI()

    print("Types as recieved: ")
    print(type(python))
    print(type(golang))

    #python = literal_eval(python) DOES NOT WORK
    golang = literal_eval(golang)
    print("Types after Literal_Eval Applied")
    print(type(python))
    print(type(golang))

    if python == golang:
        print("Both are the same!")
    else:
        print("Python API Results != Golang API Results")
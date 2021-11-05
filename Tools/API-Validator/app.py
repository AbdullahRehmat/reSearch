from requests import get
from ast import literal_eval

identifer = "abcdef123"

def Global_API_Test():
    url = str('http://localhost:8000/api/results/') + identifer
    results = get(url).json()
    return results

def Go_API_Test():
    url = str('http://localhost:5000/api/results/') + identifer
    results = get(url).json()
    return results

if __name__ == "__main__":
    python = Global_API_Test()
    golang = Go_API_Test()

    print("Types as recieved: ")
    print(type(python))
    print(type(golang))

    golang = literal_eval(golang)
    print("Types after Literal_Eval Applied")
    print(type(python))
    print(type(golang))

    if python == golang:
        print("Both are the same!")
    else:
        print("Python API Results != Golang API Results")
from subprocess import check_output
import json
import matplotlib.pyplot as plt
import sys


class Prediction:
    id:int
    value:float
    timestamp:int
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.value = float(row["value"])
        self.timestamp = int(row["timestamp"])

    def __repr__(self) -> str:
        return f'Prediction({self.id} {self.value} {self.timestamp})'

class Question:
    id:int
    question:str
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.question = row["question"]

    def __repr__(self) -> str:
        return f'Question({self.id} {self.question})'

class Answer:
    id:int
    value:float
    rating:float
    question:Question
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.value = float(row["value"])
        self.rating = float(row["rating"])
        self.question = Question(json.loads(check_output([
            "sqlite3",
            sys.argv[-1],
            f"select * from questions where id = '{row['questionId']}'",
            "-json"
        ]).decode())[0])

    def __repr__(self) -> str:
        return f'Answer({self.id} {self.value} {self.rating} {self.question})'

class Journal:
    id:int
    answers:list[Answer] = []
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.answers = [
            Answer(answer) for answer in json.loads(check_output([
                "sqlite3",
                sys.argv[-1],
                f"select * from answers where journalId = '{self.id}'",
                "-json"
            ]).decode())
        ]

    def __repr__(self) -> str:
        return f'Journal({self.id} [{",".join(str(a) for a in self.answers)}])'

class User:
    id:int
    username:str
    password:str
    journals:list[Journal] = []
    predictions:list[Prediction] = []
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.username = row["username"]
        self.password = row["password"]
        self.journals = [
            Journal(journal) for journal in json.loads(check_output([
                "sqlite3",
                sys.argv[-1],
                f"select * from journals where userId = '{self.id}'",
                "-json"
            ]).decode())
        ]
        self.predictions = [
            Prediction(prediction) for prediction in json.loads(check_output([
                "sqlite3",
                sys.argv[-1],
                f"select * from predictions where userId = '{self.id}'",
                "-json"
            ]))
        ]

    def __repr__(self) -> str:
        return f'User({self.id} {self.username} {self.password} [{",".join([str(j) for j in self.journals])}] [{",".join(str(p) for p in self.predictions)}])'



users:list[User] = []

predictions = json.loads(check_output([
    "sqlite3",
    sys.argv[-1],
    "select * from predictions",
    "-json"
]).decode())

for prediction in predictions:
    uid = prediction["userId"]
    if all([user.id != uid for user in users]):
        users.append(User(json.loads(check_output([
            "sqlite3",
            sys.argv[-1],
            f"select * from users where id = '{uid}'",
            "-json"
        ]).decode())[0]))

print(users)

fig, ax = plt.subplots()

for user in users:
    ax.plot([p.value for p in user.predictions], range(len(user.predictions)))
    
    for journal in user.journals:
        ax.plot([a.value for a in journal.answers], range(len(journal.answers)))

plt.show()

from statistics import mean
from subprocess import check_output
import sys
import json
import matplotlib.pyplot as plt

def init_plots():
    plt.rcParams['figure.figsize'] = [10, 4]
    plt.rcParams['font.size'] = 16

def regression(xs:list[float], ys:list[float]):
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = 0.0
    denominator = 0.0
    for x, y in zip (xs, ys):
        numerator += (x-x_mean) * (y-y_mean)
        denominator += pow(x - x_mean, 2)
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    return lambda x: intercept + (slope * x)

def doSQL(sql):
    if "-v" in sys.argv:
        print(sql)
    result = check_output([
        "sqlite3",
        sys.argv[1],
        sql,
        "-json"
    ]).decode()
    if result:
        return json.loads(result)
    else:
        return []
    
class Prediction:
    id:int
    value:float
    timestamp:int
    rating:int = None
    expected:bool = None

    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.value = float(row["value"])
        self.timestamp = int(row["timestamp"])
        ratings = doSQL(f"select rating,expected from ratings where predictionId = {self.id}")
        if ratings:
            self.rating = ratings[0]['rating']
            self.expected = ratings[0]['expected']
        

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
        self.question = Question(doSQL(f"select * from questions where id = '{row['questionId']}'")[0])

    def __repr__(self) -> str:
        return f'Answer({self.id} {self.value} {self.rating} {self.question})'

class Journal:
    id:int
    answers:list[Answer] = []
    timestamp:int
    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.timestamp = int(row['timestamp'])
        self.answers = [
            Answer(answer) for answer in doSQL(f"select * from answers where journalId = '{self.id}'")
        ]

    def __repr__(self) -> str:
        return f'Journal({self.id} [{",".join(str(a) for a in self.answers)}])'

tag_map = {
    "education":{
        1:"Other",
        2:"High School",
        3:"University",
        4:"Graduate"
    },
    "urban":{
        1:"Rural",
        2:"Suburban",
        3:"Urban"
    },
    "gender":{
        1:"Male",
        2:"Female",
        3:"Other"
    },
    "religion":{
        1:"Agnostic",
        2:"Atheist",
        3:"Buddhist",
        4:"Christian",
        5:"Christian",
        6:"Christian",
        7:"Christian",
        8:"Hindu",
        9:"Jewish",
        10:"Muslim",
        11:"Sikh",
        12:""
    },
    "orientation":{
        1:"Heterosexual",
        2:"Bisexual",
        3:"Homosexual",
        4:"Asexual",
        5:""
    },
    "race":{
        10:"Asian",
        20:"Arab",
        30:"Black",
        40:"Indigenous Australian",
        50:"Native American",
        60:"White",
        70:""
    }
}


class Userdata:
    id:int
    education:str
    urban:str
    gender:str
    religion:str
    orientation:str
    race:str
    married:bool
    age:int
    pets:bool
    def __init__(self, row:dict[str, str]):
        get_tag = lambda key: tag_map[key][int(row[key])]
        self.education = get_tag('education')
        self.education_level = int(row['education'])
        self.urban = get_tag('urban')
        self.gender = get_tag('gender')
        self.religion = get_tag('religion')
        self.orientation = get_tag('orientation')
        self.race = get_tag('race')
        self.married = row['married'] == '1'
        self.age = int(row['age'])
        self.pets = row['pets'] == '1'


class User:
    id:int
    username:str
    password:str
    journals:list[Journal] = []
    predictions:list[Prediction] = []
    userdata:Userdata

    def __init__(self, row:dict[str, str]):
        self.id = int(row["id"])
        self.username = row["username"]
        self.password = row["password"]
        self.journals = [
            Journal(journal) for journal in doSQL(f"select * from journals where userId = '{self.id}'")
        ]
        self.predictions = [
            Prediction(prediction) for prediction in doSQL(f"select * from predictions where userId = '{self.id}'")
        ]
        self.userdata = Userdata(doSQL(f"select * from userdata where userId = {self.id}")[0])

    def __repr__(self) -> str:
        return f'User({self.id} {self.username} {self.password} [{",".join([str(j) for j in self.journals])}] [{",".join(str(p) for p in self.predictions)}])'

def format_plot():
    plt.figure(figwidth=(10, 6))
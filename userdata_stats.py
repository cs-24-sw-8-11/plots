from statistics import mean
from subprocess import check_output
import json
import sys
import matplotlib.pyplot as plt
import datetime

def doSQL(sql):
    result = check_output([
        "sqlite3",
        sys.argv[-1],
        sql,
        "-json"
    ]).decode()
    if result:
        return json.loads(result)
    else:
        return []

ages = []
genders = []
education = []

journals = {}
predictions = {}
answers = {}
ratings = {}

users = doSQL("select * from users where username not like '%user%' and not username = 'admin'")

for user in users:
    userdata = doSQL(f"select * from userdata where userId = '{user['id']}'")[0]
    #print(user)
    #print(userdata)

    ages.append(userdata['age'])
    genders.append(userdata["gender"])
    education.append(userdata["education"])
    journals[user["id"]] = doSQL(f"select * from journals where userId = '{user['id']}'")
    predictions[user["id"]] = doSQL(f"select * from predictions where userId = '{user['id']}'")

for uid, user_journals in journals.items():
    for journal in user_journals:
        answers[journal["id"]] = doSQL(f"select * from answers where journalId = '{journal['id']}'")

for uid, user_predictions in predictions.items():
    for prediction in user_predictions:
        result = doSQL(f"select * from ratings where predictionId = '{prediction['id']}'")
        if result:
            ratings[prediction["id"]] = result[0]

males = [g for g in genders if g == 1]
females = [g for g in genders if g == 2]
others = [g for g in genders if g == 3]

print(f"""
    # participants:       {len(users)}
    Mean age:             {round(mean(ages), 2)}
    Male participants:    {int((len(males)/len(genders))*100)}%
    Female participants:  {int((len(females)/len(genders))*100)}%
    Other participants:   {int((len(others)/len(genders))*100)}%
    Mean education level: {round(mean(education), 2)} (1: elementary, 2: high school, 3: bachelor, 4: master)
    Total journals:       {sum([len(journal) for _, journal in journals.items()])}
    Journals per user:    {mean([len(journal) for _, journal in journals.items()])}
    Predictions per user: {mean([len(prediction) for _, prediction in predictions.items()])}
    Total answers:        {sum([len(answer) for _, answer in answers.items()])}
""")

# INIT MATPLOTLIB
ax:plt.Axes

# JOURNALS PLOT
fig, ax = plt.subplots()
values = [datetime.datetime.fromtimestamp(journal["timestamp"]) for _, user_journals in journals.items() for journal in user_journals]
ax.hist(values)
ax.set_title("Journal history")
plt.savefig("../figures/journal_history.pdf")

# ANSWERS PLOT

fig, ax = plt.subplots()
values = [answer['value'] for _, user_answers in answers.items() for answer in user_answers]
ax.bar(range(len(values)), values)
ax.set_title("answer values")
plt.savefig("../figures/answer_values.pdf")

# PREDICTIONS PLOT
fig, ax = plt.subplots()
mappings = []

for pid, user_predictions in predictions.items():
    for prediction in user_predictions:
        if prediction["id"] in ratings.keys():
            rating_obj = ratings[prediction["id"]]
            rating = rating_obj['rating']
            expected = bool(rating_obj["expected"])
            mappings.append({
                "color":"blue" if expected else "red",
                "value":prediction["value"],
            })
        else:
            mappings.append({
                "color":"black",
                "value":prediction["value"]
            })
ax.bar(range(len(mappings)), [mapping["value"] for mapping in mappings], color=[mapping["color"] for mapping in mappings])
ax.set_title("Predictions values")
plt.savefig("../figures/prediction_values.pdf")

plt.show()

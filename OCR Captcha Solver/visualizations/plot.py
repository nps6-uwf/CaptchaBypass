import matplotlib.pyplot as plt
import numpy as np
import pickle

# read data from pickle
with open("captchaDataRes.pickle", "rb") as fobj:
    data = pickle.load(fobj)

# Generate pie chart showing OCR result lengths:
# --------------------------
if False:

    labels = 'Match', 'No Match'
    sizes = [(54 - data["length_not_match"]), data["length_not_match"]]
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


# Generate Double Bar Chart: 'Correctness of Captcha Solver By Letter'
# --------------------------
if True:
    labels = list(data["character"].keys())
    correct = [data["character"][i]["correct"] for i in labels]
    incorrect = [len(data["character"][i]["incorrect"]) for i in labels]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, correct, width, label='correct')
    rects2 = ax.bar(x + width/2, incorrect, width, label='incorrect')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('Total')
    ax.set_title('Correctness of Captcha Solver By Letter')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()
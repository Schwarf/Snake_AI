import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, average_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training')
    plt.xlabel('Number of games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(average_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) -1, scores[-1], str(scores[-1]))
    plt.text(len(average_scores) - 1, average_scores[-1], str(average_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)
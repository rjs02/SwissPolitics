import numpy as np
import csv

def readInput(path):
    """ read data from file and store in list and matrix """
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        parties = next(reader)[2:]
        list = []
        for row in reader:
            list.extend(row[2:])
        # print(list)
        # print(f"------\n{len(parties)}\n{len(list)}-----")
        data = np.reshape(list,(int(len(list)/len(parties)), len(parties))).astype(np.int32)
        # print(np.sum(data[0]))
        # print(data)
        return data, parties

def getColors(path):
    """ read color values from file, used for plotting """
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        dict = {row[0]:row[1] for row in reader}
    return dict

def calculateScore(data):
    """ calculate score for each party according to the formula """
    score = np.matmul(data.T, data).astype(np.float32)
    for i in range(np.shape(score)[0]):
        score[i] /= score[i][i]
        score[i] += 1
        score[i] /= 2
    return score
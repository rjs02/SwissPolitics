import numpy as np
import csv
from plot import *

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

def calculateOwnScore(data, you):
    """ calculate score for yourself """
    score = np.dot(data.T, you).astype(np.float32)
    score /= np.dot(you, you)
    score += 1
    score /= 2
    return score

def generateAllSpiders(parties, score, colors, path="", type=".png"):
    """ generate plots for all parties """
    for i in range(len(score)):
        # print("Generating for", parties[i])
        # dont plot score for party with itself (skip i-th party = itself)
        arg = [parties[0:i]+parties[i+1:], (parties[i], [score[i][0:i]+score[i][i+1:]])]
        generatePlot(arg, colors, path, type)

def generateOwnSpider(name, parties, score, colors, path="", type=".png"):
    """ generate plot for yourself """
    arg = [parties, (name, [score])]
    generatePlot(arg, colors, path, type)
    
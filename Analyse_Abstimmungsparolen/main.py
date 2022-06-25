from calculations import *

def main():
    data, parties = readInput("abstimmungsparolen.CSV")
    colors = getColors("colors.CSV")
    score = calculateScore(data).tolist()
    generateAllSpiders(parties, score, colors, "results/", ".svg")
    
    # example: how to import own score and generate spider plot
    # john = np.fromfile("john_doe.txt", sep="\n", dtype=int)
    john = np.random.randint(-1,2, len(data))
    generateOwnSpider("John Doe", parties, calculateOwnScore(data, john), colors, "results/", ".svg")

if __name__ == "__main__":
    main()
    
# Liam Devlin 28/09/18 Genetic Hello World Solver
import random
import string

target = "Hello World!"
seed = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,'!"

crossover = 0.75 
mutation = 0.05 

desiredLength = len(target)
randomPossibilities = len(seed) ** desiredLength 
maxPopulation = 250

def randomGenerate(popSize):
    print("Generating Population")
    new = []

    for i in range(popSize):
        individual = ""
        for j in range(desiredLength):
            individual += random.choice(seed)

        new.append(individual)
    return new

def calcFitness(pop = []):
    fitnessWeights = {}

    for i in range(len(pop)):
        fitness = 0.0

        for j in range(desiredLength):
            if(pop[i][j] == target[j]):
                fitness += 1.0  

        # normalize 
        fitness = fitness / desiredLength
        fitnessWeights[i] = fitness

    # sort the population to front load fittest
    s = [(k,fitnessWeights[k]) for k in sorted(fitnessWeights, key = fitnessWeights.get, reverse = True)]
    return s

def mutate(pop = []):
    for i in range(len(pop)):
        if(random.random() < mutation):
            slot = random.randint(0, desiredLength - 1)
            c = list(pop[i])
            c[slot] = random.choice(seed)
            pop[i] = ''.join(c)

def sortPopulation(pop = [] , fitness = []):
    # sorts population by fitness, based on return of calcFitness
    newPop = []
    i = 0
    for key, val in fitness:
        newPop.insert(i, pop[key])
        i += 1
    return newPop
        
def selection(pop = [], fitness = []):
    newPop = []
    selection = (int)(maxPopulation / 5) # Top 20% of the population
    while(len(newPop) < len(pop)):

        if(random.random() < 0.9):
        # Fittest individuals selection
            parent1 = pop[fitness[random.randrange(0, selection)][0]]
            parent2 = pop[fitness[random.randrange(0, selection)][0]]
            
            if(random.random() < crossover):
                #crossover    
                slot = random.randint(0, len(target))
                s1 = parent1[:slot]
                s2 = parent2[slot:]
                final = s1 + s2
                newPop.append(final)
        
            else:
            ## return one of the two parents randomnly 
                if(random.random() > 0.5):
                    newPop.append(parent1)
                else:
                    newPop.append(parent2)

        else:
            # totally random selection
            parent1 = pop[fitness[random.randrange(0, maxPopulation)][0]]
            parent2 = pop[fitness[random.randrange(0, maxPopulation)][0]]

            if(random.random() < crossover):
                slot = random.randint(0, len(target))
                s1 = parent1[:slot]
                s2 = parent2[slot:]
                final = s1 + s2
                newPop.append(final)
        
            else:
                if(random.random() > 0.5):
                    newPop.append(parent1)
                else:
                    newPop.append(parent2)
    return newPop

def GAMainLoop():
    population = randomGenerate(maxPopulation)
    populationFitness = calcFitness(population)
    population = sortPopulation(population, populationFitness)
    result = ""
    gen = 0
    while(result != target):
        population = selection(population, populationFitness)
        mutate(population)
        populationFitness = calcFitness(population)
        population = sortPopulation(population, populationFitness)
        result = population[populationFitness[0][0]]
        print("Generation %d : Fittest individual: %s" %(gen, result))
        gen += 1
    numGeneticIndividuals = gen * maxPopulation
    print("Total number of random possibilities (individuals): %d" % randomPossibilities)
    print("Genetic Algorithm took %d generations to complete, from a total of %d individuals" % (gen, numGeneticIndividuals))
    print("Genetic algorithm %d times more efficient than random search" % (randomPossibilities / numGeneticIndividuals))

GAMainLoop()
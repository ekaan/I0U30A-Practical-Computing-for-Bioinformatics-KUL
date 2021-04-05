import numpy as np
import operator


# Read and process the given "GOannotations.txt" file
def processGO(fileReader):
    # Initialize three empty dictionaries
    goExpD = {}
    geneCount = {}
    goToID = {}
    next(fileReader) # Using this to get rid of the header line

    for line in fileReader:
        lineArr = line.split("\t")

        goExp = lineArr[2][:-1]
        geneID = lineArr[0] # Extracting the information from the line
        goTerm = lineArr[1]

        # go explanation dictionary
        if goTerm not in goExpD.keys(): # If GO term does not exist as a key in goExp
            goExpD[goTerm] = goExp  # Add the instance of GO term key and its explanation

        # gene count dictionary
        if geneID in geneCount.keys(): # If gene ID exists as key
            geneCount[geneID] += 1 # Increase the counter by 1 for that gene ID
        else:
            geneCount[geneID] = 1 # If this gene ID in not in the dictionary, add a new instance and set the counter to 1

        if goTerm not in goToID.keys(): # If GO term is not in the dictionary as key
            goToID[goTerm] = [geneID] # Then add the GO term to list and put the corresponding gene ID to the list
        else:
            goToID[goTerm].append(geneID) # Otherwise add the gene ID to already existing list

    return geneCount, goToID, goExpD

# Read and process the given "IDS2.txt" and "allGenes.txt" file
def processGenes(reader):
    geneCount = {}
    for line in reader:
        lineArr = line.split("\t") # Extracting the values in line
        geneID = lineArr[0][:-1]

        if geneID in geneCount:
            geneCount[geneID] += 1 # If gene ID exists in the dictionary, increase the counter for it by 1
        else:
            geneCount[geneID] = 1 # If not, set the counter to 1 and create a new instance

    return geneCount


# Differentiate the Selected genes from the other genes
def extractSelOrNot(selected, all):
    sel = {}
    notSel = {}

    for key in all:
        if key not in selected: # Check how many instances in All genes is not inside of the Selected genes
            if key not in notSel:
                notSel[key] = all[key] # If key is not added to dictionary, add the key and the value corresponding to it

    for key in selected:
        if key in all: # Check how many of the selected genes are inside of the All genes
            if key not in sel: # If selected genes are inside of the all genes, then add them to selected dictionary with their counter
                sel[key] = selected[key]

    return sel, notSel


# Calculate Chi square statistic for each GO term
def determineChiSq(expected, observed):
    result = 0
    for row in range(0, 2):
        for col in range(0, 2):
            if expected[row][col] != 0:
                result = result + ((observed[row][col] - expected[row][col]) ** 2) / expected[row][col]

    return result   # Calculate the Chi square value for each square in matrix by using the given matrices

# Find and add the chi square value for each GO term into the dictionary
def processGOterms(sel, notSel, goToID):
    goValue = {}
    for GO in goToID: # For each GO term

        A = 0
        B = 0 # Set the counters to 0 before start counting

        for ID in goToID[GO]:
            if ID in sel: # For every gene ID corresponding to GO term, if its inside of the selected increase the counter
                A += 1

            if ID in notSel: # For every gene ID corresponding to GO term, if its inside of the not selected increase the counter
                B += 1

        C = len(sel) - A
        D = len(notSel) - B # Determine C and D value given that we have the A and B

        Row1 = A + B
        Row2 = C + D
        Col1 = A + C # Calculate the marginal values in addition to N
        Col2 = B + D
        N = A + B + C + D

        exp_A = (Row1 * Col1) / N
        exp_B = (Row1 * Col2) / N
        exp_C = (Row2 * Col1) / N # Determine the expected values for each square and create numpy arrays for it
        exp_D = (Row2 * Col2) / N

        expected = np.array([[exp_A, exp_B], [exp_C, exp_D]])
        observed = np.array([[A, B], [C, D]])

        chiVal = determineChiSq(expected, observed) # Call the method that calculates the Chi Square value

        goValue[GO] = chiVal # Add this value of chi square to corresponding GO term

    return goValue

# Method to create a list such that it will only consist unique values
def unique(list):
    # intialize a null list
    unique_list = []
    # traverse for all elements
    for x in list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


# ------Main Code------------------

# Adding the files to our code
allGenes = open("allGenes.txt", 'r')
go = open("GOannotations.txt", 'r') # Create the readers
selected = open("IDS2.txt", 'r')

idCount, goToID, goExp = processGO(go)
selectedCount = processGenes(selected) # Generate the dictionaries, for further calculation
allCount = processGenes(allGenes)

for GO in goToID:
    goToID[GO] = unique(goToID[GO]) # Dont forget to generate a list that only has unique gene IDs for every GO term

print("Number of genes in IDS2.txt:", len(selectedCount))
print("Number of genes in GOannonations.txt:", len(idCount))
print("Number of total genes in allGenes.txt:", len(allCount))

sel, notSel = extractSelOrNot(selectedCount, allCount) # Generate the selected and not selected dictionary by giving the readers

result = processGOterms(sel, notSel, goToID) # Obtain the result dictionary that stores the Chi Square values for each GO term

sorted_dict = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True)) # Sort the list based on the values of it

final = []
for key in sorted_dict: # Generate the list to unify all the obtained information and also to display best 5 GO terms
    element = str(key) + "-" + str(sorted_dict[key]) + "-" + goExp[key]
    final.append(element)

print("Printing the TOP 5 Results:") # Display top 5 GO terms
for i in final[:5]:
    print(i)

print("Writing all the results to a file...")

# Open a new text file to insert the results
with open("GO_categories.txt", 'w') as output: # Generate the output text file based on the sorted dictionary
    output.write("Go term" + '\t\t' + "Chi square" + '\t\t\t' + "GO Term Explanation" + '\n')

    for key in sorted_dict:
        output.write(str(key) + '\t' + str(sorted_dict[key]) + '\t' + (goExp[key]) + '\n')
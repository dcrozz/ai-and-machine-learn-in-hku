
"""
Run python autograder.py 
"""

def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    return sum(set(priceList))*1.0/len(set(priceList))

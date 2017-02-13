"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    totalcost = []
    for fruitShop in fruitShops:
        totalcost.append(sum([x[1]*fruitShop.fruitPrices[x[0]] for x in orderList]))
    return fruitShops[min(enumerate(totalcost), key=lambda p : p[1])[0]]
    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
    #  max_list = []
    #  for fruitShop in fruitShops:
    #      totalcost = 0
    #      for order in orderList:
    #          totalcost += order[1] * fruitShop[order[0]]
    #      max_list.append(totalcost)
    #  return max_list
    minPrice = fruitShops[0].fruitPrices.copy()
    maxPrice = fruitShops[0].fruitPrices.copy()
    for fruitShop in fruitShops[1:]:
        fruitPrice = fruitShop.fruitPrices
        for key,value in fruitPrice.iteritems():
            if key in minPrice:
                if fruitPrice[key] < minPrice[key]:
                    minPrice[key] = fruitPrice[key]
                if fruitPrice[key] > maxPrice[key]:
                    maxPrice[key] = fruitPrice[key]
            else:
                minPrice[key] = fruitPrice[key]
                maxPrice[key] = fruitPrice[key]
    arbitrageList = {x:maxPrice[x]-minPrice[x] for x in minPrice}
    return sum([x[1]*arbitrageList[x[0]] for x in orderList])

def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    minPrice = fruitShops[0].fruitPrices
    for fruitShop in fruitShops[1:]:
        fruitPrice = fruitShop.fruitPrices
        for key,value in fruitPrice.iteritems():
            if key in minPrice:
                if fruitPrice[key] < minPrice[key]:
                    minPrice[key] = fruitPrice[key]
            else:
                minPrice[key] = fruitPrice[key]
    return sum([x[1]*minPrice[x[0]] for x in orderList])

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())

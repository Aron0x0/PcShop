
# PC Shop Inventory and Sales System

# Status:
#  0 = Empty
#  1 = Flexible space
#  2 = Incoming stock
# -1 = Sold
#  3 or greater = Unique barcode

import numpy as np 


ItemType = [
    ["CPU", 100], 
    ["Motherboard", 200], 
    ["Ram", 160], 
    ["Storage", 40]
]
ItemInCart = []
LastError = ""
ErrorBuffer = []
Logger = []
ItemTotalCost = 0

shelves = [
    # CPU
    [
        [1001, 0, 1002, 1, 0],
        [1003, 2, 0, 1004, 1],
        [0, 1005, 1006, 0, 2]
    ],
    # Motherboard
    [
        [0, 1007, 1, 1008, 0],
        [1009, 0, 2, 1, 1010],
        [1011, 1012, 0, 0, 1]
    ],
    # RAM
    [
        [1013, 1014, 0, 1015, 1],
        [0, 1016, 1017, 1, 0],
        [1018, 0, 2, 1019, 1020]
    ],
    # Storage
    [
        [1, 0, 1021, 1022, 2],
        [1023, 1, 0, 1024, 0],
        [1025, 1026, 1, 0, 1027]
    ]
]

sizeX = 4
sizeY = 3
sizeZ = 5
flatDimensionaShelves = [z for x in shelves for y in x for z in y]
flatDimensionalItemType = [y for x in ItemType for y in x]

print(flatDimensionaShelves)
print(flatDimensionalItemType)


def findARangeOfListIndex(x, y, z):
    return (x-1) * (sizeY * sizeZ) + (y-1) * sizeZ + (z-1)

def decodePositionIndex(ItemIndex):
    return [
        ItemIndex // (sizeY * sizeZ) + 1, # X value
        (ItemIndex % (sizeY * sizeZ)) // sizeZ + 1, # Y Value
        ItemIndex % sizeZ + 1 #Z Value
    ]

def findARangeOfListValue(x, y, z):
    return flatDimensionaShelves[findARangeOfListIndex(x, y, z)]

print("Index of: ", findARangeOfListIndex(4, 3, 5))
print(f"Result: {findARangeOfListValue(4, 3, 5)}")

decodedPosition = decodePositionIndex(findARangeOfListIndex(4, 3, 5))
print(f"Index Position in 3d: {decodedPosition[0]}, {decodedPosition[1]}, {decodedPosition[2]}")

def findItemInList(barcode):
    for ItemIndex, ItemValue in enumerate(flatDimensionaShelves):
        if barcode == ItemValue:
            return [True, ItemIndex, ItemValue, [decodePositionIndex(ItemIndex)[0], decodePositionIndex(ItemIndex)[1], decodePositionIndex(ItemIndex)[2]]]
    return [False, Null, Null,[decodePositionIndex(ItemIndex)[0], decodePositionIndex(ItemIndex)[1], decodePositionIndex(ItemIndex)[2]]]

def markItemAsSold(barcode):
    Product = findItemInList(barcode)
    if Product[0]:
        flatDimensionaShelves[Product[1]] = -1
        print(f"Product code: {Product[1]} -> Sold")
    print(Product)

def showInvetoryList():
    Products = flatDimensionaShelves
    LayerLayout = 1
    for Index, Items in enumerate(Products):
        # print(f"Shelf Number: {(Index+1):^40}")
        if (Index) % 15 == 0:
            print()
            print(f"{f'Shelf Number: {(LayerLayout)}':^40}")  
            LayerLayout+=1
        print(f"| {Items:^10} ", end='')
        if (Index+1) % 5 == 0:
            print("|")
            
showInvetoryList()

def Log(Data):
    Logger.append(Data)

def formatThe2dShelves(Item):
    displayText = ""

    for e in Item:
        if e == 0:
            displayText = "Empty"
        elif e == 1:
            displayText = "Flexible Space"
        elif e == 2:
            displayText = "Incoming Stock"
        elif e == -1:
            displayText = "Sold"
        elif e >= 3:
            displayText = "InStock"
        print(f"| {displayText:^17}", end='')
    print("|")


    
def addToCart(buffer):
    for i in range(len(ItemInCart)):
        if buffer[0] == barcode:
            print(f"{'Barcode Already Exist!':^20}")
            return
    ItemInCart.append([buffer[2], "Null", 1])


def ShowAvailableItemInShelf(shelvesNumber):
    print("\n", ItemType[shelvesNumber], "Inventory:")

    for row in shelves[shelvesNumber]:
        formatThe2dShelves(row)

oneTime = 0;
while True:
    #if oneTime >= 3:
    #    break;
    print("\n===== PC SHOP SALES SYSTEM =====")
    print("1. Sell an item")
    print("2. Show Item Available On Shelf")
    print("9. Exit")

    choice = input("************\nEnter choice: ")

    if choice == "1":
        print("Sell Item. Type 99 to checkout.")

        while True:
            try:
                barcode = int(input("Enter the barcode: "))
                SearchBuffer = findItemInList(barcode)
                
                if barcode == 99:
                    print("\n\n*-------------Items Already Payed!:---------------*")
                    for i in range(len(ItemInCart)):
                        print(f"|{(i+1):^5}# Barcode:{ItemInCart[i][0]:^10}| ItemName:{ItemInCart[i][1]:^10}| Price:{ItemInCart[i][2]}|")
                        ItemTotalCost += ItemInCart[i][2]
                    print(f"-----> Total Item Cost: {ItemTotalCost:^10} <----")
                    print("*-------------------------------------------------*")
                    print("Total Price: Null")
                    break

                if barcode == 1 or barcode == 2 or barcode == -1 or barcode == 0:
                    print("?/> This is Reserve Key Numbers.")
                    continue
            
                if SearchBuffer[0]:
                    print(f"Added To Cart: {SearchBuffer[1]} --> Price: {SearchBuffer[2]}")
                    addToCart(SearchBuffer)
                else:
                    LastError = "Invalid Barcode."
                    print(f"!/> Error: {LastError:^20}")

                if len(ItemInCart) > 0:
                    print("*------------------------------------------------------*")
                    print(ItemInCart)
                    for i in range(len(ItemInCart)):
                        print(f"|Barcode:{ItemInCart[i][0]:^10}| ItemName:{ItemInCart[i][1]:^10}| Price:{ItemInCart[i][2]}|")
                        ItemTotalCost += ItemInCart[i][2]
                    print(f"-----> Total Estimate Cost: {ItemTotalCost:^10} <----")
                    print("*------------------------------------------------------*")

            except Exception as e:
                print(f"Error: {e}")
                ErrorBuffer.append(e)

           
    elif choice == "2":
        print("Inventory Item. Type 99 tov exit.")

        try:
            while True:
                itemShelfType = input("Enter CPU, Motherboard, RAM, or Storage: ")

                if itemShelfType == "99":
                    break
                elif itemShelfType.upper() == "CPU":
                    ShowAvailableItemInShelf(0)
                elif itemShelfType.upper() == "MOTHERBOARD":
                    ShowAailableItemInShelf(1)
                elif itemShelfType.upper() == "RAM":
                    ShowAvailableItemInShelf(2)
                elif itemShelfType.upper() == "STORAGE":
                    ShowAvailableItemInShelf(3)
                else:
                    print("Invalid shelf type!")
        except Exception as e:
            print(f"Error: {e}")
            ErrorBuffer.append(e)
    elif choice == "9":
        print("Exiting system...")
        break

    else:
        print("Invalid choice!")
    oneTime+=1

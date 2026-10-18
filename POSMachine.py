
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
print(flatDimensionaShelves)


def findARangeOfListIndex(x, y, z):
    return (x-1) * (sizeY * sizeZ) + (y-1) * sizeZ + (z-1)
def decodePositionIndex(ItemIndex):
    # return [(ItemIndex // (sizeY*sizeZ)), (ItemIndex % (sizeY*sizeZ)) // sizeZ, (ItemIndex % sizeY)]
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
            return [True]
    return False


def Log(Data):
    Logger.append(Data)

def sell_item(barcode): 
    for s in range(4):
        for r in range(3):
            for c in range(5):
                if shelves[s][r][c] == barcode:
                    shelves[s][r][c] = -1

                    print("\nItem found!")
                    print("Barcode:", barcode)
                    print("Shelf:", s + 1)
                    print("Row:", r + 1)
                    print("Column:", c + 1)
                    print("Status: SOLD")
                    return

    print("\nBarcode not found in stock:", barcode)

def CheckItemBarcode(barcode):
    for indexA, ValueA in enumerate(shelves):
        for indexB, ValueB in enumerate(ValueA):
            for indexC, ValueC in enumerate(ValueB):
                if shelves[indexA][indexB][indexC] == barcode:
                    return [True, ItemType[indexA][0], ItemType[indexA][1], [indexA, indexB, indexC]]
    return [False, "Null", 0, [indexA, indexB, indexC]]

def CheckItemBarcodeMod(barcode):
    result = next(
        (
            (s, r, c)
            for s, shelf in enumerate(shelves)
            for r, row in enumerate(shelf)
            for c, col in enumerate(row)
            if value == barcode
        ),
        None
    )
    if result is not None:
        s, r, c = result
        return [True, ItemType[s][0], ItemType[r][1], [s, r, c]]
    return [false, "Null", 0, [-1, -1, -1]]

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


    
def addToCart(barcode, ItemName, ItemPrice):
    for i in range(len(ItemInCart)):
        if ItemInCart[i][0] == barcode:
            print(f"{'Barcode Already Exist!':^20}")
            return
    ItemInCart.append([barcode, ItemName, ItemPrice])


def ShowAvailableItemInShelf(shelvesNumber):
    print("\n", ItemType[shelvesNumber], "Inventory:")

    for row in shelves[shelvesNumber]:
        formatThe2dShelves(row)

while True:
    print("\n===== PC SHOP SALES SYSTEM =====")
    print("1. Sell an item")
    print("2. Show Item Available On Shelf")
    print("9. Exit")

    # choice = input("************\nEnter choice: ")
    choice = "9"

    if choice == "1":
        print("Sell Item. Type 99 to checkout.")

        while True:
            try:
                barcode = int(input("Enter the barcode: "))
                SearchBuffer = CheckItemBarcode(barcode)
                
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
                    addToCart(barcode, SearchBuffer[1], SearchBuffer[2])
                else:
                    LastError = "Invalid Barcode."
                    print(f"!/> Error: {LastError:^20}")

                if len(ItemInCart) > 0:
                    print("*------------------------------------------------------*")
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

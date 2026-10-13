
# PC Shop Inventory and Sales System

# Status:
#  0 = Empty
#  1 = Flexible space
#  2 = Incoming stock
# -1 = Sold
#  3 or greater = Unique barcode

ItemType = [
    ["CPU", 100], 
    ["Motherboard", 200], 
    ["Ram", 160], 
    ["Storage", 40]
]
ItemInCart = []
LastError = ""

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
                    return [True, ItemType[indexA][0], ItemType[indexA][1]]
    return [False, "Null", 0]

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

    choice = input("************\nEnter choice: ")

    if choice == "1":
        print("Sell Item. Type 99 to checkout.")

        while True:
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
            
            if SearchBuffer[0]:
                print(f"Added To Cart: {SearchBuffer[1]} --> Price: {SearchBuffer[2]}")
                addToCart(barcode, SearchBuffer[1], SearchBuffer[2])
            else:
                LastError = "Invalid Barcode."
                print(f"!/> Error: {LastError:^20}")

            if len(ItemInCart) > 0:
                ItemTotalCost = 0
                print("*------------------------------------------------------*")
                for i in range(len(ItemInCart)):
                    print(f"|Barcode:{ItemInCart[i][0]:^10}| ItemName:{ItemInCart[i][1]:^10}| Price:{ItemInCart[i][2]}|")
                    ItemTotalCost += ItemInCart[i][2]
                print(f"-----> Total Estimate Cost: {ItemTotalCost:^10} <----")
                print("*------------------------------------------------------*")

    elif choice == "2":
        print("Inventory Item. Type 99 to exit.")

        while True:
            itemShelfType = input("Enter CPU, Motherboard, RAM, or Storage: ")

            if itemShelfType == "99":
                break
            elif itemShelfType.upper() == "CPU":
                ShowAvailableItemInShelf(0)
            elif itemShelfType.upper() == "MOTHERBOARD":
                ShowAvailableItemInShelf(1)
            elif itemShelfType.upper() == "RAM":
                ShowAvailableItemInShelf(2)
            elif itemShelfType.upper() == "STORAGE":
                ShowAvailableItemInShelf(3)
            else:
                print("Invalid shelf type!")

    elif choice == "9":
        print("Exiting system...")
        break

    else:
        print("Invalid choice!")

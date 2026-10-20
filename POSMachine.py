
# PC Shop Inventory and Sales System

# Status:
#  0 = Empty
#  1 = Flexible space
#  2 = Incoming stock
# -1 = Sold
#  3 or greater = Unique barcode


ItemType = [
    [10, "CPU", 100],
    [20, "Motherboard", 200],
    [30, "RAM", 160],
    [40, "Storage", 40]
]

# ItemInCart = []
ErrorBuffer = []
ItemTotalCost = 0
ItemTotalCostState = True

shelves = [
    # CPU (10xxxx)
    [
        [100001, 0, 100002, 1, 0],
        [100003, 2, 0, 100004, 1],
        [0, 100005, 100006, 0, 2]
    ],

    # Motherboard (20xxxx)
    [
        [0, 200001, 1, 200002, 0],
        [200003, 0, 2, 1, 200004],
        [200005, 200006, 0, 0, 1]
    ],

    # RAM (30xxxx)
    [
        [300001, 300002, 0, 300003, 1],
        [0, 300004, 300005, 1, 0],
        [300006, 0, 2, 300007, 300008]
    ],

    # Storage (40xxxx)
    [
        [1, 0, 400001, 400002, 2],
        [400003, 1, 0, 400004, 0],
        [400005, 400006, 1, 0, 400007]
    ]
]

size3dXShelves = 4 #3d Array Size X size3dXShelves
size3dYShelves = 3 #3d Array Size Y size3dYShelves
size3dZShelves = 5 #3d Array Size Z size3dZShelves

size2dXItemTypes = 4 #2d Array Size X size2dXItemTypes
size2dYItemTypes = 3 #2d Array Size Y size2dYItemTypes

flatDimensionaShelves = [z for x in shelves for y in x for z in y]
flatDimensionalItemType = [y for x in ItemType for y in x]
flatDimensionalItemInCart = []

print(flatDimensionaShelves)
print(flatDimensionalItemType)


def findARangeOfListIndexIn3d(x, y, z):
    return (x-1) * (size3dYShelves * size3dZShelves) + (y-1) * size3dZShelves + (z-1)

def findARangeOfListIndexIn2d(x, y):
    return (x-1) * size2dYItemTypes + (y-1)

def decodePositionIndexIn3d(ItemIndex):
    return [
        ItemIndex // (size3dYShelves * size3dZShelves) + 1, # X value
        (ItemIndex % (size3dYShelves * size3dZShelves)) // size3dZShelves + 1, # Y Value
        ItemIndex % size3dZShelves + 1 #Z Value
    ]

def findARangeOfListValue(x, y, z):
    return flatDimensionaShelves[findARangeOfListIndexIn3d(x, y, z)]

# print("Index of: ", findARangeOfListIndexIn3d(4, 3, 5))
# print(f"Result: {findARangeOfListValue(4, 3, 5)}")

# decodedPosition = decodePositionIndexIn3d(findARangeOfListIndexIn3d(4, 3, 5))
# print(f"Index Position in 3d: {decodedPosition[0]}, {decodedPosition[1]}, {decodedPosition[2]}")

def findItemInList(barcode):
    for ItemIndex, ItemValue in enumerate(flatDimensionaShelves):
        if barcode == ItemValue:
            return [True, ItemIndex, ItemValue, [decodePositionIndexIn3d(ItemIndex)[0], decodePositionIndexIn3d(ItemIndex)[1], decodePositionIndexIn3d(ItemIndex)[2]]]
    return [False, 0, 0,[decodePositionIndexIn3d(ItemIndex)[0], decodePositionIndexIn3d(ItemIndex)[1], decodePositionIndexIn3d(ItemIndex)[2]]]

def markItemAsSold(barcode):
    Product = findItemInList(barcode)
    if Product[0]:
        flatDimensionaShelves[Product[1]] = -1
        print(f"Product code: {Product[1]} -> Sold")
    #print(Product)

def showInvetoryList():
    Products = flatDimensionaShelves
    LayerLayout = 1
    for Index, Items in enumerate(Products):
        if (Index) % 15 == 0:
            print()
            print("="*66)
            print(f"|{f'<--> Shelf Number: {(LayerLayout)} <-->':^64}|")  
            LayerLayout+=1
        print(f"| {Items:^10} ", end='')
        if (Index+1) % 5 == 0:
            print("|")
            print("="*66)

def addToCart(buffer):
    for i in range(1, len(flatDimensionalItemInCart) // size2dYItemTypes + 1):
        if buffer[2] == flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 1)]:
            print(f"{'Barcode Already Exist!':^20}")
            return False

    Prefix = [str(buffer[2])[:2], "", 0]

    for i in range(len(flatDimensionalItemType)):
        if i % size2dYItemTypes == 0:
            if int(Prefix[0]) == flatDimensionalItemType[i]:
                Prefix[1] = flatDimensionalItemType[i+1]
                Prefix[2] = flatDimensionalItemType[i+2]

    flatDimensionalItemInCart.append(buffer[2])
    flatDimensionalItemInCart.append(Prefix[1])
    flatDimensionalItemInCart.append(Prefix[2])

    return True


def ShowAvailableItemInShelf(shelvesNumber):
    print("\n", ItemType[shelvesNumber], "Inventory:")

    for row in shelves[shelvesNumber]:
        formatThe2dShelves(row)


def Log(Data):
    Logger.append(Data)

def checkItemStatus(Item):
    if Item == 0:
        displayText = "Empty"
    elif Item == 1:
        displayText = "Flexible Space"
    elif Item == 2:
        displayText = "Incoming Stock"
    elif Item == -1:
        displayText = "Sold"
    elif Item >= 3:
        displayText = "InStock"
    else: 
        displayText = "Unknown Status"
    return displayText

def formatTerminalResult3dShelves(Item):

    Products = flatDimensionaShelves
    LayerLayout = 1
    for Index, Items in enumerate(Products):
        if (Index) % 15 == 0:
            print()
            print("="*80)
            print(f"{f'Shelf Number: {(LayerLayout)}':^40}")  
            LayerLayout+=1
        print(f"| {checkItemStatus(Items):^10} ", end='')
        if (Index+1) % 5 == 0:
            print("|")
            print("="*80)

def displayShelfItemStatusIn3d(STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ):
    print("="*101)
    for x in range(findARangeOfListIndexIn3d(STARTX, STARTY, STARTZ), findARangeOfListIndexIn3d(ENDX, ENDY, ENDZ)+1):
        print(f"| {checkItemStatus(flatDimensionaShelves[x]):^17} ", end='')
        if (x+1) % size3dZShelves == 0:
            print("|")
            print("="*101)
    # print(f" {findARangeOfListIndexIn3d(1, 1, 1)} --> {findARangeOfListIndexIn3d(1, 3, 5)}")
    # print(f" {findARangeOfListIndexIn3d(2, 1, 1)} --> {findARangeOfListIndexIn3d(2, 3, 5)}")

# displayShelfItemStatusIn3d(1, 1, 1)
#
def checkItemStatusInRange(STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ):
    for x in range(findARangeOfListIndexIn3d(STARTX, STARTY, STARTZ), findARangeOfListIndexIn3d(ENDX, ENDY, ENDZ)+1):
        if flatDimensionaShelves[x] == 0 or flatDimensionaShelves[x] == 1 or flatDimensionaShelves[x] == 2:
            print("Item Index Return...")
            return x
    print("Item Slot Available")
    return False


def putItemInShelf(barcode, STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ):
    dump = checkItemStatusInRange(STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ)
    if dump == False:
        print("Failed to add barcode.")
        return
    #print(dump)
    flatDimensionaShelves[dump] = barcode
    print(f"Successfully Added Barcode: {barcode} -> IndexPosition: {dump}")
oneTime = 0;

showInvetoryList()
while True:
    try:
        #if oneTime >= 3:
        #    break;
        print("\n===== PC SHOP SALES SYSTEM =====")
        print("1. Sell an item")
        print("2. Show Item Available On Shelf")
        print("3. Put Item In Available Shelf")
        print("9. Exit")

        choice = int(input("************\nEnter choice: "))

        if choice == 1:
            print("Sell Item. Type 99 to checkout.")

            while True:
                try:
                    barcode = int(input("Enter the barcode: "))
                    SearchBuffer = findItemInList(barcode)
                    
                    if barcode == 99:
                        print("\n\nChecking out...\n")
                        print("=" * 66)
                        print(f"{'PC SHOP - SALES RECEIPT':^66}")
                        print("=" * 66)
                        print(f"{'No.':<5}{'Barcode':<15}{'Item Name':<25}{'Price':>15}")
                        print("-" * 66)

                        ItemTotalCost = 0

                        for i in range(1, len(flatDimensionalItemInCart) // size2dYItemTypes + 1):
                            itemBarcode = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 1)]
                            itemName = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 2)]
                            price = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 3)]

                            markItemAsSold(itemBarcode)

                            print(f"{i:<5}{itemBarcode:<15}{itemName:<25}{price:>15.2f}")
                            ItemTotalCost += price

                        print("-" * 66)
                        print(f"{'TOTAL:':>45}{ItemTotalCost:>21.2f}")
                        print("=" * 66)
                        flatDimensionalItemInCart.clear()
                        break

                    if barcode == 1 or barcode == 2 or barcode == -1 or barcode == 0:
                        print("?/> This is Reserve Key Numbers.")
                        continue
                
                    if SearchBuffer[0]:
                        print(f"Added To Cart: {SearchBuffer[1]} --> Price: {SearchBuffer[2]}")
                        ItemTotalCostState = addToCart(SearchBuffer)
                    else:
                        LastError = "Invalid Barcode."
                        print(f"!/> Error: {LastError:^20}")

                    if len(flatDimensionalItemInCart) > 0:
                        print("=" * 66)
                        print(f"{'PC SHOP - CART SUMMARY':^66}")
                        print("=" * 66)
                        print(f"{'No.':<5}{'Barcode':<15}{'Item Name':<25}{'Price':>15}")
                        print("-" * 66)

                        for i in range(1, len(flatDimensionalItemInCart) // size2dYItemTypes + 1):
                            barcode = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 1)]
                            itemName = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 2)]
                            price = flatDimensionalItemInCart[findARangeOfListIndexIn2d(i, 3)]

                            print(f"{i:<5}{barcode:<15}{itemName:<25}{price:>15.2f}")
                            ItemTotalCost += price

                        print("-" * 66)
                        print(f"{'TOTAL ESTIMATE:':>45}{ItemTotalCost:>21.2f}")
                        print("=" * 66)

                except Exception as e:
                    print(f"Error: {e}")
                    ErrorBuffer.append(e)

            
        elif choice == 2:
            print("Inventory Item. Type 99 tov exit.")
            showInvetoryList()
            try:
                while True:
                    itemShelfType = input("Enter CPU, Motherboard, RAM, or Storage: ")
                    
                    if itemShelfType == "99":
                        break
                    elif itemShelfType.upper() == "CPU":
                        print("="*101)
                        print(f"|{f"CPU":^99}|")
                        displayShelfItemStatusIn3d(1, size3dYShelves-(size3dYShelves-1),size3dYShelves-(size3dYShelves-1), 1, size3dYShelves, size3dZShelves)
                    elif itemShelfType.upper() == "MOTHERBOARD":
                        print("="*101)
                        print(f"|{f"MOTHERBOARD":^99}|")
                        displayShelfItemStatusIn3d(2, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 2, size3dYShelves, size3dZShelves)
                    elif itemShelfType.upper() == "RAM":
                        print("="*101)
                        print(f"|{f"RAM":^99}|")
                        displayShelfItemStatusIn3d(3, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 3, size3dYShelves, size3dZShelves)
                    elif itemShelfType.upper() == "STORAGE":
                        print("="*101)
                        print(f"|{f"STORAGE":^99}|")
                        displayShelfItemStatusIn3d(4, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 4, size3dYShelves, size3dZShelves)
                    else:
                        print("Invalid shelf type!")
            except Exception as e:
                print(f"Error: {str(e)}")
                ErrorBuffer.append(str(e))

        elif choice == 3:
            print("Re-Stock Inventory. Type 99 tov exit.")
            showInvetoryList()
            try:
                
                while True:
                    showInvetoryList()
                    print("Prefix: 10xxxx:CPU, 20xxxx:Motherboard, 30xxxx:RAM, 40xxxx:Storage")
                    itemBarcode = input("Put Barcode: ")
                    itemPrefix = int(str(itemBarcode)[:2])
                    if itemBarcode == "99":
                        break
                    elif itemPrefix == 10:
                        putItemInShelf(itemBarcode, 1, size3dYShelves-(size3dYShelves-1),size3dYShelves-(size3dYShelves-1), 1, size3dYShelves, size3dZShelves)
                    elif itemPrefix == 20:
                        putItemInShelf(itemBarcode, 2, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 2, size3dYShelves, size3dZShelves)
                    elif itemPrefix == 30:
                        putItemInShelf(itemBarcode, 3, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 3, size3dYShelves, size3dZShelves)
                    elif itemPrefix == 40:
                        putItemInShelf(itemBarcode, 4, size3dYShelves-(size3dYShelves-1), size3dYShelves-(size3dYShelves-1), 4, size3dYShelves, size3dZShelves)
                    else:
                        print("Invalid shelf type!")
            except Exception as e:
                print(f"Error: {str(e)}")
                ErrorBuffer.append(str(e))
        elif choice == 9:
                print(ErrorBuffer)
                print("Exiting system...")
                break

        else:
            print("Invalid choice!")
        oneTime+=1
    except Exception as e:
        print(f"Error: {str(e)}")
        ErrorBuffer.append(str(e))

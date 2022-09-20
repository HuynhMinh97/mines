# Bàn cờ gồm 3 đối tượng: 
from email.policy import default
import os
import queue
class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    PURPLE = '\033[45m'
    CWHITE2  = '\33[97m'
    ENDC = '\033[m'
    def render(self,index):
        match index:
            case 0:
                return self.CYAN
            case 1:
                return self.BLUE
            case 2:
                return self.GREEN
            case 3:
                return self.RED
            case 4:
                return self.YELLOW
            case 5:
                return self.PURPLE
            case default:
                return self.ENDC
class Block:pass
            
class Board:
    def __init__(self,len):
        self.len=len
        self.numList=[]
        self.blockList=[]
        self.color=Color()
    
    # Thêm ô có số
    def addNumList(self,x,y,index):
        self.numList.append(Num(x,y,index))        

    # Thêm ô trống
    def addBlockList(self,x,y):
        self.blockList.append(Block(x,y))   
    
    # Trả về cell ở vị trí x , y
    def checkCell(self,x,y):
        if x in range(0, self.len) and y in range(0,self.len):
            for num in self.numList:
                if num.x==x and num.y==y:
                    return num

            for block in self.blockList:
                if block.x==x and block.y==y:
                    return block
        return None

    def printBoard(self):
        for x in range(0,self.len):
            for y in range(0,self.len):
                cell=self.checkCell(x,y)
                if cell.isNum:
                    print("["+self.color.render(cell.index)+str(cell.index)+self.color.render('RESET')+"]", end="")
                else:
                    print("["+cell.flag+"]", end="")
            print('\n')

    def listMoveValid(self):
        rs=[]
        for ele in self.blockList:
            if self.checkFlag(ele.x,ele.y):
                rs.append(ele)
        if len(rs)>0:
            return rs
        else:
            return None

    # Tao 1 list cac o xung quanh [x+-1, y+-1]
    def blockAround(self,x,y):
        up=self.checkCell(x+1,y)
        down=self.checkCell(x-1,y)
        left=self.checkCell(x,y+1)
        right=self.checkCell(x,y-1)
        upLeft=self.checkCell(x+1,y+1)
        upRight=self.checkCell(x+1,y-1)
        downRight=self.checkCell(x-1,y-1)
        downLeft=self.checkCell(x-1,y+1)
        list = [up,down,left,right,upLeft,upRight,downRight,downLeft]
        rs=[]
        for ele in list:
            if ele is None:
                continue
            else:
                rs.append(ele)
        return rs

    # Kiem tra xung quanh ô số đã đủ cờ hay chưa
    # True la da du. False la chua
    def checkEnoughFlag(self,x,y):
        count=0
        for ele in self.blockAround(x,y):
            if isinstance(ele,Block) and ele.flag=='?':
                count+=1

        cell= self.checkCell(x,y)
        if isinstance(cell,Num) and cell.index==count:
            return True
        else:
            return False

    def renderNumListAround(self,x,y):
        list=[]
        for num in self.numList:
            if (num.x==x+1 and num.y==y) or (num.x==x-1 and num.y==y) or (num.x==x and num.y==y+1) or (num.x==x and num.y==y-1) or (num.x==x+1 and num.y==y+1) or (num.x==x+1 and num.y==y-1) or (num.x==x-1 and num.y==y+1) or (num.x==x-1 and num.y==y-1):
                list.append(num)
        return list


    def empBlock(self):
        # check tất cả ô num xung quanh
        # Nếu thỏa hết => chuyển về empty Block
        for block in self.blockList:
            list=self.renderNumListAround(block.x,block.y)
            check=False
            for num in list:
                if self.checkEnoughFlag(num.x,num.y):
                    check=True
                    break
                else:
                    continue
            
            cellBlock = self.checkCell(block.x,block.y)
            if check and isinstance(cellBlock,Block) and cellBlock.flag!='?':
                cellBlock.flag=" "
            else:
                return
        
    # Kiểm tra ô block có thể đặt cờ dc hay không
    def checkFlag(self,x,y):
        list=self.renderNumListAround(x,y)
        check=True
        for num in list:
            if self.checkEnoughFlag(num.x,num.y):
                check=False
                break
            else:
                continue
        return check

    # List nhung nuoc di hop le
    def renderMoveValid(self):
        list=[]
        for block in self.blockList:
            if block.flag=="#" and self.checkFlag(block.x,block.y):
                list.append(block)
        # Tìm những ô num nằm gần ô block
        # Xét những ô num đã valid hay chưa
        # Nếu tất cả chưa valid thì có thể thêm cờ vào
        return list

    # Tạo ra 1 board mới khi thực hiện 1 nước đi hợp lệ
    def duplicateBoard(self):
        newBoard= Board(self.len)
        newBoard.numList=list(map(lambda num:num.duplicateCellNum(),self.numList))
        newBoard.blockList=list(map(lambda block:block.duplicateCellBlock(),self.blockList))
        return newBoard

    def checkMine(self, block ):
        newBlock=self.checkCell(block.x,block.y)
        newBlock.flag="?"
        rs=[]
        for block1 in self.blockList:
            if self.checkFlag(block1.x,block1.y) or block1.flag=="?":
                continue
            else:
                rs.append(block1)
        for ele in rs:
            block=self.checkCell(ele.x,ele.y)
            block.flag=" "

        for num in self.numList:
            if self.checkEnoughFlag(num.x,num.y):
                num1=self.checkCell(num.x,num.y)
                num1.isValid=True

        print()
        self.printBoard()
        return self

    def run(self):
        # B1: Render cac nuoc di hop le dau tien
        # B2: Copy ban co theo tung nuoc di hop le
        # B3: Push vao trong 1 mang
        # B4: Sau do pop() lay tung phan tu lam tuong tu buoc 1
        # B5: Sau khi chay den khong con nuoc di hop le thi check dieu kien Goal
        #  Neu thoa thi lay ban co do.
        #  Neu khong thoa thi pop() ra khoi mang
        
        # B1, 2, 3
        queue = [] 
        for ele in self.renderMoveValid():
            newBoard = self.duplicateBoard()
            queue.append(newBoard.checkMine(ele))

        tem=[]
        while queue:
            board = queue.pop()
            if  board.renderMoveValid() is not None:
                for ele in board.renderMoveValid():
                    newBoard = board.duplicateBoard()
                    check= newBoard.checkMine(ele)
                    if check.checkIsGoal():
                        print()
                        newBoard.printBoard()
                        return
                    else:
                        
                        queue.append(check)
            else:
                continue

    def compareBoard(self,board):
        check=True
        for block in self.blockList:
            for block1 in board.blockList:
                if block.x==block1.x and block.y == block1.y and block.flag== block1.flag:
                    check=True   
                    break
                else:
                    check=False
        return check

    def checkIsGoal(self):
        for num in self.numList:
            if num.isValid ==False:
                return False
        return True

class Location:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Num(Location):
    def __init__(self, x, y, index):
        self.index=index
        self.isNum=True
        self.isValid=False
        super().__init__(x, y)
    
    # Copy ra 1 o num moi
    def duplicateCellNum(self):
        return Num(self.x,self.y,self.index)

class Block(Location):
    def __init__(self, x, y):
        self.isNum=False
        self.flag='#'
        super().__init__(x, y)
    
    # Copy ra 1 o block moi
    def duplicateCellBlock(self):
        block=Block(self.x,self.y)
        block.flag=self.flag
        block.isNum=self.isNum
        return block

def main():
    initBoard=[
    ['w',3,'w',2,'w'],
    ['w',4,1,'w','w'],
    ['w','w','w',2,'w'],
    ['w',2,'w','w',1],
    [1,1,'w',1,'w']
]
    lenBoard=len(initBoard)
    board=Board(lenBoard)
    for x in range(0,lenBoard):
        for y in range(0,lenBoard):
            if initBoard[x][y]!='w':
                board.addNumList(x,y,initBoard[x][y])
            else:
                board.addBlockList(x,y)

    board.printBoard()
    board.run()


    # for ele in board.numList:
    #     print(ele)


main()

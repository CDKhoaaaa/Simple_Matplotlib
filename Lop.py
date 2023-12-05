class Lop:
    def __init__(self, malop, soluong, tenlop):
        self.malop = malop
        self.soluong = soluong
        self.tenlop = tenlop
    def input_class(self):
        print("------------------------------------------------------------------")
        print("Nhập thông tin lớp")
        self.malop = input("Nhập vào mã lớp: ")
        self.soluong = input("Nhập vào số lượng lớp: ")
        self.tenlop = input("Nhập vào tên lớp: ")
    def print_class(self):
        print("Mã lớp: ", self.malop)
        print("Số lượng", self.soluong)
        print("Tên lớp: ", self.tenlop)




class sinhvien:
    def __init__(self, mssv, hoten, ngaysinh, phai, sdt, cccd, email, ma_lop, ngaynhaphoc):
        self.mssv = mssv
        self.hoten = hoten
        self.ngaysinh = ngaysinh
        self.phai = phai
        self.sdt = sdt
        self.cccd = cccd
        self.email = email
        self.ma_lop = ma_lop
        self.ngaynhaphoc = ngaynhaphoc

    def input_info_st(self):
        print("------------------------------------------------------------------")
        print("Nhập thông tin sinh viên")
        self.mssv = input("Nhập mã số sinh viên: ")
        self.hoten = input("Nhập tên sinh viên: ")
        self.ngaysinh = input("Nhập ngày sinh(yy-mm-dd):  ")
        self.phai = input("Nhập phái Nam/Nữ: ")
        self.sdt = input("Nhập vào số điện thoại: ")
        self.cccd = input("Số căn cước công dân: ")
        self.email = input("Nhập Email: ")
        self.ma_lop = input("Nhập mã lớp: ")
        self.ngaynhaphoc = input("Nhập ngày nhập học(yy-mm-dd): ")

    def print_info_st(self):
        print("Mã số sinh viên: ", self.mssv)
        print("Họ tên: ", self.hoten)
        print("Ngày sinh: ", self.ngaysinh)
        print("Giới tính: ", self.phai)
        print("Số điện thoại: ", self.sdt)
        print("Căn cước công dân: ", self.cccd)
        print("Nhập Email: ", self.email)
        print("Nhập mã lớp: ", self.ma_lop)
        print("Nhập ngày nhập học(yy-mm-dd): ", self.ngaynhaphoc)









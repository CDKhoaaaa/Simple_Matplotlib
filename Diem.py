class score:
    def __init__(self, madiem, ma_sinhv, ma_monh, diemthi, trangthai):
        self.madiem = madiem
        self.ma_sinhv = ma_sinhv
        self.ma_monh = ma_monh
        self.diemthi = diemthi
        self.trangthai = trangthai
    def input_score(self):
        self.madiem = input("Nhập vào mã điểm: ")
        self.ma_sinhv = input("Nhập vào mã sinh viên: ")
        self.ma_monh = input("Nhập vào mã môn học: ")
        self.diemthi = input("Nhập vào điểm thi: ")
    def print_score(self):
        print("Mã điểm: ", self.madiem)
        print("Mã sinh viên: ", self.ma_sinhv)
        print("Mã môn học: ", self.ma_monh)
        print("Điểm thi: ", self.diemthi)
        print("Trạng thái: ", self.trangthai)
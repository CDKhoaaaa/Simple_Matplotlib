from datetime import datetime
class registration:
    def __init__(self, madk, ngaydk, masv, mamonhoc):
        self.madk = madk
        self.ngaydk = ngaydk
        self.masv = masv
        self.mamonhoc = mamonhoc
    def dkmon(self):
        self.madk = input("Nhập mã đăng ký: ")
        self.ngaydk = datetime.today().strftime("%Y-%m-%d")
        self.masv = input("Nhập mã sinh viên: ")
        self.mamonhoc = input("Nhập mã môn học cần đăng ký: ")
    def xem_tinhtrang_dk(self):
        print("Mã đăng ký môn: ", self.madk)
        print("Ngày đăng ký: ", self.ngaydk)
        print("Nhập mã sinh viên: ", self.masv)
        print("Nhập mã môn học: ", self.mamonhoc)



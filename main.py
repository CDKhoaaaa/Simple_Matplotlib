from Sinhvien import sinhvien
from Subject import mon
from Lop import Lop
from Dangky import registration
from Diem import score
import pyodbc as pyo
from tabulate import tabulate
import urllib.parse
from matplotlib import pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
print(pyo .drivers(), "DESKTOP-HB875Q1")  # Kiểm tra thông tin db
# Nhập thông tin DB# Kiểm tra tình trạng connect
# DESKTOP-HB875Q1

check = 0  # Biến kiểm tra trạng thái
while check == 0:   # Kết nối DB
    try:
        print("-------------------------------------------------")
        driver = input("Nhập vào driver: ")
        server = input("Nhập vào server name: ")
        namedb = input("Nhập vào database name: ")
        sql_connection = pyo.connect(f'Driver={driver};'f'Server={server};'f'Database={namedb};''Trusted_Connection=yes;')
        cursor = sql_connection.cursor()
        print("Kết nối đến SQL Server thành công!")
        check = 1
    except:
        print("Kết nối đến SQL Server thất bại! Thử kiểm tra lại thông tin Database")
        check = 0

sv = sinhvien("", "", "", "", "", "", "", "", "")
lp = Lop("", "", "")
sb = mon("", "", "")
regis = registration("", "", "", "")
sc = score("", "", "", "", "")


def dbclass():  # Thêm thông tin lớp
    try:
        while True:
            lp.input_class()
            cursor.execute(f"SELECT * FROM Class WHERE Malop = '{lp.malop}';")
            if cursor.fetchone():
                print(f"Mã {lp.malop} lớp này tồn tại trong cơ sở dữ liệu, bạn không thể thực hiện thêm lớp!")
                choice = input("Bạn có muốn nhập lại mã lớp không? (Y/N): ")
                if choice == "N" or choice == "n":
                    break
                elif choice != "N" or choice == "n" and choice != "y" or choice != "Y":
                    break
            else:
                print(f"Mã {lp.malop} lớp này không tồn tại trong cơ sở dữ liệu")
                cursor.execute("INSERT INTO Class(Malop,SL_SV,TenLop) VALUES(?,?,?)", lp.malop, lp.soluong, lp.tenlop)
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã cập nhật thông tin lớp thành công")
                print("----------------------------------------------------------------------")
            n = input("Bạn có muốn tiếp tục tạo lớp? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("----------------------------------------------------------------------")
        print("Bạn có thể đã vi phạm ràng buộc, nên không thể thêm lớp ")
        print("----------------------------------------------------------------------")

# Nhập thông tin sinh viên
def dbstudent():
    global check
    try:
        sv.input_info_st()
        cursor.execute(
            "INSERT INTO Student (MSSV, HoTen, NgaySinh, Phai, SDT, CCCD, Email, Ma_Lop, Ngaynhaphoc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (sv.mssv, sv.hoten, sv.ngaysinh, sv.phai, sv.sdt, sv.cccd, sv.email, sv.ma_lop, sv.ngaynhaphoc))
        sql_connection.commit()
        check = 1
        print("----------------------------------------------------------------------")
        print(f"Thêm sinh viên {sv.hoten} thành công")
        print("----------------------------------------------------------------------")
        return check
    except:
        check = 0
        print("----------------------------------------------------------------------")
        print("Thêm một sinh viên mới thất bại")
        print("----------------------------------------------------------------------")
        return check


# Nhập thông tin môn học
def dbsubject():
    global check
    try:
        sb.input_name_sub()
        cursor.execute("INSERT INTO Subject (MMH,TenMH,Ma_lop) VALUES (?, ?, ?)", (sb.mmh, sb.tenmh, sb.malop))
        sql_connection.commit()
        check = 1
        print("----------------------------------------------------------------------")
        print(f"Thêm một môn học {sb.tenmh} thành công")
        print("----------------------------------------------------------------------")
        return check
    except:
        check = 0
        print("----------------------------------------------------------------------")
        print("Thêm một môn học thất bại")
        print("----------------------------------------------------------------------")
        return check


def dbremove_id_class():  # Xóa lớp theo ID
    global check, result
    cursor.execute("SELECT * FROM Class")
    results = cursor.fetchall()
    table = [list(row) for row in results]
    print(tabulate(table, headers=['Mã lớp', 'Số lượng', 'Tên lớp'], tablefmt='grid'))
    b = input("Nhập mã lớp cần xóa: ")
    try:
        cursor.execute(f"DELETE FROM Class WHERE Malop='{b}';")
        sql_connection.commit()
        check = 1
        print("----------------------------------------------------------------------")
        print(f"Bạn đã xóa thành công lớp {lp.malop}")
        print("----------------------------------------------------------------------")
        return check
    except:
        print("----------------------------------------------------------------------")
        print("Bạn đã nhập sai mã lớp hoặc mã lớp không tồn tại ")
        print("----------------------------------------------------------------------")
        check = 0
        return check


def dbremove_id_student():  # Xóa sinh viên theo ID
    global check
    b = input("Nhập mã sinh viên  cần xóa: ")
    try:
        cursor.execute(f"DELETE FROM Student WHERE MSSV='{b}';")
        sql_connection.commit()
        check = 1
        print("----------------------------------------------------------------------")
        print("Bạn đã xóa thành công thông tin một sinh viên")
        print("----------------------------------------------------------------------")
        return check
    except:
        print("----------------------------------------------------------------------")
        print("Bạn đã nhập sai mã sinh viên hoặc mã sinh viên không tồn tại ")
        print("----------------------------------------------------------------------")
        check = 0
        return check


def db_remove_sb():  # Xóa môn học theo ID
    global check
    b = input("Nhập mã sinh viên  cần xóa: ")
    try:
        cursor.execute(f"DELETE FROM Subject WHERE MMH='{b}';")
        sql_connection.commit()
        check = 1
        print("----------------------------------------------------------------------")
        print("Bạn đã xóa thành công môn học")
        print("----------------------------------------------------------------------")
        return check
    except:
        print("----------------------------------------------------------------------")
        print("Bạn đã nhập sai mã sinh viên hoặc mã sinh viên không tồn tại ")
        print("----------------------------------------------------------------------")
        check = 0
        return check


# Cập nhật lớp
def db_update_class():
    global check
    while True:
        print("Mời bạn chọn dữ liệu cần cập nhật")
        print("1. Số lượng sinh viên")
        print("2. Tên lớp học")
        print("3. Hiển thị thông tin lớp")
        print("4. Trở về menu")
        print("5. Thoát chương trình")
        num_choice = input("Bạn muốn cập nhật dữ liệu nào của lớp?: ")
        if num_choice == "1":
            try:
                cursor.execute('SELECT * FROM Class')
                results = cursor.fetchall()
                table = [list(row) for row in results]
                print(tabulate(table, headers=['Mã lớp', 'Số lượng sinh viên', 'Tên lớp'], tablefmt='grid'))
                while True:
                    ma_lophoc = input("Xin vui lòng nhập mã lớp học: ")
                    cursor.execute(f"SELECT * FROM Class WHERE Malop = '{ma_lophoc}';")
                    if cursor.fetchone():
                        print(f"Mã môn học {ma_lophoc} này tồn tại trong cơ sở dữ liệu.")
                        sl_sinhvien = input("Nhập vào số lượng sinh viên muốn sửa: ")
                        cursor.execute("UPDATE Class SET SL_SV = ? WHERE Malop = ?", (sl_sinhvien, ma_lophoc))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin lớp thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã môn học {ma_lophoc} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã môn học? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("----------------------------------------------------------------------")
                print("Bạn có thể đã nhập sai mã lớp")
                print("----------------------------------------------------------------------")
        elif num_choice == "2":
            try:
                cursor.execute('SELECT * FROM Class')
                results = cursor.fetchall()
                table = [list(row) for row in results]
                print(tabulate(table, headers=['Mã lớp', 'Số lượng sinh viên', 'Tên lớp'], tablefmt='grid'))
                while True:
                    ma_lophoc = input("Xin vui lòng nhập mã lớp học: ")
                    cursor.execute(f"SELECT * FROM Class WHERE Malop = '{ma_lophoc}';")
                    if cursor.fetchone():
                        print(f"Mã môn học {ma_lophoc} này tồn tại trong cơ sở dữ liệu.")
                        name_class = input("Nhập vào tên lớp muốn sửa: ")
                        cursor.execute("UPDATE Class SET TenLop = ? WHERE Malop = ?", (name_class, ma_lophoc))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin lớp thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã môn học {ma_lophoc} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã môn học? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập sai mã lớp")
        elif num_choice == "3":
            cursor.execute("SELECT * FROM Class;")
            results = cursor.fetchall()  # Tạo ra bản ghi SQL
            table = [list(row) for row in results]
            print(tabulate(table, headers=['Mã lớp', 'Số Lượng', 'Tên lớp'], tablefmt='grid'))
        elif num_choice == "4":
            break
        elif num_choice == "5":
            sql_connection.close()
            quit()
        else:
            print("----------------------------------------------------------------------")
            print("Bạn đã chọn sai chỉ mục")
            print("----------------------------------------------------------------------")

def db_update_sv():  # Cập nhật sinh viên
    while True:
        print("Mời bạn chọn dữ liệu cần cập nhật")
        print("1. Họ tên sinh viên")
        print("2. Ngày sinh")
        print("3. Phái")
        print("4. SDT")
        print("5. CCCD")
        print("6. Email")
        print("7. Ngày nhập học")
        print("8. In ra danh sách sinh viên")
        print("9. Trở về menu")
        print("10. Thoát chương trình")
        cursor.execute('SELECT * FROM Student')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['MSSV', 'Họ tên', 'Ngày sinh', 'Phái', 'SDT', 'CCCD', 'Email', 'Mã lớp',
                                       'Ngày nhập học'], tablefmt='grid'))
        num_choice = input("Bạn muốn thay đổi nội dung nào?: ")
        if num_choice == "1":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        ten_sinhvien = input("Nhập vào tên sinh viên muốn sửa: ")
                        cursor.execute("UPDATE Student SET Hoten = ? WHERE MSSV = ?", (ten_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin lớp thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N): ")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập sai mã sinh viên")
        elif num_choice == "2":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        ngaysinh_sinhvien = input("Nhập vào ngày sinh sinh viên muốn sửa yyyy-mm-dd: ")
                        cursor.execute("UPDATE Student SET NgaySinh = ? WHERE MSSV = ?", (ngaysinh_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin lớp thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N): ")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập sai format ngày sinh yyyy-mm-dd: ")
        elif num_choice == "3":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        gioitinh_sinhvien = input("Nhập vào phái sinh viên muốn sửa(Nam/Nữ): ")
                        cursor.execute("UPDATE Student SET Phai = ? WHERE MSSV = ?", (gioitinh_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin phái thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn đã nhập sai loại giới tính")
        elif num_choice == "4":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        sdt_sinhvien = input("Nhập vào số điện thoại sinh viên muốn sửa(10 số): ")
                        cursor.execute("UPDATE Student SET SDT = ? WHERE MSSV = ?", (sdt_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin số điện thoại thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập lố độ dài của số điện thoại")
        elif num_choice == "5":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        cccd_sinhvien = input("Nhập vào số căn cước sinh viên muốn sửa(12 số): ")
                        cursor.execute("UPDATE Student SET CCCD = ? WHERE MSSV = ?", (cccd_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin CCCD thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập lố độ dài của số điện thoại")
        elif num_choice == "6":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        email_sinhvien = input("Nhập vào email sinh viên muốn sửa(phải có @): ")
                        cursor.execute("UPDATE Student SET Email = ? WHERE MSSV = ?", (email_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin Email thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã thiếu @ cho Email")
        elif num_choice == "7":
            try:
                while True:
                    ma_sinhvien = input("Xin vui lòng nhập mã sinh viên: ")
                    cursor.execute(f"SELECT * FROM Student WHERE MSSV = '{ma_sinhvien}';")
                    if cursor.fetchone():
                        print(f"Mã sinh viên {ma_sinhvien} này tồn tại trong cơ sở dữ liệu.")
                        nnh_sinhvien = input("Nhập vào số căn cước sinh viên muốn sửa(12 số): ")
                        cursor.execute("UPDATE Student SET Ngaynhaphoc = ? WHERE MSSV = ?", (nnh_sinhvien, ma_sinhvien))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin ngày nhập học thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_sinhvien} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã nhập sai format yyyy-mm-dd: ")
        elif num_choice == "8":
            cursor.execute("SELECT * FROM Student;")
            results = cursor.fetchall()  # Tạo ra bản ghi SQL
            table = [list(row) for row in results]
            print(tabulate(table, headers=['MSSV', 'Họ tên', 'Ngày sinh', 'Phái', 'SDT', 'CCCD', 'Email', 'Mã lớp', 'Ngày nhập học'], tablefmt='grid'))
        elif num_choice == "9":
            break
        elif num_choice == "10":
            sql_connection.close()
            quit()
        else:
            print("Bạn có thể đã chọn sai chỉ mục")


def db_update_sb():  # Cập nhật môn học
    while True:
        print("1. Sửa tên môn học")
        print("2. In danh sách môn học")
        print("3. Trở lại menu")
        print("4. Thoát chương trình")
        cursor.execute('SELECT * FROM Subject')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã môn', 'Tên môn', 'Tên lớp'], tablefmt='grid'))
        num_choice = input("Bạn muốn thực hiện thao tác nào?: ")
        if num_choice == "1":
            try:
                while True:
                    ma_monhoc = input("Xin vui lòng nhập mã môn học: ")
                    cursor.execute(f"SELECT * FROM Subject WHERE MMH = '{ma_monhoc}';")
                    if cursor.fetchone():
                        print(f"Mã {ma_monhoc} này tồn tại trong cơ sở dữ liệu.")
                        ten_monhoc = input("Nhập vào tên môn học muốn sửa: ")
                        cursor.execute("UPDATE Subject SET TenMH = ? WHERE MMH = ?", (ten_monhoc, ma_monhoc))
                        sql_connection.commit()
                        print("----------------------------------------------------------------------")
                        print("Bạn đã cập nhật thông tin tên môn học thành công")
                        print("----------------------------------------------------------------------")
                    else:
                        print(f"Mã {ma_monhoc} này không tồn tại trong cơ sở dữ liệu.")
                        choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N): ")
                        if choice == "N" or choice == "n":
                            break
                    break
            except:
                print("Bạn có thể đã vi phạm ràng buộc")
        elif num_choice == "2":
            cursor.execute("SELECT * FROM Subject;")
            results = cursor.fetchall()  # Tạo ra bản ghi SQL
            table = [list(row) for row in results]
            print(tabulate(table, headers=['Mã môn', 'Tên môn'], tablefmt='grid'))
        elif num_choice == "3":
            break
        elif num_choice == "4":
            sql_connection.close()
            quit()
        else:
            print("Bạn có thể chọn sai chỉ mục")


def db_registration_sub():  # Đăng ký môn học
    try:
        cursor.execute('SELECT * FROM Subject')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã môn học', 'Tên môn học', 'Mã lớp'], tablefmt='grid'))

        while True:
            regis.dkmon()
            cursor.execute(f"SELECT * FROM Subject WHERE MMH = '{regis.mamonhoc}';")
            if cursor.fetchone():
                print(f"Mã {regis.mamonhoc} này tồn tại trong cơ sở dữ liệu.")
                cursor.execute("INSERT INTO Registration(MaDK,ngaydangky,Ma_SV,Ma_MonHoc) VALUES(?,?,?,?)", regis.madk,
                               regis.ngaydk, regis.masv, regis.mamonhoc)
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã cập nhật thông tin lớp thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {regis.mamonhoc} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã môn học? (Y/N): ")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục đăng ký? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã vi phạm ràng buộc")


def db_registration_sub_remove():  # Xóa đăng ký
    try:
        cursor.execute('SELECT * FROM Registration')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã đăng ký', 'Ngày đăng ký ', 'Mã sinh viên', 'Mã môn học'], tablefmt='grid'))
        while True:
            ma_monhoc = input("Xin vui lòng nhập mã môn học: ")
            cursor.execute(f"SELECT * FROM Subject WHERE MMH = '{ma_monhoc}';")
            if cursor.fetchone():
                print(f"Mã {ma_monhoc} này tồn tại trong cơ sở dữ liệu.")
                ma_sinhv = input("Nhập vào mã sinh viên: ")
                cursor.execute(f"DELETE FROM Registration WHERE Ma_MonHoc = '{ma_monhoc}' AND Ma_SV = '{ma_sinhv}';")
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã xóa thông tin đăng ký thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {ma_monhoc} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã môn học? (Y/N): ")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục xóa? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã vi phạm ràng buộc")


def db_registration_sub_update():  # Cập nhật đăng ký môn
    try:
        cursor.execute('SELECT * FROM Registration')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã đăng ký', 'Ngày đăng ký ', 'Mã sinh viên', 'Mã môn học'], tablefmt='grid'))
        while True:
            ma_monhoc = input("Xin vui lòng nhập mã môn học cần thay đổi: ")
            cursor.execute(f"SELECT * FROM Subject WHERE MMH = '{ma_monhoc}';")
            if cursor.fetchone():
                print(f"Mã môn học {ma_monhoc} này tồn tại trong cơ sở dữ liệu.")
                ma_mh_thaydoi = input("Nhập vào môn học muốn thay đổi : ")
                ma_sinhvien = input("Nhập vào mã sinh viên: ")
                cursor.execute("UPDATE Registration SET Ma_MonHoc = ? WHERE Ma_SV = ?", (ma_mh_thaydoi, ma_sinhvien))
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã cập nhật thông tin lớp thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {ma_monhoc} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục cập nhật? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã nhập sai thông tin hoặc vi phạm ràng buộc")


def db_nhapdiem():  # Thêm điểm
    try:
        cursor.execute("SELECT * FROM Registration")
        result = cursor.fetchall()
        table = [list(row) for row in result]
        print(tabulate(table, headers=["Mã đăng ký","Ngày đăng ký", "Mã sinh viên", "Mã môn học"], tablefmt='grid'))
        while True:
            sc.input_score()
            cursor.execute(f"SELECT * FROM Registration WHERE Ma_MonHoc = '{sc.ma_monh}' AND MA_SV = '{sc.ma_sinhv}';")
            if cursor.fetchone():
                print(f"Mã {sc.ma_monh} này đã được đăng ký bởi {sc.ma_sinhv}.")
                cursor.execute("INSERT INTO Score(MaDiem,Ma_sinhvien,Ma_MH,DiemThi) VALUES(?,?,?,?)", sc.madiem,
                               sc.ma_sinhv, sc.ma_monh, sc.diemthi)
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã cập nhật thông tin điểm thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {sc.ma_monh} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã môn học? (Y/N): ")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục đăng ký? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã vi phạm ràng buộc")


def db_suadiem():
    try:
        cursor.execute('SELECT * FROM Score')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã điểm', 'Mã sinh viên ', 'Mã môn học', 'Điểm Thi', 'Trạng thái'], tablefmt='grid'))
        while True:
            ma_monhoc = input("Xin vui lòng nhập mã môn học cần thay đổi: ")
            cursor.execute(f"SELECT * FROM Subject WHERE MMH = '{ma_monhoc}';")
            if cursor.fetchone():
                print(f"Mã môn học {ma_monhoc} này tồn tại trong cơ sở dữ liệu.")
                ma_sinhvien = input("Nhập vào mã sinh viên: ")
                so_diem = input("Số điểm muốn thay đổi: ")
                cursor.execute("UPDATE Score SET DiemThi = ? WHERE Ma_sinhvien = ? AND Ma_MH = ?",
                               (so_diem, ma_sinhvien, ma_monhoc))
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã cập nhật thông tin lớp thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {ma_monhoc} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã sinh viên? (Y/N)")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục cập nhật? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã nhập sai thông tin hoặc vi phạm ràng buộc")


def db_xoadiem():
    try:
        cursor.execute('SELECT * FROM Score')
        results = cursor.fetchall()
        table = [list(row) for row in results]
        print(tabulate(table, headers=['Mã điểm', 'Mã sinh viên ', 'Mã môn học', 'Điểm Thi', 'Trạng thái'], tablefmt='grid'))
        while True:
            ma_diem = input("Xin vui lòng nhập mã điểm: ")
            cursor.execute(f"SELECT * FROM Score WHERE MaDiem = '{ma_diem}';")
            if cursor.fetchone():
                print(f"Mã {ma_diem} này tồn tại trong cơ sở dữ liệu.")
                ma_sinhv = input("Nhập vào mã sinh viên: ")
                ma_mh = input("Nhập vào mã môn học")
                cursor.execute(f"DELETE FROM Score WHERE Ma_sinhvien= '{ma_sinhv}' AND Ma_MH = '{ma_mh}';")
                sql_connection.commit()
                print("----------------------------------------------------------------------")
                print("Bạn đã xóa thông tin đăng ký thành công")
                print("----------------------------------------------------------------------")
            else:
                print(f"Mã {ma_diem} này không tồn tại trong cơ sở dữ liệu.")
                choice = input("Bạn có muốn nhập lại mã môn học? (Y/N): ")
                if choice == "N" or choice == "n":
                    break
            n = input("Bạn có muốn tiếp tục xóa? Y/N: ")
            if n == "N" or n == "n":
                break
    except:
        print("Bạn có thể đã vi phạm ràng buộc")
def main():
    global check, idea, num_choice, results, table, cursor
    while True:
        print("--------------------MENU----------------------")
        print("----------------CHỨC NĂNG THÊM----------------")
        print("1. Nhập thông tin lớp")
        print("2. Nhập thông tin sinh viên")
        print("3. Nhập thông tin môn học  ")
        print("-----------------CHỨC NĂNG IN-----------------")
        print("4. In thông tin lớp")
        print("5. In thông tin sinh viên")
        print("6. In danh sách môn học  ")
        print("-----------------CHỨC NĂNG XÓA-----------------")
        print("7. Xóa một lớp ")
        print("8. Xóa thông tin sinh viên")
        print("9. Xóa thông tin môn học  ")
        print("------------------TÌM KIẾM---------------------")
        print("10. Tìm thông tin lớp")
        print("11. Tìm thông tin sinh viên")
        print("12. Tìm thông tin môn học")
        print("--------------CẬP NHẬT THÔNG TIN----------------")
        print("13. Cập nhật thông tin lớp")
        print("14. Cập nhật thông tin sinh viên")
        print("15. Cập nhật thông tin môn học")
        print("------------SINH VIÊN ĐĂNG KÝ MÔN--------------")
        print("16. Sinh viên đăng ký môn")
        print("17. Sinh viên hủy môn đăng ký")
        print("18. Sinh viên sửa thông tin đăng ký")
        print("19. Sinh viên xem thông tin đăng ký trước.")
        print("20. In toàn bộ danh sách tình trạng đăng ký môn")
        print("-------------------NHẬP ĐIỂM-------------------")
        print("21. Giáo viên nhập điểm")
        print("22. Xem điểm")
        print("23. Sửa điểm")
        print("24. Xóa điểm")
        print("25. In danh sách điểm")
        print("-------------------THỐNG KÊ--------------------")
        print("26. Thống kê")
        print("27. Kiểm ta sinh viên A đăng ký bao nhiêu môn")
        print("28. Vẽ biểu đồ thống kê số lương nam và nữ trong lớp bằng matplotlib (barchart)")
        print("29. Vẽ biểu đồ thống kê số lương nam và nữ của từng lớp bằng matplotlib (linechart)")
        print("30. Vẽ biểu đồ thống kê số lượng sinh viên đăng ký theo môn học matplotlib (pie chart)")
        print("-------------------THOÁT-----------------------")
        print("31. Thoát")
        print("------------------------------------------------")
        choice = input("Nhập lựa chọn của bạn: ")
        if choice == "1":
            dbclass()
        elif choice == "2":
            while dbstudent() == 0:
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn nhập lại thông tin sinh viên? Y/N")
                    if a == "Y" or a == "y":
                        dbstudent()
                    else:
                        break
                break
        elif choice == "3":
            while dbsubject() == 0:
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn nhập lại thông tin môn học? Y/N")
                    if a == "Y" or a == "y":
                        dbsubject()
                    else:
                        break
                break
        elif choice == "4":
            while True:
                print("4.1 In ra lớp vừa thêm")
                print("4.2 In ra toàn bộ danh sách lớp")
                print("4.3 Trở lại menu")
                print("4.4 Thoát chương trình")
                num_choice = input("Bạn muốn in loại danh sách nào? 4.1/4.2: ")
                if num_choice == "4.1":
                    if lp.print_class() is None:
                        print("Bạn chưa nhập bất kỳ nội dung nào trước đó")
                    else:
                        lp.print_class()
                elif num_choice == "4.2":
                    cursor.execute('SELECT * FROM Class')
                    results = cursor.fetchall()
                    table = [list(row) for row in results]
                    print(tabulate(table, headers=['Mã lớp', 'Số Lượng', 'Tên lớp'], tablefmt='grid'))
                elif num_choice == "4.3":
                    break
                elif num_choice == "4.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")
        elif choice == "5":
            while True:
                print("5.1 In ra thông tin sinh viên vừa thêm")
                print("5.2 In ra toàn bộ danh sách sinh viên")
                print("5.3 Trở lại menu")
                print("5.4 Thoát chương trình")
                num_choice = input("Bạn muốn in loại danh sách nào? 5.1/5.2: ")
                if num_choice == "5.1":
                    if sv.print_info_st() is None:
                        print("Bạn chưa nhập thông tin sinh viên trước đó")
                    else:
                        sv.print_info_st()
                elif num_choice == "5.2":
                    cursor.execute('SELECT * FROM Student')
                    results = cursor.fetchall()  # Tạo ra bản ghi SQL
                    table = [list(row) for row in results]
                    print(tabulate(table, headers=['MSSV', 'Họ tên', 'Ngày sinh', 'Phái', 'SDT', 'CCCD', 'Email', 'Mã lớp', 'Ngày nhập học'], tablefmt='grid'))
                elif num_choice == "5.3":
                    break
                elif num_choice == "5.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")
        elif choice == "6":
            while True:
                print("6.1 In ra môn học vừa thêm")
                print("6.2 In ra toàn bộ danh sách môn học")
                print("6.3 Trở lại menu")
                print("6.4 Thoát chương trình")
                num_choice = input("Bạn muốn in loại danh sách nào? 6.1/6.2: ")
                if num_choice == "6.1":
                    if sb.print_name_sub() is None:
                        print("Bạn chưa nhập thông tin môn học nào trước đó")
                    else:
                        sb.print_name_sub()
                elif num_choice == "6.2":
                    cursor.execute('SELECT * FROM Subject')
                    results = cursor.fetchall()  # Tạo ra bản ghi SQL
                    table = [list(row) for row in results]
                    print(tabulate(table, headers=['MMH', 'Tên môn'], tablefmt='grid'))
                elif num_choice == "6.3":
                    break
                elif num_choice == "6.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")
        elif choice == "7":
            while dbremove_id_class() == 0:  # Thực hiện xóa lớp, hãy chắc chắn rằng lớp đó không có học sinh nào
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn thực hiện lại thao tác xóa? Y/N: ")
                    if a == "Y" or a == "y":
                        dbremove_id_class()
                    else:
                        break
                break
        elif choice == "8":
            while dbremove_id_student() == 0:  # Thực hiện xóa lớp, hãy chắc chắn rằng lớp đó không có học sinh nào
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn thực hiện lại thao tác xóa? Y/N: ")
                    if a == "Y" or a == "y":
                        dbremove_id_student()
                    else:
                        break
                break
        elif choice == "9":
            while db_remove_sb() == 0:  # Thực hiện xóa lớp, hãy chắc chắn rằng lớp đó không có học sinh nào
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn thực hiện lại thao tác xóa? Y/N: ")
                    if a == "Y" or a == "y":
                        db_remove_sb()
                    else:
                        break
                break
        elif choice == "10":
            while True:
                print("10.1 Tìm kiếm lớp theo mã ")
                print("10.2 Tìm kiếm lớp theo tên ")
                print("10.3 Trở về menu")
                print("10.4 Thoát chương trình")
                num_choice = input("Bạn muốn tìm kiếm theo phương pháp nào? 10.1/10.2: ")
                if num_choice == "10.1":
                    try:
                        a = input("Nhập vào mã lớp cần tìm kiếm thông tin: ")
                        cursor.execute(f"SELECT * FROM Class WHERE Malop=N'{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['Mã môn học', 'Tên môn'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai mã lớp")
                elif num_choice == "10.2":
                    try:
                        a = input("Nhập vào tên lớp cần tìm kiếm thông tin: ")
                        cursor.execute(f"SELECT * FROM Class WHERE TenLop=N'{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['Mã môn học', 'Tên môn'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai tên lớp")
                elif num_choice == "10.3":
                    break
                elif num_choice == "10.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")
        elif choice == "11":
            while True:
                print("11.1 Tìm kiếm sinh viên theo mã ")
                print("11.2 Tìm kiếm sinh viên theo tên ")
                print("11.3 Trở về menu")
                print("11.4 Thoát chương trình")
                num_choice = input("Bạn muốn tìm kiếm theo phương pháp nào? 11.1/11.2: ")
                if num_choice == "11.1":
                    try:
                        a = input("Nhập vào mã sinh viên cần tìm kiếm thông tin: ")
                        cursor.execute(f"SELECT * FROM Student WHERE MSSV='{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['MSSV', 'Họ tên', 'Ngày sinh', 'Phái', 'SDT', 'CCCD', 'Email', 'Mã lớp', 'Ngày nhập học'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai mã lớp")
                elif num_choice == "11.2":
                    try:
                        a = input("Nhập vào họ tên sinh viên cần tìm kiếm thông tin: ")
                        cursor.execute(f"SELECT * FROM Student WHERE HoTen=N'{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['MSSV', 'Họ tên', 'Ngày sinh', 'Phái', 'SDT', 'CCCD', 'Email', 'Mã lớp', 'Ngày nhập học'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai tên lớp")
                elif num_choice == "11.3":
                    break
                elif num_choice == "11.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")

        elif choice == "12":
            while True:
                print("12.1 Tìm kiếm sinh viên theo mã ")
                print("12.2 Tìm kiếm sinh viên theo tên ")
                print("12.3 Trở về menu")
                print("12.4 Thoát chương trình")
                num_choice = input("Bạn muốn tìm kiếm theo phương pháp nào? 12.1/12.2: ")
                if num_choice == "12.1":
                    try:
                        a = input("Nhập vào mã môn học cần tìm: ")
                        cursor.execute(f"SELECT * FROM Subject WHERE MMH='{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['Mã môn học', 'Tên môn học'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai mã lớp")
                elif num_choice == "12.2":
                    try:
                        a = input("Nhập vào tên môn học cần tìm: ")
                        cursor.execute(f"SELECT * FROM Subject WHERE TenMH=N'{a}';")
                        results = cursor.fetchall()  # Tạo ra bản ghi SQL
                        table = [list(row) for row in results]
                        print(tabulate(table, headers=['Mã môn học', 'Tên môn học'], tablefmt='grid'))
                    except:
                        print("Không có lớp mà bạn tìm hoặc bạn nhập sai tên lớp")
                elif num_choice == "12.3":
                    break
                elif num_choice == "12.4":
                    sql_connection.close()
                    quit()
                else:
                    print("Bạn đã chọn sai chỉ mục")
        elif choice == "13":
            db_update_class()
        elif choice == "14":
            db_update_sv()
        elif choice == "15":
            db_update_sb()
        elif choice == "16":
            db_registration_sub()
        elif choice == "17":
            while db_registration_sub_remove() == 0:
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn nhập lại thông tin lớp? Y/N")
                    if a == "Y" or a == "y":
                        db_registration_sub_remove()
                    else:
                        break
                break
        elif choice == "18":
            db_registration_sub_update()
        elif choice == "19":
            if regis.xem_tinhtrang_dk() is None:
                print("Bạn chưa nhập bất kỳ nội dung nào trước đó")
            else:
                regis.xem_tinhtrang_dk()
        elif choice == "20":
            cursor.execute("SELECT * FROM Registration;")
            results = cursor.fetchall()  # Tạo ra bản ghi SQL
            table = [list(row) for row in results]
            print(tabulate(table, headers=['Mã đăng ký', 'Ngày đăng ký', 'Mã sinh viên', 'Mã môn học'], tablefmt='grid'))

        elif choice == "21":
            db_nhapdiem()
        elif choice == "22":
            sc.print_score()
        elif choice == "23":
            while db_suadiem() == 0:
                if check == 1:
                    break
                else:
                    a = input("Bạn có muốn nhập lại thông tin lớp? Y/N")
                    if a == "Y" or a == "y":
                        db_suadiem()
                    else:
                        break
                break
        elif choice == "24":
            db_xoadiem()
        elif choice == "25":
            cursor.execute("SELECT * FROM Score;")
            results = cursor.fetchall()  # Tạo ra bản ghi SQL
            table = [list(row) for row in results]
            print(tabulate(table, headers=['Mã điểm', 'Mã sinh viên', 'Mã môn học', 'Điểm thi', 'Trạng Thái'], tablefmt='grid'))
        elif choice == "26":
            # Tổng số lượng học sinh
            cursor.execute("Select COUNT(*) FROM Student")
            count = cursor.fetchone()[0]
            # Tổng số lượng lớp
            cursor.execute("Select COUNT(*) FROM Class")
            count_class = cursor.fetchone()[0]
            # Tổng số lượng môn học
            cursor.execute("Select COUNT(*) FROM Subject")
            count_sub = cursor.fetchone()[0]
            # Lớp có nhiều sinh viên nhất
            cursor.execute("SELECT c.Malop, COUNT(*) AS SoLuongHocSinh FROM Student s JOIN Class c ON s.Ma_Lop = c.Malop GROUP BY c.Malop ORDER BY SoLuongHocSinh DESC")
            max_sv = cursor.fetchone()
            # Lớp có ít sinh viên nhất
            cursor.execute("SELECT c.Malop, COUNT(*) AS SoLuongHocSinh FROM Student s JOIN Class c ON s.Ma_Lop = c.Malop GROUP BY c.Malop ORDER BY SoLuongHocSinh ASC")
            min_class = cursor.fetchone()
            # Môn có số lượng học sinh đăng ký nhiều nhất
            cursor.execute("SELECT Ma_MonHoc, COUNT(*) AS SoLuong FROM Registration GROUP BY Ma_MonHoc;")
            sub_max = cursor.fetchone()
            # Môn có số lượng sinh viên đăng ký ít nhất
            cursor.execute("SELECT Ma_MonHoc, COUNT(*) AS SoLuong From Registration GROUP BY Ma_MonHoc ORDER BY SoLuong ASC;")
            sub_min = cursor.fetchone()
            # Số lượng học sinh đậu
            cursor.execute("SELECT Count(Ma_sinhvien) as SL FROM Score WHERE TrangThai = N'đậu'")
            good_score = cursor.fetchone()
            # Số lượng sinh viên rớt
            cursor.execute("SELECT Count(Ma_sinhvien) as SL FROM Score WHERE TrangThai = N'rớt'")
            bad_score = cursor.fetchone()
            print("----------------------------------------------------------------------------")
            print("Tổng số học sinh: ", count)
            print("Tổng số lượng lớp: ", count_class)
            print("Tổng số lượng môn học: ", count_sub)
            print("Lớp có số lượng sinh viên nhiều nhất hiện tại là:", max_sv[0], "với", max_sv[1], "sinh viên")
            print("Lớp có số lượng sinh viên ít nhất hiện tại là:", min_class[0], "với", min_class[1], "sinh viên")
            print("Môn học có số lượng sinh viên đăng ký nhiều nhất là:", sub_max[0].strip(), "với", sub_max[1], "sinh viên")
            print("Môn học có số lượng sinh viên đăng ký ít nhất là:", sub_min[0].strip(), "với", sub_min[1],"sinh viên")
            print("Số lượng sinh viên đậu:", good_score[0])
            print("Số lượng sinh viên rớt:", bad_score[0])
            print("----------------------------------------------------------------------------")
        elif choice == "27":
            print("Bạn muốn xem sinh viên nào đăng kí bao nhiêu môn?")
            n_sinhvien = input("Nhập vào mã sinh viên cần tìm: ")
            cursor.execute(f"SELECT Ma_SV,COUNT(Ma_MonHoc) AS SL_MonDK FROM Registration WHERE Ma_SV = '{n_sinhvien}' GROUP BY Ma_SV")
            d_sach = cursor.fetchone()
            print("Sinh viên", d_sach[0], "đăng ký", d_sach[1], "môn")
        elif choice == "28":
            print("Số lượng nam và nữ của các các lớp")
            params = urllib.parse.quote_plus("Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-HB875Q1;Database=QLSV;Trusted_Connection=yes;")
            engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
            query = "SELECT Phai, COUNT(Phai) as SL FROM Student Group By Phai"
            df = pd.read_sql_query(query, engine)
            # Vẽ biểu đồ cột
            plt.bar(df['Phai'], df['SL'])
            plt.title('Số lượng học sinh nam và nữ')
            plt.xlabel('Giới tính')
            plt.ylabel('Số lượng')
            plt.show()
        elif choice == "29":
            print('Số lượng nam nữ của từng lớp')
            params = urllib.parse.quote_plus("Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-HB875Q1;Database=QLSV;Trusted_Connection=yes;")
            engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
            query = "SELECT Ma_Lop,Phai, COUNT(Phai) as SL FROM Student GROUP BY Ma_Lop,Phai"
            df = pd.read_sql_query(query, engine)
            # Tách dữ liệu của nam và nữ ra thành hai bảng riêng
            df_nam = df[df['Phai'] == 'Nam']
            df_nu = df[df['Phai'] == 'Nữ']
            # Vẽ biểu đồ đường
            plt.plot(df_nam['Ma_Lop'], df_nam['SL'], label='Nam')
            plt.plot(df_nu['Ma_Lop'], df_nu['SL'], label='Nữ')
            # Đặt tiêu đề và hiển thị chú thích
            plt.title('Số lượng nam và nữ của từng lớp')
            plt.legend()
            # Hiển thị biểu đồ
            plt.show()
        elif choice == "30":
            cursor = sql_connection.cursor()
            cursor.execute('SELECT Ma_MonHoc, COUNT(*) AS so_luong_MH FROM Registration GROUP BY Ma_MonHoc')
            data = cursor.fetchall()

            values = [row.so_luong_MH for row in data]
            labels = [row.Ma_MonHoc for row in data]

            # Vẽ biểu đồ tròn
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')
            plt.title("Phần trăm số lượng môn học đăng ký của sinh viên so với tỉ lệ đăng ký của trường")

            # Định nghĩa danh sách nhãn mới
            new_labels = ['KTPM: Kiểm thử phần mềm', 'LTNC: Lập trình nâng cao', 'LTW: Lập trình web',
                          'CNPM: Công nghệ phần mềm', 'LTCB: Lập trình cơ bản']

            # Cập nhật lại bảng ghi chú và đặt vị trí ở phía trên bên phải
            plt.legend(labels=new_labels, bbox_to_anchor=(1.0, 1.0), loc='best')

            plt.show()
        elif choice == "31":
            sql_connection.close()
            exit()
        else:
            print("Bạn đã chọn sai chỉ mục")


if __name__ == "__main__":
    main()




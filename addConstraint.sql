-- Kiểm tra phái chỉ có thể là Nam hoặc Nu
ALTER TABLE Student
ADD CONSTRAINT ST_Phai_CHK CHECK (Phai= 'Nam' OR Phai = N'Nữ' OR Phai = 'Nu');
GO
-- Kiểm tra Email phải chứa giá trị @
ALTER TABLE Student
ADD CONSTRAINT ST_Email_CHK CHECK (Email LIKE '%@%');
GO
-- Kiểm tra độ dài của số điện thoại phải bằng 10
ALTER TABLE Student
ADD CONSTRAINT ST_SDT_CHK CHECK (LEN(SDT) = 10);
GO
-- Kiểm tra chữ cái đầu tiên của số điện thoại phải bằng không.
ALTER TABLE Student
ADD CONSTRAINT ST_firstnum_CHK CHECK (LEFT(SDT, 1) = '0')
GO
-- Kiểm tra độ dài CCCD phải bằng 12	
ALTER TABLE Student
ADD CONSTRAINT ST_CCCD_CHK CHECK (LEN(CCCD) = 12);
GO
-- Kiểm tra CCCD, số đầu bằng 0
ALTER TABLE Student
ADD CONSTRAINT ST_firstcccd_CHK CHECK (LEFT(CCCD,1) = '0')
GO
-- Kiểm tra giá trị của SDT chỉ chứa các số 0 đến 9
ALTER TABLE Student
ADD CONSTRAINT ST_sdt_CHK CHECK (SDT NOT LIKE '%[^0-9]%');
GO
-- Kiểm tra giá trị của căn cước công dân chỉ chứa các giá trị từ 0 đến 9
ALTER TABLE Student
ADD CONSTRAINT ST_cccd_CHK CHECK (CCCD NOT LIKE '%[^0-9]%');
GO
-- Kiểm tra giá trị của độ dài của MSSV phải bằng 10	
ALTER TABLE Student
ADD CONSTRAINT ST_MSSV_CHK CHECK (LEN(MSSV) = 10);
GO
-- Kiểm tra điểm thi 0 đến 10
ALTER TABLE Score
ADD CONSTRAINT ST_DiemThi_CHK CHECK (DiemThi >= 0 AND DiemThi <= 10)
GO
-- Ngày nhập học phải lớn hơn ngày sinh 18 năm
ALTER TABLE Student
ADD CONSTRAINT ST_Ngaynhaphoc_CHK CHECK (DATEDIFF(yy, NgaySinh, Ngaynhaphoc) >= 18);
GO 


-- Tạo hàm Scalar
CREATE FUNCTION GetStudentDateOfAdmission (@mssv INT)
RETURNS DATE
AS
BEGIN
DECLARE @date DATE
SELECT @date = Ngaynhaphoc FROM Student WHERE MSSV = @mssv
RETURN @date
END

-- Năm đăng ký môn học phải lớn hơn ngày nhập học
ALTER TABLE Registration
ADD CONSTRAINT RG_ngaydangky_CHK CHECK (DATEDIFF(yy, dbo.GetStudentDateOfAdmission(Ma_SV), ngaydangky) >= 0)


-- Tạo trigger để tự động update trạng thái đậu hoặc rớt
CREATE TRIGGER update_status
ON Score
AFTER INSERT, UPDATE
AS
BEGIN
    UPDATE Score
    SET TrangThai = CASE 
                        WHEN Score.DiemThi>= 4 THEN N'đậu'
                        ELSE N'rớt'
                    END
    FROM Score
    JOIN inserted ON Score.Ma_sinhvien = inserted.Ma_sinhvien AND Score.Ma_MH = inserted.Ma_MH
END





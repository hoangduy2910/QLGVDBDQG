from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from app import db, admin
from flask_admin import BaseView, expose
from flask_login import UserMixin


class DoiBong(db.Model):
    __tablename__ = "doibong"

    MaDB = Column(Integer, primary_key=True, autoincrement=True)
    TenDB = Column(String(100), nullable=False)
    SanNha = Column(String(255), nullable=False)
    DiaDiem = Column(String(255), nullable=False)
    CauThu = relationship('CauThu', backref='doibong', lazy=True)
    HuanLuyenVien = relationship('HuanLuyenVien', backref='doibong', lazy=True)
    KetQuaTranDau = relationship('KetQuaTranDau', backref='doibong', lazy=True)

    def __str__(self):
        return self.TenDB


class HuanLuyenVien(db.Model):
    __tablename__ = "huanluyenvien"

    MaHLV = Column(Integer, primary_key=True, autoincrement=True)
    TenHLV = Column(String(100), nullable=False)
    NgaySinh = Column(DateTime, nullable=False)
    GhiChu = Column(String(255), nullable=True)
    MaDB = Column(Integer, ForeignKey(DoiBong.MaDB), nullable=False)

    def __str__(self):
        return self.TenHLV


class LoaiCauThu(db.Model):
    __tablename__ = "loaicauthu"

    MaLCT = Column(Integer, primary_key=True, autoincrement=True)
    TenLCT = Column(String(100), nullable=False)
    CauThu = relationship('CauThu', backref='loaicauthu', lazy=True)

    def __str__(self):
        return self.TenLCT


class CauThu(db.Model):
    __tablename__ = "cauthu"

    MaCT = Column(Integer, primary_key=True, autoincrement=True)
    TenCT = Column(String(100), nullable=False)
    NgaySinh = Column(DateTime, nullable=False)
    GhiChu = Column(String(255), nullable=True)
    MaLCT = Column(Integer, ForeignKey(LoaiCauThu.MaLCT), nullable=False)
    MaDB = Column(Integer, ForeignKey(DoiBong.MaDB), nullable=False)
    BanThang = relationship('BanThang', backref='cauthu', lazy=True)

    def __str__(self):
        return self.TenCT


class GiaiDau(db.Model):
    __tablename__ = "giaidau"

    MaGD = Column(Integer, primary_key=True, autoincrement=True)
    TenGD = Column(String(100), nullable=False)
    VongDau = relationship('VongDau', backref='giaidau', lazy=True)

    def __str__(self):
        return self.TenGD


class VongDau(db.Model):
    __tablename__ = "vongdau"

    MaVD = Column(Integer, primary_key=True, autoincrement=True)
    TenVD = Column(String(100), nullable=False)
    MaGD = Column(Integer, ForeignKey(GiaiDau.MaGD), nullable=False)
    TranDau = relationship('TranDau', backref='vongdau', lazy=True)

    def __str__(self):
        return self.TenVD


class TranDau(db.Model):
    __tablename__ = "trandau"

    MaTD = Column(Integer, primary_key=True, autoincrement=True)
    MaVD = Column(Integer, ForeignKey(VongDau.MaVD), nullable=False)
    DoiNha = Column(Integer, ForeignKey(DoiBong.MaDB), nullable=False)
    DoiKhach = Column(Integer, ForeignKey(DoiBong.MaDB), nullable=False)
    SanTD = Column(String(255), nullable=False)
    NgayTD = Column(DateTime, nullable=False)
    KetQuaTranDau = relationship('KetQuaTranDau', backref='trandau', lazy=True)

    def __str__(self):
        return self.MaVD + " - " + self.DoiNha + " - " + self.DoiKhach


class LoaiBanThang(db.Model):
    __tablename__ = "loaibanthang"

    MaLBT = Column(Integer, primary_key=True, autoincrement=True)
    TenLBT = Column(String(100), nullable=False)

    def __str__(self):
        return self.TenLBT


class BanThang(db.Model):
    __tablename__ = "banthang"

    MaBT = Column(Integer, primary_key=True, autoincrement=True)
    MaLBT = Column(Integer, ForeignKey(LoaiBanThang.MaLBT), nullable=False)
    MaCT = Column(Integer, ForeignKey(CauThu.MaCT), nullable=False)
    MaTD = Column(Integer, ForeignKey(TranDau.MaTD), nullable=False)
    ThoiDiem = Column(DateTime, nullable=False)

    def __str__(self):
        return self.MaLBT + " - " + self.MaCT + " - " + self.MaTD


class LoaiKetQua(db.Model):
    __tablename__ = "loaiketqua"

    MaLKQ = Column(Integer, primary_key=True, autoincrement=True)
    TenLKQ = Column(String(100), nullable=False)

    def __str__(self):
        return self.TenLKQ


class KetQuaTranDau(db.Model):
    __tablename__ = "ketquatrandau"

    MaKQ = Column(Integer, primary_key=True, autoincrement=True)
    MaTD = Column(Integer, ForeignKey(TranDau.MaTD), nullable=False)
    MaDB = Column(Integer, ForeignKey(DoiBong.MaDB), nullable=False)
    MaLKQ = Column(Integer, ForeignKey(LoaiKetQua.MaLKQ), nullable=False)

    def __str__(self):
        return self.MaTD + " - " + self.MaDB + " - " + self.MaLKQ


class QuyDinh(db.Model):
    __tablename__ = "quydinh"

    MaQD = Column(Integer, primary_key=True, autoincrement=True)
    TenQD = Column(String(100), nullable=False)
    SoQD = Column(Integer, nullable=False)
    GhiChu = Column(String(255), nullable=True)

    def __str__(self):
        return self.TenQD + " - " + self.SoQD + " - "


class DoiBongModelView(ModelView):
    column_display_pk = True
    form_columns = ('TenDB', 'SanNha', 'DiaDiem')
    create_modal = True
    can_view_details = True


class HlvModelView(ModelView):
    column_display_pk = True
    create_modal = True
    can_view_details = True
    list_template = 'create-league.html'


class LoaiCauThuModelView(ModelView):
    create_modal = True


class CauThuModelView(ModelView):
    create_modal = True


class GiaiDauModelView(ModelView):
    create_modal = True


class VongDauModelView(ModelView):
    create_modal = True


class TranDauModelView(ModelView):
    create_modal = True


class LoaiBanThangModelView(ModelView):
    create_modal = True


class BanThangModelView(ModelView):
    create_modal = True


class LoaiKetQuaModelView(ModelView):
    create_modal = True


class KetQuaModelView(ModelView):
    create_modal = True


class QuyDinhModelView(ModelView):
    create_modal = True


admin.add_view(DoiBongModelView(DoiBong, db.session, category="Quản lý đội bóng"))
admin.add_view(HlvModelView(HuanLuyenVien, db.session, category="Quản lý đội bóng"))
admin.add_view(CauThuModelView(CauThu, db.session, category="Cầu thủ"))
admin.add_view(LoaiCauThuModelView(LoaiCauThu, db.session, category="Cầu thủ"))
admin.add_view(GiaiDauModelView(GiaiDau, db.session, category="Thông tin về giải đấu"))
admin.add_view(VongDauModelView(VongDau, db.session, category="Thông tin về giải đấu"))
admin.add_view(TranDauModelView(TranDau, db.session, category="Thông tin về giải đấu"))
admin.add_view(BanThangModelView(BanThang, db.session, category="Kết quả"))
admin.add_view(LoaiBanThangModelView(LoaiBanThang, db.session, category="Kết quả"))
admin.add_view(LoaiKetQuaModelView(LoaiKetQua, db.session, category="Kết quả"))
admin.add_view(KetQuaModelView(KetQuaTranDau, db.session, category="Kết quả"))
admin.add_view(QuyDinhModelView(QuyDinh, db.session, category="Quy Định"))


class HomeAdmin(BaseView):
    @expose('/')
    def index (self):
        return self.render('admin/About us.html')


admin.add_view(HomeAdmin(name="About Us"))


# Tạo chức năng Login cho Admin
# Tạo bảng user
class User(db.Model, UserMixin): # Đa kế thừa
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True) # autoincrement: tăng tự động
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()

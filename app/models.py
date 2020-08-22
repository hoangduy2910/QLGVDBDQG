from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from app import db, admin


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

# Tạo các trang admin
    admin.add_view(ModelView(DoiBong, db.session))
    admin.add_view(ModelView(HuanLuyenVien, db.session))
    admin.add_view(ModelView(LoaiCauThu, db.session))
    admin.add_view(ModelView(CauThu, db.session))
    admin.add_view(ModelView(GiaiDau, db.session))
    admin.add_view(ModelView(VongDau, db.session))
    admin.add_view(ModelView(TranDau, db.session))
    admin.add_view(ModelView(LoaiBanThang, db.session))
    admin.add_view(ModelView(BanThang, db.session))
    admin.add_view(ModelView(LoaiKetQua, db.session))
    admin.add_view(ModelView(KetQuaTranDau, db.session))

    # NameError: name
    # 'QuyDinh' is not defined ???
    # admin.add_view(ModelView(QuyDinh, db.session))


if __name__ == "__main__":
    db.create_all()

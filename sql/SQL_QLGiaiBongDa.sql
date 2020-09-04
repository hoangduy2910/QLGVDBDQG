/* Loại bàn thắng */
insert into db_qlgiaibongda.type_goal (name) values ('Trực tiếp'), ('Phản lưới nhà'), ('Đá phạt'), ('Đá phạt đền');

/* Loại cầu thủ */
insert into db_qlgiaibongda.type_player (name) values ('Cầu thủ trong nước'), ('Cầu thủ ngoài nước');

/* Loại kết quả */
insert into db_qlgiaibongda.type_result (name) values ('Thắng'), ('Hòa'), ('Thua');

/* Giới tính */
insert into db_qlgiaibongda.gender (name) values ('Nam'), ('Nữ');

/* Trình độ */
insert into db_qlgiaibongda.level (name) values ('Chuyên nghiệp'), ('Bán chuyên'), ('Cao cấp'), ('Trung cấp'), ('Vui');

/* Trạng thái xét duyệt */
insert into db_qlgiaibongda.status (name, color) values ('Đang duyệt', 'primary'), ('Chấp nhận', 'success'), ('Từ chối', 'danger');

/* Giải đấu */
insert into db_qlgiaibongda.league values (1, 'Bóng Đá Nam OU', '217 Lý Thường Kiệt', '', 1, 31, NOW(), NOW() + INTERVAL 1 DAY, 2);

/* Đội bóng*/
insert into db_qlgiaibongda.club values (1, 'DH17TH02', '1231231231', 'HCM', '', 1, 4, 3), (2, 'DH17TH03', '4565464564', 'HCM', '', 1, 4, 4);

/* Đội bóng tham gia giải đấu */
insert into db_qlgiaibongda.league_club values (1, 1, 1, 2), (2, 1, 2, 2);

/* Người dùng */
insert into db_qlgiaibongda.user (name, username, password, phone, birthday, active, user_role) values
('admin', 'admin', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-01-01', 1, 2),
('user1', 'user1', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-01-01', 1, 1),
('user2', 'user2', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-02-02', 1, 1),
('user3', 'user3', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-02-02', 1, 1);

/* Các tỉnh thành */
insert into db_qlgiaibongda.city (name) values
('An Giang'),
('Bà Rịa – Vũng Tàu'),
('Bắc Giang'),
('Bắc Kạn'),
('Bạc Liêu'),
('Bắc Ninh'),
('Bến Tre'),
('Bình Định'),
('Bình Dương'),
('Bình Phước'),
('Bình Thuận'),
('Cà Mau'),
('Cao Bằng'),
('Cần Thơ'),
('Đà Nẵng'),
('Đắk Lắk'),
('Đắk Nông'),
('Điện Biên'),
('Đồng Nai'),
('Đồng Tháp'),
('Gia Lai'),
('Hà Giang'),
('Hà Nam'),
('Hà Nội'),
('Hà Tĩnh'),
('Hải Dương'),
('Hải Phòng'),
('Hậu Giang'),
('Hòa Bình'),
('Hưng Yên'),
('Hồ Chí Minh'),
('Khánh Hòa'),
('Kiên Giang'),
('Kon Tum'),
('Lai Châu'),
('Lâm Đồng'),
('Lạng Sơn'),
('Lào Cai'),
('Long An'),
('Nam Định'),
('Nghệ An'),
('Ninh Bình'),
('Ninh Thuận'),
('Phú Thọ'),
('Phú Yên'),
('Quảng Bình'),
('Quảng Nam'),
('Quảng Ngãi'),
('Quảng Ninh'),
('Quảng Trị'),
('Sóc Trăng'),
('Sơn La'),
('Tây Ninh'),
('Thái Bình'),
('Thái Nguyên'),
('Thanh Hóa'),
('Thừa Thiên Huế'),
('Tiền Giang'),
('Trà Vinh'),
('Tuyên Quang'),
('Vĩnh Long'),
('Vĩnh Phúc'),
('Yên Bái')
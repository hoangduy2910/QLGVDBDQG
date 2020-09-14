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
('Yên Bái');

/* Trạng thái xét duyệt */
insert into db_qlgiaibongda.status (name, color) values ('Đang duyệt', 'primary'), ('Chấp nhận', 'success'), ('Từ chối', 'danger');

/* Người dùng */
insert into db_qlgiaibongda.user (name, username, password, phone, birthday, active, user_role) values
('admin', 'admin', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-01-01', 1, 2),
('user1', 'user1', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-01-01', 1, 1),
('user2', 'user2', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-02-02', 1, 1),
('user3', 'user3', '202cb962ac59075b964b07152d234b70', '1234567891', '1998-02-02', 1, 1);

/* Giải đấu */
insert into db_qlgiaibongda.league (name, address, image, gender_id, city_id, date_begin, date_end, user_id, has_scheduled, win_point, draw_point, lose_point) values
('Giải Bóng Đá Nam OU Khóa 2017 (KHMT)', 'Sân Phú Thọ 221 Lý Thường Kiệt, Phường 9, Quận 11', '', 1, 31, NOW(), NOW() + INTERVAL 1 DAY, 2, False, 3, 1, 0);

/* Quy định */
insert into db_qlgiaibongda.rule (min_age, max_age, min_player, max_player, max_foreign_player, league_id) values
(18, 22, 5, 7, 0, 1);

/* Đội bóng*/
insert into db_qlgiaibongda.club (name, phone, address, image, gender_id, level_id, user_id) values
('DH17TH01', '1231231231', 'HCM', '', 1, 4, 3), 
('DH17TH02', '4565464564', 'HCM', '', 1, 4, 3),
('DH17TH03', '4565464564', 'HCM', '', 1, 4, 3),
('DH17TH04', '4565464564', 'HCM', '', 1, 4, 3),
('DH17TH05', '4565464564', 'HCM', '', 1, 4, 3),
('DH17TK01', '4565464564', 'HCM', '', 1, 4, 4),
('DH17TK02', '4565464564', 'HCM', '', 1, 4, 4),
('DH17TK03', '4565464564', 'HCM', '', 1, 4, 4),
('DH17TK04', '4565464564', 'HCM', '', 1, 4, 4),
('DH17TK05', '4565464564', 'HCM', '', 1, 4, 4);

/* Cầu thủ */
insert into db_qlgiaibongda.player (name, birthday, phone, image, type_player_id, club_id) values
('Nguyễn Vân Bình', '1999-01-01', '1231231231', '', 1, 1),
('Bùi Đức Anh', '1999-01-01', '1231231231', '', 1, 1),
('Nguyễn Lê Quốc Bảo', '1999-01-01', '1231231231', '', 1, 1),
('Trần Trí Minh Dũng', '1999-01-01', '1231231231', '', 1, 1),
('Phạm Tiến Đạt', '1999-01-01', '1231231231', '', 1, 1),
('Nguyễn Quang Dũng', '1999-01-01', '1231231231', '', 1, 2),
('Bùi Trần Hoàng Hiệp', '1999-01-01', '1231231231', '', 1, 2),
('Nguyễn Hải Trung Hiếu', '1999-01-01', '1231231231', '', 1, 2),
('Nguyễn Duy Hưng', '1999-01-01', '1231231231', '', 1, 2),
('Trương Đăng Khoa', '1999-01-01', '1231231231', '', 1, 2),
('Trần Trí Kiên', '1999-01-01', '1231231231', '', 1, 3),
('Bùi Hoàng Minh', '1999-01-01', '1231231231', '', 1, 3),
('Dương Khả Minh', '1999-01-01', '1231231231', '', 1, 3),
('Nguyễn Văn Khôi Nguyên', '1999-01-01', '1231231231', '', 1, 3),
('Bùi Hoàng Phúc', '1999-01-01', '1231231231', '', 1, 3),
('Đoàn Ngọc Tấn', '1999-01-01', '1231231231', '', 1, 4),
('Vũ Minh Tú', '1999-01-01', '1231231231', '', 1, 4),
('Nguyễn Đức Anh', '1999-01-01', '1231231231', '', 1, 4),
('Nguyễn Trọng Đạt', '1999-01-01', '1231231231', '', 1, 4),
('Nguyễn Lê  Minh Hiếu', '1999-01-01', '1231231231', '', 1, 4),
('Nguyễn Việt Hưng', '1999-01-01', '1231231231', '', 1, 5),
('Nguyễn Gia Khánh', '1999-01-01', '1231231231', '', 1, 5),
('Đỗ Đức Khôi', '1999-01-01', '1231231231', '', 1, 5),
('Ngô Tiểu Long', '1999-01-01', '1231231231', '', 1, 5),
('Vũ Lại Quang Minh', '1999-01-01', '1231231231', '', 1, 5);


insert into db_qlgiaibongda.league_club (league_id, club_id, status_id) values 
(1, 1, 1), 
(1, 2, 1),
(1, 3, 1),
(1, 4, 1),
(1, 5, 1);
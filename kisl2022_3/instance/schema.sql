DROP TABLE IF EXISTS all_cr;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS lecture_division;

CREATE TABLE all_cr (
  building TEXT NOT NULL,
  support_room TEXT NOT NULL,
  class_room TEXT PRIMARY KEY,
  VTR INTEGER(1) NOT NULL,
  DVD INTEGER(1) NOT NULL,
  projector INTEGER(1) NOT NULL,
  OHP INTEGER(1) NOT NULL,
  screen INTEGER(1) NOT NULL,
  blackout_curtain INTEGER(1) NOT NULL,
  document_camera INTEGER(1) NOT NULL,
  automatic_recording INTEGER(1) NOT NULL,
  remote_lecture INTEGER(1) NOT NULL,
  fixed_desk INTEGER(1) NOT NULL,
  capacity INTEGER(1) NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  book_date TEXT NOT NULL,
  book_lecture INTEGER NOT NULL,
  class_room TEXT NOT NULL,
  book_group TEXT NOT NULL,
  book_matter TEXT NOT NULL
);

CREATE TABLE lecture_division (
  lecture_id INTEGER PRIMARY KEY,
  lecture TEXT UNIQUE NOT NULL
);

INSERT INTO lecture_division VALUES (1,'1限(8:40-9:55)'),
                                    (2,'2限(10:10-11:25)'),
                                    (3,'昼休み(11:25-12:15)'),
                                    (4,'3限(12:15-13:30)'),
                                    (5,'4限(13:45-15:00)'),
                                    (6,'5限(15:15-16:30)'),
                                    (7,'6限(16:45-18:00)'),
                                    (8,'7限(18:15-19:30)'),
                                    (9,'8限(19:45-21:00)');

INSERT INTO all_cr VALUES ('1B棟','人文社会エリア支援室','1B202',0,1,1,0,1,0,0,0,0,0,46),
                          ('2B棟','生命環境エリア支援室','2B206',0,1,1,0,1,1,0,0,0,0,43),
                          ('3A棟','システム情報エリア支援室','3A402',1,1,1,0,1,1,0,1,0,1,202),
                          ('5C棟','体育芸術エリア支援室','5C213',1,1,1,0,1,1,0,1,0,0,219),
                          ('7A棟','図書館情報エリア支援室','7A101',0,0,1,0,1,1,0,0,0,0,70),
                          ('CEGLOC（外国語教育部門）','CEGLOC','9P101',0,1,1,0,1,1,0,0,0,0,10);

INSERT INTO book VALUES (1,1,'2022-05-30',4,'7A101','ばらばら','会議'),
                        (2,1,'2022-05-30',5,'7A101','ばらばら','発表'),
                        (3,1,'2022-05-29',3,'7A101','筑波大学KISL','会議'),
                        (4,1,'2022-05-29',2,'7A101','筑波大学KISL','会議'),
                        (5,1,'2022-05-29',1,'7A101','筑波大学KISL','会議');


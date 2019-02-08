--
-- File generated with SQLiteStudio v3.1.1 on Fri Feb 8 09:54:28 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: province_priority
CREATE TABLE province_priority (
    province TEXT,
    priority REAL
);

INSERT INTO province_priority (province, priority) VALUES ('北京', 0);
INSERT INTO province_priority (province, priority) VALUES ('上海', 5);
INSERT INTO province_priority (province, priority) VALUES ('天津', 0);
INSERT INTO province_priority (province, priority) VALUES ('重庆', 10);
INSERT INTO province_priority (province, priority) VALUES ('河北', 0);
INSERT INTO province_priority (province, priority) VALUES ('江苏', 0);
INSERT INTO province_priority (province, priority) VALUES ('浙江', 8);
INSERT INTO province_priority (province, priority) VALUES ('广东', 0);
INSERT INTO province_priority (province, priority) VALUES ('山西', 6);
INSERT INTO province_priority (province, priority) VALUES ('辽宁', 0);
INSERT INTO province_priority (province, priority) VALUES ('吉林', 1);
INSERT INTO province_priority (province, priority) VALUES ('黑龙江', 7);
INSERT INTO province_priority (province, priority) VALUES ('安徽', 2);
INSERT INTO province_priority (province, priority) VALUES ('福建', 0);
INSERT INTO province_priority (province, priority) VALUES ('江西', 0);
INSERT INTO province_priority (province, priority) VALUES ('山东', 0);
INSERT INTO province_priority (province, priority) VALUES ('河南', 0);
INSERT INTO province_priority (province, priority) VALUES ('湖北', 0);
INSERT INTO province_priority (province, priority) VALUES ('湖南', 0);
INSERT INTO province_priority (province, priority) VALUES ('四川', 9);
INSERT INTO province_priority (province, priority) VALUES ('贵州', 0);
INSERT INTO province_priority (province, priority) VALUES ('云南', 0);
INSERT INTO province_priority (province, priority) VALUES ('陕西', 0);
INSERT INTO province_priority (province, priority) VALUES ('甘肃', 0);
INSERT INTO province_priority (province, priority) VALUES ('青海', 0);
INSERT INTO province_priority (province, priority) VALUES ('内蒙古', 0);
INSERT INTO province_priority (province, priority) VALUES ('广西', 0);
INSERT INTO province_priority (province, priority) VALUES ('海南', 0);
INSERT INTO province_priority (province, priority) VALUES ('西藏', 0);
INSERT INTO province_priority (province, priority) VALUES ('宁夏', 0);
INSERT INTO province_priority (province, priority) VALUES ('新疆', 0);

-- View: vw_numer_region_priority
CREATE VIEW vw_numer_region_priority AS
    SELECT num.phone_num_region,
           num.city,
           num.province,
           p.priority
      FROM number_region num
           JOIN
           province_priority p ON num.province = p.province;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

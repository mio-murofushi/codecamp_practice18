# ドリンク情報
DROP TABLE drink_data;

CREATE TABLE drink_data(
    drink_id INT AUTO_INCREMENT,
    drink_name VARCHAR(20),
    drink_photo VARCHAR(100),
    price INT,
    add_drink_date datetime DEFAULT CURRENT_TIMESTAMP,
    update_drink_date datetime DEFAULT CURRENT_TIMESTAMP,
    publicprivate boolean DEFAULT "0",
    PRIMARY KEY (drink_id)
);

DELETE FROM drink_data;

INSERT INTO drink_data(
    drink_id, drink_name, price, publicprivate, drink_photo
) VALUES
(1, "COLA", 130, 1, "コーラ.jpeg"),
(2, "WATER", 100, 1, "水.jpeg"),
(3, "TEA", 130, 0, "サイダー.jpeg");

# 在庫数管理
DROP TABLE manegiment_drink_number;

CREATE TABLE manegiment_drink_number(
    drink_id INT AUTO_INCREMENT,
    drink_number INT,
    create_managiment_date datetime DEFAULT CURRENT_TIMESTAMP,
    update_managiment_date datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (drink_id)
);

DELETE FROM manegiment_drink_number;
INSERT INTO manegiment_drink_number(
    drink_id, drink_number
) VALUES
(1, 10),
(2, 20),
(3, 3);

# 購入履歴
CREATE TABLE buy_list(
    drink_id INT AUTO_INCREMENT,
    buy_date datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (drink_id)
);

INSERT INTO buy_list(
    drink_id
) VALUES
(1),
(2),
(3);
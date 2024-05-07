-- sql script


CREATE DATABASE IF NOT EXISTS Whisper_db;
       CREATE USER IF NOT EXISTS 'Whisper_user'@'localhost' IDENTIFIED BY 'Whisper_pwd123@';
              GRANT ALL PRIVILEGES ON Whisper_db.* TO 'Whisper_user'@'localhost';
                                      GRANT SELECT ON performance_schema.* TO 'Whisper_user'@'localhost';
FLUSH PRIVILEGES;
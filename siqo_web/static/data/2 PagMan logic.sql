-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE=TRADITIONAL,ALLOW_INVALID_DATES;

-- -----------------------------------------------------
-- Schema PAGMAN
-- -----------------------------------------------------
USE PAGMAN ;
-- -----------------------------------------------------
-- Placeholder table for view VFORUM
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS VFORUM (ITEM_ID INT, PARENT_ID INT, USER_ID INT, FORUM_ID INT, C_FUNC INT, N_LVL INT, TITLE INT, NARRATOR INT, ITEM INT, D_CREATED INT, D_CHANGED INT, WHO INT);

-- -----------------------------------------------------
-- Placeholder table for view SSESS_ADDRESS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS SSESS_ADDRESS (USER_ADDRESS INT, USER_ID INT, N_CNT INT, N_WORK INT, D_FIRST INT, D_LAST INT);

-- -----------------------------------------------------
-- Placeholder table for view SSESS_USER
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS SSESS_USER (USER_ID INT, N_CNT INT, N_WORK INT, D_FIRST INT, D_LAST INT);

-- -----------------------------------------------------
-- View VFORUM
-- -----------------------------------------------------
DROP VIEW IF EXISTS VFORUM ;
DROP TABLE IF EXISTS VFORUM;
CREATE  OR REPLACE VIEW VFORUM AS
SELECT * FROM SITEM
WHERE N_LVL = 0;


-- -----------------------------------------------------
-- View SSESS_ADDRESS
-- -----------------------------------------------------
DROP VIEW IF EXISTS SSESS_ADDRESS ;
DROP TABLE IF EXISTS SSESS_ADDRESS;
CREATE 
   OR REPLACE SQL SECURITY DEFINER 
  
VIEW SSESS_ADDRESS AS  
select 
   USER_ADDRESS 
  ,USER_ID 
  ,COUNT(D_CREATED)                         AS N_CNT 
  ,SEC_TO_TIME(SUM(D_CHANGED-D_CREATED))    AS N_WORK
  ,DATE_FORMAT(MIN(D_CREATED), %d.%m.%Y ) AS D_FIRST
  ,DATE_FORMAT(MAX(D_CREATED), %d.%m.%Y ) AS D_LAST 
  
from SSESSION
  where DATE_ADD( D_CREATED, INTERVAL 30 DAY) >= sysdate()
  GROUP BY USER_ADDRESS, USER_ID
  ORDER BY N_WORK DESC;

-- -----------------------------------------------------
-- View SSESS_USER
-- -----------------------------------------------------
DROP VIEW IF EXISTS SSESS_USER ;
DROP TABLE IF EXISTS SSESS_USER;
CREATE 
   OR REPLACE ALGORITHM=UNDEFINED 
  SQL SECURITY DEFINER 
  
VIEW SSESS_USER AS 
select 
   USER_ID                                  AS USER_ID
  ,COUNT(D_CREATED)                         AS N_CNT 
  ,SEC_TO_TIME(SUM(D_CHANGED-D_CREATED))    AS N_WORK
  ,DATE_FORMAT(MIN(D_CREATED), %d.%m.%Y ) AS D_FIRST 
  ,DATE_FORMAT(MAX(D_CREATED), %d.%m.%Y ) AS D_LAST 
  
from SSESSION 
  where DATE_ADD( D_CREATED, INTERVAL 30 DAY) >= sysdate()
  GROUP BY USER_ID 
  ORDER BY N_WORK DESC;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

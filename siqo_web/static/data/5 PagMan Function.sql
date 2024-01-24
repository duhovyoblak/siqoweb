-- =============================================================================
--                                                      (c) SIQO 18
-- PagMan Basic SQL Functions
--
-- -----------------------------------------------------------------------------
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE=TRADITIONAL,ALLOW_INVALID_DATES;

-- -----------------------------------------------------
-- Schema HASAR
-- Hierarchical associative area memory
-- -----------------------------------------------------
USE PAGMAN;

-- ============================================================================
--                                                         (c) SIQO 2018
-- function STR_OVERLAP
--
-- Vyhlada maximalnu hodnotu poctu prekryvajucich sa znakov
-- dvoch stringov a vrati ju ako zaporne cislo
-- 
-- Ak sa stringy neprekryvaju vrati 0
-- 
-- ============================================================================
DROP function IF EXISTS STR_OVERLAP;

DELIMITER $$

CREATE FUNCTION STR_OVERLAP ( StrB VARCHAR(512), StrR VARCHAR(512) ) RETURNS INT
DETERMINISTIC
SQL SECURITY INVOKER 
BEGIN
  DECLARE pos, len, ovr    INT;

  -- ==========================================================================
  -- Priprava
  
  SET len = CHAR_LENGTH( StrB );
  SET pos = 1;

  -- ==========================================================================
  -- Prechod cez vsetky znaky StrB

  WHILE pos <= len DO
  
    SET ovr = len - pos + 1;
  
    -- Test prekryvu
    IF SUBSTR( StrB, pos, ovr ) = SUBSTR( StrR, 1, ovr ) THEN RETURN -ovr; END IF;

    -- Nasledujuca pozicia v StrB  
    SET pos = pos + 1;

  END WHILE;
    
  RETURN 0;
END$$

DELIMITER ;

-- ============================================================================
-- Koniec kodu
-- -----------------------------------------------------------------------------

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- ==============================KONIEC=SUBORU==================================

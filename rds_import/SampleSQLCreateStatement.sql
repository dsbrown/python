SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema CoLo_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `CoLo_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `CoLo_db` ;

-- -----------------------------------------------------
-- Table `CoLo_db`.`SiteTbl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CoLo_db`.`SiteTbl` ;

CREATE TABLE IF NOT EXISTS `CoLo_db`.`SiteTbl` (
  `SiteId_tbl` INT NOT NULL AUTO_INCREMENT,
  `ClusterName` VARCHAR(45) NOT NULL,
  `ClusterID` VARCHAR(45) NULL,
  `ProjectName` VARCHAR(45) NULL,
  `AWSSiteCode` VARCHAR(45) NULL,
  `VendorName` VARCHAR(45) NULL,
  `VendorSiteName` VARCHAR(45) NULL,
  `VendorSiteAddress` VARCHAR(90) NULL,
  `VendorSiteCity` VARCHAR(45) NULL,
  `VendorSiteState` VARCHAR(45) NULL,
  `VendorSitePostalCode` VARCHAR(45) NULL,
  `VendorSiteCountry` VARCHAR(45) NULL,
  `VendorSiteLatitude` DOUBLE NULL,
  `VendorSiteLongitude` DOUBLE NULL,
  `BizDevSelectDate` DATETIME NULL,
  `InProd` INT NULL,
  `InDev` INT NULL,
  `TypeEC2` INT NULL,
  `TypeCritNet` INT NULL,
  `TypeHPC` INT NULL,
  `TypeVPC` INT NULL,
  `TypeProd` INT NULL,
  `TypeCorp` INT NULL,
  `TypeDX` INT NULL,
  `TypeAIV_CF` INT NULL,
  `TypeTCF_CF` INT NULL,
  `TypeGrumpy` INT NULL,
  `Type_X1` INT NULL,
  `Type_X2` INT NULL,
  `Type_X3` INT NULL,
  `Type_X4` INT NULL,
  `TypeOther` INT NULL,
  `LSEvents` INT NULL,
  `SiteUUID` VARCHAR(128) NULL,
  PRIMARY KEY (`SiteId_tbl`),
  UNIQUE INDEX `SiteId Table_UNIQUE` (`SiteId_tbl` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoLo_db`.`AssessmentResultsTbl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CoLo_db`.`AssessmentResultsTbl` ;

CREATE TABLE IF NOT EXISTS `CoLo_db`.`AssessmentResultsTbl` (
  `idAssessmentTable` INT NOT NULL AUTO_INCREMENT,
  `SiteId` INT NOT NULL,
  `VendorSiteVisitDate` DATETIME NULL,
  `IPSGOEngineer` VARCHAR(45) NULL,
  `BizDevRepresentative` VARCHAR(45) NULL,
  `Ph1ScoreTotal` FLOAT NULL,
  `Ph1ScoreAIA02` FLOAT NULL,
  `Ph1ScoreAIA11` FLOAT NULL,
  `Ph1ScoreAIA21` FLOAT NULL,
  `Ph1ScoreAIA23` FLOAT NULL,
  `Ph1ScoreAIA25` FLOAT NULL,
  `Ph1ScoreAIA26` FLOAT NULL,
  `Ph1ScoreAIA27` FLOAT NULL,
  `Ph1ScoreAIA28` FLOAT NULL,
  `Ph1ScoreAIA33` FLOAT NULL,
  `Ph2ScoreTotal` FLOAT NULL,
  `Ph2ScoreAIA02` FLOAT NULL,
  `Ph2ScoreAIA11` FLOAT NULL,
  `Ph2ScoreAIA21` FLOAT NULL,
  `Ph2ScoreAIA23` FLOAT NULL,
  `Ph2ScoreAIA25` FLOAT NULL,
  `Ph2ScoreAIA26` FLOAT NULL,
  `Ph2ScoreAIA27` FLOAT NULL,
  `Ph2ScoreAIA28` FLOAT NULL,
  `Ph2ScoreAIA33` FLOAT NULL,
  `Ph3ScoreTotal` FLOAT NULL,
  `Ph3ScoreAIA02` FLOAT NULL,
  `Ph3ScoreAIA11` FLOAT NULL,
  `Ph3ScoreAIA21` FLOAT NULL,
  `Ph3ScoreAIA23` FLOAT NULL,
  `Ph3ScoreAIA25` FLOAT NULL,
  `Ph3ScoreAIA26` FLOAT NULL,
  `Ph3ScoreAIA27` FLOAT NULL,
  `Ph3ScoreAIA28` FLOAT NULL,
  `Ph3ScoreAIA33` FLOAT NULL,
  `CompScoreAIA02` FLOAT NULL,
  `CompScoreAIA11` FLOAT NULL,
  `CompScoreAIA21` FLOAT NULL,
  `CompScoreAIA23` FLOAT NULL,
  `CompScoreAIA25` FLOAT NULL,
  `CompScoreAIA26` FLOAT NULL,
  `CompScoreAIA27` FLOAT NULL,
  `CompScoreAIA28` FLOAT NULL,
  `CompScoreAIA33` FLOAT NULL,
  `CompScoreTotal` FLOAT NULL,
  `ReasonsFor` TEXT(16384) NULL,
  `ReasonsAgainst` TEXT(16384) NULL,
  `ShowStoppers` TEXT(16384) NULL,
  `PrelimReportDate` DATETIME NULL,
  `FinalReportDate` DATETIME NULL,
  `SiteDeliverDate` DATETIME NULL,
  `IPSGOSelect` INT NULL,
  `BizDevSelect` INT NULL,
  `BizDevSelectDate` DATETIME NULL,
  `AssessmentGUID` VARCHAR(128) NULL,
  `SiteUUID` VARCHAR(128) NULL,
  PRIMARY KEY (`idAssessmentTable`),
  INDEX `SiteId_idx` (`SiteId` ASC),
  CONSTRAINT `SiteId`
    FOREIGN KEY (`SiteId`)
    REFERENCES `CoLo_db`.`SiteTbl` (`SiteId_tbl`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoLo_db`.`AuditResultsTbl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CoLo_db`.`AuditResultsTbl` ;

CREATE TABLE IF NOT EXISTS `CoLo_db`.`AuditResultsTbl` (
  `idAuditTbl` INT NOT NULL AUTO_INCREMENT,
  `AuditDate` DATETIME NULL,
  `AuditFnlRpt` DATETIME NULL,
  `AuditPrelimRpt` DATETIME NULL,
  `C_SPOFS` INT NULL,
  `C_Risks` INT NULL,
  `SPOFS` INT NULL,
  `Risks` INT NULL,
  `PreviousAI` INT NULL,
  `NewAI` INT NULL,
  `AgreedAI` INT NULL,
  `RemediedAI` INT NULL,
  `SiteId` INT NULL,
  `SiteUUID` VARCHAR(128) NULL,
  `AuditResults` TEXT(16384) NULL,
  `AuditActions` TEXT(16384) NULL,
  PRIMARY KEY (`idAuditTbl`),
  INDEX `SiteIda_idx` (`SiteId` ASC),
  CONSTRAINT `SiteIda`
    FOREIGN KEY (`SiteId`)
    REFERENCES `CoLo_db`.`SiteTbl` (`SiteId_tbl`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoLo_db`.`QuestionTbl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CoLo_db`.`QuestionTbl` ;

CREATE TABLE IF NOT EXISTS `CoLo_db`.`QuestionTbl` (
  `idQuestionTbl` INT NOT NULL AUTO_INCREMENT,
  `QuestionNo` INT NULL,
  `QuestionText` VARCHAR(450) CHARACTER SET 'utf8' NULL,
  `QuestionnaireGUID` VARCHAR(64) NULL,
  `DocEngVersion` FLOAT NULL,
  PRIMARY KEY (`idQuestionTbl`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoLo_db`.`QuestionDetailTbl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CoLo_db`.`QuestionDetailTbl` ;

CREATE TABLE IF NOT EXISTS `CoLo_db`.`QuestionDetailTbl` (
  `idQuestionDetailTbl` INT NOT NULL AUTO_INCREMENT,
  `QId` INT NOT NULL,
  `QuestionNo` INT NULL,
  `VendorResponse` VARCHAR(1024) NULL,
  `VendorComment` VARCHAR(1024) NULL,
  `VendorExtComment` VARCHAR(1024) NULL,
  `PrimaryCategory` INT NULL,
  `SecondaryCategory` INT NULL,
  `TeritaryCategory` INT NULL,
  `QuestionnairePhase` INT NULL,
  `Score` INT NULL,
  `DCEOverrideAnswer` INT NULL,
  `DCEOverrideRescore` INT NULL,
  `DCEOverrideComment` INT NULL,
  `DCEOverrideFlag` INT NULL,
  `QuestionnaireGUID` VARCHAR(128) NULL,
  `AssessmentGUID` VARCHAR(128) NULL,
  `MaxQuestions` INT NULL,
  `DocEngVersion` FLOAT NULL,
  PRIMARY KEY (`idQuestionDetailTbl`),
  CONSTRAINT `QId`
    FOREIGN KEY (`idQuestionDetailTbl`)
    REFERENCES `CoLo_db`.`QuestionTbl` (`idQuestionTbl`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


--
-- Data Base: `SmokeOut - app and startup`
--

-- --------------------------------------------------------

--
-- Structure of table `User`
--
-- It's not storing information about passwords for security reasons
-- especially that the project is aimed to be publicly available for some time
--
CREATE TABLE `User` (
    `UserID` int(10),
    `username` varchar(30),
    `StartTime` datetime2(0),
    `PlanID` int(2),
);
-----------------------------------------------------------
--

-- Structure of table `Usage_Plans`
--
CREATE TABLE `Usage_Plans` (
    `PlanID` int(2),
    `Name` varchar(20),
    `Price` money,
);

-- --------------------------------------------------------

--
-- Structure of table `InApp_User_Data`
--
CREATE TABLE `InApp_User_Data` (
    `InDataID` int
    `UserID` int(10),
    `OpenPckg` datetime2(0),
    `SwitchPckg` datetime2(0),
);

-- --------------------------------------------------------

--
-- Structure of table `InAppReporting`
--
CREATE TABLE `InAppReporting` (
    `ReportID` int
    `UserID` int(10),
    `RepInt` tinyint,
    `PckgOpened` int(10) NULL,
    `PckgSwitch` int(10) NULL,
    `ReportStatus` binary(10),
);

-- --------------------------------------------------------

--
-- Structure of table `ReportStatus`
--
CREATE TABLE `ReportStatus` (
    `ReportID` int
    `ReportStatus` binary(10),
    `Start` datetime2(0),
    `Last` datetime2(0),
    `Current` datetime2(0),
    `Close` binary(1),
);

-- --------------------------------------------------------
--
-- Indexes for Tables:

-- Table `User`
ALTER TABLE `User`
    ADD PRIMARY KEY (`UserID`),
    ADD KEY `FKf8p8s0` (`PlanID`);

-- Table `Usage_Plans`
ALTER TABLE `Usage_Plans`
    ADD PRIMARY KEY (`PlanID`);

-- Table `InApp_User_Data`
ALTER TABLE `InApp_User_Data`
    ADD PRIMARY KEY (`InDataID`),
    ADD KEY `FKqey4eo` (`UserID`);

-- Table `InAppReporting`
ALTER TABLE `InAppReporting`
    ADD PRIMARY KEY (`ReportID`),
    ADD KEY `FKmvey3h` (`UserID`),
    ADD KEY `FKj7pogq` (`ReportStatus`);

-- Table `ReportStatus`
ALTER TABLE `ReportStatus`
    ADD PRIMARY KEY (`ReportStatus`),
    ADD KEY `FKenmj0a` (`ReportID`);

-- --------------------------------------------------------
--
-- Auto incrementing of IDs

-- Table `User`
ALTER TABLE `User`
    MODIFY `UserID` int(10) NOT NULL AUTO_INCREMENT;

-- Table `InApp_User_Data`
ALTER TABLE `InApp_User_Data`
    MODIFY `InDataID` int NOT NULL AUTO_INCREMENT,
    MODIFY `UserID` int(10) NOT NULL AUTO_INCREMENT,

-- Table `InAppReporting`
ALTER TABLE `InAppReporting`
    MODIFY `ReportID` int NOT NULL AUTO_INCREMENT,
    MODIFY `UserID` int(10) NOT NULL AUTO_INCREMENT;

-- Table `ReportStatus`
ALTER TABLE `ReportStatus`
    MODIFY `ReportID` int NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------
--
-- Adding constrains for Tables:

-- Table `User`
ALTER TABLE `User`
    ADD CONSTRAINT `FKf8p8s0` FOREIGN KEY (`PlanID`) REFERENCES `Usage_Plans` (`PlanID`);

-- Table `InApp_User_Data`
ALTER TABLE `InApp_User_Data`
    ADD CONSTRAINT `FKqey4eo` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`);

-- Table `InAppReporting`
ALTER TABLE `InAppReporting`
    ADD CONSTRAINT `FKmvey3h` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`),
    ADD CONSTRAINT `FKj7pogq` FOREIGN KEY (`ReportStatus`) REFERENCES `ReportStatus` (`ReportStatus`);

-- Table `ReportStatus`
ALTER TABLE `ReportStatus`
    ADD CONSTRAINT `FKenmj0a` FOREIGN KEY (`ReportID`) REFERENCES `InAppReporting` (`ReportID`);

COMMIT;
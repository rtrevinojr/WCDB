BEGIN;
CREATE TABLE `wcdb_organizations` (
    `idref` varchar(11) NOT NULL PRIMARY KEY,
    `name` longtext NOT NULL,
    `kind` longtext,
    `location` longtext,
    `summary` longtext
)
;
CREATE TABLE `wcdb_people_organizations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `people_id` varchar(11) NOT NULL,
    `organizations_id` varchar(11) NOT NULL,
    UNIQUE (`people_id`, `organizations_id`)
)
;
ALTER TABLE `wcdb_people_organizations` ADD CONSTRAINT `organizations_id_refs_idref_8f7c6e40` FOREIGN KEY (`organizations_id`) REFERENCES `wcdb_organizations` (`idref`);
CREATE TABLE `wcdb_people` (
    `idref` varchar(11) NOT NULL PRIMARY KEY,
    `name` longtext NOT NULL,
    `kind` longtext,
    `location` longtext,
    `summary` longtext
)
;
ALTER TABLE `wcdb_people_organizations` ADD CONSTRAINT `people_id_refs_idref_1c4389e` FOREIGN KEY (`people_id`) REFERENCES `wcdb_people` (`idref`);
CREATE TABLE `wcdb_crises_organizations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `crises_id` varchar(11) NOT NULL,
    `organizations_id` varchar(11) NOT NULL,
    UNIQUE (`crises_id`, `organizations_id`)
)
;
ALTER TABLE `wcdb_crises_organizations` ADD CONSTRAINT `organizations_id_refs_idref_b389642` FOREIGN KEY (`organizations_id`) REFERENCES `wcdb_organizations` (`idref`);
CREATE TABLE `wcdb_crises_people` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `crises_id` varchar(11) NOT NULL,
    `people_id` varchar(11) NOT NULL,
    UNIQUE (`crises_id`, `people_id`)
)
;
ALTER TABLE `wcdb_crises_people` ADD CONSTRAINT `people_id_refs_idref_1bae81c4` FOREIGN KEY (`people_id`) REFERENCES `wcdb_people` (`idref`);
CREATE TABLE `wcdb_crises` (
    `idref` varchar(11) NOT NULL PRIMARY KEY,
    `name` longtext NOT NULL,
    `kind` longtext,
    `date` date,
    `time` time,
    `summary` longtext
)
;
ALTER TABLE `wcdb_crises_organizations` ADD CONSTRAINT `crises_id_refs_idref_fb8e6cb6` FOREIGN KEY (`crises_id`) REFERENCES `wcdb_crises` (`idref`);
ALTER TABLE `wcdb_crises_people` ADD CONSTRAINT `crises_id_refs_idref_adb9cc9a` FOREIGN KEY (`crises_id`) REFERENCES `wcdb_crises` (`idref`);
CREATE TABLE `wcdb_list_item` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `idref` varchar(11) NOT NULL,
    `list_type` longtext,
    `href` longtext,
    `embed` longtext,
    `text` longtext,
    `body` longtext
)
;
COMMIT;

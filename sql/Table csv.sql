SET GLOBAL local_infile = 1;

SET SESSION local_infile = 1;

CREATE TABLE messi_career_data (
    `Date` DATE,
    `Competition` VARCHAR(100),
    `Home Team` VARCHAR(100),
    `Result` VARCHAR(10),
    `Away Team` VARCHAR(100),
    `Lineup` TEXT,
    `Minutes` TEXT,
    `Goals` TEXT,
    `Assists` TEXT,
    `Cards` TEXT
);


USE messi_career_data;


LOAD DATA LOCAL INFILE 'F:/JCMDataCenter/Cursos/Evolve Academy/Data Scientist IA/Evolve_Proyecto_Abril/data/processed/messi_cleaned_data.csv'
INTO TABLE messi_career_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    `Date`,
    `Competition`,
    `Home Team`,
    `Result`,
    `Away Team`,
    `Lineup`,
    `Minutes`,
    `Goals`,
    `Assists`,
    `Cards`
);

SELECT * FROM messi_career_data

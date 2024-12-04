CREATE SCHEMA `khmerpenalcode`;
USE khmerpenalcode;

CREATE TABLE crime(
ID INT NOT NULL AUTO_INCREMENT,
CrimeNameEnglish VARCHAR(1000) NOT NULL,
CrimeNameKhmer VARCHAR(1000) NOT NULL,
FineMaximum decimal(15,2),
FineMinimum decimal(15,2),
SentenceMaximum INT,
SentenceMinimum INT,
SentenceMaximumUnit ENUM("Y","M","D"),
SentenceMinimumUnit ENUM("Y","M","D"),
CONSTRAINT crime_PK PRIMARY KEY(ID)
);

CREATE TABLE articles(
ArticleNumber INT NOT NULL,
DescriptionEnglish TEXT,
DescriptionKhmer TEXT,
CONSTRAINT articles_PK PRIMARY KEY (articleNumber)
);

CREATE TABLE clauses(
ClauseID INT NOT NULL AUTO_INCREMENT,
ArticleNumber INT NOT NULL,
ClauseEnglish TEXT,
ClauseKhmer TEXT,
CONSTRAINT clauses_PK PRIMARY KEY (ClauseID),
CONSTRAINT article_clause_FK FOREIGN KEY (ArticleNumber) REFERENCES articles(ArticleNumber)
);


CREATE TABLE aggrivations(
CrimeID INT NOT NULL,
ClauseID INT NOT NULL,
SentenceMaximum INT,
SentenceMinimum INT,
SentenceMaximumUnit ENUM("Y","M","D"),
SentenceMinimumUnit ENUM("Y","M","D"),
CONSTRAINT FK_CrimeID FOREIGN KEY (CrimeID) REFERENCES crime(ID),
CONSTRAINT PK_Aggrivation PRIMARY KEY (CrimeID,ClauseID)
);
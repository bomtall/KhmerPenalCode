CREATE SCHEMA `khmerpenalcode`;
USE khmerpenalcode;

CREATE TABLE crime(
ID INT NOT NULL,
CrimeNameEnglish VARCHAR(1000) NOT NULL,
CrimeNameKhmer VARCHAR(1000) NOT NULL,
FineMinimum decimal(15,2),
FinaMaximum decimal(15,2),
SentenceMaximum INT,
SentenceMinimum INT,
SentenceMaximumUnit VARCHAR(5),
SentenceMinimumUnit VARCHAR(5),
CONSTRAINT crime_PK PRIMARY KEY(ID)
);

CREATE TABLE articles(
ArticleNumber INT NOT NULL,
DescriptionEnglish TEXT,
DescriptionKhmer TEXT,
CONSTRAINT articles_PK PRIMARY KEY (articleNumber)
);

CREATE TABLE clauses(
ClauseID INT NOT NULL,
ArticleNumber INT NOT NULL,
ClauseEnglish TEXT,
ClauseKhmer TEXT,
CONSTRAINT clauses_PK PRIMARY KEY (ClauseID, ArticleNumber),
CONSTRAINT article_clause_FK FOREIGN KEY (ArticleNumber) REFERENCES articles(ArticleNumber)
);


CREATE TABLE aggrivations(
CrimeID INT NOT NULL,
ClauseID INT NOT NULL,
FineMinimum decimal(15,2),
FineMaximum decimal(15,2),
SentenceMaximum INT,
SentenceMinimum INT,
SentenceMaximumUnit VARCHAR(5),
SentenceMinimumUnit VARCHAR(5),
CONSTRAINT FK_CrimeID FOREIGN KEY (CrimeID) REFERENCES crime(ID),
CONSTRAINT PK_Aggrivation PRIMARY KEY (CrimeID,ClauseID)
);
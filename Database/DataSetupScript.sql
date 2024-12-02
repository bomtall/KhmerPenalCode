USE khmerpenalcode;

INSERT INTO `khmerpenalcode`.`crime`
(`CrimeNameEnglish`,
`CrimeNameKhmer`,
`FineMaximum`,
`FineMinimum`,
`SentenceMaximum`,
`SentenceMinimum`,
`SentenceMaximumUnit`,
`SentenceMinimumUnit`)
VALUES
("Theft", "ចោរកម្ម",6000000, 1000000, 6, 3,"Y", "M"),
 ("Murder", "ឃាតកម្ម",NULL, NULL, 10, 15,"Y", "Y");
 
 INSERT INTO `khmerpenalcode`.`articles`
(`ArticleNumber`,
`DescriptionEnglish`,
`DescriptionKhmer`)
VALUES
(357 ,"",""),( 358,"",""),( 359,"",""),(360 ,"",""),( 199,"",""),( 200,"",""),(201 ,"",""),( 202,"",""),( 203,"",""),(204 ,"",""),(205 ,"","");

INSERT INTO `khmerpenalcode`.`clauses`
(`ArticleNumber`,
`ClauseEnglish`,
`ClauseKhmer`)
VALUES
(357,"if it is commited by breaking or entering",""),
(357,"Preceded, accompanied or followed by acts of violence",""),
(358,"Preceded, accompanied or followed by acts of violence causing mutilation or permanent disability",""),
(359,"Preceded, accompanied or followed by torture or acts of cruelty",""),
(360,"Preceded, accompanied or followed by violence unintentionally causing the death of the victim.",""),
(199,"Wilful killing of another person with or without a weapon with no aggravating circumstances",""),

( 200,"Murder committed with premeditation or by ambush",""),
(201 ,"Murder by poisoning",""),
(202,"against a person who is particularly vulnerable by reason of his or her age",""),
(202,"against a pregnant woman whose pregnancy is obvious or known to the perpetrator",""),
(202,"against a person who is particularly vulnerable by reason of his or her illness or disability which is obvious or known to the perpetrator",""),
(202,"against a public official in the performance of his or her duties or in connection therewith",""),
(203,"against a victim or a civil party, either to prevent him or her from reporting an offence or seeking reparation for harm",""),
(203,"against a witness to prevent him or her from testifying at an investigation, a judicial investigation, a trial or in the proceedings of other complaints",""),
(203,"against a victim or a civil party for reporting an offence or seeking reparation for harm suffered",""),
(203,"against a witness for testifying at an investigation, a judicial investigation, a trial or in the proceedings of other complaints",""),
(204,"committed by a public official in the performance of his or her duties or in connection therewith",""),
(205,"Murder preceded or followed by torture, cruelty or rape","");

INSERT INTO `khmerpenalcode`.`aggrivations`
(`CrimeID`,
`ClauseID`,
`SentenceMaximum`,
`SentenceMinimum`,
`SentenceMaximumUnit`,
`SentenceMinimumUnit`)
VALUES
(1,1,3,10,"Y","Y"),
(1,2,10,20,"Y","Y"),
(1,3,15,30,"Y","Y"),
(1,4,15,30,"Y","Y"),
(2,6,15,30,"Y","Y"),
(2,7,15,30,"Y","Y"),
(2,8,15,30,"Y","Y"),
(2,9,15,30,"Y","Y"),
(2,10,15,30,"Y","Y"),
(2,11,15,30,"Y","Y"),
(2,12,15,30,"Y","Y"),
(2,13,15,30,"Y","Y"),
(2,14,15,30,"Y","Y"),
(2,15,15,30,"Y","Y"),
(2,16,15,30,"Y","Y"),
(2,17,15,30,"Y","Y"),
(2,18,15,30,"Y","Y");
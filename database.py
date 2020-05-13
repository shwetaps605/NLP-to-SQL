import pymysql

databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
databaseUserName            = "root"       # User name of the database server
databaseUserPassword        = "root"           # Password for the database user
charSet                     = "utf8mb4"     # Character set
cusrorType                  = pymysql.cursors.DictCursor
connectionInstance   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,charset=charSet,cursorclass=cusrorType)


try:
    cur = connectionInstance.cursor()                       
    cur .execute("USE INS")

    createHeadquarterTable =  """
    CREATE TABLE headquarter (
        SrcHqID varchar(50) NOT NULL, 
        HeadQuarterKey int(4) NOT NULL, 
        SrcOrgID  varchar(50) NOT NULL, 
        HeadQuarterName varchar(50) NOT NULL,
        HQFileNumber varchar(50) NOT NULL,
        PRIMARY KEY (SrcHqID))
    """

    createPetitionerTable = """
    CREATE TABLE petitioner(
			`PetitionerKey` int(4) NOT NULL unique,
			`SrcPetitionerID` varchar(50) NOT NULL,
			`PetitionerType` varchar(510) NOT NULL,
			`PetitionerName` varchar(510) NOT NULL,
			`FileNumber` varchar(100) NOT NULL,
			`PetitionerTitle` varchar(300) NOT NULL,
			`SignatoryName`	varchar(500) NOT NULL,
			`ContactPersonAddress` varchar(300) NOT NULL,
            `SigningPersonName` varchar(300) NOT NULL,
            `ContactPersoneEmail` varchar(300) NOT NULL,
			`SigningPersonFirstName` varchar(100) NOT NULL,
			`SigningPersonLastName`	varchar(100) NOT NULL,
			`SigningPersonMiddleName` varchar(100) NOT NULL,
			`CorporationCaseManager` varchar(100) NOT NULL,
			`Corp_Case_Mgr`	varchar(100) NOT NULL,
			`SrcHQId` varchar(50) NOT NULL,
	 		 PRIMARY KEY (`SrcPetitionerID`)
        )
    """

    createBeneficiaryTable= """
    CREATE TABLE Beneficiary(
		`BeneficiaryKey` int(4) NOT NULL unique,
		`BNFType` varchar(100) NOT NULL,
		`SrcBnfID` varchar(50) NOT NULL,
		`BNFEmployeeID` varchar(100) NOT NULL,
		`FirstName` varchar(200) NOT NULL,
		`LastName` varchar(200) NOT NULL,
		`MiddleName` varchar(200) NOT NULL,
		`BNFFileNumber` varchar(100) NOT NULL,
		`BNFEmail` varchar(1200) NOT NULL,
		`Gender` char(1) NOT NULL,
		`Qualification`	varchar(200) NOT NULL,
		`CountryOfBirth` varchar(200) NOT NULL,
		`Nationality` varchar(100) NOT NULL,
		`CitizenshipCountry` varchar(300) NOT NULL,
		`MaritalStatus` varchar(2) NOT NULL,
		`RelationshipType` varchar(50) NOT NULL,
		`IsBNFPrimary` int(4) NOT NULL,
		`IsBNFActive` int(4) NOT NULL,
		`Occupation` varchar(300) NOT NULL,
		`BeneficiaryVisa` varchar(200) NOT NULL,
		`Experience` varchar(2000) NOT NULL,
		`ImmigrationStatus` varchar(400) NOT NULL,
		`Supervisors` varchar(100) NOT NULL,
		`PassportIssueCountry` varchar(800) NOT NULL,
		`BNFRelation` varchar(1000) NOT NULL,
		`MainBNFID` varchar(50) NOT NULL,
		`MainBNFCorpID`	varchar(50) NOT NULL,
		`DateOfBirth` datetime(6) NOT NULL,
		`FirstUSEntry` datetime(6) NOT NULL,
		`FirstUSVisaType` varchar(400) NOT NULL,
		`SupervisorEmailID` varchar(100) NOT NULL,
		`MainBNFEmail` varchar(510) NOT NULL,
		`JobType` char(1) NOT NULL,
		`ProjectName` varchar(200) NOT NULL,
		`BNFWorkPhones` varchar(100) NOT NULL,
		`BNFCorpID` varchar(50) NOT NULL,
		`Spouse_COB` varchar(100) NOT NULL,
		`Mailing Address` varchar(100) NOT NULL,
		`Work Address` varchar(100) NOT NULL,
		 PRIMARY KEY (`SrcBnfID`)
         )
    """

    createDocumentTable = """
    CREATE TABLE Document_details(
                    `SrcBnfId` varchar(50) NOT NULL,
                    `ClientArrivalDate` datetime(6) NOT NULL,
                    `ClientArrivalPlace_I94` varchar(100) NOT NULL,
                    `AdvParoleReceiptNumber` varchar(200) NOT NULL,
                    `AdvParoleValidFrom` datetime(6) NOT NULL,
                    `AdvParoleValidTo` datetime(6) NOT NULL,
                    `DS2019IssueDate` datetime(6) NOT NULL,
                    `DS2019Comments` varchar(2000) NOT NULL,
                    `DS2019ValidFrom` datetime(6) NOT NULL,
                    `DS2019ValidTo` datetime(6) NOT NULL,
                    `EADDocNumber` varchar(200) NOT NULL,
                    `EADCategory` varchar(400) NOT NULL,
                    `EADValidFrom` datetime(6) NOT NULL,
                    `EADValidTo` datetime(6) NOT NULL,
                    `EAD/APDDocNumber` varchar(200) NOT NULL,
                    `EAD/APDReceiptNumber` varchar(100) NOT NULL,
                    `EAD/APDValidFrom` datetime(6) NOT NULL,
                    `EAD/APDValidTo` datetime(6) NOT NULL,
                    `GreenCardValidFrom` datetime(6) NOT NULL,
                    `GreenCardValidTo` datetime(6) NOT NULL,
                    `HorLStatusStatus` varchar(400) NOT NULL,
                    `HorLStatusValidFrom` datetime(6) NOT NULL,
                    `HorLStatusValidTo` datetime(6) NOT NULL,
                    `I94DocNumber` varchar(200) NOT NULL,
                    `I94ValidFrom` datetime(6) NOT NULL,
                    `I94ValidTo` datetime(6) NOT NULL,
                    `I797Status` varchar(400) NOT NULL,
                    `I797ApprovedDate` datetime(6) NOT NULL,
                    `I797GovtSentDate` datetime(6) NOT NULL,
                    `I797ApprovedReceiptDate` datetime(6) NOT NULL,
                    `I797ValidFrom` datetime(6) NOT NULL,
                    `I797ValidTo` datetime(6) NOT NULL,
                    `PassportDocNumber` varchar(200) NOT NULL,
                    `PassportValidFrom` datetime(6) NOT NULL,
                    `PassportValidTo` datetime(6) NOT NULL,
                    `PassportIssuePlace` varchar(200) NOT NULL,
                    `PassportIssueState` varchar(200) NOT NULL,
                    `PassportIssueCountry` varchar(200) NOT NULL,
                    `PassportFirstName` varchar(200) NOT NULL,
                    `PassportMiddleName` varchar(200) NOT NULL, 
                    `PassportLastName` varchar(200) NOT NULL,
                    `ReEntryPermitDocNumber` varchar(200) NOT NULL,
                    `ReEntryPermitCategory` varchar(400) NOT NULL,
                    `ReEntryPermitValidFrom` datetime(6) NOT NULL,
                    `ReEntryPermitValidTo` datetime(6) NOT NULL,
                    `VisaDocNumber` varchar(200) NOT NULL,
                    `VisaCategory` varchar(400) NOT NULL,
                    `VisaComments` varchar(2000) NOT NULL,
                    `VisaValidFrom` datetime(6) NOT NULL,
                    `VisaValidTo` datetime(6) NOT NULL,
                    `EAD/APDType` varchar(400) NOT NULL, 
                    `I94_DS_YN` char(1) NOT NULL,
                    `I129SValidFrom` datetime(6) NOT NULL,
                    `I129SValidTo` datetime(6) NOT NULL
                    )
    """
    createCaseApprovalTable= """
    CREATE TABLE caseapproval(
                    `PetitionerKey` int(4) NOT NULL,
                    `BeneficiaryKey` int(4) NOT NULL,
                    `SrcCaseID` varchar(50) NOT NULL,
                    `ApprovalValidFromDate` datetime(6) NOT NULL,
                    `ApprovalValidToDate` datetime(6) NOT NULL,
                    `RFEDueDate` datetime(6) NOT NULL,
                    `DateRFESubmitted` datetime(6) NOT NULL,
                    `RFEDecisionDate` datetime(6) NOT NULL,
                    `RFEReceivedDate`datetime(6) NOT NULL,
                    `ApprovalDate` datetime(6) NOT NULL,
                    `CaseDeniedDate` datetime(6) NOT NULL,
                    `CaseMainReceiptDenialDate` datetime(6) NOT NULL, 
                    `CaseMainReceiptWithdrawnDate` datetime(6) NOT NULL
)
"""

    createCaseProcessTable= """
    CREATE TABLE caseprocess(
                    `SrcCaseID` varchar(50) NOT NULL,
                    `CaseLCAID` varchar(100) NOT NULL,
                    `CaseFileNumber` varchar(100) NOT NULL,
                    `CaseFiledDate` datetime(6) NOT NULL,
                    `GovtSentDate` datetime(6) NOT NULL,
                    `CaseDescription` varchar(100) NOT NULL,
                    `CaseType` varchar(100) NOT NULL,
                    `CaseNotes` varchar(100) NOT NULL,
                    `Country` varchar(100) NOT NULL,
                    `CaseStatus` char(1) NOT NULL,
                    `CaseName` varchar(100) NOT NULL,
                    `IsCaseActive` char(5) NOT NULL, 
                    `CaseLongDescription` varchar(1024) NOT NULL,  
                    `CasePriorityDate` datetime(6) NOT NULL,
                    `SrcBnfID` varchar(50) NOT NULL,
                    `SrcEprID`varchar(50) NOT NULL,
                    `FirmCaseStatus` varchar(1800) NOT NULL,
                    `CasePriorityCategory` varchar(25) NOT NULL,
                    `CasePriorityCountry` varchar(200) NOT NULL, 
                    `AnnualSalary` varchar(100) NOT NULL,  
                    `IsCasePriorityDateCurrent` varchar(5) NOT NULL,
                    `Case_Category` varchar(50) NOT NULL,
                    `Petition_Type`varchar(25) NOT NULL,
                    `CaseSub_Category` varchar(400) NOT NULL,
                    `Case_Group` varchar(400) NOT NULL,
                    `CaseNextActionId` varchar(50) NOT NULL, 
                    `CaseNextActionDueDate` datetime(6) NOT NULL,  
                    `CaseLastActionDescription` varchar(100) NOT NULL,
                    `CaseLastActionId` varchar(50) NOT NULL,
                    `CaseLastActionDueDate`datetime(6) NOT NULL,
                    `CaseLastActionUpdatedTS` datetime(6) NOT NULL,
                    `CaseNextActionUpdatedTS` datetime(6) NOT NULL,
                    `CaseMainReceiptTypeDescription` varchar(100) NOT NULL, 
                    `LastStepCompletedName` varchar(1020) NOT NULL,  
                    `LastStepCompletedDate` datetime(6)  NOT NULL,
                    `NextStepToBeCompletedName` varchar(1020) NOT NULL,
                    `NextStepToBeCompletedDueDate`datetime(6) NOT NULL,  
                     PRIMARY KEY (`SrcCaseID`)
                    )
    """
    
    cur.execute(createHeadquarterTable)
    
    cur.execute ("""
    ALTER TABLE `Petitioner`
    ADD CONSTRAINT `petitioner_ibfk_1` FOREIGN KEY (`SrcHQId`) REFERENCES `Headquarter` (`SrcHqID`)
    """)

    cur.execute ("""
    ALTER TABLE `Beneficiary`
    ADD CONSTRAINT FOREIGN KEY (`BNFCorpID`) REFERENCES `Petitioner` (`SrcPetitionerID`)
    """)

    cur.execute("""
    ALTER TABLE `caseprocess`
    ADD CONSTRAINT FOREIGN KEY (`SrcEprID`) REFERENCES `Petitioner` (`SrcPetitionerID`)
    """)

    cur.execute("""
    ALTER TABLE `caseprocess`
    ADD CONSTRAINT  FOREIGN KEY (`SrcBnfID`) REFERENCES `Beneficiary` (`SrcBnfID`)
    """)

    cur.execute("""
    ALTER TABLE `Document_details`
    ADD CONSTRAINT  FOREIGN KEY (`SrcBnfID`) REFERENCES `Beneficiary` (`SrcBnfID`)
    """)

    cur.execute("""
    ALTER TABLE `caseapproval`
    ADD CONSTRAINT `caseapproval_ibfk_1` FOREIGN KEY (`SrcCaseID`) REFERENCES `caseprocess` (`SrcCaseID`)
    """)

    cur.execute("""
    ALTER TABLE `caseapproval`
  ADD CONSTRAINT  FOREIGN KEY (`PetitionerKey`) REFERENCES `Petitioner` (`PetitionerKey`)
    """)

    cur.execute("""
    ALTER TABLE `caseapproval`
    ADD CONSTRAINT  FOREIGN KEY (`BeneficiaryKey`) REFERENCES `Beneficiary` (`BeneficiaryKey`)
    """)

    cur.execute("""
    insert into headquarter values ("A1","1","S1","New York","123")
    """)

    cur.execute("""
    insert into headquarter values ("A2","2","S2","Ohio","345")
    """)

    cur.execute("""
    insert into headquarter values ("A3","3","S3","California","567")
    """)

    cur.execute("""
    insert into petitioner values ("1","P1","abc","Company1","ABC123","pet_title1","name1","New york","sig_name_1","email_1","Raj","Kumar","Ramesh","ccm1","cccm1","A1")
    """)

    cur.execute("""
    insert into petitioner values ("2","P2","abc","Company2","ABC345","pet_title2","name2","New york_2","sig_name_2","email_2","Sonu","Kumar","Anant","ccm2","cccm2","A2")
    """)

    cur.execute("""
    insert into beneficiary values ( "2",
    "BNF_type2",
    "B2",
    "bnf_emp_2",
    "Robert",
    "Jackson",
    "Liam",
    "bnf_file_2",
    "bnf_email_2",
    "M",
    "UG",
    "USA",
    "Indian",
    "USA",
    "M",
    "r_type_2",
    "0",
    "1",
    "Worker",
    "visa2",
    "exp_2",
    "no status",
    "sup_2",
    "Canada",
    "rel_2",
    "main_bnf_id_2",
    " main_bnf_corp_2 ",
    "2019-11-05",
    "2016-11-05",
    "vtype_2",
    "sup_mail_2",
    "bnf_mail_2",
    "100",
    "Y",
    "Pname2",
    "123488",
    "P2",
    "COB_2",
    "ma_2",
    "wa_2")
    """)

    cur.execute("""
    insert into beneficiary values ( "1",
    "BNF_type1",
    "B1",
    "bnf_emp_1",
    "Sam",
    "Jackson",
    "Haden",
    "bnf_file_1",
    "bnf_email_1",
    "M",
    "UG",
    "USA",
    "American",
    "USA",
    "UM",
    "r_type_1",
    "1",
    "0",
    "Manager",
    "visa1",
    "exp_1",
    "no status",
    "sup_1",
    "Canada",
    "rel_1",
    "main_bnf_id_1",
    " main_bnf_corp_1 ",
    "2015-11-05",
    "2015-11-05",
    "vtype_1",
    "sup_mail_1",
    "bnf_mail_1",
    "10000",
    "Y",
    "Pname1",
    "1234",
    "P1",
    "COB_1",
    "ma_1",
    "wa_1")
    """)

    cur.execute("""
    insert into caseprocess values(
    "C1",
    "LCAID_1",
    "123xyz",
    "2012-03-11",
    "2012-05-11",
    "desc_1",
    "H-1B",
    "notes_1",
    "USA",
    "P",
    "case_name_1",
    "1",
    "descp_1",
    "2011-09-19",
    "B1",
    "P1",
    "fc_status_1",
    "cat_1",
    "usa",
    "5000",
    "No",
    "yes",
    "case_cat_1"
    "pet_type_1",
    "case_sub_cat_1",
    "case_group_1",
    "ID1",
    "2019-08-19",
    "Case_desc_1",
    "la_id_1",
    "2021-07-12",
    "2021-10-12",
    "2021-12-12",
    "case_main_1",
    "ls_name1",
    "2020-03-21",
    "ns_name_1",
    "2021-09-12")
    """)

    cur.execute("""
    insert into caseprocess values(
    "C2",
    "LCAID_2",
    "345xyz",
    "2014-03-11",
    "2014-05-11",
    "desc_2",
    "F-1",
    "notes_2",
    "Canada",
    "A",
    "case_name_2",
    "0",
    "descp_2",
    "2018-09-19",
    "B2",
    "P2",
    "fc_status_2",
    "cat_2",
    "usa",
    "50",
    "No",
    "yes",
    "case_cat_2"
    "pet_type_2",
    "case_sub_cat_2",
    "case_group_2",
    "ID2",
    "2014-08-19",
    "Case_desc_2",
    "la_id_2",
    "2021-02-12",
    "2021-07-12",
    "2021-11-12",
    "case_main_2",
    "ls_name2",
    "2020-01-21",
    "ns_name_2",
    "2021-01-10")
    """)

    cur.execute("""
    insert into caseapproval values (
    "1",
    "1",
    "C1",
    "2018-02-19",
    "2021-09-11",
    "2020-08-10",
    "2020-01-10",
    "2020-06-10",
    "2020-08-17",
    "2020-08-20",
    "2020-08-11",
    "2021-04-10",
    "2020-11-10")
    """)

    cur.execute("""
    insert into caseapproval values (
    "2",
    "1",
    "C2",
    "2016-02-19",
    "2020-09-11",
    "2020-02-10",
    "2020-06-10",
    "2020-01-10",
    "2020-09-17",
    "2020-02-20",
    "2020-07-11",
    "2021-01-10",
    "2020-10-10")
    """)

    cur.execute("""
    insert into Document_details values(
    "B1",
    "2010-02-11",
    "place_1",
    "1234",
    "2013-02-11",
    "2015-02-11",
    "2015-07-11",
    "No comments",
    "2012-02-11",
    "2014-02-11",
    "doc_1",
    "doc_cat_1",
    "2011-02-11",
    "2013-02-11",
    "apd_doc_1",
    "apd_rcpt_1",
    "2010-02-11",
    "2010-11-11",
    "2019-02-11",
    "2019-12-11",
    "status_1",
    "2013-02-11",
    "2017-02-11",
    "doc_n_1",
    "2016-02-11",
    "2020-02-11",
    "status_1",
    "2010-02-11",
    "2010-04-11",
    "2010-09-11",
    "2010-10-11",
    "2010-12-11",
    "pass_num_1",
    "2010-09-11",
    "2021-09-11",
    "USA airport",
    "Ohio",
    "USA",
    "Lamming",
    "Josh",
    "Heraldtown",
    "pd_1",
    "pc_cat_1",
    "2019-02-11",
    "2020-02-11",
    "visa_num_1",
    "visa_cat_1",
    "visa_comments",
    "2011-02-11",
    "2019-02-11",
    "Apd_type_1",
    "A",
    "2013-02-11",
    "2018-02-11")
    """)

    cur.execute("""
    insert into Document_details values(
    "B2",
    "2011-02-11",
    "place_2",
    "1934",
    "2013-09-11",
    "2015-01-11",
    "2015-03-11",
    "No comments",
    "2016-02-11",
    "2019-02-11",
    "doc_2",
    "doc_cat_2",
    "2011-02-21",
    "2013-02-21",
    "apd_doc_2",
    "apd_rcpt_2",
    "2010-02-11",
    "2010-11-21",
    "2019-02-21",
    "2019-12-21",
    "status_2",
    "2013-02-21",
    "2017-02-21",
    "doc_n_2",
    "2016-02-21",
    "2020-02-21",
    "status_2",
    "2010-02-21",
    "2010-04-21",
    "2010-09-21",
    "2010-10-21",
    "2010-12-21",
    "pass_num_2",
    "2010-09-21",
    "2021-09-21",
    "USA airport",
    "New York",
    "USA",
    "Matthew",
    "Kerauld",
    "Perry",
    "pd_2",
    "pc_cat_2",
    "2019-02-11",
    "2020-02-21",
    "visa_num_2",
    "visa_cat_2",
    "visa_comments_2",
    "2011-02-21",
    "2019-02-21",
    "Apd_type_2",
    "B",
    "2013-02-21",
    "2018-02-12")
    """)

    cur.execute("commit")

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionInstance.close()

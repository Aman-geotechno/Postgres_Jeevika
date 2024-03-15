examples = [
    {
    
            "input": "What is the total count of shg?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS shg_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'SHG' AND c.record_status=1""",
            "result": "[(1075033)]",
            "answer": "There are total 1075033 SHG ",

},
{
    "input": "What is the total count of CLF?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS clf_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'CLF' AND c.record_status=1""",
            "result": "[(1658)]",
            "answer": "There are total 1658 CLF",
},


{
    "input": "What is the total count of VO?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS vo_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'VO' AND c.record_status=1""",
            "result": """[(75368)]""",
            "answer": """There are total 75368 VO""",
},
{
            "input": "Number of cbo per block per district",
            "sql_cmd": """SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos \
                        FROM m_cbo c \
                        INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID \
                        INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID \
                        WHERE c.record_status=1 \
                        GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME""",
            "result": """ARARIA	Palasi	3410
                            ARARIA	Sikti	2330
                            BANKA	Katoria	2673
                            BANKA	Shambhuganj	2302
                            BEGUSARAI	Sahebpur Kamal	2057
                            BEGUSARAI	Teghra	1972
                            BEGUSARAI	Naokothi	1407
                            BHAGALPUR	Naugachhia	1605
                            BHOJPUR	Sahar	1207
                            BHOJPUR	Charpokhari	1190
                            BHOJPUR	Garhani	1044
                            BUXAR	Barhampur	1903""",
            "answer": """ARARIA	Palasi	3410
                            ARARIA	Sikti	2330
                            BANKA	Katoria	2673
                            BANKA	Shambhuganj	2302
                            BEGUSARAI	Sahebpur Kamal	2057
                            BEGUSARAI	Teghra	1972
                            BEGUSARAI	Naokothi	1407
                            BHAGALPUR	Naugachhia	1605
                            BHOJPUR	Sahar	1207
                            BHOJPUR	Charpokhari	1190
                            BHOJPUR	Garhani	1044
                            BUXAR	Barhampur	1903""",
        },
        
        {
            "input": "total count of 9 month old shg saving account",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count
FROM m_cbo c
INNER JOIN m_district d ON d.district_id = c.district_id
WHERE c.record_status = 1
AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
AND c.formation_date <= CURRENT_DATE - INTERVAL '9 MONTH'
AND c.formation_date > CURRENT_DATE - INTERVAL '10 MONTH'""",
            "result": """[(2110)]""",
            "answer": """2110 are count of 9 month old shg saving account""",
        },
        {
            "input": "total count of shg in project nrlm in current year",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRLM' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
                        AND EXTRACT(YEAR FROM c.formation_date) = EXTRACT(YEAR FROM SYSDATE)
                        AND c.record_status=1""",
            "result": """[(32)]""",
            "answer": """There are total 32 SHG in project NRLM in current year""",
        },
        {
            "input": "how many clf are in NRETP project",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS clf_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRETP' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'CLF')
                        AND c.record_status=1""",
            "result": """[(306)]""",
            "answer": """There are total 306 CLF in project NRETP """,
        },
        {
            "input": "how many shg, vo and clf in district bhojpur",
            "sql_cmd": """SELECT
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
                FROM m_cbo c
                WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'BHOJPUR')
                AND c.record_status=1""",
            "result": """[(20863	1535	37)]""",
            "answer": """There are total 20863 shg	1535 vo and	37 CLF in district BHOJPUR """,
        },
        {
             "input": "What is the count of all members across SHGs, VOs and CLFs in district Patna?",
            "sql_cmd": """SSELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1""",
            "result": """[(41010	2725	65)]""",
            "answer": """There are total 41010 shg	12725 vo and	65 CLF in district PATNA """,
        },
        {
            "input": "how many shg saving account in last 6 months?",
            "sql_cmd": """SELECT
                    COUNT(DISTINCT c.CBO_ID) AS SHG_Saving_ACC
                FROM
                    M_CBO c
                JOIN
                    T_CBO_APPL_MAPPING cam ON c.CBO_ID = cam.CBO_ID
                JOIN
                    T_BULK_BANK_ACC bba ON cam.APPLICATION_ID = bba.APPLICATION_ID
                JOIN
                    M_CBO_TYPE ct ON c.CBO_TYPE_ID = ct.CBO_TYPE_ID
                WHERE
                    bba.ACC_TYPE_ID = 1
                    AND upper(ct.TYPE_SHORT_NAME) = 'SHG'
                    AND c.RECORD_STATUS = 1
                    AND cam.ACC_OPENING_STATUS = 2
                    AND bba.APPLICATION_DATE >= CURRENT_DATE - INTERVAL '6 MONTH'""",
            "result": """[(11083)]""",
            "answer": """There are total 11083 shg saving account in last 6 months """,
        },
        {
            "input": "how many shg saving account, vo saving account, clf saving account in last 6 month",
            "sql_cmd": """SELECT
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'SHG' THEN 1 ELSE 0 END) AS SHG_Saving_Accounts,
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'VO' THEN 1 ELSE 0 END) AS VO_Saving_Accounts,
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'CLF' THEN 1 ELSE 0 END) AS CLF_Saving_Accounts
                FROM
                    M_CBO c
                JOIN
                    T_CBO_APPL_MAPPING cam ON c.CBO_ID = cam.CBO_ID
                JOIN
                    T_BULK_BANK_ACC bba ON cam.APPLICATION_ID = bba.APPLICATION_ID
                JOIN
                    M_CBO_TYPE ct ON c.CBO_TYPE_ID = ct.CBO_TYPE_ID
                WHERE
                    bba.ACC_TYPE_ID = 1
                    AND c.RECORD_STATUS = 1
                    AND cam.ACC_OPENING_STATUS = 2
                    AND bba.APPLICATION_DATE >= CURRENT_DATE - INTERVAL '6 MONTH'""",
            "result": """[(11218	936	25)]""",
            "answer": """There are total 11218 shg_saving_account 936 VO_Saving_Accounts and 25 CLF_Saving_Accounts in last 6 months""",
        },
        {
            "input": "total count of shg in district patna in year 2023",
            "sql_cmd": """SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND c.record_status=1""",
            "result": """[(1286)]""",
            "answer": """1286 SHG were formed in district Patna in 2023""",
        },
        {
            "input": "total count of members in district patna and darbhanga",
            "sql_cmd": """SELECT d.DISTRICT_NAME, COUNT(cm.MEMBER_ID) AS member_count
                           FROM m_district d 
                           INNER JOIN m_cbo_member cm ON  cm.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(d.DISTRICT_NAME) IN ('PATNA', 'DARBHANGA')
                            AND cm.record_status=1
                            GROUP BY d.DISTRICT_NAME""",
            "result": """[(DARBHANGA	526984
                            PATNA	493022)]""",
            "answer": """there are 526984 members in Darbhanga and 493022 members in Patna""",
        },
        {
            "input": "total count of vo in december 2023",
            "sql_cmd": """SELECT 
                            COUNT(cbo_id) AS vo_count
                            FROM 
                            m_cbo c
                            INNER JOIN 
                            m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                            WHERE
                            upper(t.type_short_name) = 'VO'
                            AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND EXTRACT(MONTH FROM c.formation_date) = 12
                            AND c.record_status=1""",
            "result": """[(81)]""",
            "answer": """total 81 vo were formed in december 2023""",
        },
        {
            "input": "What is the total number of VOs in Samastipur district?",
            "sql_cmd": """SELECT COUNT(c.CBO_ID) AS total_vos
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'VO' AND upper(d.DISTRICT_NAME) = 'SAMASTIPUR'
                            AND c.record_status=1
""",
            "result": """[(3402)]""",
            "answer": """there are 3402 VOs in Samastipur district"""
        },
        {
            "input": "How many SHGs  in Patna district formed between Jan to March 2023?",
            "sql_cmd": """SELECT
                        COUNT(*) AS shg_count  
                        FROM 
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN 
                        m_district d ON c.district_id = d.district_id
                        WHERE
                        upper(t.type_short_name) = 'SHG'
                        AND upper(d.district_name)= 'PATNA' 
                        AND EXTRACT(MONTH FROM c.formation_date) BETWEEN 1 AND 3 
                        AND EXTRACT(YEAR FROM c.formation_date) = 2023
                        AND c.record_status=1
""",
            "result": """[(627)]""",
            "answer": """627 SHGs formed between Jan to March 2023"""
        },
        {
            "input": "What is the count of SHGs formed in Saharsa district in 2022?",
            "sql_cmd": """SELECT
                COUNT(*) AS shg_count
                FROM
                m_cbo c
                INNER JOIN
                m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                INNER JOIN
                m_district d ON c.district_id = d.district_id
                WHERE
                upper(t.type_short_name) = 'SHG'
                AND upper(d.district_name) = 'SAHARSA'
                AND EXTRACT(YEAR FROM c.formation_date) = 2022
                AND c.record_status=1""",
            "result": """[(222)]""",
            "answer": """total 222 SHGs formed in Saharsa district in 2022""",
        },
        {
            "input": "total count of shg",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'SHG' \
                            AND c.record_status=1""",
            "result": """[(1075033)]""",
            "answer": """There are total 1075033 SHG """,
        },
        {
            "input": "What is the total count of shg?",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'SHG' \
                            AND c.record_status=1""",
            "result": """[(1075033)]""",
            "answer": """There are total 1075033 SHG """,
        },
        {
             "input": "How many SHGs in Patna district formed between Jan to March 2023?",
            "sql_cmd": """
                                SELECT
                                    COUNT(*) AS shg_count
                                FROM
                                    m_cbo c
                                INNER JOIN
                                    m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                                INNER JOIN
                                    m_district d ON c.district_id = d.district_id
                                WHERE
                                    upper(t.type_short_name) = 'SHG'
                                    AND upper(d.district_name) = 'PATNA'
                                    AND EXTRACT(MONTH FROM c.formation_date) BETWEEN 1 AND 3
                                    AND EXTRACT(YEAR FROM c.formation_date) = 2023
                                    AND c.record_status = 1
                            """,
            "result": """[(631)]""",
            "answer": """There are total 631 SHG formed in Patna district between Jan to March 2023 """,
        },
        {
            "input": "Number of cbo per block per district",
            "sql_cmd": """
                                SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
                                FROM m_cbo c
                                INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
                                INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
                                WHERE c.record_status = 1
                                GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
                                ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
                            """,
            "result": """[(ARARIA	Araria	4560
                                    ARARIA	Bhargama	3278
                                    ARARIA	Forbesganj	3726
                                    ARARIA	Jokihat	3147
                                    ARARIA	Kursakatta	2205)]""",
            "answer": """ARARIA	Araria	4560
                            ARARIA	Bhargama	3278
                            ARARIA	Forbesganj	3726
                            ARARIA	Jokihat	3147
                            ARARIA	Kursakatta	2205""",
        },
        {
             "input": "What is the distribution of Community Based Organizations (CBOs) by their types, and how many CBOs are there for each type",
            "sql_cmd": """SELECT t.TYPE_SHORT_NAME, COUNT(c.CBO_ID) AS cbo_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            WHERE c.record_status = 1
                            GROUP BY t.TYPE_SHORT_NAME
                            ORDER BY cbo_count DESC""",
            "result": """[(SHG	1073354
                                VO	75448
                                PG	5998
                                CLF	1658
                                TLC	29
                                PC	18)]""",
            "answer": """there are SHG	1073354
                                VO	75448
                                PG	5998
                                CLF	1658
                                TLC	29
                                PC	18""",
        },
        {
            "input": "What is the most common CBO type in district Vaishali?",
            "sql_cmd": """SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME)= 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC
""",
            "result": """[(Self Helped Group	37395
                            village Organization	2653
                            Producer Group	241
                            Cluster Level Federa	60
                            Producer Company	3)]""",
            "answer": """There are Self Helped Group	37395
                            village Organization	2653
                            Producer Group	241
                            Cluster Level Federa	60
                            Producer Company	3 in Vaishali"""
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025)]""",
            "answer": """1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025""",
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.block_id = p.block_id
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025)]""",
            "answer": """1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025""",
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025)]""",
            "answer": """1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025""",
        },
        {
            "input": "how many shg in lakhani bigha panchayat?",
            "sql_cmd": """SELECT
    COUNT(c.CBO_ID) AS shg_count
FROM
    m_cbo c
INNER JOIN
    m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
INNER JOIN
    m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
INNER JOIN
    m_block b ON c.BLOCK_ID = b.BLOCK_ID
INNER JOIN
    m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
WHERE
    upper(t.TYPE_SHORT_NAME) = 'SHG'
    AND upper(p.PANCHAYAT_NAME) = 'LAKHANI BIGHA'
    AND c.record_status = 1""",
            "result": """[(1456)]""",
            "answer": """There are 1456 shg in lakhani bigha panchayat"""
        },
        {
            "input": "give me toatal members between 2020 and 2021",
            "sql_cmd": """SELECT 
                            COUNT(DISTINCT m.member_id) AS total_members
                            FROM
                            m_cbo_member m
                            INNER JOIN
                            mp_cbo_member t on m.member_id=t.member_id
                            INNER JOIN
                            m_cbo c ON t.cbo_id = c.cbo_id
                            WHERE
                            EXTRACT(YEAR FROM m.date_of_joining) BETWEEN 2020 AND 2021
                            AND c.record_status=1""",
            "result": """[(1652157)]""",
            "answer": """There are total 1652157 members""",
        },
        {
            "input": "total cadre in shg",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN 
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  AND  upper(k.TYPE_SHORT_NAME) = 'SHG'
    
    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(89603)]""",
            "answer": """There are total 89603 in SHG """
        },
        {
            "input": "give me toatal members between 2020 and 2021",
            "sql_cmd": """SELECT 
                            COUNT(DISTINCT m.member_id) AS total_members
                            FROM
                            m_cbo_member m
                            INNER JOIN
                            mp_cbo_member t on m.member_id=t.member_id
                            INNER JOIN
                            m_cbo c ON t.cbo_id = c.cbo_id
                            WHERE
                            EXTRACT(YEAR FROM m.date_of_joining) BETWEEN 2020 AND 2021
                            AND c.record_status=1""",
            "result": """[(1652157)]""",
            "answer": """There are total 1652157 members""",
        },
        {
            "input": "total male cadre in shg",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  AND  upper(k.TYPE_SHORT_NAME) = 'SHG'
  AND m.GENDER='M'

    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(1037)]""",
            "answer": """There are total 1037 in SHG """ 
        },
        {
              "input": "female cadre in gaya district?",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  
  AND m.GENDER='F'
  AND c.DISTRICT_ID=(SELECT DISTRICT_ID FROM M_DISTRICT WHERE UPPER(DISTRICT_NAME)='GAYA')
    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(6297)]""",
            "answer": """There are total 6297 female cadre in gaya district """  
        },
        {
            "input": "how many cadre of designation CM?",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  AND  upper(l.DESIGNATION_SHORT_NAME) = 'CM'

    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(88748)]""",
            "answer": """There are total 88748 cadre of designation CM """
        },
        {
            "input": "How many cadre of designation VRP in NALANDA district",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  
  AND  upper(l.DESIGNATION_SHORT_NAME) = 'VRP'
  AND c.DISTRICT_ID=(SELECT DISTRICT_ID FROM M_DISTRICT WHERE UPPER(DISTRICT_NAME)='NALANDA')
    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(498)]""",
            "answer": """There are total 498 cadre of designation VRP in NALANDA district"""
        },
        {
            "input": "count of total graded clf?",
            "sql_cmd": """SELECT COUNT(distinct clf.clf_id) AS clf_count
            FROM clf_masik_grading clf
            INNER JOIN m_cbo c ON clf.clf_id = c.cbo_id
            WHERE c.record_status = 1""",
            "result": """[(1596,)]""",
            "answer": """The count of total graded clf is 1596.""",
        },
        {
            "input": "count of total graded clf in 2023?",
            "sql_cmd": """SELECT COUNT(distinct clf.clf_id) AS clf_count
            FROM clf_masik_grading clf
            INNER JOIN m_cbo c ON clf.clf_id = c.cbo_id
            WHERE c.record_status = 1 and clf.year = 2023""",
            "result": """[(1556,)]""",
            "answer": """The count of total graded clf in 2023 is 1556.""",
        },
        {
            "input": "count of total graded clf in december 2023?",
            "sql_cmd": """SELECT COUNT(distinct clf.clf_id) AS clf_count
            FROM clf_masik_grading clf
            INNER JOIN m_cbo c ON clf.clf_id = c.cbo_id
            WHERE c.record_status = 1 and clf.year = 2023 and clf.month_name = 'Dec'""",
            "result": """[(17,)]""",
            "answer": """The count of total graded clf in december 2023 is 17.""",
        },
        {
            "input": "count of B graded clf in december 2023?",
            "sql_cmd": """SELECT COUNT(clf.clf_id) AS clf_count
            FROM clf_masik_grading clf
            INNER JOIN m_cbo c ON clf.clf_id = c.cbo_id
            WHERE clf.year = 2023 and clf.month_name = 'Dec' AND clf.final_grade = 'B' AND c.record_status = 1""",
            "result": """[(7,)]""",
            "answer": """The count of B graded clf in december 2023 is 7.""",
        },
        {
            "input": "how many clf are not graded?",
            "sql_cmd": """SELECT COUNT(*) AS clf_not_graded
            FROM m_cbo a
            WHERE a.record_status = 1
            AND a.cbo_type_id = 1
            AND NOT EXISTS (SELECT 1 FROM clf_masik_grading b WHERE a.cbo_id = b.clf_id)""",
            "result": """[(64,)]""",
            "answer": """64 clf that are not graded.""",
        },
        {
            "input": "count of total graded vo?",
            "sql_cmd": """SELECT COUNT(distinct a.vo_id) AS vo_count
            FROM vo_masik_grading a
            INNER JOIN m_cbo c ON a.vo_id = c.cbo_id
            WHERE c.record_status = 1""",
            "result": """[(65819,)]""",
            "answer": """The count of total graded vo is 65819.""",
        },
        {
            "input": "count of total graded vo in 2023?",
            "sql_cmd": """SELECT COUNT(distinct a.vo_id) AS vo_count
            FROM vo_masik_grading a
            INNER JOIN m_cbo c ON a.vo_id = c.cbo_id
            WHERE c.record_status = 1 and a.year = 2023""",
            "result": """[(64145,)]""",
            "answer": """The count of total graded vo in 2023 is 64145.""",
        },
        {
            "input": "count of total graded vo in december 2023?",
            "sql_cmd": """SELECT COUNT(distinct a.vo_id) AS vo_count
            FROM vo_masik_grading a
            INNER JOIN m_cbo c ON a.vo_id = c.cbo_id
            WHERE c.record_status = 1 and a.year = 2023 and a.month_name = 'Dec'""",
            "result": """[(32381,)]""",
            "answer": """The count of total graded vo in december 2023 is 32381.""",
        },

        {
            "input": "count of a graded vo in december 2023?",
            "sql_cmd": """SELECT COUNT(a.clf_id) AS vo_count
            FROM vo_masik_grading a
            INNER JOIN m_cbo c ON a.vo_id = c.cbo_id
            WHERE a.year = 2023 and a.month_name = 'Dec' AND a.final_grade = 'A' AND c.record_status = 1""",
            "result": """[(97,)]""",
            "answer": """The count of A graded vo in december 2023 is 97.""",
        },
        {
            "input": "count of total graded shg?",
            "sql_cmd": """SELECT COUNT(distinct a.shg_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE c.record_status = 1""",
            "result": """[(889467,)]""",
            "answer": """The count of total graded shg is 889467.""",
        },
        {
            "input": "count of total graded shg in 2023?",
            "sql_cmd": """SELECT COUNT(distinct a.shg_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE c.record_status = 1 and a.year = 2023""",
            "result": """[(852340,)]""",
            "answer": """The count of total graded shg in 2023 is 852340.""",
        },
        {
            "input": "count of total graded shg in december 2023?",
            "sql_cmd": """SELECT COUNT(distinct a.shg_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE c.record_status = 1 and a.year = 2023 and a.month_name = 'Dec'""",
            "result": """[(737400,)]""",
            "answer": """The count of total graded shg in december 2023 is 737400.""",
        },
        {
            "input": "count of total graded shg in feb 2023?",
            "sql_cmd": """SELECT COUNT(distinct a.shg_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE c.record_status = 1 and a.year = 2023 and a.month_name = 'Dec'""",
            "result": """[(737400,)]""",
            "answer": """The count of total graded shg in december 2023 is 737400.""",
        },
        {
            "input": "count of a graded shg in december 2023?",
            "sql_cmd": """SELECT COUNT(a.clf_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE a.year = 2023 and a.month_name = 'Dec' AND a.final_grade = 'A' AND c.record_status = 1""",
            "result": """[(245001,)]""",
            "answer": """The count of A graded shg in december 2023 is 245001.""",
        },
        {
            "input": "Distribution of a and a+ grade shg in januray 2024?",
            "sql_cmd": """SELECT distinct a.final_grade as grade
            , COUNT(a.clf_id) AS shg_count
            FROM shg_masik_grading a
            INNER JOIN m_cbo c ON a.shg_id = c.cbo_id
            WHERE a.year = 2024 and a.month_name = 'Jan' AND a.final_grade in ('A+', 'A') AND c.record_status = 1
            group by 1""",
            "result": """[(('A', 256853), ('A+', 115866),)]""",
            "answer": """Distribution of a and a+ grade shg in januray 2024 are:
            - A: 256853
            - A+: 115866 """,
        },
        {
            "input": "give the grade distribution of vo for december 2023?",
            "sql_cmd": """SELECT a.final_grade, COUNT(a.clf_id) AS vo_count
            FROM vo_masik_grading a
            INNER JOIN m_cbo c ON a.vo_id = c.cbo_id
            WHERE a.year = 2023 and a.month_name = 'Dec' AND c.record_status = 1
            GROUP BY a.final_grade""",
            "result": """[('A', 97), ('B', 3809), ('C', 28475)]""",
            "answer": """The grade distribution of village organisations (VOs) for December 2023 is as follows:

            - A: 97
            - B: 3809
            - C: 28475""",
        },
        {
           "input": "total count of farmers",
            "sql_cmd": """SELECT
                            COUNT(DISTINCT FARMER_ID) AS total_farmers
                        FROM
                            m_farmer""",
            "result": """[(3477121,)]""",
            "answer": """There are 3477121 total farmers""", 
        },
        {
            "input": "total count of engaged farmers or active farmers or farmers with active transaction",
            "sql_cmd": """SELECT
                            COUNT(DISTINCT FARMER_ID) AS total_farmers
                        FROM
                            t_farmer_transaction""",
            "result": """[(2439044,)]""",
            "answer": """There are 2439044 total engaged farmers or ctive farmers or transaction farmers""", 
        },
        {
              "input": "active farmers in 2023-2024",
            "sql_cmd": """SELECT
    COUNT(DISTINCT FARMER_ID) AS total_farmers
FROM
    t_farmer_transaction
WHERE
    FY = '2023-2024'""",
            "result": """[(2006052,)]""",
            "answer": """There are 2006052 active farmers in 2023-2024""", 
        },
        {
            "input": "number of farmers having lease land",
            "sql_cmd": """SELECT
    COUNT(DISTINCT FARMER_ID) AS farmers_with_lease_land
FROM
    m_farmer_land
WHERE
    LANDHOLDINGLEASE > 0""",
            "result": """[(1682700,)]""",
            "answer": """There are 1682700 number of farmers having lease land""", 
        },
        {
            "input": "no of shg having farmer",
            "sql_cmd": """select count(distinct shg_id) from t_farmer_transaction""",
            "result": """[(3877787,)]""",
            "answer": """There are 3877787 shg having farmer"""
        },
        {
            "input": "number of active farmers in banka",
            "sql_cmd": """SELECT
    COUNT(DISTINCT tf.FARMER_ID) AS total_farmers
FROM
    t_farmer_transaction tf
    
INNER JOIN m_farmer f ON tf.farmer_id=f.farmer_id
INNER JOIN mp_cbo_member t ON t.member_id=f.member_id
INNER JOIN m_cbo c ON c.cbo_id=t.cbo_id

        WHERE
            c.DISTRICT_ID = (
                SELECT
                    DISTRICT_ID
                FROM
                    m_district
                WHERE
                    upper(DISTRICT_NAME) = 'BANKA'
            )""",
            "result": """[(69435,)]""",
            "answer": """There are 69435 active farmers in banka district"""
        },
        {
            "input": "count of local seed used by farmer in 2018-2019",
            "sql_cmd": """select count(distinct farmer_id) as seed_count from t_farmer_transaction ft
inner join m_farmer_seed s on ft.seed_type_id=s.seed_type_id
where UPPER(s.seed_type)='LOCAL' AND
ft.FY='2018-2019'""",
            "result": """[(82811,)]""",
            "answer": """82811 local seed used by farmer in 2018-2019"""
        },
        {
             "input": "count number of farmers grew kharif crops",
            "sql_cmd": """SELECT
    COUNT(DISTINCT f.FARMER_ID) AS total_farmers
FROM
    m_farmer f
INNER JOIN
    t_farmer_transaction t ON f.FARMER_ID = t.FARMER_ID
WHERE
    t.CROP_TYPE_ID = (
        SELECT
            CROP_TYPE_ID
        FROM
            m_farmer_croptype
        WHERE
            CROP_TYPE = 'Kharif Crops'
    )""",
            "result": """[(82811,)]""",
            "answer": """82811 farmers grew kharif crops"""
        },
        {
            "input": "total count of agri enterprenure",
            "sql_cmd": """select count(id) from profile_entry""",
            "result": """[(3932,)]""",
            "answer": """3932 count of agri enterprenure"""
        },
        {
                "input": "total count of agri enterprenure in 2024",
            "sql_cmd": """SELECT COUNT(id) 
FROM profile_entry 
WHERE EXTRACT(YEAR FROM date_of_joining) = 2024""",
            "result": """[(220,)]""",
            "answer": """220 total count of agri enterprenure in 2024"""
        },
        {
           "input": "total expenditure amount of agri enterprenures",
            "sql_cmd": """select sum(amount) from t_expenditure_details""",
            "result": """[(3156902,)]""",
            "answer": """total expenditure amount of agri enterprenures 3156902""" 
        },
        {
               "input": "total sell grain amount of agri enterprenures",
            "sql_cmd": """select sum(total_amount) from t_sell_grain""",
            "result": """[(12652544.70)]""",
            "answer": """total sell grain amount of agri enterprenures are 12652544.70""" 
        },
        {
            "input": "no of active enterprenure in agri input ativity",
            "sql_cmd": """select count(distinct entry_by) from t_agri_input where entry_by is not null""",
            "result": """[(177)]""",
            "answer": """177 no of active enterprenure in agri input ativity""" 
        },
        {
            "input": "no of active enterprenure in advisory farmer activity",
            "sql_cmd": """select count(distinct entry_by) from t_advisory_farmer_entry where entry_by is not null""",
            "result": """[(180)]""",
            "answer": """180 no of active enterprenure in advisory farmer activity"""
        },
        {
            "input": "no of active enterprenure in marketing services activity",
            "sql_cmd": """select count(distinct entry_by) from t_marketing_services where entry_by is not null""",
            "result": """[(73)]""",
            "answer": """73 no of active enterprenure in marketing services activity"""
        },
        {
            "input": "no of active enterprenure in digital banking activity",
            "sql_cmd": """select count(distinct entry_by) from t_digital_banking where entry_by is not null""",
            "result": """[(205)]""",
            "answer": """205 no of active enterprenure in digital banking activity"""
        },
        {
             "input": "no of active enterprenure in nursery services activity",
            "sql_cmd": """select count(distinct entry_by) from t_nursery_services where entry_by is not null""",
            "result": """[(89)]""",
            "answer": """89 no of active enterprenure in nursery services activity"""
        },
        {
              "input": "total active agri enterprenures district wise",
            "sql_cmd": """SELECT pe.district_name, 
       COUNT(DISTINCT CASE WHEN ai.entry_by = pe.person_id THEN pe.person_id END) +
       COUNT(DISTINCT CASE WHEN afe.entry_by = pe.person_id THEN pe.person_id END) +
       COUNT(DISTINCT CASE WHEN ms.entry_by = pe.person_id THEN pe.person_id END) +
       COUNT(DISTINCT CASE WHEN db.entry_by = pe.person_id THEN pe.person_id END) +
       COUNT(DISTINCT CASE WHEN ns.entry_by = pe.person_id THEN pe.person_id END) AS total_active_entrepreneurs
FROM profile_entry pe
LEFT JOIN t_agri_input ai ON pe.person_id = ai.entry_by
LEFT JOIN t_advisory_farmer_entry afe ON pe.person_id = afe.entry_by
LEFT JOIN t_marketing_services ms ON pe.person_id = ms.entry_by
LEFT JOIN t_digital_banking db ON pe.person_id = db.entry_by
LEFT JOIN t_nursery_services ns ON pe.person_id = ns.entry_by
WHERE pe.person_id IS NOT NULL
GROUP BY pe.district_name""",
            "result": """[("ARARIA"	67
"ARWAL"	2
"AURANGABAD"	167
"BANKA"	35
"BEGUSARAI"	24
"BHAGALPUR"	3
"BHOJPUR"	90
"BUXAR"	88
"DARBHANGA"	20)]""",
            "answer": """"ARARIA"	67
"ARWAL"	2
"AURANGABAD"	167
"BANKA"	35
"BEGUSARAI"	24
"BHAGALPUR"	3
"BHOJPUR"	90
"BUXAR"	88
"DARBHANGA"	20"""
        },
        {
            "input": "total count of chc",
            "sql_cmd": """select count(distinct id) from m_chc_details """,
            "result": """[(511)]""",
            "answer": """511 are total chc""" 
        },
        {
            "input": "total count of active chc",
            "sql_cmd": """select count(distinct chc_id) from t_farmer_booking""",
            "result": """[(462)]""",
            "answer": """total active chc are 462""" 
        },
        {
            "input": "give me total count of active chc",
            "sql_cmd": """select count(distinct chc_id) from t_farmer_booking""",
            "result": """[(462)]""",
            "answer": """total active chc are 462""" 
        },
        {
            "input": "how many service booking completed by farmer?",
            "sql_cmd": """select count(distinct booking_id) from t_farmer_booking where service_completed_satus=1""",
            "result": """[(462)]""",
            "answer": """total active chc are 462""" 
        },
        {
            "input": "give me total expenditure details of chc",
            "sql_cmd": """select sum(amount) from t_chc_expenditure_details""",
            "result": """[(13232575)]""",
            "answer": """13232575 total expenditure details of chc""" 
        },
        {
            "input": "give me total revenue generated of chc",
            "sql_cmd": """select sum(total_amount) from t_freight_details""",
            "result": """[(19335019.00)]""",
            "answer": """19335019.00 total revenue generated of chc"""
        },
        {
            "input": "give me number of machines used in chc",
            "sql_cmd": """select count(id) from m_machine""",
            "result": """[(37)]""",
            "answer": """37 number of machines used in chc"""
        },
        {
            "input": "machines used in hours",
            "sql_cmd": """select sum(total_area_or_hour) from t_freight_details t
inner join m_chc_details mc on t.chc_id=mc.id
inner join m_machine m on m.id=t.machine_id
where mc.district_id is not null
and m.machine_name is not null
and upper(t.unit_type)='HOUR'""",
            "result": """[(26156.73)]""",
            "answer": """26156.73 machines used in hours"""
        },
        {
             "input": "machines used in kathas",
            "sql_cmd": """select sum(total_area_or_hour) from t_freight_details t
inner join m_chc_details mc on t.chc_id=mc.id
inner join m_machine m on m.id=t.machine_id
where mc.district_id is not null
and m.machine_name is not null
and upper(t.unit_type)='KATTHA'""",
            "result": """[(26156.73)]""",
            "answer": """26156.73 machines used in hours"""
        },
        {
             "input": "total booking done by farmers",
            "sql_cmd": """select count(booking_id) from t_farmer_booking tf
inner join m_district d on tf.district_id=d.district_id
where d.district_name is not null""",
            "result": """[(47004)]""",
            "answer": """47004 total booking done by farmers"""
        },
        {
            "input": "total booking done by farmers in nawada district",
            "sql_cmd": """select count(booking_id) from t_farmer_booking tf
inner join m_district d on tf.district_id=d.district_id
where upper(d.district_name)='NAWADA'""",
            "result": """[(1)]""",
            "answer": """1 booking done by farmers in nawada district"""
        },
        {
             "input": "total quantity of neera sold",
            "sql_cmd": """SELECT 
    SUM(fresh_neera) + SUM(temp_sell_center_sold_neera) + SUM(compfed) + SUM(perm_sell_center_sold_neera) AS total_sum
FROM neera_selling
""",
            "result": """[(20606429.640)]""",
            "answer": """20606429.640 total quantity of neera sold"""

        },
        {
            
            "input": "quantity of neera collected",
            "sql_cmd": """select sum(quantity) from neera_collection """,
            "result": """[(21832429.220)]""",
            "answer": """21832429.220 quantity of neera collected"""
        },
        {
            "input": "group of neera production",
            "sql_cmd": """select count(id) from m_pg where bank_ac_number is not null and upper(is_active)='Y'""",
            "result": """[(577)]""",
            "answer": """577 group of neera production"""
        },
        {
             "input": "Total count of PG in neera",
            "sql_cmd": """select count(pg_id) from m_pg where is_active='Y'""",
            "result": """[(1014)]""",
            "answer": """1014 Total count of PG in neera"""
        },
        {
            "input": "Total count of tappers",
            "sql_cmd": """select count(id) from pg_non_pg_memberes where is_active='Y'""",
            "result": """[(16879)]""",
            "answer": """16879 Total count of tappers"""
        },
        {
             "input": "Total number of libraries in didi ki library",
            "sql_cmd": """select count(distinct clcdc_id) from m_clcdc where clcdc_name is not null and district_id is not null""",
            "result": """[(124)]""",
            "answer": """124 Total number of libraries in didi ki library"""
        },
        {
             "input": "Total number of vidya didi",
            "sql_cmd": """select count(distinct id) from t_vidya_didi where district_name is not null""",
            "result": """[(93)]""",
            "answer": """93 Total number of vidya didi"""
        },
        {
            "input": "Total number of learners",
            "sql_cmd": """select count(distinct registration_no) from t_learner_profile where district_name is not null""",
            "result": """[(20634)]""",
            "answer": """20634 Total number of learners"""
        },
        {
            "input": "Total number of libraries district wise",
            "sql_cmd": """SELECT m.district_name, COUNT(DISTINCT cl.clcdc_id)
FROM m_clcdc cl
INNER JOIN m_district m ON cl.district_id = m.district_id
WHERE cl.clcdc_name IS NOT NULL AND m.district_id IS NOT NULL
GROUP BY m.district_name""",
            "result": """"ARARIA"	3
"ARWAL"	3
"AURANGABAD"	2
"BANKA"	2
"BEGUSARAI"	4
"BHAGALPUR"	4
"BHOJPUR"	5
"BUXAR"	5
"DARBHANGA"	4
"GOPALGANJ"	3""",
            "answer": """"ARARIA"	3
"ARWAL"	3
"AURANGABAD"	2
"BANKA"	2
"BEGUSARAI"	4
"BHAGALPUR"	4
"BHOJPUR"	5
"BUXAR"	5
"DARBHANGA"	4
"GOPALGANJ"	3"""
        },
        {
            "input": "Total vidya didi district wise",
            "sql_cmd": """SELECT m.district_name, count(distinct id) from t_vidya_didi t
INNER JOIN m_district m ON t.district_id = m.district_id
GROUP BY m.district_name;""",
            "result": """[("ARARIA"	2
"ARWAL"	3
"AURANGABAD"	3
"BANKA"	1
"BEGUSARAI"	3
"BHAGALPUR"	4
"BHOJPUR"	4
"BUXAR"	4
"DARBHANGA"	4
"GOPALGANJ"	3)]""",
            "answer": """"ARARIA"	2
"ARWAL"	3
"AURANGABAD"	3
"BANKA"	1
"BEGUSARAI"	3
"BHAGALPUR"	4
"BHOJPUR"	4
"BUXAR"	4
"DARBHANGA"	4
"GOPALGANJ"	3"""
        },
        {
            
             "input": "total count of nursery till now",
            "sql_cmd": """SELECT (
    SELECT COUNT(DISTINCT id) FROM mp_nursery_fy
) +
(
    SELECT COUNT(DISTINCT id) FROM profile_entry_2
) AS total_count""",
            "result": """[(602)]""",
            "answer": """602 total count of nursery till now"""
        },
        {
            "input": "total count of nursery in 2023-2024",
            "sql_cmd": """SELECT (
    SELECT COUNT(DISTINCT id)
    FROM mp_nursery_fy
    WHERE fy = '2023-2024'
) +
(
    SELECT COUNT(DISTINCT id)
    FROM profile_entry_2
	where financial_year_name='2023-2024'
) AS total_count""",
            "result": """[(183)]""",
            "answer": """183 total count of nursery in 2023-2024"""
        },
        {
            "input": "total number of plant to sell",
            "sql_cmd": """select sum(total_plant_to_sell) from t_sell_plant""",
            "result": """[(1100)]""",
            "answer": """1100 total number of plant to sell"""
        },
        {
            "input": "give total number of plant to sell in 2023-2024",
            "sql_cmd": """select sum(total_plant_to_sell) from t_sell_plant where fy='2023-2024'  """,
            "result": """[(225)]""",
            "answer": """225 total number of plant to sell in 2023-2024"""
        },
        {
            "input": "total plant sell in didi ki nursery year wise",
            "sql_cmd": """select tp.fy,sum(tp.total_plant_to_sell) from t_sell_plant tp 
inner join m_district m on tp.district_id=m.district_id
group by tp.fy""",
            "result": """[("2022-2023"	175
"2023-2024"	225
"2019-2020"	700)]""",
            "answer": """"2022-2023"	175
"2023-2024"	225
"2019-2020"	700"""
        },
        {
            "input": "total recieved amount in didi ki nursery",
            "sql_cmd": """select sum(total_amount) from t_payment_receive_details  """,
            "result": """[(50000)]""",
            "answer": """50000 total recieved amount in didi ki nursery"""
        },
        {
            "input": "total expenditure in didi ki nursery",
            "sql_cmd": """select sum(amount) from t_expenditure_details  """,
            "result": """[(3444992)]""",
            "answer": """3444992 total expenditure in didi ki nursery"""
        },
        {
              "input": "total expenditure in didi ki nursery in 2023-2024",
            "sql_cmd": """select sum(amount) from t_expenditure_details  """,
            "result": """[(3444992)]""",
            "answer": """3444992 total expenditure in didi ki nursery"""
        },
        {
            "input": "total expenditure details in didi ki nursery district wise",
            "sql_cmd": """select m.district_name,sum(t.amount) from t_expenditure_details t
inner join m_district m on t.district_id=m.district_id
group by m.district_name""",
            "result": """[("MUNGER"	40000
"PATNA"	203775
"LAKHISARAI"	17250
"DARBHANGA"	82700
"SARAN"	20000
"ROHTAS"	25000
"SITAMARHI"	10000)]""",
            "answer": """3"MUNGER"	40000
"PATNA"	203775
"LAKHISARAI"	17250
"DARBHANGA"	82700
"SARAN"	20000
"ROHTAS"	25000
"SITAMARHI"	10000"""
        },
        {
            
              "input": "total expenditure in didi ki nursery year wise",
            "sql_cmd": """select t.fy,sum(t.amount) from t_expenditure_details t
inner join m_district m on t.district_id=m.district_id
group by t.fy""",
            "result": """[("2023-2024"	3317721
"2022-2023"	127271)]""",
            "answer": """"2023-2024"	3317721
"2022-2023"	127271"""
        },
        {
            
             "input": "Total count agent in bank sakhi",
            "sql_cmd": """select count(distinct agent_id) from m_bankdataupload""",
            "result": """[(5511)]""",
            "answer": """5511 Total count agent in bank sakhi"""
        },
        {
             "input": "Total count transacted agent in bank sakhi",
            "sql_cmd": """select count(distinct agent_name) from m_bankdataupload where agent_name is not null""",
            "result": """[(5167)]""",
            "answer": """5167 Total count transacted agent in bank sakhi"""
        },
        {
            
             "input": "Total count of iibf certified agent in bank sakhi",
            "sql_cmd": """select count(distinct mg.agent_id) from m_agentnew mg
inner join m_bankdataupload mb on mg.agent_id=mb.agent_id
where mb.agent_name is not null and  mg.iibf='PASS'""",
            "result": """[(4073)]""",
            "answer": """4073 Total count of iibf certified agent in bank sakhi"""
        },
        {
            "input": "Total number of account open in bank sakhi",
            "sql_cmd": """select sum(total_account_open) from m_bankdataupload where agent_name is not null""",
            "result": """[(942432)]""",
            "answer": """942432 Total number of account open in bank sakhi"""
        },
        {
            "input": "Total number of transaction in bank sakhi",
            "sql_cmd": """select sum(total_no_of_tranx) from m_bankdataupload where agent_name is not null""",
            "result": """[(27893538)]""",
            "answer": """27893538 Total number of transaction in bank sakhi"""
        },
        {
            "input": "total amount of transaction in bank sakhi",
            "sql_cmd": """select sum(total_amt_of_tranx) from m_bankdataupload where agent_name is not null""",
            "result": """[(118563008461.11722)]""",
            "answer": """118563008461.11722 total amount of transaction in bank sakhi"""
        },
        {
            "input": "total commission earned in bank sakhi",
            "sql_cmd": """select sum(total_commission) from m_bankdataupload where agent_name is not null""",
            "result": """[(285589411.90768486)]""",
            "answer": """285589411.90768486 total commission earned in bank sakhi"""
        },
        {
            "input": "total count of agent in 2018 and 2019 in bank sakhi",
            "sql_cmd": """SELECT COUNT(DISTINCT mg.agent_id) 
FROM m_agentnew mg 
INNER JOIN m_bankdataupload mb ON mg.agent_id = mb.agent_id 
WHERE mb.agent_name IS NOT NULL 
AND EXTRACT(YEAR FROM mg.date_of_activation) IN (2018, 2019);""",
            "result": """[(495)]""",
            "answer": """495 total count of agent in 2018 and 2019 in bank sakhi"""
        },
        {
            "input": "total count of agent in BANKA district",
            "sql_cmd": """SELECT COUNT(DISTINCT mg.agent_id) 
FROM m_agentnew mg 
INNER JOIN m_bankdataupload mb ON mg.agent_id = mb.agent_id 
WHERE mb.agent_name IS NOT NULL 
AND upper(mg.district_name)='BANKA'""",
            "result": """[(128)]""",
            "answer": """128 total count of agent in BANKA district"""
        }, 
        {
            "input": "In how many districts poultry is there?",
            "sql_cmd": """select count(distinct district_id) as total_districts
            from mp_pg_member""",
            "result": """[(38,)]""",
            "answer": """Poultry is present in 38 districts.""",
        },
        {
            "input": "Poultry is open in how many districts?",
            "sql_cmd": """select count(distinct district_id) as total_districts
            from mp_pg_member""",
            "result": """[(38,)]""",
            "answer": """Poultry is open in 38 districts.""",
        },
        {
            "input": "Poultry is open in how many districts in IPDS-2 scheme?",
            "sql_cmd": """select count(distinct a.district_id) as total_districts
            from mp_pg_member a
			inner join t_household_batch b on a.member_id = b.member_id
			where upper(b.scheme) = 'IPDS-2'""",
            "result": """[(36,)]""",
            "answer": """Poultry is open in 36 districts in IPDS-2 scheme.""",
        },
        {
            "input": "In how many blocks poultry is there?",
            "sql_cmd": """select count(distinct block_id) as total_blocks
            from mp_pg_member""",
            "result": """[(303,)]""",
            "answer": """Poultry is present in 303 blocks.""",
        },
        {
            "input": "Poultry is open in how many blocks?",
            "sql_cmd": """select count(distinct block_id) as total_blocks
            from mp_pg_member""",
            "result": """[(303,)]""",
            "answer": """Poultry is open in 303 blocks.""",
        },
        {
            "input": "Poultry is open in how many blocks in IPDS-2 scheme?",
            "sql_cmd": """select count(distinct a.block_id) as total_districts
            from mp_pg_member a
			inner join t_household_batch b on a.member_id = b.member_id
			where upper(b.scheme) = 'IPDS-2'""",
            "result": """[(276,)]""",
            "answer": """Poultry is open in 276 blocks in IPDS-2 scheme.""",
        },
        {
            "input": "what is the total number of pgs in poultry?",
            "sql_cmd": """select count(distinct pg_id) as total_pgs
            from t_household_batch""",
            "result": """[(377,)]""",
            "answer": """Total number of pgs in poultry is 377.""",
        },
        {
            "input": "what is the total number of pgs in poultry in IPDS-2 scheme?",
            "sql_cmd": """select count(distinct pg_id) as total_pgs
            from t_household_batch
            where upper(scheme) = 'IPDS-2'""",
            "result": """[(362,)]""",
            "answer": """Total number of pgs in poultry is 362.""",
        },
        {
            "input": "what is the total number of pgs in poultry in patna district",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where upper(c.district_name) = 'PATNA'""",
            "result": """[(13,)]""",
            "answer": """Total number of pgs in poultry in patna district is 13.""",
        },
        {
            "input": "what is the total number of pgs in poultry in patna district in IPDS-2 scheme",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where upper(c.district_name) = 'PATNA'
            and upper(scheme) = 'IPDS-2'""",
            "result": """[(11,)]""",
            "answer": """Total number of pgs in poultry in patna district in IPDS-2 scheme is 11.""",
        },
        {
            "input": "what is the total number of pgs in poultry in arrah block",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where upper(c.block_name) = 'ARRAH'""",
            "result": """[(1,)]""",
            "answer": """Total number of pgs in poultry in arrah block is 1.""",
        },
        {
            "input": "what is the total number of pgs in poultry in arrah block in IPDS-2 scheme",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where upper(c.block_name) = 'ARRAH'
            and upper(scheme) = 'IPDS-2'""",
            "result": """[(1,)]""",
            "answer": """Total number of pgs in poultry in arrah block in IPDS-2 scheme is 1.""",
        },
        {
            "input": "What is the total number of pg in poultry in 2023",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            where b.created_on BETWEEN '2023-01-01' AND '2023-12-31'""",
            "result": """[(161,)]""",
            "answer": """The total number of pg in poultry in 2023 is 161.""",
        },
        {
            "input": "Total number of pg in poultry in 2023-2024",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            where b.created_on BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(175,)]""",
            "answer": """The total number of pg in poultry in 2023-2024 is 175.""",
        },
        {
            "input": "Total number of pg in poultry in 2023-2024 in nalanda district?",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where b.created_on BETWEEN '2023-04-01' AND '2024-03-31'
            and upper(c.district_name) = 'PATNA'""",
            "result": """[(7,)]""",
            "answer": """The total number of pg in poultry in 2023-2024 in nalanda district is 7.""",
        },
        {
            "input": "Total number of pg in poultry in 2023-2024 in arrah block?",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where b.created_on BETWEEN '2023-04-01' AND '2024-03-31'
            and upper(c.block_name) = 'ARRAH'""",
            "result": """[(0,)]""",
            "answer": """The total number of pg in poultry in 2023-2024 in arrah block is 0.""",
        },
        {
            "input": "what is the total number of pgs in poultry in patna district in 2023-2024",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where upper(c.district_name) = 'PATNA'
			and b.created_on BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(7,)]""",
            "answer": """Total number of pgs in poultry in patna district in 2023-2024 is 7""",
        },
        {
            "input": "Total number of pg in poultry in january 2024",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            where b.created_on BETWEEN '2024-01-01' AND '2024-01-31'""",
            "result": """[(26,)]""",
            "answer": """The total number of pg in poultry in january 2024is 26.""",
        },
        {
            "input": "Total number of pg in poultry in january 2024 in nalanda district",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where b.created_on BETWEEN '2024-01-01' AND '2024-01-31'
            and upper(c.district_name) = 'NALANDA'""",
            "result": """[(2,)]""",
            "answer": """The total number of pg in poultry in january 2024 in nalanda district is 2.""",
        },
        {
            "input": "Total number of pg in poultry in january 2024 in arrah block",
            "sql_cmd": """select count(distinct a.pg_id) as total_pgs
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where b.created_on BETWEEN '2024-01-01' AND '2024-01-31'
            and upper(c.block_name) = 'ARRAH'""",
            "result": """[(0,)]""",
            "answer": """The total number of pg in poultry in january 2024 in arrah block is 0.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry?",
            "sql_cmd": """select count(distinct member_id) as total_members
            from t_household_batch""",
            "result": """[(64167,)]""",
            "answer": """Total number of beneficiaries or members in poultry is 64167.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry in IPDS-2 scheme?",
            "sql_cmd": """select count(distinct member_id) as total_members
            from t_household_batch
            where upper(scheme) = 'IPDS-2'""",
            "result": """[(62551,)]""",
            "answer": """Total number of beneficiaries or members in poultry in IPDS-2 scheme is 62551.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry in patna district",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where upper(c.district_name) = 'PATNA'""",
            "result": """[(2310,)]""",
            "answer": """Total number of beneficiaries or members in poultry in patna district is 2310.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry in patna district in IPDS-2 scheme",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where upper(c.district_name) = 'PATNA'
            and upper(scheme) = 'IPDS-2'""",
            "result": """[(2112,)]""",
            "answer": """Total number of beneficiaries or members in poultry in patna district in IPDS-2 scheme is 2112.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry in arrah block",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where upper(c.block_name) = 'ARRAH'""",
            "result": """[(180,)]""",
            "answer": """Total number of beneficiaries or members in poultry in arrah block is 180.""",
        },
        {
            "input": "what is the total number of beneficiaries or members in poultry in arrah block in IPDS-2 scheme",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from t_household_batch a
            inner join mp_pg_member b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where upper(c.block_name) = 'ARRAH'
            and upper(scheme) = 'IPDS-2'""",
            "result": """[(180,)]""",
            "answer": """Total number of beneficiaries or members in poultry in arrah block in IPDS-2 scheme is 180.""",
        },
        {
            "input": "What is the count of chicks distributed?",
            "sql_cmd": """SELECT SUM(quantity_received) AS total_chicks_distributed
            FROM t_household_batch""",
            "result": """[(2528433,)]""",
            "answer": """The count of chicks distributed is 2528433""",
        },
        {
            "input": "Total number of chicks distributed?",
            "sql_cmd": """SELECT SUM(quantity_received) AS total_chicks_distributed
            FROM t_household_batch""",
            "result": """[(2528433,)]""",
            "answer": """The total number of chicks distributed is 2528433""",
        },
        {
            "input": "Total number of chicks distributed in IPDS-2 scheme?",
            "sql_cmd": """SELECT SUM(quantity_received) AS total_chicks_distributed
            FROM t_household_batch
            where upper(scheme) = 'IPDS-2'""",
            "result": """[(2508012,)]""",
            "answer": """The total number of chicks distributed in IPDS-2 scheme is 2508012""",
        },
        {
            "input": "What is the total number of chicks distributed in patna district",
            "sql_cmd": """SELECT SUM(a.quantity_received) AS total_chicks_distributed
            FROM t_household_batch a
            INNER JOIN mp_pg_member b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'PATNA'""",
            "result": """[(98494,)]""",
            "answer": """Total number of chicks distributed in patna district is 98494.""",
        },
        {
            "input": "What is the total number of chicks distributed in patna district IN IPDS-2 scheme",
            "sql_cmd": """SELECT SUM(a.quantity_received) AS total_chicks_distributed
            FROM t_household_batch a
            INNER JOIN mp_pg_member b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'PATNA'
            and upper(scheme) = 'IPDS-2'""",
            "result": """[(93494,)]""",
            "answer": """Total number of chicks distributed in patna district IPDS-2 scheme is 93494.""",
        },
        {
            "input": "What is the total number of chicks distributed in the finalcial year 2023-2024 in Patna district",
            "sql_cmd": """SELECT SUM(a.quantity_received) AS total_chicks_distributed
            FROM t_household_batch a
            INNER JOIN mp_pg_member b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'PATNA' AND b.created_on BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(15445,)]""",
            "answer": """Total number of chicks distributed in the finalcial year 2023-2024 in Patna district is 15445.""",
        },
        {
            "input": "What is the total number of chicks distributed in last six months",
            "sql_cmd": """SELECT SUM(a.quantity_received) AS total_chicks_distributed
            FROM t_household_batch a
            INNER JOIN mp_pg_member b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            WHERE b.created_on BETWEEN CURRENT_DATE - INTERVAL '6 MONTH' AND CURRENT_DATE""",
            "result": """[(155549,)]""",
            "answer": """The total number of chicks distributed in last six months in Patna district is 155549.""",
        },
        {
            "input": "What is the total number of chicks distributed in last six months in Patna district",
            "sql_cmd": """SELECT SUM(a.quantity_received) AS total_chicks_distributed
            FROM t_household_batch a
            INNER JOIN mp_pg_member b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            WHERE upper(c.district_name) = 'PATNA' 
            AND b.created_on BETWEEN CURRENT_DATE - INTERVAL '6 MONTH' AND CURRENT_DATE""",
            "result": """[(5445,)]""",
            "answer": """The total number of chicks distributed in last six months in Patna district is 5445.""",
        },
        {
            "input": "In how many districts goatry is there?",
            "sql_cmd": """select count(distinct district_id)
            from g_member_mapping""",
            "result": """[(19,)]""",
            "answer": """Goatry service is available in 19 districts.""",
        },
        {
            "input": "In how many districts goatry is there in IGSDS-4 scheme?",
            "sql_cmd": """select count(distinct a.district_id)
            from g_member_mapping a
			inner join g_goatry_distribution b on a.member_id = b.member_id
			where upper(scheme_name) = 'IGSDS-4'""",
            "result": """[(12,)]""",
            "answer": """Goatry service is available in 12 districts in IGSDS-4 scheme.""",
        },
        {
            "input": "What is the count of pgs in nalanda district in the financial year 2020-2021 in goatry?",
            "sql_cmd": """SELECT count( distinct a.pg_id) AS total_pgs
            FROM g_goatry_distribution a
            INNER JOIN g_member_mapping b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'NALANDA' AND a.date_of_procurement BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(10,)]""",
            "answer": """The count of pgs in nalanda district in the financial year 2020-2021 in goatry is 10.""",
        },
        {
            "input": "Total number of pg in goatry?",
            "sql_cmd": """select count(distinct pg_id)
            from g_goatry_distribution""",
            "result": """[(423,)]""",
            "answer": """Toatl number of PGs is 423.""",
        },
        {
            "input": "What is the total number of beneficiaries or members in goatry?",
            "sql_cmd": """select count(distinct member_id)
            from g_goatry_distribution""",
            "result": """[(16294,)]""",
            "answer": """Toatl number of beneficiaries or members in goatry is 16294.""",
        },
        {
            "input": "What is the total number of members in goatry?",
            "sql_cmd": """select count(distinct member_id)
            from g_goatry_distribution""",
            "result": """[(16294,)]""",
            "answer": """Toatl number of members in goatry is 16294.""",
        },
        {
            "input": "What is the count of goats distributed?",
            "sql_cmd": """SELECT SUM(no_of_goat_received) AS total_goats_distributed
            FROM g_goatry_distribution""",
            "result": """[(48882,)]""",
            "answer": """The count of goats distributed is 48882.""",
        },
        {
            "input": "What is the count of goats distributed in patna district in IGSDS-5 scheme?",
            "sql_cmd": """SELECT SUM(a.no_of_goat_received) AS total_goats_distributed
            FROM g_goatry_distribution a
            INNER JOIN g_member_mapping b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'PATNA' 
			AND upper(a.scheme_name) = 'IGSDS-5'""",
            "result": """[(1170,)]""",
            "answer": """Count of goats distributed in patna district in IGSDS-5 scheme is 1170.""",
        },
        {
            "input": "What is the count of goats distributed in arrah block in IGSDS-5 scheme?",
            "sql_cmd": """select count(distinct a.member_id) as total_goats_distributed
            from g_goatry_distribution a
            inner join g_member_mapping b on a.member_id = b.member_id
            inner join m_block c on b.block_id = c.block_id
            where upper(c.block_name) = 'ARRAH'
            and upper(scheme_name) = 'IGSDS -5'""",
            "result": """[(,)]""",
            "answer": """Count of goats distributed in arrah block in IGSDS-5 scheme is 0.""",
        },
        {
            "input": "What is the count of goats distributed in patna district in the financial year 2023-2024?",
            "sql_cmd": """SELECT SUM(a.no_of_goat_received) AS total_goats_distributed
            FROM g_goatry_distribution a
            INNER JOIN g_member_mapping b on a.member_id = b.member_id
            INNER join m_district c on b.district_id = c.district_id
            INNER join m_block d on b.block_id = d.block_id
            WHERE upper(c.district_name) = 'PATNA' AND b.created_on BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(1170,)]""",
            "answer": """Count of goats distributed in patna district in the financial year 2023-2024 is 1170.""",
        },
        {
            "input": "Give the list of blocks in which dairy is there?",
            "sql_cmd": """select distinct b.block_name
            from m_dcs_profile a
            inner join m_block b on a.block_id = b.block_id""",
            "result": """[(Alauli, Saraiya, Sandesh)]""",
            "answer": """The list of blocks in which dairy is there are:
            - Alauli
            - Saraiya
            - Sandesh""",
        },
        {
            "input": "Total number of districts in which dairy is there?",
            "sql_cmd": """select count(distinct district_id) as total_districts
            from m_dcs_profile""",
            "result": """[(3,)]""",
            "answer": """The total number of districts in which dairy is there is 3.""",
        },
        {
            "input": "Total number of blocks in which dairy is there?",
            "sql_cmd": """select count(distinct block_id) as total_blocks
            from m_dcs_profile""",
            "result": """[(3,)]""",
            "answer": """The total number of blocks in which dairy is there is 3.""",
        },
        {
            "input": "Total number of panchayats in which dairy is there?",
            "sql_cmd": """select count(distinct dcs_panchayat_id) as total_panchayats
            from m_dcs_profile""",
            "result": """[(5,)]""",
            "answer": """The total number of panchayats in which dairy is there is 5.""",
        },
        {
            "input": "what is the total number of shg member in dairy",
            "sql_cmd": """select count(distinct member_id) as total_member
            from mp_member_dcs
            where is_active = '1'""",
            "result": """[(33,)]""",
            "answer": """The total number of shg member in dairy is 33.""",
        },
        {
            "input": "what is the total number of dcs(dairy cop society)",
            "sql_cmd": """select count(distinct dcs_id) as total_dcs
            from m_dcs_profile""",
            "result": """[(5,)]""",
            "answer": """The total number of dcs is 5.""",
        },
        {
            "input": "what is the total number members involved in dairy in bhojpur district?",
            "sql_cmd": """select count(distinct a.member_id) as total_member
            from mp_member_dcs a
            inner join m_dcs_profile b on a.dcs_id = b.dcs_id
            inner join m_district d on b.district_id = d.district_id
            where upper(d.district_name) = 'BHOJPUR'""",
            "result": """[(1,)]""",
            "answer": """The total number members involved in dairy in bhojpur district is 1.""",
        },
        {
            "input": "what is the total number members involved in dairy in arrah block?",
            "sql_cmd": """select count(distinct a.member_id) as total_member
            from mp_member_dcs a
            inner join m_dcs_profile b on a.dcs_id = b.dcs_id
            inner join m_block d on b.block_id = d.block_id
            where upper(d.block_name) = 'ARRAH'""",
            "result": """[(0,)]""",
            "answer": """The total number members involved in dairy in arrah block is 0.""",
        },
        {
            "input": "what is the total number districts in which fishery is there",
            "sql_cmd": """select count(distinct district_id) as total_district
            from mp_pond_fpg_mapping""",
            "result": """[(26,)]""",
            "answer": """The total number districts in which fishery is there is 26.""",
        },
        {
            "input": "what is the total number blocks in which fishery is there",
            "sql_cmd": """select count(distinct block_id) as total_block
            from mp_pond_fpg_mapping""",
            "result": """[(78,)]""",
            "answer": """The total number blocks in which fishery is there is 78.""",
        },
        {
            "input": "what is the total number of batch in fishery?",
            "sql_cmd": """select count(distinct batch_number) as total_batch
            from batch_creation""",
            "result": """[(2,)]""",
            "answer": """The total number of batch in fishery is 2.""",
        },
        {
            "input": "what is the total number of batch in fishery in gaya district?",
            "sql_cmd": """select count(distinct a.batch_number) as total_batch
            from batch_creation a
			inner join m_district b on a.district_id = b.district_id
			where upper(b.district_name) = 'GAYA'""",
            "result": """[(1,)]""",
            "answer": """The total number of batch in fishery in gaya district is 1.""",
        },
        {
            "input": "what is the total number of batch in fishery in arrah block?",
            "sql_cmd": """select count(distinct a.batch_number) as total_batch
            from batch_creation a
			inner join m_block b on a.block_id = b.block_id
			where upper(b.block_name) = 'ARRAH'""",
            "result": """[(1,)]""",
            "answer": """The total number of batch in fishery in arrah block is 1.""",
        },
        {
            "input": "What is the total number of stocking pond water area",
            "sql_cmd": """select count(distinct actual_water_area_pond)
            from m_pond""",
            "result": """[(47,)]""",
            "answer": """the total number of stocking pond water area is 47.""",
        },
        {
            "input": "What is the total number of stocking pond water area in patna district?",
            "sql_cmd": """select count(distinct a.actual_water_area_pond)
            from m_pond a
			inner join m_district b on a.district_id = b.district_id
			where upper(b.district_name) = 'PATNA'""",
            "result": """[(4,)]""",
            "answer": """the total number of stocking pond water area in patna district is 4.""",
        },
        {
            "input": "What is the total number of stocking pond water area in arrah block?",
            "sql_cmd": """select count(distinct a.actual_water_area_pond)
            from m_pond a
			inner join m_block b on a.block_id = b.block_id
			where upper(b.block_name) = 'ARRAH'""",
            "result": """[(2,)]""",
            "answer": """the total number of stocking pond water area in arrah block is 2.""",
        },
        {
            "input": "What is the total number of harvesting done?",
            "sql_cmd": """select count(distinct id) as total_harvesting
            from batch_creation
            where is_cycle_completed = 1""",
            "result": """[(5,)]""",
            "answer": """The total number of harvesting done is 5""",
        },
        {
            "input": "What is the total number of harvesting done in patna district?",
            "sql_cmd": """select count(distinct a.id) as total_harvesting
            from batch_creation a
			inner join m_district b on a.district_id = b.district_id
            where a.is_cycle_completed = 1
			and upper(b.district_name) = 'PATNA'""",
            "result": """[(0,)]""",
            "answer": """The total number of harvesting done in patna district is 0.""",
        },
        {
            "input": "What is the total number of harvesting done in arrah block?",
            "sql_cmd": """select count(distinct a.id) as total_harvesting
            from batch_creation a
			inner join m_block b on a.block_id = b.block_id
            where a.is_cycle_completed = 1
			and upper(b.block_name) = 'ARRAH'""",
            "result": """[(1,)]""",
            "answer": """The total number of harvesting done in arrah block is 1.""",
        },
        {
            "input": "What is the quantity of fish harvested?",
            "sql_cmd": """select sum(weight_in_kg) as total_fish_harvested
            from t_sell_details""",
            "result": """[(94784,)]""",
            "answer": """The total number of harvesting done is 94784""",
        },
        {
            "input": "What is the quantity of fish harvested in patna district?",
            "sql_cmd": """select sum(a.weight_in_kg) as total_fish_harvested
            from t_sell_details a
			inner join m_district b on a.district_id = b.district_id
            where upper(b.district_name) = 'PATNA'""",
            "result": """[(0,)]""",
            "answer": """The total number of harvesting done in patna district is 0""",
        },
        {
            "input": "What is the quantity of fish harvested in arrah block?",
            "sql_cmd": """select sum(a.weight_in_kg) as total_fish_harvested
            from t_sell_details a
			inner join m_block b on a.block_id = b.block_id
            where upper(b.block_name) = 'ARRAH'""",
            "result": """[(310,)]""",
            "answer": """The total number of harvesting done in arrah block is 310""",
        },
        {
            "input": "What is the revenue generated from fish?",
            "sql_cmd": """select sum(sell_amount) as revenue_generated_from_fish
            from t_sell_details
            where fish_type_id != '8'""",
            "result": """[(1117312.00,)]""",
            "answer": """The revenue generated from fish is 1117312.00""",
        },
        {
            "input": "What is the revenue generated from fish in nawada district?",
            "sql_cmd": """select sum(a.sell_amount) as revenue_generated_from_fish
            from t_sell_details a
			inner join m_district b on a.district_id = b.district_id
			where fish_type_id != '8'
            and upper(b.district_name) = 'NAWADA'""",
            "result": """[(8000.00,)]""",
            "answer": """The revenue generated from fish in nawada district is 8000.00""",
        },
        {
            "input": "What is the revenue generated from fish in arrah block?",
            "sql_cmd": """select sum(a.sell_amount) as revenue_generated_from_fish
            from t_sell_details a
			inner join m_block b on a.block_id = b.block_id
			where fish_type_id != '8'
            and upper(b.block_name) = 'ARRAH'""",
            "result": """[(47510.00,)]""",
            "answer": """The revenue generated from fish in arrah block is 47510.00""",
        },
        {
            "input": "What is the total number of matasya sakhi ponds?",
            "sql_cmd": """select count(distinct matasya_sakhi_id) as total_matasya_sakhi_ponds
            from mp_matasya_sakhi_pond_mapping""",
            "result": """[(37,)]""",
            "answer": """The total number of matasya sakhi ponds is 37""",
        },
        {
            "input": "What is the total number of matasya sakhi ponds in nawada district?",
            "sql_cmd": """select count(distinct a.matasya_sakhi_id) as total_matasya_sakhi_ponds
            from mp_matasya_sakhi_pond_mapping a
			inner join m_district b on a.district_id = b.district_id
            where upper(b.district_name) = 'NAWADA'""",
            "result": """[(1,)]""",
            "answer": """The total number of matasya sakhi ponds in nawada district is 1.""",
        },
        {
            "input": "What is the total number of matasya sakhi ponds in arrah block?",
            "sql_cmd": """select count(distinct a.matasya_sakhi_id) as total_matasya_sakhi_ponds
            from mp_matasya_sakhi_pond_mapping a
			inner join m_block b on a.block_id = b.block_id
            where upper(b.block_name) = 'ARRAH'""",
            "result": """[(1,)]""",
            "answer": """The total number of matasya sakhi ponds in arrah block is 1.""",
        },
        {
            "input": "What is the total number of members in fishery?",
            "sql_cmd": """select count(distinct member_id) as total_members
            from mp_member_with_fpg_mapping""",
            "result": """[(387,)]""",
            "answer": """The total number of members in fishery is 387.""",
        },
        {
            "input": "What is the total number of members in fishery in nalanda district?",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from mp_member_with_fpg_mapping a
			inner join m_district b on a.district_id = b.district_id
            where upper(b.district_name) = 'NALANDA'""",
            "result": """[(43,)]""",
            "answer": """The total number of members in fishery in nalanda district is 43.""",
        },
        {
            "input": "What is the total number of members in fishery in arrah block?",
            "sql_cmd": """select count(distinct a.member_id) as total_members
            from mp_member_with_fpg_mapping a
			inner join m_block b on a.block_id = b.block_id
            where upper(b.block_name) = 'ARRAH'""",
            "result": """[(3,)]""",
            "answer": """The total number of members in fishery in arrah blockis 3.""",
        },
        {
            "input": "What is the total number of cnrp?",
            "sql_cmd": """select count(distinct a.user_id) as toatl_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1""",
            "result": """[(8772,)]""",
            "answer": """The total number cnrp is 8772.""",
        },
        {
            "input": "What is the total number of cnrp in munger district?",
            "sql_cmd": """select count(distinct a.user_id) as toatl_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district c on a.district_code = c.district_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and upper(c.district_name) = 'MUNGER'""",
            "result": """[(94,)]""",
            "answer": """The total number of cnrp in munger district is 94.""",
        },
        {
            "input": "What is the total number of cnrp in alauli block?",
            "sql_cmd": """select count(distinct a.user_id) as toatl_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_block c on a.block_code = c.block_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
			and upper(c.block_name) = 'ALAULI'""",
            "result": """[(24,)]""",
            "answer": """The total number of cnrp in alauli block is 24.""",
        },
        {
            "input": "What is the total number of cnrp in the year 2023-2024?",
            "sql_cmd": """select count(distinct a.user_id) as total_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(3650,)]""",
            "answer": """The total number of cnrp in the year 2023-2024 is 3650.""",
        },
        {
            "input": "What is the total number of cnrp in the year 2023-2024 in munger district?",
            "sql_cmd": """select count(distinct a.user_id) as total_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district d on a.district_code = d.district_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and upper(d.district_name) = 'MUNGER'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(19,)]""",
            "answer": """The total number of cnrp in the year 2023-2024 munger district is 19.""",
        },
        {
            "input": "What is the total number of cnrp in the year 2023-2024 in alauli block?",
            "sql_cmd": """select count(distinct a.user_id) as total_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_block d on a.block_code = d.block_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and upper(d.block_name) = 'ALAULI'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(10,)]""",
            "answer": """The total number of cnrp in the year 2023-2024 alauli block is 10.""",
        },
        {
            "input": "What is the count of trained cnrp in the year 2023-2024?",
            "sql_cmd": """select count(distinct c.cm_cnrp_id) as toatl_trained_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join t_training_of_cadre_and_pmt c on a.user_id = c.cm_cnrp_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and c.training_completed_status = 'Yes'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(1243,)]""",
            "answer": """The total count of trained cnrp in the year 2023-2024 is 1243 """,
        },
        {
            "input": "What is the count of trained cnrp in the year 2023-2024 in munger district?",
            "sql_cmd": """select count(distinct c.cm_cnrp_id) as toatl_trained_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join t_training_of_cadre_and_pmt c on a.user_id = c.cm_cnrp_id
            inner join m_district d on a.district_code = d.district_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and c.training_completed_status = 'Yes'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'
            and upper(d.district_name) = 'MUNGER'""",
            "result": """[(14,)]""",
            "answer": """The total count of trained cnrp in the year 2023-2024 in munger district is 15.""",
        },
        {
            "input": "What is the total number of active trained cnrp in buxar district?",
            "sql_cmd": """select count(distinct c.cm_cnrp_id) as toatl_trained_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join t_training_of_cadre_and_pmt c on a.user_id = c.cm_cnrp_id
            inner join m_district d on a.district_code = d.district_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and upper(c.training_completed_status) = 'YES'
            and upper(d.district_name) = 'BUXAR'""",
            "result": """[(129,)]""",
            "answer": """The total number of active trained cnrp in buxar district is 129""",
        }
        ,
        {
            "input": "What is the total number of active cnrp in arrah block in the financial year 2023-2024?",
            "sql_cmd": """select count(distinct a.user_id) as toatl_cnrp
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_block c on a.block_code = c.block_id
            where upper(a.user_type) = 'CNRP USER'
            and b.active = 1
            and upper(c.block_name) = 'ARRAH'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(10,)]""",
            "answer": """The total number of active cnrp in arrah block in the financial year 2023-2024 is 10""",
        },
        {
            "input": "What is the total number of mrp?",
            "sql_cmd": """select count(distinct a.user_id) as total_mrp_user
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1""",
            "result": """[(1692,)]""",
            "answer": """The total number mrp is 1692""",
        },
        {
            "input": "What is the total number of mrp in patna district?",
            "sql_cmd": """select count(distinct a.user_id) as total_mrp_user
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district c on a.district_code = c.district_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(c.district_name) = 'PATNA'""",
            "result": """[(75,)]""",
            "answer": """The total number of mrp user in patna district is 75.""",
        },
        {
            "input": "What is the total number of mrp in hilsa block?",
            "sql_cmd": """select count(distinct a.user_id) as total_mrp_user
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_block c on a.block_code = c.block_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(c.block_name) = 'HILSA'""",
            "result": """[(3,)]""",
            "answer": """The total number of mrp user in hilsa block is 3.""",
        },
        {
            "input": "What is the total number of mrp user in nalanda district in the financial year 2023-2024?",
            "sql_cmd": """select count(distinct a.user_id) as total_mrp_user
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district d on a.district_code = d.district_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(d.district_name) = 'NALANDA'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(15,)]""",
            "answer": """The total number of mrp user in nalanda district in the financial year 2023-2024 is 15""",
        },
        {
            "input": "What is the total number of hh member visit?",
            "sql_cmd": """select count(distinct a.user_id) as total_hh_visit
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1""",
            "result": """[(1692,)]""",
            "answer": """The total number hh member visit is 1692""",
        },
        {
            "input": "What is the total number of hh member visit in patna district?",
            "sql_cmd": """select count(distinct a.user_id) as total_hh_visit
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district c on a.district_code = c.district_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(c.district_name) = 'PATNA'""",
            "result": """[(75,)]""",
            "answer": """The total number of hh member visit in patna district is 75.""",
        },
        {
            "input": "What is the total number of hh member visit in hilsa block?",
            "sql_cmd": """select count(distinct a.user_id) as total_hh_visit
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_block c on a.block_code = c.block_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(c.block_name) = 'HILSA'""",
            "result": """[(3,)]""",
            "answer": """The total number of hh member visit in hilsa block is 3.""",
        },
        {
            "input": "What is the total number of hh member visit in nalanda district in the financial year 2023-2024?",
            "sql_cmd": """select count(distinct a.user_id) as total_hh_visit
            from m_profile a
            inner join m_shg_hns_user_table b on a.user_id = b.user_id
            inner join m_district d on a.district_code = d.district_id
            where upper(a.user_type) = 'MRP USER'
            and b.active = 1
            and upper(d.district_name) = 'NALANDA'
            and a.created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(15,)]""",
            "answer": """The total number of hh member visit in nalanda district in the financial year 2023-2024 is 15""",
        },

        {
            "input": "What is the total number of swasthya mitra?",
            "sql_cmd": """select count(distinct user_id) as total_swasthya_mitra
            from m_user_profile
            where active = 1
            and upper(user_type) = 'SWASTHYA MITRA'""",
            "result": """[(151,)]""",
            "answer": """The total number of swasthya mitra is 151.""",
        },
        {
            "input": "What is the total number of swasthya mitra in katihar district?",
            "sql_cmd": """select count(distinct user_id) as total_swasthya_mitra
            from m_user_profile
            where active = 1
            and upper(user_type) = 'SWASTHYA MITRA'
            and upper(dist_name) = 'KATIHAR'""",
            "result": """[(5,)]""",
            "answer": """The total number of swasthya mitra in katihar district is 5.""",
        },
        {
            "input": "What is the total number of swasthya mitra in fy(financial year 2023-2024)?",
            "sql_cmd": """select count(distinct user_id) as total_swasthya_mitra
            from m_user_profile
            where active = 1
            and upper(user_type) = 'SWASTHYA MITRA'
            and created_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(151,)]""",
            "answer": """The total number of swasthya mitra is 151.""",
        },
        {
            "input": "Total ipd?",
            "sql_cmd": """select count(distinct id) as total_ipd
            from t_patient_info
            where upper(service_type) = 'IPD'""",
            "result": """[(125699,)]""",
            "answer": """The total number of IPD is 125699.""",
        },
        {
            "input": "Total ipd in the fy(financial year) 2023-2024?",
            "sql_cmd": """select count(distinct id) as total_ipd
            from t_patient_info
            where upper(service_type) = 'IPD'
            and ipd_opd_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(115105,)]""",
            "answer": """The total number of ipd in the fy(financial year) 2023-2024 is 115105.""",
        },
        {
            "input": "What is the total number of ipd in rohtas district?",
            "sql_cmd": """select count(distinct a.id) as tatal_ipd
            from t_patient_info a
            inner join m_user_profile b on a.entry_by = b.user_id
            where upper(a.service_type) = 'IPD'
            and upper(b.dist_name) = 'ROHTAS'""",
            "result": """[(463,)]""",
            "answer": """The total number of ipd in rohtas district is 463.""",
        },
        {
            "input": "What is the total number of ipd in barh block?",
            "sql_cmd": """select count(distinct a.id) as total_ipd
            from t_patient_info a
            inner join m_block b on a.block_id = b.block_id
            where upper(a.service_type) = 'IPD'
            and upper(b.block_name) = 'BARH'""",
            "result": """[(36,)]""",
            "answer": """The total number of ipd in barh block is 36.""",
        },
        {
            "input": "Total opd?",
            "sql_cmd": """select count(distinct id) as total_opd
            from t_patient_info
            where upper(service_type) = 'OPD'""",
            "result": """[(618271,)]""",
            "answer": """The total number of OPD is 618271.""",
        },
        {
            "input": "Total opd in the fy(financial year) 2023-2024?",
            "sql_cmd": """select count(distinct id) as total_opd
            from t_patient_info
            where upper(service_type) = 'OPD'
            and ipd_opd_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(556693,)]""",
            "answer": """The total number of opd in the fy(financial year) 2023-2024 is 556693.""",
        },
        {
            "input": "What is the total number of opd in rohtas district?",
            "sql_cmd": """select count(distinct a.id) as total_opd
            from t_patient_info a
            inner join m_user_profile b on a.entry_by = b.user_id
            where upper(a.service_type) = 'OPD'
            and upper(b.dist_name) = 'ROHTAS'""",
            "result": """[(24217,)]""",
            "answer": """The total number of opd in rohtas district is 24217.""",
        },
        {
            "input": "What is the total number of opd in barh block?",
            "sql_cmd": """select count(distinct a.id) as total_opd
            from t_patient_info a
            inner join m_block b on a.block_id = b.block_id
            where upper(a.service_type) = 'OPD'
            and upper(b.block_name) = 'BARH'""",
            "result": """[(0,)]""",
            "answer": """The total number of opd in barh block is 0.""",
        },
        {
            "input": "What is the total number of opd in rohtas district in the fy (finalcial year) 2023-2024?",
            "sql_cmd": """select count(distinct a.id) as total_opd
            from t_patient_info a
            inner join m_user_profile b on a.entry_by = b.user_id
            where upper(a.service_type) = 'OPD'
            and upper(b.dist_name) = 'ROHTAS'
            and ipd_opd_date BETWEEN '2023-04-01' AND '2024-03-31'""",
            "result": """[(23374,)]""",
            "answer": """The total number of opd in in rohtas district in the fy (finalcial year) 2023-2024 23374.""",
        },
        {
            "input": "How many members are there in one (1) activity?",
            "sql_cmd": """SELECT COUNT(distinct member_id) AS member_count
            FROM(SELECT member_id, COUNT(DISTINCT activity_id) AS number_of_activities
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity)
            GROUP BY 1)
            WHERE number_of_activities = 1""",
            "result": """[(344153,)]""",
            "answer": """344153 memebers are there in one (1) activity.""",
        },
        {
            "input": "How many members are involved in multiple activity?",
            "sql_cmd": """SELECT number_of_activities, COUNT(*) AS member_count
            FROM(SELECT member_id, COUNT(DISTINCT activity_id) AS number_of_activities
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity)
            GROUP BY 1)
            GROUP BY 1""",
            "result": """[([(1, 344153), (2, 19654), (3, 2054, (4, 212), (5, 4), (6, 1)],)]""",
            "answer": """Members are involved in multiple activity are:
            - 1:  344153
            - 2: 19654
            - 3: 2054
            - 4: 212
            - 5: 4
            - 6: 1
            """,
        },
        {
            "input": "What is the total number of members involved in any activity in ARARIA district?",
            "sql_cmd": """SELECT count(distinct a.member_id) as member_count
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity
            ) as a
            inner join m_cbo_member b on a.member_id = b.member_id
            inner join m_district c on b.district_id = c.district_id
            where 0=0
            and upper(c.district_name) = 'ARARIA'""",
            "result": """[(5621,)]""",
            "answer": """The total number of members involved in any activity in ARARIA district is 5621.""",
        },
        {
            "input": "What is the count of total members in stitching?",
            "sql_cmd": """select count(distinct member_id) as total_member
            from mp_cbo_member_activity a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            where a.activity_id not in(1,2,3,19)
            and upper(b.activity_short_name) = 'STITCHING'""",
            "result": """[(2584,)]""",
            "answer": """The total number of members involved in stitching activity is 2584.""",
        },
        {
            "input": "Total members in araria district in vegetable farming?",
            "sql_cmd": """SELECT count(distinct a.member_id) as member_count
            FROM mp_cbo_member_activity a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            inner join m_cbo_member c on a.member_id = c.member_id
            inner join m_district d on c.district_id = d.district_id
            where a.activity_id not in(1,2,3,19)
            and upper(b.activity_short_name) = 'VEGETABLE FARMING'
            and upper(d.district_name) = 'ARARIA'""",
            "result": """[(174,)]""",
            "answer": """The total members in araria district in vegetable farming activity is 174.""",
        },
        {
            "input": "Total members in arrah block in vegetable farming?",
            "sql_cmd": """SELECT count(distinct a.member_id) as member_count
            FROM mp_cbo_member_activity a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            inner join m_cbo_member c on a.member_id = c.member_id
            inner join m_block d on c.block_id = d.block_id
            where a.activity_id not in(1,2,3,19)
            and upper(b.activity_short_name) = 'VEGETABLE FARMING'
            and upper(d.block_name) = 'ARRAH'""",
            "result": """[(37,)]""",
            "answer": """The total members in arrah block in vegetable farming activity is 37.""",
        },
        {
            "input": "Total members in bhopatpur village in vegetable farming?",
            "sql_cmd": """SELECT count(distinct a.member_id) as member_count
            FROM mp_cbo_member_activity a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            inner join m_cbo_member c on a.member_id = c.member_id
            inner join m_village d on c.village_id = d.village_id
            where a.activity_id not in(1,2,3,19)
            and upper(b.activity_short_name) = 'VEGETABLE FARMING'
            and upper(d.village_name) = 'BHOPATPUR'""",
            "result": """[(38,)]""",
            "answer": """The total members in bhopatpur village in vegetable farming activity is 38.""",
        },
        {
            "input": "Total members in angra panchayat in regular farming?",
            "sql_cmd": """SELECT count(distinct a.member_id) as member_count
            FROM mp_cbo_member_activity a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            inner join m_cbo_member c on a.member_id = c.member_id
            inner join m_village d on c.village_id = d.village_id
            inner join m_panchayat e on d.panchayat_id = e.panchayat_id
            where a.activity_id not in(1,2,3,19)
            and upper(b.activity_short_name) = 'REGULAR FARMING'
            and upper(e.panchayat_name) = 'ANGRA'""",
            "result": """[(58,)]""",
            "answer": """The total members in angra panchayat in regular farming activity is 58.""",
        },
        {
            "input": "List of activites and its member count",
            "sql_cmd": """SELECT distinct b.activity_short_name as activity_name
            , count(distinct a.member_id) as member_count
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity where activity_id not in(1,2,3,19)
            ) as a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            group by 1""",
            "result": """[(Aggarbatti, 6011), (Art and Craft, 3599), (Beekeeping, 7868), (Dairy, 36), (Fisheries, 387), (General Store, 176), (Goatery, 16339), (Jute, 2584), (Kirana Dukan, 45), (Lac Bangle, 116), (Madhubani Painting, 63), (Mulberry, 1018), (Neera, 3619), (Nutri Enterprise, 28), (Poultry, 63838), (R, 243), (Regular Farming, 49951), (Stitching, 410), (Vegetable Farming, 15367)]""",
            "answer": """The total number of members involved in stitching activity is (Aggarbatti, 6011), (Art and Craft, 3599), (Beekeeping, 7868), (Dairy, 36), (Fisheries, 387), (General Store, 176), (Goatery, 16339), (Jute, 2584), (Kirana Dukan, 45), (Lac Bangle, 116), (Madhubani Painting, 63), (Mulberry, 1018), (Neera, 3619), (Nutri Enterprise, 28), (Poultry, 63838), (R, 243), (Regular Farming, 49951), (Stitching, 410), (Vegetable Farming, 15367).""",
        },
        {
            "input": "Top 5 activites with highest number of members",
            "sql_cmd": """SELECT distinct b.activity_short_name as activity_name
            , count(distinct a.member_id) as member_count
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity where activity_id not in(1,2,3,19)
            ) as a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            group by 1
			order by member_count desc
			limit 5""",
            "result": """[(Poultry, 63838), (Regular Farming, 49951), (Goatery, 16339), (Vegetable Farming, 15367), (Beekeeping, 7868),]""",
            "answer": """Top 5 activites with highest number of members are: (Poultry, 63838), (Regular Farming, 49951), (Goatery, 16339), (Vegetable Farming, 15367), (Beekeeping, 7868).""",
        },
        {
            "input": "Bottom 5 activites with least number of members",
            "sql_cmd": """SELECT distinct b.activity_short_name as activity_name
            , count(distinct a.member_id) as member_count
            FROM (
            SELECT member_id, 1 AS activity_id FROM t_household_batch
            UNION
            SELECT member_id, 2 AS activity_id FROM g_goatry_distribution
            UNION
            SELECT member_id, 3 AS activity_id FROM mp_member_dcs
            UNION
            SELECT member_id, 19 AS activity_id FROM mp_member_with_fpg_mapping
            UNION
            SELECT member_id, activity_id FROM mp_cbo_member_activity where activity_id not in(1,2,3,19)
            ) as a
            inner join m_intervention_activity b on a.activity_id = b.activity_id
            group by 1
			order by member_count
			limit 5""",
            "result": """[(Nutri Enterprise, 28), (Dairy, 36), (Kirana Dukan, 45), (Madhubani Painting, 63), (Lac Bangle, 116),]""",
            "answer": """Bottom 5 activites with least number of members are: (Nutri Enterprise, 28), (Dairy, 36), (Kirana Dukan, 45), (Madhubani Painting, 63), (Lac Bangle, 116).""",
        },
        {
            "input": "What is the total number of employer registered?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window""",
            "result": """[(411,)]""",
            "answer": """The total number of employer registered is 411.""",
        },
        {
            "input": "What is the total number of employer registered in gaya district?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(district_name) = 'GAYA'""",
            "result": """[(40,)]""",
            "answer": """The total number of employer registered in gaya district is 40.""",
        },
        {
            "input": "What is the total number of employer registered in alauli block?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(block_name) = 'ALAULI'""",
            "result": """[(5,)]""",
            "answer": """The total number of employer registered in alauli block is 5""",
        },
        {
            "input": "What is the total number of employer registered in agri business?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(company_profile) = 'AGRI BUSINESS'""",
            "result": """[(6,)]""",
            "answer": """The total number of employer registered in agri business is 6.""",
        },
        {
            "input": "What is the total number of employer registered in consultancy work?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(company_profile) = 'CONSULTANCY WORK'""",
            "result": """[(1,)]""",
            "answer": """The total number of employer registered in consultancy work is 1.""",
        },
        {
            "input": "What is the total number of employer registered in agriculture in gaya district?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(district_name) = 'GAYA'
            and upper(company_profile) = 'AGRICULTURE'""",
            "result": """[(0,)]""",
            "answer": """The total number of employer registered in agriculture in gaya district is 0.""",
        },
        {
            "input": "What is the total number of employer registered in agriculture in alauli block?",
            "sql_cmd": """select count(district_id) as total_employer_registered
            from employer_window
            where upper(block_name) = 'ALAULI'
            and upper(company_profile) = 'AGRICULTURE'""",
            "result": """[(0,)]""",
            "answer": """The total number of employer registered in agriculture in alauli block is 0.""",
        },
        {
            "input": "What is the total number of job fair conducted?",
            "sql_cmd": """select count(district_id) as total_job_fair_conducted
            from plan_job_fair_training
            where upper(activity) = 'JOB FAIR'""",
            "result": """[(454,)]""",
            "answer": """The total number of job fair conducted is 454.""",
        },
        {
            "input": "What is the total number of job fair conducted in gaya district?",
            "sql_cmd": """select count(district_id) as total_job_fair_conducted
            from plan_job_fair_training
            where upper(activity) = 'JOB FAIR'
            and upper(district_name) = 'GAYA'""",
            "result": """[(12,)]""",
            "answer": """The total number of job fair conducted in gaya district is 12.""",
        },
        {
            "input": "What is the total number of job fair conducted in alauli block?",
            "sql_cmd": """select count(district_id) as total_job_fair_conducted
            from plan_job_fair_training
            where upper(activity) = 'JOB FAIR'
            and upper(block_name) = 'ALAULI'""",
            "result": """[(1,)]""",
            "answer": """The total number of job fair conducted in alauli block is 1.""",
        },
        {
            "input": "What is the total number of candidates registered?",
            "sql_cmd": """select count(distinct registration_number) as total_candidates_registered
            from candidates_profile""",
            "result": """[(223269,)]""",
            "answer": """The total number of candidates registered is 223269.""",
        },
        {
            "input": "What is the total number of candidates registered in patna district?",
            "sql_cmd": """select count(distinct a.registration_number) as total_candidates_registered
            from candidates_profile a
            inner join m_district b on a.district_id = b.district_id
            where upper(b.district_name) = 'PATNA'""",
            "result": """[(4639,)]""",
            "answer": """The total number of candidates registered in patna district is 4639.""",
        },
        {
            "input": "What is the total number of candidates registered in alauli block?",
            "sql_cmd": """select count(distinct a.registration_number) as total_candidates_registered
            from candidates_profile a
            inner join m_block b on a.block_id = b.block_id
            where upper(b.block_name) = 'ALAULI'""",
            "result": """[(99,)]""",
            "answer": """The total number of candidates registered in alauli block is 99.""",
        },
        {
            "input": "What is the total number of candidates registered in dabri village?",
            "sql_cmd": """select count(distinct a.registration_number) as total_candidates_registered
            from candidates_profile a
            inner join m_village b on a.village_id = b.village_id
            where upper(b.village_name) = 'DABRI'""",
            "result": """[(0,)]""",
            "answer": """The total number of candidates registered in dabri village is 0.""",
        },
        {
            "input": "What is the total number of candidates selected?",
            "sql_cmd": """select count(distinct registration_num) as total_candidates_selected
            from is_letter_offered
            where upper(is_offer_letter_issued) = 'Y'""",
            "result": """[(5051,)]""",
            "answer": """The total number of candidates selected is 5051.""",
        },
        {
            "input": "What is the total number of candidates selected in gaya district?",
            "sql_cmd": """select count(distinct registration_num) as total_candidates_selected
            from is_letter_offered
            where upper(is_offer_letter_issued) = 'Y'
            and upper(district_name) = 'GAYA'""",
            "result": """[(617,)]""",
            "answer": """total number of candidates selected in gaya district is 617.""",
        },
        {
            "input": "What is the total number of candidates selected in alauli block?",
            "sql_cmd": """select count(distinct registration_num) as total_candidates_selected
            from is_letter_offered
            where upper(is_offer_letter_issued) = 'Y'
            and upper(block_name) = 'ALAULI'""",
            "result": """[(22,)]""",
            "answer": """The total number of candidates selected in alauli block is 22.""",
        },
        {
            "input": "What is the total number of candidates selected in consultancy work?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidates_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_letter_issued) = 'Y'
            and upper(b.company_profile) = 'CONSULTANCY WORK'""",
            "result": """[(18,)]""",
            "answer": """The total number of candidates selected in consultancy work is 18.""",
        },
        {
            "input": "What is the total number of candidates selected in profile security guard?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidates_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_letter_issued) = 'Y'
            and upper(b.company_profile) = 'SECURITY GUARD'""",
            "result": """[(118,)]""",
            "answer": """The total number of candidates selected in profile security guard is 118.""",
        },
        {
            "input": "What is the total number of candidates selected in gaya district in agriculture?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidates_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_letter_issued) = 'Y'
            and upper(a.district_name) = 'GAYA'
            and upper(b.company_profile) = 'AGRICULTURE'""",
            "result": """[(0,)]""",
            "answer": """The total number of candidates selected in gaya district in agriculture is 0.""",
        },
        {
            "input": "What is the total number of candidates selected in alauli block in agriculture?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidates_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_letter_issued) = 'Y'
            and upper(a.block_name) = 'ALAULI'
            and upper(b.company_profile) = 'AGRICULTURE'""",
            "result": """[(0,)]""",
            "answer": """The total number of candidates selected in alauli block in agriculture is 0.""",
        },
        {
            "input": "What is the total number of candidates joined?",
            "sql_cmd": """select count(distinct registration_num) as total_candidated_joined
            from is_letter_offered
            where upper(is_offer_accepted) = 'Y'""",
            "result": """[(3953,)]""",
            "answer": """The total number of candidates joined is 3953.""",
        },
        {
            "input": "What is the total number of candidates joined in gaya district?",
            "sql_cmd": """select count(distinct registration_num) as total_candidated_joined
            from is_letter_offered
            where upper(is_offer_accepted) = 'Y'
            and upper(district_name) = 'GAYA'""",
            "result": """[(609,)]""",
            "answer": """The total number of candidates joined in gaya district is 609.""",
        },
        {
            "input": "What is the total number of candidates joined in alauli block?",
            "sql_cmd": """select count(distinct registration_num) as total_candidated_joined
            from is_letter_offered
            where upper(is_offer_accepted) = 'Y'
            and upper(block_name) = 'ALAULI'""",
            "result": """[(15,)]""",
            "answer": """The total number of candidates joined in alauli block is 15.""",
        },
        {
            "input": "What is the total number of candidates joined in consultancy work?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidates_joined
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_accepted) = 'Y'
            and upper(b.company_profile) = 'CONSULTANCY WORK'""",
            "result": """[(18,)]""",
            "answer": """The total number of candidates joined in consultancy work is 18.""",
        },
        {
            "input": "What is the total number of candidates joined in gaya district in agriculture?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidated_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_accepted) = 'Y'
            and upper(a.district_name) = 'GAYA'
            and upper(b.company_profile) = 'AGRICULTURE'""",
            "result": """[(0,)]""",
            "answer": """The total number of candidates joined in gaya district in agriculture is 0.""",
        },
        {
            "input": "What is the total number of candidates joined in alauli block in consultancy work?",
            "sql_cmd": """select count(distinct a.registration_num) as total_candidated_selected
            from is_letter_offered a
            inner join employer_window b on a.emp_id = b.id
            where upper(a.is_offer_accepted) = 'Y'
            and upper(a.block_name) = 'ALAULI'
            and upper(b.company_profile) = 'CONSULTANCY WORK'""",
            "result": """[(0,)]""",
            "answer": """The total number of candidates joined in alauli block in consultancy work is 0.""",
        }
        ]

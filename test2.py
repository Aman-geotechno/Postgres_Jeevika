from langchain_community.utilities import SQLDatabase
import streamlit as st
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from operator import itemgetter
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate

import cx_Oracle
import os
from sqlalchemy import create_engine
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from prompted import examples
from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from flask_cors import CORS
#from langchain_google_vertexai import ChatVertexAI
from langchain_community.chat_models import ChatGooglePalm
#import prompted
import psycopg2
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

example = [
    {"input": "What is the total count of shg?", "query": """SELECT COUNT(DISTINCT c.cbo_id) AS shg_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'SHG' AND c.record_status=1"""},
    {
        "input": "What is the total count of CLF?",
        "query": """SELECT COUNT(DISTINCT c.cbo_id) AS clf_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'CLF' AND c.record_status=1""",
    },
    {
        "input": "What is the total count of VO?",
        "query": """SELECT COUNT(DISTINCT c.cbo_id) AS vo_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'VO' AND c.record_status=1""",
    },
    {
        "input":"Number of cbo per block per district",
        "query": """SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos \
                        FROM m_cbo c \
                        INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID \
                        INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID \
                        WHERE c.record_status=1 \
                        GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME""",
    },
    {
        "input": "total count of 9 month old shg saving account",
        "query": """SELECT COUNT(c.cbo_id) AS shg_count
FROM m_cbo c
INNER JOIN m_district d ON d.district_id = c.district_id
WHERE c.record_status = 1
AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
AND c.formation_date <= CURRENT_DATE - INTERVAL '9 MONTH'
AND c.formation_date > CURRENT_DATE - INTERVAL '10 MONTH'""",
    },
    {
        "input": "total count of shg in project nrlm in current year",
        "query": """SELECT COUNT(c.cbo_id) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRLM' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
                        AND EXTRACT(YEAR FROM c.formation_date) = EXTRACT(YEAR FROM SYSDATE)
                        AND c.record_status=1""",
    },
    {
        "input": "how many clf are in NRETP project",
        "query": """SELECT COUNT(c.cbo_id) AS clf_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRETP' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'CLF')
                        AND c.record_status=1""",
    },
    {
        "input": "how many shg, vo and clf in district bhojpur",
        "query": """SELECT
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
                FROM m_cbo c
                WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'BHOJPUR')
                AND c.record_status=1""",
    },
    {
        "input": "What is the count of all members across SHGs, VOs and CLFs in district Patna?",
        "query": """SELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1""",
    },
    {
        "input": "how many shg saving account in last 6 months?",
        "query": """SELECT
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
    },
    {
        "input": "how many shg saving account, vo saving account, clf saving account in last 6 month",
        "query": """SELECT
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
    },
    {
          "input": "total count of shg in district patna in year 2023",
        "query": """SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND c.record_status=1""",
    },
    {
          "input": "total count of members in district patna and darbhanga",
        "query": """SELECT d.DISTRICT_NAME, COUNT(cm.MEMBER_ID) AS member_count
                           FROM m_district d 
                           INNER JOIN m_cbo_member cm ON  cm.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(d.DISTRICT_NAME) IN ('PATNA', 'DARBHANGA')
                            AND cm.record_status=1
                            GROUP BY d.DISTRICT_NAME""",
    },
    {
          "input": "total count of vo in december 2023",
        "query": """SELECT 
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
    },
    {
          "input": "What is the total number of VOs in Samastipur district?",
        "query": """SELECT COUNT(c.CBO_ID) AS total_vos
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'VO' AND upper(d.DISTRICT_NAME) = 'SAMASTIPUR'
                            AND c.record_status=1
""",
    },
    {
          "input": "How many SHGs  in Patna district formed between Jan to March 2023?",
        "query": """SELECT
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
    },
    {
          "input":  "What is the count of SHGs formed in Saharsa district in 2022?",
        "query": """SELECT
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
    },
    {
          "input": "total count of shg",
        "query": """SELECT COUNT(c.cbo_id) AS shg_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'SHG' 
                            AND c.record_status=1""",
    },
    {
          "input": "What is the total count of shg?",
        "query": """SELECT COUNT(c.cbo_id) AS shg_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'SHG' 
                            AND c.record_status=1""",
    },
    {
          "input": "How many SHGs in Patna district formed between Jan to March 2023?",
        "query": """
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
    },
    {
          "input": "Number of cbo per block per district",
        "query": """
                                SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
                                FROM m_cbo c
                                INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
                                INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
                                WHERE c.record_status = 1
                                GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
                                ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
                            """,
    },
    {
          "input": "What is the distribution of Community Based Organizations (CBOs) by their types, and how many CBOs are there for each type",
        "query": """SELECT t.TYPE_SHORT_NAME, COUNT(c.CBO_ID) AS cbo_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            WHERE c.record_status = 1
                            GROUP BY t.TYPE_SHORT_NAME
                            ORDER BY cbo_count DESC""",
    },
    {
           "input": "What is the most common CBO type in district Vaishali?",
        "query": """SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME)= 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC
""",
    },
    {
           "input": "give me count of panchayat wise shg from patna district?",
        "query": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
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
    },
    {
           "input": "how many shg in lakhani bigha panchayat?",
        "query": """SELECT
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
    },
    {
           "input": "give me toatal members between 2020 and 2021",
        "query": """SELECT 
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
    },
    {
           "input": "total cadre in shg",
        "query": """SELECT
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
    },
    {
           "input": "give me toatal members between 2020 and 2021",
        "query": """SELECT 
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
    },
    {
           "input": "total male cadre in shg",
        "query": """SELECT
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
    },
    {
           "input": "female cadre in gaya district?",
        "query": """SELECT
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
    },
    {
           "input": "how many cadre of designation CM?",
        "query": """SELECT
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
    },
    {
           "input":  "How many cadre of designation VRP in NALANDA district",
        "query": """SELECT
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
    },
    {
            "input": "count of B graded clf in december 2023?",
        "query": """SELECT COUNT(clf.clf_id) AS clf_count
            FROM clf_masik_grading clf
            INNER JOIN m_cbo c ON clf.clf_id = c.cbo_id
            WHERE clf.year = 2023 and clf.month_name = 'Dec' AND clf.final_grade = 'B' AND c.record_status = 1""",
    },
    {
            "input": "how many clf are not graded?",
        "query": """SELECT COUNT(*) AS clf_not_graded
            FROM m_cbo a
            WHERE a.record_status = 1
            AND a.cbo_type_id = 1
            AND NOT EXISTS (SELECT 1 FROM clf_masik_grading b WHERE a.cbo_id = b.clf_id)""",
    },
    {
            "input": "total count of farmers",
        "query": """SELECT
                            COUNT(DISTINCT FARMER_ID) AS total_farmers
                        FROM
                            m_farmer""",
    },
    {
            "input":  "total count of engaged farmers or active farmers or farmers with active transaction",
        "query": """SELECT
                            COUNT(DISTINCT FARMER_ID) AS total_farmers
                        FROM
                            t_farmer_transaction""",
    },
    {
            "input": "active farmers in 2023-2024",
        "query": """SELECT
    COUNT(DISTINCT FARMER_ID) AS total_farmers
FROM
    t_farmer_transaction
WHERE
    FY = '2023-2024'""",
    },
    {
         "input": "number of farmers having lease land",
            "query": """SELECT
    COUNT(DISTINCT FARMER_ID) AS farmers_with_lease_land
FROM
    m_farmer_land
WHERE
    LANDHOLDINGLEASE > 0""", 
    },
    {
          "input": "no of shg having farmer",
            "query": """select count(distinct shg_id) from t_farmer_transaction""",
    },
    {
          "input": "number of active farmers in banka",
            "query": """SELECT
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
    },
    {
          "input": "count of local seed used by farmer in 2018-2019",
            "query": """select count(distinct farmer_id) as seed_count from t_farmer_transaction ft
inner join m_farmer_seed s on ft.seed_type_id=s.seed_type_id
where UPPER(s.seed_type)='LOCAL' AND
ft.FY='2018-2019'""",
    },
    {
          "input": "count number of farmers grew kharif crops",
            "query": """SELECT
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
    },
    {
          "input": "total count of agri enterprenure",
            "query": """select count(id) from profile_entry""",
    },
    {
          "input": "total expenditure amount of agri enterprenures",
            "query": """select sum(amount) from t_expenditure_details""",
    },
    {
          
               "input": "total sell grain amount of agri enterprenures",
            "query": """select sum(total_amount) from t_sell_grain""",
    },
    {
          "input": "no of active enterprenure in agri input ativity",
            "query": """select count(distinct entry_by) from t_agri_input where entry_by is not null"""
    },
    {
          "input": "no of active enterprenure in advisory farmer activity",
            "query": """select count(distinct entry_by) from t_advisory_farmer_entry where entry_by is not null""",
    },
    {
          "input": "no of active enterprenure in marketing services activity",
            "query": """select count(distinct entry_by) from t_marketing_services where entry_by is not null""",
    },
    {
          "input": "no of active enterprenure in digital banking activity",
            "query": """select count(distinct entry_by) from t_digital_banking where entry_by is not null""",
    },
    {
          "input": "no of active enterprenure in nursery services activity",
            "query": """select count(distinct entry_by) from t_nursery_services where entry_by is not null""",
    }
]




app = Flask(__name__)
CORS(app)

#postgres_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#postgres_connection = psycopg2.connect(database='jeevika_data_warehouse', user='postgres', password='1234', host='10.0.0.19', port='5432')

# Example usage:
db_user = 'postgres'
db_password = '1234'
db_host = '10.0.0.19'
db_port = '5432'
db_name = 'jeevika_data_warehouse'


try:
        # Establish connection to the PostgreSQL database
    connection = psycopg2.connect(
            database='jeevika_data_warehouse',
            user='postgres',
            password='1234',
            host='10.0.0.19',
            port='5432'
        )
    print("Successfully connected to the PostgreSQL database")
        
except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database:", error)


db = SQLDatabase.from_uri(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",include_tables=["m_cbo","m_cbo_type","m_cbo_member","m_cbo_shg_member","t_cbo_appl_mapping","t_cbo_loan_register","m_designation","t_acc_voucher","t_bulk_bank_acc","m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
"m_farmer_pest_management", "mp_cbo_member","m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology","m_block",
"m_district","m_designation","m_village","m_panchayat","clf_masik_grading",
                    "vo_masik_grading",
                    "shg_masik_grading","profile_entry","t_expenditure_details","t_sell_grain","t_digital_banking","t_advisory_farmer_entry","t_agri_input","t_marketing_services","t_nursery_services","m_expenditure_type"])




llm4= ChatGoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyBtNpUSSM6QHsq2QrkUtvcwM-0Hp3gXY_Q',convert_system_message_to_human=True, temperature=0)
agent_executor = create_sql_agent(llm4, db=db, agent_type="openai-tools", verbose=True)

embeddings = HuggingFaceEmbeddings()

example_selector = SemanticSimilarityExampleSelector.from_examples(
    example,
    embeddings,
    FAISS,
    k=5,
    input_keys=["input"],
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

This query will run on a database whose schema is represented below:
CREATE TABLE M_CBO (
   CBO_ID INTEGER PRIMARY KEY,
   CBO_NAME VARCHAR(255),
   DISTRICT_ID INTEGER,
   BLOCK_ID INTEGER,
   VILLAGE_ID INTEGER,
   CBO_TYPE_ID INTEGER,
   THEME_ID INTEGER,
   LATITUDE DECIMAL(10,8),
   LONGITUDE DECIMAL(11,8),
   TOLA_MOHALLA_NAME VARCHAR(255),
   MEETING_PERIODICITY VARCHAR(50),
   MEETING_DAY VARCHAR(20),
   MEETING_DATE DATE,
   GENERAL_SAVING_AMOUNT DECIMAL(10,2),
   HRF_SAVING_AMOUNT DECIMAL(10,2),
   CREATED_BY INTEGER,
   CREATED_ON TIMESTAMP,
   UPDATED_BY INTEGER,
   UPDATED_ON TIMESTAMP,
   RECORD_STATUS VARCHAR(10),
   SHARE_RATE DECIMAL(10,2),
   MEETING_START_TIME TIME,
   STATE_ID INTEGER,
   FORMATION_DATE DATE,
   SCHEME_ID INTEGER,
   CBO_NAME_HINDI VARCHAR(255),
   OTHER_SAVING_1 DECIMAL(10,2),
   OTHER_SAVING_2 DECIMAL(10,2),
   OTHER_SAVING_3 DECIMAL(10,2),
   MEMBERSHIP_FEE DECIMAL(10,2),
   REGISTRATION_NUMBER VARCHAR(50),
   REGISTRATION_DATE DATE,
   COMPLETE_STATUS VARCHAR(10),
   NRLM_CODE VARCHAR(50),
   PWD VARCHAR(255),
   LOKOS_CODE VARCHAR(50)
);

CREATE TABLE M_CBO_TYPE (
   CBO_TYPE_ID INTEGER PRIMARY KEY,
   TYPE_SHORT_NAME VARCHAR(50),
   TYPE_DESCRIPTION VARCHAR(255),
   CREATED_BY INTEGER,
   CREATED_ON TIMESTAMP,
   UPDATED_BY INTEGER,
   UPDATED_ON TIMESTAMP,
   RECORD_STATUS VARCHAR(10),
   TYPE_SHORT_NAME_HINDI VARCHAR(50),
   TYPE_DESCRIPTION_HINDI VARCHAR(255),
   PARENT_CBO_TYPE_ID INTEGER
);
                                          
CREATE TABLE M_CBO_MEMBER (
    MEMBER_ID INTEGER PRIMARY KEY,
    NAME VARCHAR(255),
    FATHER_NAME VARCHAR(255),
    HUSBAND_NAME VARCHAR(255),
    DOB DATE,
    GENDER VARCHAR(10),
    ADDRESS VARCHAR(255),
    EDUCATION VARCHAR(50),
    DATE_OF_JOINING DATE,
    EMAIL_ADDRESS VARCHAR(100),
    PHONE_NO VARCHAR(20),
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    UPDATED_BY INTEGER,
    UPDATED_ON TIMESTAMP,
    RECORD_STATUS VARCHAR(10),
    STATE_ID INTEGER,
    DISTRICT_ID INTEGER,
    BLOCK_ID INTEGER,
    VILLAGE_ID INTEGER,
    NAME_HINDI VARCHAR(255),
    FATHER_NAME_HINDI VARCHAR(255),
    HUSBAND_NAME_HINDI VARCHAR(255),
    POSTOFFICE VARCHAR(100),
    THANA VARCHAR(100),
    KYC_TYPE VARCHAR(50),
    KYC_NUMBER VARCHAR(50),
    EBS_MEMBER_ID VARCHAR(50),
    SECC_PIN_NO VARCHAR(50),
    STATEID INTEGER,
    DISTRICTID INTEGER,
    BLOCKID INTEGER,
    VILLAGEID INTEGER,
    TOILET VARCHAR(10),
    AADHAR_NUMBER VARCHAR(20),
    AADHER_CARD_SEEDED VARCHAR(10),
    NRLM_MEMBER_ID VARCHAR(50),
    REF_CODE VARCHAR(50),
    AADHAR_STATUS VARCHAR(20),
    LOKOS_MEMBER_CODE VARCHAR(50)
);

CREATE TABLE M_CBO_SHG_MEMBER (
    MEMBER_ID INTEGER PRIMARY KEY,
    CATEGORY VARCHAR(50),
    CASTE VARCHAR(50),
    RELIGION VARCHAR(50),
    TOLA_NAME VARCHAR(100),
    CREATED_BY INTEGER,
    UPDATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    UPDATED_ON TIMESTAMP,
    RECORD_STATUS VARCHAR(10),
    CBO_ID INTEGER,
    ENDORSED_BY_GRAMSABHA VARCHAR(10),
    DISTRICTID INTEGER
);

CREATE TABLE T_CBO_APPL_MAPPING (
    APPLICATION_ID INTEGER PRIMARY KEY,
    ACC_NUMBER VARCHAR(50),
    ACC_OPENING_DATE DATE,
    ACC_OPENING_STATUS VARCHAR(20),
    CBO_ID INTEGER,
    CREATED_ON TIMESTAMP,
    UPDATED_ON TIMESTAMP,
    CREATED_BY INTEGER,
    UPDATED_BY INTEGER
);

CREATE TABLE T_CBO_LOAN_REGISTER (
    LOAN_REGISTER_ID INTEGER PRIMARY KEY,
    CBO_ID INTEGER,
    LOAN_TYPE_ID INTEGER,
    LOAN_AMOUNT DECIMAL(10,2),
    LOAN_INSTALLMENTS INTEGER,
    LOAN_DATE DATE,
    RECORD_UPDATED_ON TIMESTAMP,
    RECORD_UPDATED_BY INTEGER,
    RECORD_CREATED_ON TIMESTAMP,
    RECORD_CREATED_BY INTEGER,
    LOAN_REASON VARCHAR(255),
    INTEREST_AMOUNT DECIMAL(10,2),
    PAID DECIMAL(10,2),
    TILL_DATE DATE,
    LOAN_FROM_CBO_ID INTEGER,
    IMEI_NUMBER VARCHAR(50),
    RECORD_SYNCED_ON TIMESTAMP
);

CREATE TABLE T_ACC_VOUCHER (
    VOUCHER_ID INTEGER PRIMARY KEY,
    VOUCHER_DATE DATE,
    CBO_ID INTEGER,
    DEBIT_ACCOUNT INTEGER,
    CREDIT_ACCOUNT INTEGER,
    REMARKS VARCHAR(255),
    OTHER_NAME VARCHAR(100),
    DEBIT_STAKEHOLDER_ID INTEGER,
    VOUCHER_TYPE_ID INTEGER,
    CREATED_ON TIMESTAMP,
    CREATED_BY INTEGER,
    CREDIT_STAKEHOLDER_ID INTEGER,
    IMEI_NUMBER VARCHAR(50),
    RECORD_SYNCED_ON TIMESTAMP,
    CHEQUE_NO VARCHAR(20),
    CHEQUE_DATE DATE
);

CREATE TABLE M_BLOCK (
    BLOCK_ID INTEGER PRIMARY KEY,
    BLOCK_NAME VARCHAR(100),
    DISTRICT_ID INTEGER,
    STATE_ID INTEGER,
    BLOCK_NAME_HINDI VARCHAR(100),
    NRLM_BLOCK_CODE VARCHAR(50),
    ADDOPED_BY_SCHEME VARCHAR(100),
    PROJECT_CODE VARCHAR(50),
    PROJECT_CODE_TILL_APRIL_2023 VARCHAR(50)
);

CREATE TABLE M_DISTRICT (
    DISTRICT_ID INTEGER PRIMARY KEY,
    DISTRICT_NAME VARCHAR(100),
    STATE_ID INTEGER,
    DISTRICT_NAME_HINDI VARCHAR(100),
    DISTRICT_CENS_2011_ID VARCHAR(50),
    NRLM_DISTRICT_CODE VARCHAR(50)
);

CREATE TABLE M_PANCHAYAT (
    STATE_ID INTEGER,
    DISTRICT_ID INTEGER,
    BLOCK_ID INTEGER,
    PANCHAYAT_ID INTEGER PRIMARY KEY,
    PANCHAYAT_NAME VARCHAR(100),
    PANCHAYAT_NAME_HINDI VARCHAR(100),
    NRLM_PANCHAYAT_CODE VARCHAR(50)
);

CREATE TABLE M_VILLAGE (
    VILLAGE_ID INTEGER PRIMARY KEY,
    VILLAGE_NAME VARCHAR(100),
    BLOCK_ID INTEGER,
    OTHER_POPULATION INTEGER,
    SC_POPULATION INTEGER,
    ST_POPULATION INTEGER,
    DISTRICT_ID INTEGER,
    STATE_ID INTEGER,
    PANCHAYAT_ID INTEGER,
    VILLAGE_NAME_HINDI VARCHAR(100),
    EBC_POPULATION INTEGER,
    BC_POPULATION INTEGER,
    MD_POPULATION INTEGER,
    NRLM_VILLAGE_CODE VARCHAR(50)
);

CREATE TABLE MP_CBO_MEMBER (
    MEMBER_ID INTEGER,
    CBO_ID INTEGER,
    DESIGNATION_ID INTEGER,
    RECORD_STATUS VARCHAR(10),
    ID INTEGER PRIMARY KEY,
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    UPDATED_BY INTEGER,
    UPDATED_ON TIMESTAMP,
    DISTRICTID INTEGER
);

CREATE TABLE T_BULK_BANK_ACC (
    APPLICATION_ID INTEGER PRIMARY KEY,
    BRANCH_ID INTEGER,
    ACC_TYPE_ID INTEGER,
    APPLICATION_DATE DATE,
    CREATED_ON TIMESTAMP,
    UPDATED_ON TIMESTAMP,
    BANK_ID INTEGER,
    NO_OF_APPLICATIONS INTEGER,
    STATUS VARCHAR(20),
    REMARKS VARCHAR(255),
    ACCOUNT_HOLDER_TYPE VARCHAR(50)
);

CREATE TABLE M_DESIGNATION (
    DESIGNATION_ID INTEGER PRIMARY KEY,
    DESIGNATION_SHORT_NAME VARCHAR(50),
    DESIGNATION_FULL_NAME VARCHAR(100),
    MEMBER_GROUP_ID INTEGER,
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    UPDATED_BY INTEGER,
    UPDATED_ON TIMESTAMP,
    RECORD_STATUS VARCHAR(10),
    DESIGNATION_SHORT_NAME_HINDI VARCHAR(50),
    DESIGNATION_FULL_NAME_HINDI VARCHAR(100),
    EBS_JOB_ID VARCHAR(50),
    EBS_THEMATIC_ID VARCHAR(50)
);

CREATE TABLE CLF_MASIK_GRADING (
    SL INTEGER PRIMARY KEY,
    YEAR INTEGER,
    MONTH INTEGER,
    CRITERIA4 DECIMAL(5,2),
    CRITERIA5 DECIMAL(5,2),
    CRITERIA6 DECIMAL(5,2),
    TOTAL_MARKS DECIMAL(5,2),
    CLF_ID INTEGER,
    CRITERIA1 DECIMAL(5,2),
    CRITERIA2 DECIMAL(5,2),
    CRITERIA3 DECIMAL(5,2),
    MONTH_NAME VARCHAR(20),
    DISTRICT_ID INTEGER,
    BLOCK_ID INTEGER,
    FINAL_GRADE VARCHAR(10)
);

CREATE TABLE VO_MASIK_GRADING (
    SL INTEGER PRIMARY KEY,
    YEAR INTEGER,
    MONTH INTEGER,
    CRITERIA2 DECIMAL(5,2),
    CRITERIA3 DECIMAL(5,2),
    CRITERIA4 DECIMAL(5,2),
    CRITERIA5 DECIMAL(5,2),
    TOTAL_MARKS DECIMAL(5,2),
    VO_ID INTEGER,
    CRITERIA1 DECIMAL(5,2),
    MONTH_NAME VARCHAR(20),
    DISTRICT_ID INTEGER,
    BLOCK_ID INTEGER,
    CLF_ID INTEGER,
    FINAL_GRADE VARCHAR(10)
);

CREATE TABLE SHG_MASIK_GRADING (
    SL INTEGER PRIMARY KEY,
    YEAR INTEGER,
    MONTH INTEGER,
    CRITERIA4 DECIMAL(5,2),
    CRITERIA5 DECIMAL(5,2),
    CRITERIA6 DECIMAL(5,2),
    TOTAL_MARKS DECIMAL(5,2),
    SHG_ID INTEGER,
    CRITERIA1 DECIMAL(5,2),
    CRITERIA2 DECIMAL(5,2),
    CRITERIA3 DECIMAL(5,2),
    MONTH_NAME VARCHAR(20),
    CLF_ID INTEGER,
    VO_ID INTEGER,
    FINAL_GRADE VARCHAR(10)
);

                                    
Join Conditions:
-- cbo.CBO_TYPE_ID can be joined with cbo_type.CBO_TYPE_ID 
-- M_CBO_MEMBER can be joined with M_DISTRICT, M_BLOCK, and M_VILLAGE on DISTRICT_ID, BLOCK_ID, and VILLAGE_ID columns, respectively.
-- M_CBO_SHG_MEMBER can be joined with M_CBO on the CBO_ID column.
-- product_suppliers.product_id can be joined with products.product_id
-- T_CBO_LOAN_REGISTER can be joined with M_CBO on the CBO_ID column, and with itself on the LOAN_FROM_CBO_ID column.
-- T_ACC_VOUCHER can be joined with M_CBO on the CBO_ID column.
-- M_BLOCK can be joined with M_DISTRICT on the DISTRICT_ID column.
-- M_PANCHAYAT can be joined with M_DISTRICT, M_BLOCK, and M_VILLAGE on DISTRICT_ID, BLOCK_ID, and PANCHAYAT_ID columns, respectively.
-- M_VILLAGE can be joined with M_DISTRICT, M_BLOCK, and M_PANCHAYAT on DISTRICT_ID, BLOCK_ID, and PANCHAYAT_ID columns, respectively.
-- MP_CBO_MEMBER can be joined with M_CBO_MEMBER on the MEMBER_ID column, and with M_CBO on the CBO_ID column.
-- MP_CBO_MEMBER can be joined with M_DESIGNATION on the DESIGNATION_ID column.
-- CLF_MASIK_GRADING can be joined with M_CBO on the CLF_ID column (where CBO_TYPE_ID = 1), and with M_DISTRICT and M_BLOCK on DISTRICT_ID and BLOCK_ID columns, respectively.
-- VO_MASIK_GRADING can be joined with M_CBO on the VO_ID column (where CBO_TYPE_ID = 2), with CLF_MASIK_GRADING on the CLF_ID column, and with M_DISTRICT and M_BLOCK on DISTRICT_ID and BLOCK_ID columns, respectively.
-- SHG_MASIK_GRADING can be joined with M_CBO on the SHG_ID column (where CBO_TYPE_ID = 3), with VO_MASIK_GRADING on the VO_ID column, with CLF_MASIK_GRADING on the CLF_ID column, and with M_DISTRICT and M_BLOCK on DISTRICT_ID and BLOCK_ID columns, respectively.




CREATE TABLE M_FARMER (
    FARMER_ID INTEGER PRIMARY KEY,
    MEMBER_ID INTEGER,
    AADHAR VARCHAR(20),
    MOBILENO VARCHAR(20),
    BANK_ID INTEGER,
    BRANCH_ID INTEGER,
    ACCOUNT_NO VARCHAR(50),
    PHOTO BLOB,
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP
);

CREATE TABLE M_FARMER_CROP (
    CROP_ID INTEGER PRIMARY KEY,
    CROP_NAME VARCHAR(100),
    CROP_TYPE_ID INTEGER
);

CREATE TABLE M_FARMER_CROP_TECHNOLOGY (
    TECHNOLOGY_ID INTEGER PRIMARY KEY,
    CROP_ID INTEGER,
    TECHNOLOGY VARCHAR(255)
);

CREATE TABLE M_FARMER_CROPTYPE (
    CROP_TYPE_ID INTEGER PRIMARY KEY,
    CROP_TYPE VARCHAR(100)
);

CREATE TABLE M_FARMER_LAND (
    LAND_ID INTEGER PRIMARY KEY,
    FARMER_ID INTEGER,
    LANDHOLDINGOWN DECIMAL(10,2),
    LANDHOLDINGLEASE DECIMAL(10,2),
    IRRIGATEDLAND DECIMAL(10,2),
    NONIRRIGATEDLAND DECIMAL(10,2),
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP
);

CREATE TABLE M_FARMER_PEST_MANAGEMENT (
    P_TREATMENT_ID INTEGER PRIMARY KEY,
    TREATMENT VARCHAR(255)
);

CREATE TABLE M_FARMER_SEED (
    SEED_TYPE_ID INTEGER PRIMARY KEY,
    SEED_TYPE VARCHAR(100)
);

CREATE TABLE M_FARMER_SOIL_MANAGEMENT (
    SOILPRACTISE_ID INTEGER PRIMARY KEY,
    SOIL_PRACTISE VARCHAR(255)
);

CREATE TABLE T_FARMER_TRANSACTION (
    TRANSACTION_ID INTEGER PRIMARY KEY,
    FARMER_ID INTEGER,
    VO_ID INTEGER,
    SHG_ID INTEGER,
    FY VARCHAR(10),
    CROP_TYPE_ID INTEGER,
    CULTIVATION_AREA DECIMAL(10,2),
    SEEDS_USED DECIMAL(10,2),
    SEEDS_VARIETY VARCHAR(100),
    SEED_TYPE_ID INTEGER,
    TECHNOLOGY_ID INTEGER,
    TOTAL_YIELD DECIMAL(10,2),
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    CROP_ID INTEGER,
    SOILPRACTISE_ID INTEGER,
    TREATMENT_ID INTEGER
);

CREATE TABLE T_MP_FARMER_TRANSACTION_PEST (
    TRANSACTION_ID INTEGER,
    P_TREATMENT_ID INTEGER,
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    PRIMARY KEY (TRANSACTION_ID, P_TREATMENT_ID)
);

CREATE TABLE T_MP_FARMER_TRANSACTION_SOIL (
    TRANSACTION_ID INTEGER,
    SOILPRACTISE_ID INTEGER,
    CREATED_BY INTEGER,
    PRIMARY KEY (TRANSACTION_ID, SOILPRACTISE_ID)
);

CREATE TABLE T_MP_TRANSACTION_CROPTECHNOLOGY (
    TRANSACTION_ID INTEGER,
    TECHNOLOGY_ID INTEGER,
    CREATED_BY INTEGER,
    CREATED_ON TIMESTAMP,
    PRIMARY KEY (TRANSACTION_ID, TECHNOLOGY_ID)
);

CREATE TABLE profile_entry (
    training_period_rabi_season_module INTEGER,
    training_period_zaid_season_module INTEGER,
    training_period_organic_formulations INTEGER,
    id_of_bank_for_banking_services INTEGER,
    training_period_natural_farming INTEGER,
    date_of_joining DATE,
    updated_on TIMESTAMP,
    date_of_birth DATE,
    created_on TIMESTAMP,
    date_training_period_from DATE,
    date_training_period_to DATE,
    loan_first_tranch DECIMAL(10,2),
    loan_second_tranch DECIMAL(10,2),
    training_period_kharif_season_module INTEGER,
    updated_date DATE,
    id INTEGER PRIMARY KEY,
    gram_panchayat_name VARCHAR(100),
    village_id INTEGER,
    village_name VARCHAR(100),
    pin_code VARCHAR(10),
    mobile_number VARCHAR(20),
    aadhaar_number VARCHAR(20),
    pan_number VARCHAR(20),
    account_number VARCHAR(50),
    bank_id INTEGER,
    bank_name VARCHAR(100),
    branch_id INTEGER,
    branch_name VARCHAR(100),
    ifsc_code VARCHAR(20),
    clf_id INTEGER,
    clf_name VARCHAR(100),
    vo_id INTEGER,
    vo_name VARCHAR(100),
    shg_id INTEGER,
    shg_name VARCHAR(100),
    shg_member_id INTEGER,
    shg_member_name VARCHAR(100),
    course_name_id INTEGER,
    course_name_name VARCHAR(100),
    certification_agency_id INTEGER,
    certification_agency_name VARCHAR(100),
    course_training_mode_id INTEGER,
    course_training_mode_name VARCHAR(100),
    gst_value DECIMAL(5,2),
    is_seed_licence BOOLEAN,
    seed_licence_number VARCHAR(50),
    is_fertilizer_licence_number BOOLEAN,
    fertilizer_licence_number VARCHAR(50),
    is_banking_licence_number BOOLEAN,
    banking_licence_number VARCHAR(50),
    created_by INTEGER,
    person_id INTEGER,
    user_pwd VARCHAR(100),
    appiculture BOOLEAN,
    mushroom BOOLEAN,
    nursery BOOLEAN,
    dairy BOOLEAN,
    procurement BOOLEAN,
    seed BOOLEAN,
    fertilizer BOOLEAN,
    banking BOOLEAN,
    is_updates_approved BOOLEAN,
    name_of_bank_for_banking_services VARCHAR(100),
    services_offered VARCHAR(255),
    training_subject_id INTEGER,
    training_subject_name VARCHAR(100),
    training_period_indays INTEGER,
    isloanprovided BOOLEAN,
    is_updated BOOLEAN,
    updated_by INTEGER,
    type_id INTEGER,
    type_name VARCHAR(100),
    name VARCHAR(100),
    father_husband_name VARCHAR(100),
    gender_id INTEGER,
    gender_name VARCHAR(50),
    cast_belong_to_id INTEGER,
    cast_belong_to_name VARCHAR(100),
    highest_qualification VARCHAR(100),
    address VARCHAR(255),
    district_id INTEGER,
    district_name VARCHAR(100),
    block_id INTEGER,
    block_name VARCHAR(100),
    gram_panchayat_id INTEGER
);

CREATE TABLE t_expenditure_details (
    amount DECIMAL(10,2),
    entry_date DATE,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    district_id INTEGER,
    block_id INTEGER,
    ae_id INTEGER,
    remarks VARCHAR(255),
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    address VARCHAR(255),
    entry_by INTEGER,
    expenditure_id INTEGER PRIMARY KEY,
    fy VARCHAR(10)
);

CREATE TABLE t_digital_banking (
    entry_date DATE,
    amount DECIMAL(10,2),
    fy VARCHAR(10),
    transaction_type VARCHAR(50),
    entry_by INTEGER,
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    member_id INTEGER,
    address VARCHAR(255),
    member_name VARCHAR(100)
);

CREATE TABLE t_advisory_farmer_entry (
    crop_intervention_id INTEGER,
    crop_intervention_name VARCHAR(100),
    entry_by INTEGER,
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    member_id INTEGER,
    address VARCHAR(255),
    member_name VARCHAR(100),
    fy VARCHAR(10)
);

CREATE TABLE t_agri_input (
    amount DECIMAL(10,2),
    quantity DECIMAL(10,2),
    entry_date DATE,
    transaction_type VARCHAR(50),
    crop_season_id INTEGER,
    crop_season_name VARCHAR(100),
    crop_name_id INTEGER,
    crop_name VARCHAR(100),
    seed_variety_name VARCHAR(100),
    company_name VARCHAR(100),
    unit_type VARCHAR(20),
    entry_by INTEGER,
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    member_id INTEGER,
    address VARCHAR(255),
    member_name VARCHAR(100),
    fy VARCHAR(10)
);

CREATE TABLE t_marketing_services (
    purchase_date DATE,
    entry_date DATE,
    rate_per_kg DECIMAL(10,2),
    quantity_in_kg DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    crop_name_id INTEGER,
    crop_name VARCHAR(100),
    entry_by INTEGER,
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    member_id INTEGER,
    address VARCHAR(255),
    member_name VARCHAR(100),
    fy VARCHAR(10),
    crop_season_id INTEGER,
    crop_season_name VARCHAR(100)
);

CREATE TABLE t_nursery_services (
    amount DECIMAL(10,2),
    quantity INTEGER,
    entry_date DATE,
    plant_type VARCHAR(100),
    plant_id INTEGER,
    entry_by INTEGER,
    lat_val DECIMAL(10,8),
    long_val DECIMAL(11,8),
    member_id INTEGER,
    address VARCHAR(255),
    member_name VARCHAR(100),
    fy VARCHAR(10)
);

CREATE TABLE m_expenditure_type (
    expenditure_id INTEGER PRIMARY KEY,
    expenditure_name VARCHAR(100),
    expenditure_name_hin VARCHAR(100)
);

Join Conditions:

M_FARMER can be joined with MP_CBO_MEMBER on the MEMBER_ID column.
M_FARMER_CROP can be joined with M_FARMER_CROPTYPE on the CROP_TYPE_ID column.
M_FARMER_CROP_TECHNOLOGY can be joined with M_FARMER_CROP on the CROP_ID column.
M_FARMER_LAND can be joined with M_FARMER on the FARMER_ID column.
T_FARMER_TRANSACTION can be joined with M_FARMER on the FARMER_ID column, with M_FARMER_CROP on the CROP_ID column, with M_FARMER_CROPTYPE on the CROP_TYPE_ID column, with M_FARMER_SEED on the SEED_TYPE_ID column, with M_FARMER_CROP_TECHNOLOGY on the TECHNOLOGY_ID column, and with M_FARMER_SOIL_MANAGEMENT on the SOILPRACTISE_ID column.
T_MP_FARMER_TRANSACTION_PEST can be joined with T_FARMER_TRANSACTION on the TRANSACTION_ID column, and with M_FARMER_PEST_MANAGEMENT on the P_TREATMENT_ID column.
T_MP_FARMER_TRANSACTION_SOIL can be joined with T_FARMER_TRANSACTION on the TRANSACTION_ID column, and with M_FARMER_SOIL_MANAGEMENT on the SOILPRACTISE_ID column.
T_MP_TRANSACTION_CROPTECHNOLOGY can be joined with T_FARMER_TRANSACTION on the TRANSACTION_ID column, and with M_FARMER_CROP_TECHNOLOGY on the TECHNOLOGY_ID column.
profile_entry can be joined with M_FARMER on the MEMBER_ID column, with M_BLOCK on the block_id column, with M_DISTRICT on the district_id column, and with M_VILLAGE on the village_id column.
t_expenditure_details can be joined with m_expenditure_type on the expenditure_id column, and with M_DISTRICT and M_BLOCK on the district_id and block_id columns, respectively.
t_digital_banking can be joined with MP_CBO_MEMBER on the member_id column.
t_advisory_farmer_entry can be joined with MP_CBO_MEMBER on the member_id column.
t_agri_input can be joined with MP_CBO_MEMBER on the member_id column.
t_marketing_services can be joined with MP_CBO_MEMBER on the member_id column.
t_nursery_services can be joined with MP_CBO_MEMBER on the member_id column."""

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_sql_agent(
    llm=llm4,
    db=db,
    prompt=full_prompt,
    verbose=True,
    agent_type="openai-tools",
)
# print(full_prompt)
# print(agent)
print(agent.invoke({"input": "no of active enterprenure in advisory farmer activity"}))
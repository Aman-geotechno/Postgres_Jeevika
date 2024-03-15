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
from langchain.memory import ConversationBufferMemory

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


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Jeevika_Traces"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__1faaa817b79d42ab9a043148b7094ea9"  # Update to your API key

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
"m_farmer_pest_management", "mp_cbo_member","m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology","m_block", "m_district","m_designation","m_village","m_panchayat","clf_masik_grading","vo_masik_grading","shg_masik_grading","profile_entry","t_expenditure_details","t_sell_grain",
"t_digital_banking","t_advisory_farmer_entry","t_agri_input","t_marketing_services","t_nursery_services","m_expenditure_type","m_chc_details","t_farmer_booking","t_chc_expenditure_details","t_freight_details","neera_selling","neera_collection","m_pg","pg_non_pg_memberes","m_clcdc","t_vidya_didi","t_learner_profile","mp_nursery_fy","t_sell_plant","t_payment_receive_details",
"t_expenditure_details","profile_entry_2","m_bankdataupload","m_agentnew","mp_pg_member","t_household_batch","g_member_mapping","g_goatry_distribution","m_dcs_profile","mp_member_dcs","mp_pond_fpg_mapping","batch_creation","t_sell_details","m_pond","t_sell_details","mp_matasya_sakhi_pond_mapping",
"mp_member_with_fpg_mapping","m_profile", "m_shg_hns_user_table", "t_training_of_cadre_and_pmt","m_user_profile","t_patient_info","mp_cbo_member_activity","m_intervention_activity", "employer_window", "plan_job_fair_training", "candidates_profile", "is_letter_offered"])

#print(db.get_usable_table_names())

#print(db.get_context())

llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True,google_api_key="AIzaSyC1mncPJJKSU70yJspuzPx-jw_sH89jiCE", temperature=0)
#'AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ'
#google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ'
#api_key="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"
# llm = ChatVertexAI(
#     model_name="codechat-bison", max_output_tokens=1000, temperature=0.5
# )

#llm = ChatGooglePalm(google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ', temperature=0)


example_prompt = PromptTemplate(
input_variables=["input", "sql_cmd", "result", "answer",],
template="\nQuestion: {input}\nSQLQuery: {sql_cmd}\nSQLResult: {result}\nAnswer: {answer}",
)

# examples=prompted.main()
# print(examples)

embeddings = HuggingFaceEmbeddings()

to_vectorize = [" ".join(example.values()) for example in examples]
print('t1')

vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)
print('t2')
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=1,
)



    
   
#print(connection.version)
_postgres_prompt = """You are a postgres SQL expert. Given an input question, first create a syntactically correct postgres SQL query to run,.....and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query.. then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the WHERE LIMIT<=1 clause as per Postgres SQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Use join and other oracle sql advance query to get the best query according to user query.
Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
Pay attention to write district name in capital letter while generating sql query..for example DISTRICT_NAME='DARBHANGA'
Detail information about table and its columns are as follows:-
       
       The table M_CBO is a master table storing information about Community Based Organizations (CBOs),vo(Village Organisation),shg(Self Help Group) and clf(Cluster Level Federation) with columns including CBO_ID, CBO_NAME, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, CBO_TYPE_ID, THEME_ID, LATITUDE, LONGITUDE, TOLA_MOHALLA_NAME, MEETING_PERIODICITY, MEETING_DAY, MEETING_DATE, GENERAL_SAVING_AMOUNT, HRF_SAVING_AMOUNT, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, SHARE_RATE, MEETING_START_TIME, STATE_ID, FORMATION_DATE, SCHEME_ID, CBO_NAME_HINDI, OTHER_SAVING_1, OTHER_SAVING_2, OTHER_SAVING_3, MEMBERSHIP_FEE, REGISTRATION_NUMBER, REGISTRATION_DATE, COMPLETE_STATUS, NRLM_CODE, PWD, LOKOS_CODE.\n
        The table M_CBO_TYPE is a master table containing information about different types of Community Based Organizations (CBO types) with columns such as CBO_TYPE_ID, TYPE_SHORT_NAME, TYPE_DESCRIPTION, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, TYPE_SHORT_NAME_HINDI, TYPE_DESCRIPTION_HINDI, PARENT_CBO_TYPE_ID.\n
       The table M_CBO_MEMBER is a master table containing information about individual members of a Community Based Organization (CBO) with columns such as MEMBER_ID, NAME, FATHER_NAME, HUSBAND_NAME, DOB (Date of Birth), GENDER, ADDRESS, EDUCATION, DATE_OF_JOINING, EMAIL_ADDRESS, PHONE_NO, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, STATE_ID, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, NAME_HINDI, FATHER_NAME_HINDI, HUSBAND_NAME_HINDI, POSTOFFICE, THANA, KYC_TYPE, KYC_NUMBER, EBS_MEMBER_ID, SECC_PIN_NO, STATEID, DISTRICTID, BLOCKID, VILLAGEID, TOILET, AADHAR_NUMBER, AADHER_CARD_SEEDED, NRLM_MEMBER_ID, REF_CODE, AADHAR_STATUS, LOKOS_MEMBER_CODE.\n
       The table M_CBO_SHG_MEMBER is a master table that stores detailed information about individual members associated with a Self Help Group (SHG) within a Community Based Organization (CBO). It includes columns such as MEMBER_ID, CATEGORY, CASTE, RELIGION, TOLA_NAME, CREATED_BY, UPDATED_BY, CREATED_ON, UPDATED_ON, RECORD_STATUS, CBO_ID, ENDORSED_BY_GRAMSABHA, DISTRICTID.\n
       The table T_CBO_APPL_MAPPING is a transactional table responsible for storing information related to transactions involving the mapping of applications to a Community Based Organization (CBO). It includes columns such as APPLICATION_ID, ACC_NUMBER, ACC_OPENING_DATE, ACC_OPENING_STATUS, CBO_ID, CREATED_ON, UPDATED_ON, CREATED_BY, and UPDATED_BY to track transactional details associated with this mapping.\n
       The table T_CBO_LOAN_REGISTER is a transactional table that maintains records of loans registered within a Community Based Organization (CBO). It contains columns such as LOAN_REGISTER_ID, CBO_ID, LOAN_TYPE_ID, LOAN_AMOUNT, LOAN_INSTALLMENTS, LOAN_DATE, RECORD_UPDATED_ON, RECORD_UPDATED_BY, RECORD_CREATED_ON, RECORD_CREATED_BY, LOAN_REASON, INTEREST_AMOUNT, PAID, TILL_DATE, LOAN_FROM_CBO_ID, IMEI_NUMBER, and RECORD_SYNCED_ON.\n
       The table T_ACC_VOUCHER is a transactional table that stores accounting vouchers within the context of a Community Based Organization (CBO). It includes columns such as VOUCHER_ID, VOUCHER_DATE, CBO_ID, DEBIT_ACCOUNT, CREDIT_ACCOUNT, REMARKS, OTHER_NAME, DEBIT_STAKEHOLDER_ID, VOUCHER_TYPE_ID, CREATED_ON, CREATED_BY, CREDIT_STAKEHOLDER_ID, IMEI_NUMBER, RECORD_SYNCED_ON, CHEQUE_NO, and CHEQUE_DATE. \n
       The table M_BLOCK represents information about different blocks. It includes columns such as BLOCK_ID, BLOCK_NAME, DISTRICT_ID, STATE_ID, BLOCK_NAME_HINDI, NRLM_BLOCK_CODE, ADDOPED_BY_SCHEME, PROJECT_CODE, and PROJECT_CODE_TILL_APRIL_2023. \n
       The table M_DISTRICT contains information about different districts. It includes columns such as DISTRICT_ID, DISTRICT_NAME, STATE_ID, DISTRICT_NAME_HINDI, DISTRICT_CENS_2011_ID, and NRLM_DISTRICT_CODE.\n
       The table M_PANCHAYAT contains information about various panchayats. It includes columns such as STATE_ID, DISTRICT_ID, BLOCK_ID, PANCHAYAT_ID, PANCHAYAT_NAME, PANCHAYAT_NAME_HINDI, and NRLM_PANCHAYAT_CODE. \n
       The table M_VILLAGE contains information about various villages. It includes columns such as VILLAGE_ID, VILLAGE_NAME, BLOCK_ID, OTHER_POPULATION, SC_POPULATION, ST_POPULATION, DISTRICT_ID, STATE_ID, PANCHAYAT_ID, VILLAGE_NAME_HINDI, EBC_POPULATION, BC_POPULATION, MD_POPULATION, and NRLM_VILLAGE_CODE. \n
       The table MP_CBO_MEMBER is a mapping table that associates members with a specific Community Based Organization (CBO). It includes columns such as MEMBER_ID, CBO_ID, DESIGNATION_ID, RECORD_STATUS, ID, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, and DISTRICTID.\n
        T_BULK_BANK_ACC is a transactional tabe which contains columns APPLICATION_ID BRANCH_ID,ACC_TYPE_ID,APPLICATION_DATE,CREATED_ON,UPDATED_ON,BANK_ID,NO_OF_APPLICATIONS,STATUS,REMARKS,ACCOUNT_HOLDER_TYPE this able is used in conjunction with other tables when question asked about saving account of shg,vo or clf  \n
        M_DESIGNATION is a master tables which contain the following columns DESIGNATION_ID DESIGNATION_SHORT_NAME DESIGNATION_FULL_NAME MEMBER_GROUP_ID CREATED_BY CREATED_ON UPDATED_BY UPDATED_ON RECORD_STATUS DESIGNATION_SHORT_NAME_HINDI DESIGNATION_FULL_NAME_HINDI EBS_JOB_ID EBS_THEMATIC_ID...whenever the question is the count of member then member_group_id=3 and designation_id!=31 \
        The  table CLF_MASIK_GRADING contains information about the grades assigned to the clf. It includes columns such as sl, year, month, criteria4, criteria5, criteria6, total_marks, clf_id, criteria1, criteria2, criteria3, month_name, district_id, block_id and final_grade. The cbo_type_id of the clf is 1. \n
       The  table VO_MASIK_GRADING contains information about the grades assigned to the vo. It includes columns such as sl, year, month, criteria2, criteria3, criteria4, criteria5, total_marks, vo_id, criteria1, month_name, district_id, block_id, clf_id and final_grade. The cbo_type_id of the vo is 2. \n
       The  table SHG_MASIK_GRADING contains information about the grades assigned to the shg. It includes columns such as sl, year, month, criteria4, criteria5, criteria6, total_marks, shg_id, criteria1, criteria2, criteria3, month_name, clf_id, vo_id and final_grade. The cbo_type_id of the shg is 3. \n

       The M_FARMER table stores essential details about farmers. Its columns include:
                                                                    FARMER_ID: Unique identifier.
                                                                    MEMBER_ID: Linked to a Community Based Organization (CBO) member.
                                                                    AADHAR: Aadhar number for identification.
                                                                    MOBILENO: Contact number.
                                                                    BANK_ID: Bank identifier.
                                                                    BRANCH_ID: Branch identifier.
                                                                    ACCOUNT_NO: Bank account number.
                                                                    PHOTO: Farmer's photograph.
                                                                    CREATED_BY: Creator information.
                                                                    CREATED_ON: Creation timestamp.   \n

        The M_FARMER_CROP table manages information about crops cultivated by farmers. Its columns include:
                                                                                        CROP_ID: Unique identifier for each crop record.
                                                                                        CROP_NAME: Name of the crop being cultivated.
                                                                                        CROP_TYPE_ID: Identifier representing the type of crop (e.g., cereal, legume, vegetable). \n
        The M_FARMER_CROP_TECHNOLOGY table stores data related to agricultural technologies used for specific crops. Its columns are:
                                                                                                        TECHNOLOGY_ID: Unique identifier for each technology entry.
                                                                                                        CROP_ID: Identifier linking the technology to a specific crop.
                                                                                                        TECHNOLOGY: Description or name of the agricultural technology utilized.  \n                                                                             
        The M_FARMER_CROPTYPE table manages information about different types of crops. Its columns include:
                                                                                            CROP_TYPE_ID: Unique identifier for each crop type.
                                                                                            CROP_TYPE: Name or description of the crop type. \n

        The M_FARMER_LAND table stores data regarding landholdings of farmers. Its columns include:
                                                                                LAND_ID: Unique identifier for each land record.
                                                                                FARMER_ID: Identifier linking the land to a specific farmer.
                                                                                LANDHOLDINGOWN: Area of land owned by the farmer.
                                                                                LANDHOLDINGLEASE: Area of land leased by the farmer.
                                                                                IRRIGATEDLAND: Area of land that is irrigated.
                                                                                NONIRRIGATEDLAND: Area of land that is not irrigated.
                                                                                CREATED_BY: Information about the user or process that created the land record.
                                                                                CREATED_ON: Timestamp indicating the date and time when the land record was created in the system. \n

The M_FARMER_PEST_MANAGEMENT table contains data related to pest management treatments for farmers. Its columns include:
                                                                                                    P_TREATMENT_ID: Unique identifier for each pest treatment entry.
                                                                                                    TREATMENT: Description or name of the pest management treatment. \n

The M_FARMER_SEED table maintains information about different types of seeds used by farmers. Its columns include:

                                                                                            SEED_TYPE_ID: Unique identifier for each seed type.
                                                                                            SEED_TYPE: Description or name of the seed type. \n                                                                                                 

The M_FARMER_SOIL_MANAGEMENT table stores details regarding soil management practices adopted by farmers. Its columns include:

                                                                                            SOILPRACTISE_ID: Unique identifier for each soil management practice entry.
                                                                                            SOIL_PRACTISE: Description or name of the soil management practice. \n

The T_FARMER_TRANSACTION table records transactional data associated with farmers' activities.It also indicate that farmers are engaged and active. Its columns include:
                                                            TRANSACTION_ID: Unique identifier for each transaction.
                                                            FARMER_ID: Identifier linking the transaction to a specific farmer.
                                                            VO_ID: Identifier for the Village Organisation (VO) associated with the transaction.
                                                            SHG_ID: Identifier for the Self Help Group (SHG) associated with the transaction.
                                                            FY: Fiscal year of the transaction.
                                                            CROP_TYPE_ID: Identifier representing the type of crop involved in the transaction.
                                                            CULTIVATION_AREA: Area of land cultivated for the transaction.
                                                            SEEDS_USED: Quantity of seeds used.
                                                            SEEDS_VARIETY: Variety of seeds used.
                                                            SEED_TYPE_ID: Identifier representing the type of seed used.
                                                            TECHNOLOGY_ID: Identifier representing the agricultural technology used.
                                                            TOTAL_YIELD: Total yield obtained from the transaction.
                                                            CREATED_BY: Information about the user or process that created the transaction.
                                                            CREATED_ON: Timestamp indicating the date and time when the transaction was created.
                                                            CROP_ID: Identifier for the specific crop involved in the transaction.
                                                            SOILPRACTISE_ID: Identifier representing the soil management practice employed.
                                                            TREATMENT_ID: Identifier representing the pest management treatment applied.  \n

The T_MP_FARMER_TRANSACTION_PEST is mapping table records transactional data related to pest management treatments for farmers. Its columns include:
                                                                                                        TRANSACTION_ID: Unique identifier for each transaction.
                                                                                                        P_TREATMENT_ID: Identifier for the pest management treatment applied.
                                                                                                        CREATED_BY: Information about the user or process that created the transaction.
                                                                                                        CREATED_ON: Timestamp indicating the date and time when the transaction was created.   \n  

The T_MP_FARMER_TRANSACTION_SOIL table contains transactional data related to soil management practices adopted by farmers. Its columns include:
                                                                                                                            TRANSACTION_ID: Unique identifier for each transaction.
                                                                                                                            SOILPRACTISE_ID: Identifier for the soil management practice applied.
                                                                                                                            CREATED_BY: Information about the user or process that created the transaction. \n
  
The T_MP_TRANSACTION_CROPTECHNOLOGY is mapping table stores transactional data related to crop technologies used by farmers. Its columns include:
                                                                                            TRANSACTION_ID: Unique identifier for each transaction.
                                                                                            TECHNOLOGY_ID: Identifier for the crop technology applied.
                                                                                            CREATED_BY: Information about the user or process that created the transaction.
                                                                                            CREATED_ON: Timestamp indicating the date and time when the transaction was created.   \n                                                                                                                       CREATED_ON: Timestamp indicating the date and time when the transaction was created. \n                                                                                    

                                                                                            
The profile_entry table provides comprehensive information about farmers profiles, including personal details, training periods, banking information, farming activities, and certification statuses.The columns are.. \

                                                                                training_period_rabi_season_module: Training period for Rabi season module.
                                                                                training_period_zaid_season_module: Training period for Zaid season module.
                                                                                training_period_organic_formulations: Training period for organic formulations.
                                                                                id_of_bank_for_banking_services: Identifier of the bank for banking services.
                                                                                training_period_natural_farming: Training period for natural farming.
                                                                                date_of_joining: Date of joining the program.
                                                                                updated_on: Timestamp of the last update.
                                                                                date_of_birth: Date of birth of the individual.
                                                                                created_on: Timestamp of the creation.
                                                                                date_training_period_from: Starting date of the training period.
                                                                                date_training_period_to: Ending date of the training period.
                                                                                loan_first_tranch: Amount of the first tranche of the loan.
                                                                                loan_second_tranch: Amount of the second tranche of the loan.
                                                                                training_period_kharif_season_module: Training period for Kharif season module.
                                                                                updated_date: Date of the last update.
                                                                                id: Unique identifier.
                                                                                gram_panchayat_name: Name of the gram panchayat.
                                                                                village_id: Identifier of the village.
                                                                                village_name: Name of the village.
                                                                                pin_code: PIN code of the area.
                                                                                mobile_number: Mobile number of the individual.
                                                                                aadhaar_number: Aadhaar number of the individual.
                                                                                pan_number: PAN number of the individual.
                                                                                account_number: Bank account number.
                                                                                bank_id: Identifier of the bank.
                                                                                bank_name: Name of the bank.
                                                                                branch_id: Identifier of the bank branch.
                                                                                branch_name: Name of the bank branch.
                                                                                ifsc_code: IFSC code of the bank branch.
                                                                                clf_id: Identifier of the Cluster Level Federation (CLF).
                                                                                clf_name: Name of the CLF.
                                                                                vo_id: Identifier of the Village Organization (VO).
                                                                                vo_name: Name of the VO.
                                                                                shg_id: Identifier of the Self Help Group (SHG).
                                                                                shg_name: Name of the SHG.
                                                                                shg_member_id: Identifier of the SHG member.
                                                                                shg_member_name: Name of the SHG member.
                                                                                course_name_id: Identifier of the course name.
                                                                                course_name_name: Name of the course.
                                                                                certification_agency_id: Identifier of the certification agency.
                                                                                certification_agency_name: Name of the certification agency.
                                                                                course_training_mode_id: Identifier of the course training mode.
                                                                                course_training_mode_name: Name of the course training mode.
                                                                                gst_value: GST value.
                                                                                is_seed_licence: Indicator for seed license.
                                                                                seed_licence_number: Seed license number.
                                                                                is_fertilizer_licence_number: Indicator for fertilizer license.
                                                                                fertilizer_licence_number: Fertilizer license number.
                                                                                is_banking_licence_number: Indicator for banking license.
                                                                                banking_licence_number: Banking license number.
                                                                                created_by: Creator of the entry.
                                                                                person_id: Identifier of the person.
                                                                                user_pwd: User password.
                                                                                appiculture: Indicator for apiculture.
                                                                                mushroom: Indicator for mushroom farming.
                                                                                nursery: Indicator for nursery.
                                                                                dairy: Indicator for dairy farming.
                                                                                procurement: Indicator for procurement.
                                                                                seed: Indicator for seed.
                                                                                fertilizer: Indicator for fertilizer.
                                                                                banking: Indicator for banking.
                                                                                is_updates_approved: Indicator for updates approval.
                                                                                name_of_bank_for_banking_services: Name of the bank for banking services.
                                                                                services_offered: Services offered.
                                                                                training_subject_id: Identifier of the training subject.
                                                                                training_subject_name: Name of the training subject.
                                                                                training_period_indays: Training period in days.
                                                                                isloanprovided: Indicator for loan provision.
                                                                                is_updated: Indicator for update.
                                                                                updated_by: Updater of the entry.
                                                                                type_id: Identifier of the type.
                                                                                type_name: Name of the type.
                                                                                name: Name.
                                                                                father_husband_name: Father or husband's name.
                                                                                gender_id: Identifier of the gender.
                                                                                gender_name: Gender.
                                                                                cast_belong_to_id: Identifier of the caste.
                                                                                cast_belong_to_name: Name of the caste.
                                                                                highest_qualification: Highest qualification.
                                                                                address: Address.
                                                                                district_id: Identifier of the district.
                                                                                district_name: Name of the district.
                                                                                block_id: Identifier of the block.
                                                                                block_name: Name of the block.
                                                                                gram_panchayat_id: Identifier of the gram panchayat.  \ 

The "t_expenditure_details" table records expenditure details of farmers on agriculture...The columns are...
                                                                                amount: The amount spent for the expenditure.
                                                                                entry_date: The date when the expenditure entry was made.
                                                                                year: The year associated with the expenditure.
                                                                                month: The numerical representation of the month.
                                                                                month_name: The name of the month.
                                                                                district_id: Identifier for the district where the expenditure occurred.
                                                                                block_id: Identifier for the block where the expenditure occurred.
                                                                                ae_id: Identifier for the Agricultural Extension (AE) responsible for the expenditure.
                                                                                remarks: Additional remarks or notes regarding the expenditure.
                                                                                lat_val: Latitude value indicating the location of the expenditure.
                                                                                long_val: Longitude value indicating the location of the expenditure.
                                                                                address: Address where the expenditure took place.
                                                                                entry_by: Identifier for the person who made the expenditure entry.
                                                                                expenditure_id: Unique identifier for the expenditure entry.
                                                                                fy: Fiscal year associated with the expenditure.   \
                                                                                
The "t_digital_banking" table records digital banking transactions of farmers on agriculture..the columns are...

                                                                                        entry_date: The date when the digital banking transaction occurred.
                                                                                        amount: The amount involved in the digital banking transaction.
                                                                                        fy: The fiscal year associated with the transaction.
                                                                                        transaction_type: The type of digital banking transaction (e.g., deposit, withdrawal, transfer).
                                                                                        entry_by: Identifier for the person who made the transaction entry.
                                                                                        lat_val: Latitude value indicating the location of the transaction.
                                                                                        long_val: Longitude value indicating the location of the transaction.
                                                                                        member_id: Identifier for the member involved in the transaction.
                                                                                        address: Address associated with the transaction.
                                                                                        member_name: Name of the member involved in the transaction. \
                                                                                        
The "t_advisory_farmer_entry" table maintains entries related to advisory services for farmers, including crop intervention ID and name, entry by, geographical coordinates, member ID, address, member name, and fiscal year.The columns are...

                                                                                        crop_intervention_id: Identifier for the crop intervention provided to the farmer.
                                                                                        crop_intervention_name: Name of the crop intervention provided to the farmer.
                                                                                        entry_by: Identifier for the person who made the advisory entry.
                                                                                        lat_val: Latitude value indicating the location of the advisory entry.
                                                                                        long_val: Longitude value indicating the location of the advisory entry.
                                                                                        member_id: Identifier for the member (farmer) who received the advisory service.
                                                                                        address: Address associated with the advisory entry.
                                                                                        member_name: Name of the member (farmer) who received the advisory service.
                                                                                        fy: Fiscal year associated with the advisory entry.

The "t_agri_input" table captures agricultural input transactions, including the amount, quantity, entry date, transaction type, crop season details, crop name and variety, company name, unit type, entry by, geographical coordinates, member details, and fiscal year.The columns are... \

                                                                                    amount: The monetary value of the agricultural input transaction.
                                                                                    quantity: The quantity of the agricultural input involved in the transaction.
                                                                                    entry_date: The date when the transaction occurred.
                                                                                    transaction_type: The type of transaction (e.g., purchase, sale).
                                                                                    crop_season_id: Identifier for the crop season.
                                                                                    crop_season_name: Name of the crop season.
                                                                                    crop_name_id: Identifier for the crop name.
                                                                                    crop_name: Name of the crop.
                                                                                    seed_variety_name: Name of the seed variety.
                                                                                    company_name: Name of the company providing the agricultural input.
                                                                                    unit_type: Type of unit for the quantity (e.g., kg, liters).
                                                                                    entry_by: Identifier for the person who made the transaction entry.
                                                                                    lat_val: Latitude value indicating the location of the transaction.
                                                                                    long_val: Longitude value indicating the location of the transaction.
                                                                                    member_id: Identifier for the member (e.g., farmer) involved in the transaction.
                                                                                    address: Address associated with the transaction.
                                                                                    member_name: Name of the member (e.g., farmer) involved in the transaction.
                                                                                    fy: Fiscal year associated with the transaction.


The "t_marketing_services" table stores data related to marketing services, including purchase date, entry date, rate per kilogram, quantity in kilograms, total amount, crop name and identifier, entry by, geographical coordinates, member details, fiscal year, and crop season details.The columns are ... \

                                                                                                                purchase_date: Date when the purchase was made.
                                                                                                                entry_date: Date when the entry was made.
                                                                                                                rate_per_kg: Rate per kilogram for the purchase.
                                                                                                                quantity_in_kg: Quantity of the crop purchased in kilograms.
                                                                                                                total_amount: Total amount spent on the purchase.
                                                                                                                crop_name_id: Identifier for the crop name.
                                                                                                                crop_name: Name of the crop purchased.
                                                                                                                entry_by: Identifier for the person who made the entry.
                                                                                                                lat_val: Latitude value indicating the location of the purchase.
                                                                                                                long_val: Longitude value indicating the location of the purchase.
                                                                                                                member_id: Identifier for the member involved in the transaction.
                                                                                                                address: Address associated with the purchase.
                                                                                                                member_name: Name of the member involved in the transaction.
                                                                                                                fy: Fiscal year associated with the transaction.
                                                                                                                crop_season_id: Identifier for the crop season.
                                                                                                                crop_season_name: Name of the crop season.

The "t_nursery_services" table records nursery services, including the amount spent, quantity of plants, entry date, plant type, plant identifier, entry by, geographical coordinates, member details, address, member name, and fiscal year...the columns are... \

                                                                                                            amount: The monetary value of the nursery service.
                                                                                                            quantity: The quantity of plants involved in the service.
                                                                                                            entry_date: The date when the nursery service was provided.
                                                                                                            plant_type: The type of plant provided in the service.
                                                                                                            plant_id: Identifier for the plant.
                                                                                                            entry_by: Identifier for the person who provided the nursery service.
                                                                                                            lat_val: Latitude value indicating the location of the nursery service.
                                                                                                            long_val: Longitude value indicating the location of the nursery service.
                                                                                                            member_id: Identifier for the member (e.g., farmer) who received the nursery service.
                                                                                                            address: Address where the nursery service was provided.
                                                                                                            member_name: Name of the member (e.g., farmer) who received the nursery service.
                                                                                                           fy: Fiscal year associated with the nursery service.

The "m_expenditure_type" table contains information about different types of expenditures, including unique identifiers for each type, the name of the expenditure in English, and the name of the expenditure in Hindi...the columns are... \
                                                                                                        expenditure_id: Unique identifier for each expenditure type.
                                                                                                        expenditure_name: Name of the expenditure type in English.
                                                                                                        expenditure_name_hin: Name of the expenditure type in Hindi.      \

The "m_chc_details" table stores detailed information about Community Health Centers (CHCs), including their establishment date, location, type, associated organizations, and banking details....the columns are... \
                                                                                                                    doe: Date of establishment.
                                                                                                                    updated_on: Date of the last update.
                                                                                                                    clf_id: Cluster level federation identifier.
                                                                                                                    created_on: Date of creation.
                                                                                                                    is_geo_tagged: Indicates whether the entry is geo-tagged.
                                                                                                                    entry_date: Date of entry.
                                                                                                                    branch_id: Branch identifier.
                                                                                                                    ifsc_code: IFSC code.
                                                                                                                    account_number: Account number.
                                                                                                                    is_active: Indicates whether the entry is active.
                                                                                                                    photo: Photograph.
                                                                                                                    id: Unique identifier.
                                                                                                                    longitude: Longitude.
                                                                                                                    address_by_geo: Address derived from geographical coordinates.
                                                                                                                    type_of_project: Type of project.
                                                                                                                    type_of_chc: Type of Community Health Center (CHC).
                                                                                                                    type_of_cbo: Type of Community-Based Organization (CBO).
                                                                                                                    fpo_name: Name of Farmer Producer Organization (FPO).
                                                                                                                    updated_by: Identifier of the user who last updated.
                                                                                                                    created_by: Identifier of the user who created.
                                                                                                                    latitude: Latitude.
                                                                                                                    chc_name: Name of Community Health Center (CHC).
                                                                                                                    address: Address.
                                                                                                                    district_id: District identifier.
                                                                                                                    block_id: Block identifier.
                                                                                                                    bank_id: Bank identifier.
                                                                                                                                                                          
The t_farmer_booking table captures booking details including dates, service status, farmer information, geographical coordinates, and organizational associations for agricultural services...the columns are... \
                                                                                                        date_for_booking: Date for which the booking is made
                                                                                                        is_farmer_jeevika_member: Boolean indicating if the farmer is a Jeevika member
                                                                                                        entry_date: Date when the booking entry was made
                                                                                                        service_completed_status: Status of the service completion
                                                                                                        booking_cancel: Boolean indicating if the booking was canceled
                                                                                                        service_completed_date: Date when the service was completed
                                                                                                        booking_cancel_date: Date when the booking was canceled
                                                                                                        total_area_or_hour: Total area or hours for the booking
                                                                                                        booking_id: Primary key for the booking record
                                                                                                        shg_id: Identifier for the Self Help Group (SHG)
                                                                                                        shg_name: Name of the SHG
                                                                                                        shg_member_id: Identifier for the SHG member
                                                                                                        farmer_name: Name of the farmer
                                                                                                        gender: Gender of the farmer
                                                                                                        father_name: Father's name of the farmer
                                                                                                        farmer_mobile: Mobile number of the farmer
                                                                                                        booking_description: Description of the booking
                                                                                                        lat_val: Latitude value for the location
                                                                                                        long_val: Longitude value for the location
                                                                                                        address: Address of the farmer
                                                                                                        entry_by: Identifier for the person who made the entry
                                                                                                        device_id: Identifier for the device used for the entry
                                                                                                        auto_fetch_mobile: Boolean indicating if the mobile number is fetched automatically
                                                                                                        chc_id: Identifier for the CHC (Community Health Center)
                                                                                                        booking_activity_id: Identifier for the booking activity
                                                                                                        district_id: Identifier for the district
                                                                                                        block_id: Identifier for the block
                                                                                                        panchayat_id: Identifier for the panchayat
                                                                                                        village_id: Identifier for the village
                                                                                                        tola_name: Name of the tola (locality)
                                                                                                        unit_type: Type of unit for the total area or hours


The t_chc_expenditure_details utilized for recording and tracking expenditure details related to Community Health Centers (CHCs), including the date, amount, type, and organizational association for expenses incurred.The columns are ... \
                                                                                                                exp_date: Date of expenditure
                                                                                                                year: Year of the expenditure
                                                                                                                amount: Amount of expenditure
                                                                                                                month: Month of the expenditure
                                                                                                                entry_date: Date when the entry was made
                                                                                                                month_name: Name of the month
                                                                                                                exp_id: Primary key for the expenditure record
                                                                                                                chc_id: Identifier for the Community Health Center (CHC)
                                                                                                                expenditure_type: Type of expenditure
                                                                                                                entry_by: Identifier for the person who made the entry

The table t_freight_details  can be utilized for storing details related to freight, including machine information, area or hours, amount, geographical coordinates, and organizational associations...the columns are ... \
                                                                                                                    id: Unique identifier for each record (auto-generated)
                                                                                                                    machine_id: Identifier for the machine
                                                                                                                    total_area_or_hour: Total area or hours
                                                                                                                    total_amount: Total amount
                                                                                                                    entry_date: Date of entry
                                                                                                                    long_val: Longitude value
                                                                                                                    address: Address
                                                                                                                    entry_by: Identifier for the person who made the entry
                                                                                                                    device_id: Identifier for the device used for the entry
                                                                                                                    booking_id: Identifier for the booking
                                                                                                                    chc_id: Identifier for the Community Health Center (CHC)
                                                                                                                    lat_val: Latitude value
                                                                                                                    unit_type: Type of unit for the total area or hours \
                                                                                                                
 The neera_selling table  is designed to store information related to selling neera, including details such as dates, prices, quantities, organizational associations, and application versions....the columns are... \
                                                                                                                        "id"
                                                                                                                        "selling_date"
                                                                                                                        "uploaded_on"
                                                                                                                        "compfed"
                                                                                                                        "price_per_liter"
                                                                                                                        "total_amount"
                                                                                                                        "created_by"
                                                                                                                        "created_on"
                                                                                                                        "gp_id"
                                                                                                                        "gp_name"
                                                                                                                        "district_id"
                                                                                                                        "district_name"
                                                                                                                        "block_id"
                                                                                                                        "block_name"
                                                                                                                        "quantity_used_in_gud"
                                                                                                                        "member_row_id"
                                                                                                                        "member_name"
                                                                                                                        "member_type"
                                                                                                                        "village_id"
                                                                                                                        "pg_id"
                                                                                                                        "total_tappers"
                                                                                                                        "name_of_any_other"
                                                                                                                        "quantity_of_neeara_used"
                                                                                                                        "perm_sell_center_sold_neera"
                                                                                                                        "temp_sell_center_sold_neera"
                                                                                                                        "app_version"
                                                                                                                        "quantity_gud_produced"
                                                                                                                        "fresh_neera"                                                                                                                   
This neera_collection table is designed to store information related to the collection of neera, including details such as amounts, quantities, qualities, organizational associations, and collection dates.....columns are... \
                                                                                                                            "id"
                                                                                                                            "total_amount"
                                                                                                                            "quality"
                                                                                                                            "quantity"
                                                                                                                            "brix"
                                                                                                                            "price_per_liter"
                                                                                                                            "created_by"
                                                                                                                            "created_on"
                                                                                                                            "gp_id"
                                                                                                                            "gp_name"
                                                                                                                            "district_id"
                                                                                                                            "district_name"
                                                                                                                            "block_id"
                                                                                                                            "block_name"
                                                                                                                            "uploaded_on"
                                                                                                                            "member_row_id"
                                                                                                                            "member_name"
                                                                                                                            "member_type"
                                                                                                                            "village_id"
                                                                                                                            "pg_id"
                                                                                                                            "total_tappers"
                                                                                                                            "name_of_any_other"
                                                                                                                            "quantity_of_neeara_used"
                                                                                                                            "quantity_used_in_gud"
                                                                                                                            "quantity_gud_produced"
                                                                                                                            "app_version"
                                                                                                                            "collection_date"

                                                                                                                            
The "m_pg" table represents information related to self-help groups or similar entities, including details such as financial transactions ("amount_send_to_pg"), formation date ("formation_date"), identification details ("id"), group ID ("pg_id"), geographical information, status ("is_active"), and other relevant attributes..the columns are..
                                                                                                                                "amount_send_to_pg"
                                                                                                                                "formation_date"
                                                                                                                                "id"
                                                                                                                                "pg_id"
                                                                                                                                "panchayat_name"
                                                                                                                                "block_name"
                                                                                                                                "district_id"
                                                                                                                                "district_name"
                                                                                                                                "village_id"
                                                                                                                                "village_name"
                                                                                                                                "is_active"
                                                                                                                                "bank_ac_number"
                                                                                                                                "passbook_photo"
                                                                                                                                "pg_name"
                                                                                                                                "block_id"
                                                                                                                                "panchayat_id"
                                                                                                                            
The "pg_non_pg_members" table captures comprehensive information about members associated with self-help groups or similar entities, encompassing personal details, financial information, group affiliations, and relevant administrative data..the columns are...
                                                                                                                                                                                            "updated_on"
                                                                                                                                                                                            "created_on"
                                                                                                                                                                                            "id"
                                                                                                                                                                                            "block_id"
                                                                                                                                                                                            "block_name"
                                                                                                                                                                                            "village_id"
                                                                                                                                                                                            "village_name"
                                                                                                                                                                                            "panchayat_id"
                                                                                                                                                                                            "panchayat_name"
                                                                                                                                                                                            "member_name"
                                                                                                                                                                                            "father_name"
                                                                                                                                                                                            "husband_name"
                                                                                                                                                                                            "phone_no"
                                                                                                                                                                                            "bank_id"
                                                                                                                                                                                            "bank_name"
                                                                                                                                                                                            "branch_id"
                                                                                                                                                                                            "branch_name"
                                                                                                                                                                                            "ifsc"
                                                                                                                                                                                            "ac_number"
                                                                                                                                                                                            "tapper_tree"
                                                                                                                                                                                            "area"
                                                                                                                                                                                            "member_type"
                                                                                                                                                                                            "created_by"
                                                                                                                                                                                            "pg_id"
                                                                                                                                                                                            "pg_name"
                                                                                                                                                                                            "member_id"
                                                                                                                                                                                            "updated_by"
                                                                                                                                                                                            "jeevika_non_jeevika"
                                                                                                                                                                                            "shankul_sandh_name"
                                                                                                                                                                                            "group_name"
                                                                                                                                                                                            "group_didi_name"
                                                                                                                                                                                            "licence_number"
                                                                                                                                                                                            "aadhaar_number"
                                                                                                                                                                                            "shg_member_name"
                                                                                                                                                                                            "gram_sangathan_name"
                                                                                                                                                                                            "is_active"
                                                                                                                                                                                            "is_sjy_beneficiary"
                                                                                                                                                                                            "district_id"
                                                                                                                                                                                            "district_name"  
                                                                                                                            
 
The "m_clcdc" table stores information related to community-level climate change and disaster coordination centers, including details such as center ID, associated file references, creation information, contact details, and administrative affiliations.the columns are..                                                                                                                                                                                                                                                                                                                                                                               While generating query you have to take in consideration that only those values are considered whose record_status is 1,this record_status column is present in m_cbo table..so you have to always use where c.record_staus=1 in the query where c is alias name of m_cbo table but donot use record_status=1 if question asked for farmers \
                                                                                                                                                    "clcdc_id"
                                                                                                                                                    "clf_id"
                                                                                                                                                    "file_1"
                                                                                                                                                    "file_2"
                                                                                                                                                    "file_3"
                                                                                                                                                    "created_date"
                                                                                                                                                    "clcdc_name"
                                                                                                                                                    "address"
                                                                                                                                                    "pin"
                                                                                                                                                    "email"
                                                                                                                                                    "mobile"
                                                                                                                                                    "file_name_1"
                                                                                                                                                    "file_name_3"

   The "t_vidya_didi" table stores comprehensive information about educational facilitators, including their qualifications, personal details, contact information, and affiliations with community development centers and self-help groups.the columns are..
                                                                                                                                                                                                    "clf_id"
                                                                                                                                                                                                    "education_certificate_pic"
                                                                                                                                                                                                    "shg_id"
                                                                                                                                                                                                    "experience_certificate_pic"
                                                                                                                                                                                                    "applicant_dob"
                                                                                                                                                                                                    "aadhar_pic"
                                                                                                                                                                                                    "applicant_doj"
                                                                                                                                                                                                    "saving_account_pic"
                                                                                                                                                                                                    "id"
                                                                                                                                                                                                    "others_noneducation_certificate_pic"
                                                                                                                                                                                                    "vo_id"
                                                                                                                                                                                                    "month"
                                                                                                                                                                                                    "year"
                                                                                                                                                                                                    "vidya_didi_pic"
                                                                                                                                                                                                    "created_date"
                                                                                                                                                                                                    "aadhar"
                                                                                                                                                                                                    "caste_id"
                                                                                                                                                                                                    "caste_name"
                                                                                                                                                                                                    "nishakt_id"
                                                                                                                                                                                                    "nishakt"
                                                                                                                                                                                                    "nishakta_type"
                                                                                                                                                                                                    "temp_house_road_name_no"
                                                                                                                                                                                                    "temp_village_name"
                                                                                                                                                                                                    "temp_prakhand"
                                                                                                                                                                                                    "temp_jila"
  
  The "t_learner_profile" table records detailed profiles of learners, encompassing personal information, educational details, contact information, affiliations with community development entities, and various options for community service, providing a comprehensive overview of each student's background and engagement...the columns are...
                                                                                                                                                                                            "student_dob"
                                                                                                                                                                                        "month"
                                                                                                                                                                                        "year"
                                                                                                                                                                                        "created_date"
                                                                                                                                                                                        "student_pic"
                                                                                                                                                                                        "admission_date"
                                                                                                                                                                                        "is_active_update_date"
                                                                                                                                                                                        "registration_no"
                                                                                                                                                                                        "student_caste_category"
                                                                                                                                                                                        "student_caste_category_id"
                                                                                                                                                                                        "marital_status_id"
                                                                                                                                                                                        "marital_status"
                                                                                                                                                                                        "phone"
                                                                                                                                                                                        "email_id"
                                                                                                                                                                                        "district_id"
                                                                                                                                                                                        "district_name"
                                                                                                                                                                                        "block_id"
                                                                                                                                                                                        "block_name"
                                                                                                                                                                                        "clcdc_id"
                                                                                                                                                                                        "clcdc_name"
                                                                                                                                                                                        "panchayat_id"
                                                                                                                                                                                        "panchayat_name"
                                                                                                                                                                                        "village_id"
                                                                                                                                                                                        "village_name"
                                                                                                                                                                                        "ward_no"
                                                                                                                                                                                        "pin_code"
                                                                                                                                                                                        "emergency_name"
                                                                                                                                                                                        "emergency_relation"
                                                                                                                                                                                        "emergency_contact"
                                                                                                                                                                                        "current_employment_id"
                                                                                                                                                                                        "current_employment"
                                                                                                                                                                                        "higher_qualification_id"
                                                                                                                                                                                        "higher_qualification"
                                                                                                                                                                                        "clf_id"
                                                                                                                                                                                        "clf_name"
                                                                                                                                                                                        "vo_id"
                                                                                                                                                                                        "vo_name"
                                                                                                                                                                                        "shg_id"
                                                                                                                                                                                        "shg_name"
                                                                                                                                                                                        "seva_option_a"
                                                                                                                                                                                        "seva_option_a_name"
                                                                                                                                                                                        "seva_option_b"
                                                                                                                                                                                        "seva_option_b_name"
                                                                                                                                                                                        "seva_option_c"
                                                                                                                                                                                        "seva_option_c_name"
                                                                                                                                                                                        "seva_option_d"
                                                                                                                                                                                        "seva_option_d_name"
                                                                                                                                                                                        "seva_option_e"
                                                                                                                                                                                        "seva_option_e_name"
                                                                                                                                                                                        "seva_option_f"
                                                                                                                                                                                        "seva_option_f_name"
                                                                                                                                                                                        "seva_option_g"
                                                                                                                                                                                        "seva_option_g_name"
                                                                                                                                                                                        "seva_option_h"
                                                                                                                                                                                        "seva_option_h_name"
                                                                                                                                                                                        "seva_option_i"
                                                                                                                                                                                        "seva_option_i_name"
                                                                                                                                                                                        "seva_option_j"
                                                                                                                                                                                        "seva_option_j_name"
                                                                                                                                                                                        "seva_option_k"
                                                                                                                                                                                        "seva_option_k_name"
                                                                                                                                                                                        "seva_option_l"
                                                                                                                                                                                        "seva_option_l_name"
                                                                                                                                                                                        "seva_option_m"
                                                                                                                                                                                        "seva_option_m_name"
                                                                                                                                                                                        "fy"
                                                                                                                                                                                        "created_by"
                                                                                                                                                                                        "is_active"
                                                                                                                                                                                        "is_active_update_by"
                                                                                                                                                                                        "entry_id"
                                                                                                                                                                                        "student_name"
                                                                                                                                                                                        "student_pic_name"
                                                                                                                                                                                        "student_m_name"
                                                                                                                                                                                        "student_f_name"
                                                                                                                                                                                        "student_gender"
                                                                                                                                                                                        "student_gender_id"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     "temp_state"                                                                                                                                                 
The "mp_nursery_fy" table stores information related to nursery registrations, including member details, renewal and training dates, district and block affiliations, and other relevant information for each fiscal year, facilitating management and tracking of nursery-related activities.The columns are...
                                                                                                                                        "id"
                                                                                                                                        "member_id"
                                                                                                                                        "renewal_date"
                                                                                                                                        "training_date_from"
                                                                                                                                        "training_date_to"
                                                                                                                                        "nursery_registration_date"
                                                                                                                                        "mou_date"
                                                                                                                                        "created_on"
                                                                                                                                        "created_by"
                                                                                                                                        "mobile"
                                                                                                                                        "structure_type"
                                                                                                                                        "district_id"
                                                                                                                                        "block_id"
                                                                                                                                        "nursery_registration"
                                                                                                                                        "nursery_id"
                                                                                                                                        "nursery_name"
                                                                                                                                        "fy"
                                                                                                                                        "is_active"

The "t_sell_plant" table manages records of plant sales transactions, including details such as quantities available and sold, location information, entry specifics, and fiscal year-related data.The columns are...
                                                                                                                                        "total_plant_to_sell"
                                                                                                                                        "currently_available_plant"
                                                                                                                                        "entry_date"
                                                                                                                                        "id"
                                                                                                                                        "month"
                                                                                                                                        "month_name"
                                                                                                                                        "district_id"
                                                                                                                                        "block_id"
                                                                                                                                        "plant_size_id"
                                                                                                                                        "plant_sold_to_dept_id"
                                                                                                                                        "plant_cat_id"
                                                                                                                                        "plant_id"
                                                                                                                                        "remarks"
                                                                                                                                        "lat_val"
                                                                                                                                        "long_val"
                                                                                                                                        "address"
                                                                                                                                        "entry_by"
                                                                                                                                        "entry_type"
                                                                                                                                        "nursery_id"
                                                                                                                                        "fy"
                                                                                                                                        "year"

The "t_payment_receive_details" table tracks payment and receipt details, including monthly financial transactions, amounts received, remaining balances, and associated geographical and administrative information for efficient management and reconciliation.the columns are..
                                                                                                                                                            "id"
                                                                                                                                                            "month"
                                                                                                                                                            "total_amount"
                                                                                                                                                            "receive_amount"
                                                                                                                                                            "remaining_amount"
                                                                                                                                                            "entry_date"
                                                                                                                                                            "long_val"
                                                                                                                                                            "month_name"
                                                                                                                                                            "dept_id_from_receive_amt"
                                                                                                                                                            "address"
                                                                                                                                                            "entry_by"
                                                                                                                                                            "entry_type"
                                                                                                                                                            "remarks"
                                                                                                                                                            "lat_val"
                                                                                                                                                            "nursery_id"
                                                                                                                                                            "district_id"
                                                                                                                                                            "block_id"
                                                                                                                                                            "fy"
                                                                                                                                            
The "t_expenditure_details" table records financial expenditures, including amounts, dates, and geographical details, providing a comprehensive log for tracking and managing expenses at the district and block levels.the columns are..
                                                                                                                                                                        "amount"
                                                                                                                                                                        "entry_date"
                                                                                                                                                                        "year"
                                                                                                                                                                        "month"
                                                                                                                                                                        "month_name"
                                                                                                                                                                        "district_id"
                                                                                                                                                                        "block_id"
                                                                                                                                                                        "ae_id"
                                                                                                                                                                        "remarks"
                                                                                                                                                                        "lat_val"
                                                                                                                                                                        "long_val"
                                                                                                                                                                        "address"
                                                                                                                                                                        "entry_by"
                                                                                                                                                                        "expenditure_id"
                                                                                                                                                                        "fy"

The "m_bankdataupload" table stores data related to bank transactions and activities, including details such as transaction counts, amounts, commissions, account openings, and associated metadata, facilitating comprehensive monitoring and analysis...the columns are..
                                                                                                                                id SERIAL PRIMARY KEY,
                                                                                                                                date DATE,
                                                                                                                                isactive BOOLEAN,
                                                                                                                                year INTEGER,
                                                                                                                                created_date TIMESTAMP,
                                                                                                                                updated_by INTEGER,
                                                                                                                                updated_date TIMESTAMP,
                                                                                                                                deposit_no_of_tranx INTEGER,
                                                                                                                                deposit_amt_of_tranx DECIMAL(10, 2),
                                                                                                                                deposit_commission DECIMAL(10, 2),
                                                                                                                                withdrawal_no_of_tranx INTEGER,
                                                                                                                                withdrawal_amt_of_tranx DECIMAL(10, 2),
                                                                                                                                withdrawal_commission DECIMAL(10, 2),
                                                                                                                                total_no_of_tranx INTEGER,
                                                                                                                                total_amt_of_tranx DECIMAL(10, 2),
                                                                                                                                total_commission DECIMAL(10, 2),
                                                                                                                                total_account_open INTEGER,
                                                                                                                                action_type VARCHAR(50),
                                                                                                                                month INTEGER,
                                                                                                                                fileuploaded_by INTEGER,
                                                                                                                                fileuploaded_date TIMESTAMP,
                                                                                                                                agent_id INTEGER,
                                                                                                                                agent_name VARCHAR(255),
                                                                                                                                ip_address VARCHAR(50),
                                                                                                                                created_by INTEGER,
                                                                                                                                bank_name VARCHAR(255)

                                                                                        
 The "m_agentnew" table contains records of agents, including their activation details, contact information, affiliations with banks and administrative divisions, along with additional status indicators and training information...the columns are..
                                                                                                                            id SERIAL PRIMARY KEY,
                                                                                                                            bank_id INTEGER,
                                                                                                                            district_id INTEGER,
                                                                                                                            block_id INTEGER,
                                                                                                                            panchayat_id INTEGER,
                                                                                                                            date_of_activation DATE,
                                                                                                                            month_of_activation INTEGER,
                                                                                                                            created_date TIMESTAMP,
                                                                                                                            is_active BOOLEAN,
                                                                                                                            mobile_no VARCHAR(20),
                                                                                                                            district_name VARCHAR(255),
                                                                                                                            ip_address VARCHAR(50),
                                                                                                                            block_name VARCHAR(255),
                                                                                                                            created_by INTEGER,
                                                                                                                            agent_id INTEGER,
                                                                                                                            name VARCHAR(255),
                                                                                                                            panchayat_name VARCHAR(255),
                                                                                                                            bank_name VARCHAR(255),
                                                                                                                            status VARCHAR(255),
                                                                                                                            cbc VARCHAR(255),
                                                                                                                            iibf VARCHAR(255),
                                                                                                                            linkbranch VARCHAR(255)     


The table MP_PG_MEMBER contains information about the poultry service. It includes columns such as id, pg_id, member_id, shg_id, created_on, village_id, created_by, category_id, district_id, block_id, is_sjy and pg_name. \n
       The table T_HOUSEHOLD_BATCH contains information about the PGs, members and the quantity of the chicks distributed for poultry. It includes columns such as id, shelter_unit_id, member_id, quantity_received, contribution_received, receiving_date, created_on, material_name, address, lat_val, long_val, photo_url, photo, is_contributed, batch_name, scheme, village_id, pg_id, shg_id and created_by. Beneficiaries means members(member_id). \n
       The table G_MEMBER_MAPPING contains information about the goatry service. It includes columns such as created_on, district_id, block_id, pg_id, village_id, member_id, shg_id, id, village_name, district_name, created_by, block_name, member_name, pg_name and husband_name. \n
       The table G_GOATRY_DISTRIBUTION contains information about the PGs, members and the number of goats distributed for goatry. It includes columns such as no_of_goat_received, villag_id, date_of_procurement, shg_id, inserted_date, goat1_tagg_num, capture_date, goat2_tagg_num, updated_date, id, goat3_tagg_num, member_id, scheme_name, supplier_name, is_insurance, goat1_colour, goat2_colour, goat3_colour, photo1_url, inserted_by, pg_id and updated_by. Beneficiaries means members(member_id). Take pg_id from this table. \n
       The table M_DCS_PROFILE contains information about the dairy service. It includes columns such as month_id, year, dcs_formation_date, created_on, sl, dcs_panchayat_name, dcs_id, dcs_name, meeting_date, meeting_frequency, dcs_tolla, dcs_address, ward_no, dcs_comfed_id, dcs_type, is_active, created_by, entry_id, district_id, block_id and dcs_panchayat_id. \n
       The table MP_MEMBER_DCS contains dairy information like- members in dairy, etc. It includes columns such as sl, member_id, mapping_date, month_id, year, created_date, demap_date, updated_date, vo_name, shg_id, shg_name, is_active, member_name, member_husband_name, demaped_by, created_by, dcs_id, dcs_name, district_id, block_id, village_id, village_name and vo_id. The full form of dcs is dairy cop society. \n
       The table MP_POND_FPG_MAPPING contains information about fishery. It includes columns such as pond_fpg_mapping_date, month_id, year, created_on, fpg_formation_date, sl, fpg_id, fpg_name, meeting_frequency, meeting_date, created_by, is_active, entry_id, district_id, block_id, pond_id and pond_name. \n
       The table BATCH_CREATION contains information about fishery like number of batch etc. It includes columns such as cycle_completed_date, rohu, katla, mrigal, grass_carp, common_carp, silver_carp, others, collection_date, entry_date, is_cycle_completed, id, scheme_id, seed_id, seed_weight, seed_quantity, purchase_amount, district_id, block_id, batch_number, fpg_id, fpg_name, mobile_no, photo, lat_val, long_val, address and entry_by. \n
       The table M_POND contains information about fishery ponds. It includes columns such as sl, doa_district_authority, month_id, year, pond_area, actual_water_area_pond, is_active, is_active_update_time, created_date, pond_type_id, pond_type, entry_id, unique_code_jjha, created_by, is_active_by, pond_id, pond_name, district_id, block_id, village_id, project_name, address and fy. \n
       The table T_SELL_DETAILS contains information about fishery such as quantity of fish harvested, revenue generated from fish and others, etc. It includes columns such as entry_date, weight_in_kg, fish_quantity, avg_weight, sell_amount, sell_date, long_val, address, entry_by, district_id, block_id, fpg_id, batch_no, fish_type_id and lat_val. \n
       The table MP_MATASYA_SAKHI_POND_MAPPING contains information about fishery and pond such as total matasya sakhi ponds, etc. It includes columns such as month_id, year, created_on, matasya_sakhi_formation_date, mapping_date, demaped_time, sl, matasya_sakhi_name, matasya_sakhi_meeting_frequency, matasya_sakhi_meeting_date, matasya_sakhi_address, created_by, is_active, demaped_by, district_id, block_id, entry_id, pond_id, pond_name and matasya_sakhi_id. \n
       The table MP_MEMBER_WITH_FPG_MAPPING contains information about fishery such as hhs members in fishery etc. It includes columns such as sl, member_id, month_id, year, created_on, demaped_time, vo_id, vo_name, shg_id, shg_name, is_active, member_name, husband_name, demaped_by, created_by, entry_id, district_id, block_id, fpg_id and fpg_name. \n
       The table M_PROFILE contains information about hns and hns help desk, the full form of hns is health nutrition sanitation. It includes columns such as dob, is_clf_not_created, dow, created_date, sl, panchayat_code, dist_name, block_name, panchayat_name, name, hus_name, gender, education_details, mobile, adhar_no, address, email_id, mobile_type, lat_value, long_value, location, created_by, clf_id, clf_name, clf_name_hindi, brlps_emp_id, vo_id, vo_name, vo_name_hindi, user_id, user_type, district_code and block_code. \n
       The table M_SHG_HNS_USER_TABLE contains information about hns help desk, the full form of hns is health nutrition sanitation. It has information such as whether the user is active or not etc. It includes columns such as sl_no, active, user_id and password. \n
       The table T_TRAINING_OF_CADRE_AND_PMT contains information about hns help desk, the full form of hns is health nutrition sanitation. It has information such as the training status of a user. It includes columns such as sl, date_of_training, entry_date, cm_cnrp_id, cm_cnrp_name, module_name, session_name, dist_code, verified_data, remarks, entry_by, block_code, cadre_type and training_completed_status. \n
       The table M_USER_PROFILE contains information about swasthya mitra. It includes columns such as created_date, active, user_type, district_code, dist_name, hospital_id, name, mobile, aadhar_no, lat_value, long_value, location, created_by, user_id, swasthya_mitra_photo and password. \n
       The table T_PATIENT_INFO contains information about IPD and OPD. It includes columns such as ipd_opd_date, is_discharged, discharged_date, revisit_date, admission_date, is_closed, entry_date, id, mobile_no, service_type, disease_id, other_reason, remarks, hospital_id, entry_by, lat_val, long_val, entry_address, remarks_at_discharge, discharge_reason, discharge_reason_hin, without_treatment_discharge_reason, arrangement, health_quality_services, quick_services, doctor_services, availability_medicine_services, admission_waiting_time, opd_ipd_no, patient_name, gender, is_jeevika_member, district_id, block_id and address. \n
       The table MP_CBO_MEMBER_ACTIVITY contains information about multiple activites in which the members are involbed such as vegetable farming, regular farming, jute, atr and creft etc. It includes columns such as member_id, cbo_id, activity_id, id, record_status, created_by, created_on, updated_by and updated_on. \n
       The table M_INTERVENTION_ACTIVITY contains information about the activity names. It includes columns such as activity_id, theme_id, created_on, updated_by, updated_on, record_status, created_by, activity_short_name, activity_description, activity_description_hindi and activity_short_name_hindi. \n
       The table EMPLOYER_WINDOW acotains information about number of employer registered is differect districts, blocks and company profile. It includes columns such as id, district_id, district_name, block_id, block_name, name, company_profile, no_of_positions, age_range, salary_range, contact_person_name, designation, contact_number, created_by, created_on, updated_by, updated_on, type_of_industry and work_profile. \n
       The table PLAN_JOB_FAIR_TRAINING contains information about number of job fair conducted in different districts and blocks. It includes columns such as date_of_event, plan_id, district_name, block_id, block_name, location_address, created_by, created_on, date_of_event2, activity and district_id. \n
       The table CANDIDATES_PROFILE contains information about number of candidates registered in different districts, blocks and panchayats. It includes columns such as updated_on, id, block_id, village_id, name, father_name, dob, contact_number, education_qualification, year_of_experience, remarks_if_any, work_in_state, work_out_state, is_experienced, created_by, created_on, updated_by, in_district_id, out_district_name, aadhaar_number, photo, category_id, registration_number, latitude, longitude, isshg and district_id. \n
       The IS_LETTER_OFFERED contains information about candidates selected and candidates joined in differect districts and blocks. It includes columns such as created_on, date_of_joining, emp_id, id, block_name, registration_num, event_id, is_offer_letter_issued, created_by, salary, is_offer_accepted, reason_id, reason_other, working_location, working_in_state, district_id, district_name and block_id.                                                                                            
 
                                                                                                                                                                                        For example if question is like 
What is the total count of SHG in Patna in 2023?....then query should be...SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND c.record_status=1...you can clearly see c.record_status=1 has been used which is important  to get only the information for those values which are live..so this c.record_status=1 will be used almost in all sq query except for farmer tables \
What is the total count of farmers?....then query should be.....
                                        SELECT COUNT(DISTINCT FARMER_ID) AS total_farmers
                                                FROM m_farmer......you can clearly see here record_status=1 has not been used as it belongs question from farmer tables \
                                                
While generating sql query donot do any silly mistakes or donot give wrong query...this query will be used for very important person whch is related to their livelihoods \
For example:-

When I asked "how many shg in patna district are there?"
You returned query this..SELECT
                        (*) AS shg_count
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN
                        m_district d ON c.district_id = d.district_id
                       where upper(t.type_short_name)= 'SHG'
                        AND upper(d.district_name) = 'NA'
                        AND c.record_status=1.......which is wrong you can clearly see that you have taken d.district_name='NA'...it should be d.district_name='PATNA' \

                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...

                        SELECT
                        (*) AS shg_count
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN
                        m_district d ON c.district_id = d.district_id
                       where upper(t.type_short_name) = 'SHG'
                        AND upper(d.district_name)= 'PATNA'
                        AND c.record_status=1

While generating sql it is very important to not put or use semicolon(;) at the end of query \

When I asked "Number of cbo per block per district"
You returned query this..SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
FROM m_cbo c
INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
WHERE c.record_status=1
GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
WHERE ROWNUM <= 5;.......which is wrong you can clearly see that you have used semicolon(;) at the end of query..you should not use semicolon(;) \
                        Also the 'ROWNUM' condition is applied directly with query , \
                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...


    SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
    FROM m_cbo c
    INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
    INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
    WHERE c.record_status = 1
    GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
    ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
...

For example:-

when i ask....What is the total amount of savings for all SHGs in district Bhojpur?

then the query generated is this \
SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1
WHERE ROWNUM <= 5...which is wrong the right query is.. \

SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1...you can clearly see i have not used WHERE ROWNUM <= 5 which is not required..\



While generating query if the question is to give information for last 2 months or last 3 months or last months,then use (CURRENT_DATE - INTERVAL '' MONTH) to extract the last months information \

Never use ROWNUM with query......

For Example:- 
when asked What is the most common CBO type in district Vaishali?

then query generated is....SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
FROM M_CBO C
INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
AND C.RECORD_STATUS = 1
GROUP BY TYPE_DESCRIPTION
ORDER BY CBO_COUNT DESC
WHERE ROWNUM <= 5...which is wrong you can clearly see that ROWNUM has been used directly with query and also ROWNUM is not required here \

The right query is...SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC

fOR eXAMPLE:-
User Question:-give me count of panchayat wise shg from patna district?
The Query you generated is:-SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID
                        WHERE upper(t.TYPE_SHORT_NAME) = 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC
                        LIMIT 5...here you can clearly see that in (INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID) there should not be join between m_panchayat and m_cbo table on panchayat_id as m_cbo doesnot contains panchayat_id \

The right Query is:-   SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
FROM m_cbo c
INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
AND upper(d.DISTRICT_NAME) = 'PATNA'
AND c.record_status = 1
GROUP BY p.PANCHAYAT_NAME
ORDER BY shg_count DESC...here you can clearly see as panchayat_id was not present in m_cbo so i searched which columns are common in m_cbo and m_panchayat and founD there was district_id and block_id but i made join on block_id like this (INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID) \

For last 3 months
CURRENT_DATE - INTERVAL '3' MONTH
for last 2 months
CURRENT_DATE - INTERVAL '2' MONTH

for example:
if the question is "total count of cbo formed in sheohar district in last 3 months?" \

the query should be

SELECT COUNT(c.CBO_ID) AS cbo_count
FROM m_cbo c
INNER JOIN m_district d ON c.district_id = d.district_id
WHERE upper(d.district_name) = 'SHEOHAR'
AND c.formation_date >= CURRENT_DATE - INTERVAL '3 MONTH'
AND c.record_status = 1........you can clearly see that it is using CURRENT_DATE - INTERVAL '3' MONTH to extract the last 3 months information..you have to use this method whenever asked about last months question \

and so on \

Some more examples:-

question:-What is the count of all members across SHGs, VOs and CLFs in district Patna?", \

sql query:- SELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1


For example
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_postgres_prompt+"and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query....... Donot get confused in code and id both are same for example if there is BLOCK_CODE or BLOCK_ID both are same similarly if there is DISTRICT_CODE or DISTRICT_ID both are same ,\
same goes for village_id and village_code and panchayat_id and panchayat_code and clf_id and clf_code.\
You cannot perform join on clf_id with village_id or block_id or block_code\
but you can perform join on village_id and village_code ,similar for district_id and district_code and block_id and block_code.\
    ",
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], 
)

memory = ConversationBufferMemory(memory_key="chat_history")
query_chain = create_sql_query_chain(llm, db,prompt=few_shot_prompt)

    

  




class Table(BaseModel):
        """Table in SQL database."""

        name: str = Field(description="Name of table in SQL database.")

table_names = "\n".join(db.get_usable_table_names())
system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

    {table_names}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)



system = f"""Return the names of the SQL tables that are relevant to the user question. \
The tables are:

CBO
Farmer"""
category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)


from typing import List


def get_tables(categories: List[Table]) -> List[str]:
        tables = []
        for category in categories:
            if category.name == "CBO":
                tables.extend(
                [
                    "m_cbo",
                    "m_cbo_type",
                    "m_cbo_member",
                    "m_cbo_shg_member",
                    "t_cbo_appl_mapping",
                    "t_cbo_loan_register",
                    "t_acc_voucher",
                    "t_bulk_bank_acc",
                    "mp_cbo_member",
                    "m_block",
                    "m_district",
                    "m_designation",
                    "m_village",
                    "m_panchayat",
                    "m_designation",
                    "clf_masik_grading",
                    "vo_masik_grading",
                    "shg_masik_grading",
                    "profile_entry",
                    "t_expenditure_details",
                    "t_sell_grain",
                    "t_digital_banking",
                    "t_advisory_farmer_entry",
                    "t_agri_input",
                    "t_marketing_services",
                    "t_nursery_services",
                    "m_expenditure_type",
                    "m_chc_details",
                    "t_farmer_booking",
                    "t_chc_expenditure_details",
                    "t_freight_details",
                    "neera_selling","neera_collection","m_pg","pg_non_pg_memberes","m_clcdc","t_vidya_didi","t_learner_profile","mp_nursery_fy","t_sell_plant","t_payment_receive_details","t_expenditure_details","profile_entry_2","m_bankdataupload","m_agentnew","mp_pg_member","t_household_batch","g_member_mapping","g_goatry_distribution","m_dcs_profile","mp_member_dcs","mp_pond_fpg_mapping","batch_creation","t_sell_details","m_pond","t_sell_details","mp_matasya_sakhi_pond_mapping",
"mp_member_with_fpg_mapping","m_profile", "m_shg_hns_user_table", "t_training_of_cadre_and_pmt","m_user_profile","t_patient_info","mp_cbo_member_activity","m_intervention_activity""employer_window", "plan_job_fair_training", "candidates_profile", "is_letter_offered"
                ]
            )
            elif category.name == "Farmer":
                tables.extend(["m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
                            "m_farmer_pest_management", "m_farmer_seed", "m_farmer_soil_management","t_farmer_transaction","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology"])
        return tables


table_chain = category_chain | get_tables
table_chain = {"input": itemgetter("question")} | table_chain

full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain


# query = full_chain.invoke(
#         {"question": "how many cbo in patna district?" }) 
# print(db.run(query))


@app.route('/response', methods=['POST'])
def api():
    try:
        data = request.get_json()
        question = data.get('question', '')

        try:
            query = full_chain.invoke(
            {"question": question })
            llm2= GoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyC1mncPJJKSU70yJspuzPx-jw_sH89jiCE', temperature=0)

        
            print(query)
        except Exception as e:
             print(e)

        print("-"*20)
        print()
        print()


#         try:
#             mid_query=llm2(f"""
# As an expert in Postgres SQL, your task is to carefully analyze a user's question{question} and this query {query} to get desire result onthe given database schema,....{db.get_context()}... which includes table names, column names, and their functionality. 
# Your role is to think step by step analyse the user question and query line by line . However, 
# due to the complexity of the database structure or possible misunderstandings of the user's question, 
# the initial query which is this... {query}.. may be incorrect. Your responsibility is to identify the important keys present in the schema, check if the generated SQL query can provide the correct answer, 
# and ensure that any joins or operations are performed correctly.Here is more informstion about tables and the columns present inside.... \

# The table M_CBO is a master table storing information about Community Based Organizations (CBOs),vo(Village Organisation),shg(Self Help Group) and clf(Cluster Level Federation) with columns including CBO_ID, CBO_NAME, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, CBO_TYPE_ID, THEME_ID, LATITUDE, LONGITUDE, TOLA_MOHALLA_NAME, MEETING_PERIODICITY, MEETING_DAY, MEETING_DATE, GENERAL_SAVING_AMOUNT, HRF_SAVING_AMOUNT, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, SHARE_RATE, MEETING_START_TIME, STATE_ID, FORMATION_DATE, SCHEME_ID, CBO_NAME_HINDI, OTHER_SAVING_1, OTHER_SAVING_2, OTHER_SAVING_3, MEMBERSHIP_FEE, REGISTRATION_NUMBER, REGISTRATION_DATE, COMPLETE_STATUS, NRLM_CODE, PWD, LOKOS_CODE.\n
#         The table M_CBO_TYPE is a master table containing information about different types of Community Based Organizations (CBO types) with columns such as CBO_TYPE_ID, TYPE_SHORT_NAME, TYPE_DESCRIPTION, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, TYPE_SHORT_NAME_HINDI, TYPE_DESCRIPTION_HINDI, PARENT_CBO_TYPE_ID.\n
#        The table M_CBO_MEMBER is a master table containing information about individual members of a Community Based Organization (CBO) with columns such as MEMBER_ID, NAME, FATHER_NAME, HUSBAND_NAME, DOB (Date of Birth), GENDER, ADDRESS, EDUCATION, DATE_OF_JOINING, EMAIL_ADDRESS, PHONE_NO, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, STATE_ID, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, NAME_HINDI, FATHER_NAME_HINDI, HUSBAND_NAME_HINDI, POSTOFFICE, THANA, KYC_TYPE, KYC_NUMBER, EBS_MEMBER_ID, SECC_PIN_NO, STATEID, DISTRICTID, BLOCKID, VILLAGEID, TOILET, AADHAR_NUMBER, AADHER_CARD_SEEDED, NRLM_MEMBER_ID, REF_CODE, AADHAR_STATUS, LOKOS_MEMBER_CODE.\n
#        The table M_CBO_SHG_MEMBER is a master table that stores detailed information about individual members associated with a Self Help Group (SHG) within a Community Based Organization (CBO). It includes columns such as MEMBER_ID, CATEGORY, CASTE, RELIGION, TOLA_NAME, CREATED_BY, UPDATED_BY, CREATED_ON, UPDATED_ON, RECORD_STATUS, CBO_ID, ENDORSED_BY_GRAMSABHA, DISTRICTID.\n
#        The table T_CBO_APPL_MAPPING is a transactional table responsible for storing information related to transactions involving the mapping of applications to a Community Based Organization (CBO). It includes columns such as APPLICATION_ID, ACC_NUMBER, ACC_OPENING_DATE, ACC_OPENING_STATUS, CBO_ID, CREATED_ON, UPDATED_ON, CREATED_BY, and UPDATED_BY to track transactional details associated with this mapping.\n
#        The table T_CBO_LOAN_REGISTER is a transactional table that maintains records of loans registered within a Community Based Organization (CBO). It contains columns such as LOAN_REGISTER_ID, CBO_ID, LOAN_TYPE_ID, LOAN_AMOUNT, LOAN_INSTALLMENTS, LOAN_DATE, RECORD_UPDATED_ON, RECORD_UPDATED_BY, RECORD_CREATED_ON, RECORD_CREATED_BY, LOAN_REASON, INTEREST_AMOUNT, PAID, TILL_DATE, LOAN_FROM_CBO_ID, IMEI_NUMBER, and RECORD_SYNCED_ON.\n
#        The table T_ACC_VOUCHER is a transactional table that stores accounting vouchers within the context of a Community Based Organization (CBO). It includes columns such as VOUCHER_ID, VOUCHER_DATE, CBO_ID, DEBIT_ACCOUNT, CREDIT_ACCOUNT, REMARKS, OTHER_NAME, DEBIT_STAKEHOLDER_ID, VOUCHER_TYPE_ID, CREATED_ON, CREATED_BY, CREDIT_STAKEHOLDER_ID, IMEI_NUMBER, RECORD_SYNCED_ON, CHEQUE_NO, and CHEQUE_DATE. \n
#        The table M_BLOCK represents information about different blocks. It includes columns such as BLOCK_ID, BLOCK_NAME, DISTRICT_ID, STATE_ID, BLOCK_NAME_HINDI, NRLM_BLOCK_CODE, ADDOPED_BY_SCHEME, PROJECT_CODE, and PROJECT_CODE_TILL_APRIL_2023. \n
#        The table M_DISTRICT contains information about different districts. It includes columns such as DISTRICT_ID, DISTRICT_NAME, STATE_ID, DISTRICT_NAME_HINDI, DISTRICT_CENS_2011_ID, and NRLM_DISTRICT_CODE.\n
#        The table M_PANCHAYAT contains information about various panchayats. It includes columns such as STATE_ID, DISTRICT_ID, BLOCK_ID, PANCHAYAT_ID, PANCHAYAT_NAME, PANCHAYAT_NAME_HINDI, and NRLM_PANCHAYAT_CODE. \n
#        The table M_VILLAGE contains information about various villages. It includes columns such as VILLAGE_ID, VILLAGE_NAME, BLOCK_ID, OTHER_POPULATION, SC_POPULATION, ST_POPULATION, DISTRICT_ID, STATE_ID, PANCHAYAT_ID, VILLAGE_NAME_HINDI, EBC_POPULATION, BC_POPULATION, MD_POPULATION, and NRLM_VILLAGE_CODE. \n
#        The table MP_CBO_MEMBER is a mapping table that associates members with a specific Community Based Organization (CBO). It includes columns such as MEMBER_ID, CBO_ID, DESIGNATION_ID, RECORD_STATUS, ID, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, and DISTRICTID.\n
#         T_BULK_BANK_ACC is a transactional tabe which contains columns APPLICATION_ID BRANCH_ID,ACC_TYPE_ID,APPLICATION_DATE,CREATED_ON,UPDATED_ON,BANK_ID,NO_OF_APPLICATIONS,STATUS,REMARKS,ACCOUNT_HOLDER_TYPE this able is used in conjunction with other tables when question asked about saving account of shg,vo or clf
#         
# M_DESIGNATION is a master tables which contain the following columns DESIGNATION_ID DESIGNATION_SHORT_NAME DESIGNATION_FULL_NAME MEMBER_GROUP_ID CREATED_BY CREATED_ON UPDATED_BY UPDATED_ON RECORD_STATUS DESIGNATION_SHORT_NAME_HINDI DESIGNATION_FULL_NAME_HINDI EBS_JOB_ID EBS_THEMATIC_ID...whenever the question is the count of member then member_group_id=3 and designation_id!=31
    #     The  table CLF_MASIK_GRADING contains information about the grades assigned to the clf. It includes columns such as sl, year, month, criteria4, criteria5, criteria6, total_marks, clf_id, criteria1, criteria2, criteria3, month_name, district_id, block_id and final_grade. The cbo_type_id of the clf is 1.
    #    The  table VO_MASIK_GRADING contains information about the grades assigned to the vo. It includes columns such as sl, year, month, criteria2, criteria3, criteria4, criteria5, total_marks, vo_id, criteria1, month_name, district_id, block_id, clf_id and final_grade. The cbo_type_id of the vo is 2. \n
    #    The  table SHG_MASIK_GRADING contains information about the grades assigned to the shg. It includes columns such as sl, year, month, criteria4, criteria5, criteria6, total_marks, shg_id, criteria1, criteria2, criteria3, month_name, clf_id, vo_id and final_grade. The cbo_type_id of the shg is 3. \n
    #       The M_FARMER table stores essential details about farmers. Its columns include:
                                                                    # FARMER_ID: Unique identifier.
                                                                    # MEMBER_ID: Linked to a Community Based Organization (CBO) member.
                                                                    # AADHAR: Aadhar number for identification.
                                                                    # MOBILENO: Contact number.
                                                                    # BANK_ID: Bank identifier.
                                                                    # BRANCH_ID: Branch identifier.
                                                                    # ACCOUNT_NO: Bank account number.
                                                                    # PHOTO: Farmer's photograph.
                                                                    # CREATED_BY: Creator information.
                                                                    # CREATED_ON: Creation timestamp. \n
        # The M_FARMER_CROP table manages information about crops cultivated by farmers. Its columns include:

        #                                                                                 CROP_ID: Unique identifier for each crop record.
        #                                                                                 CROP_NAME: Name of the crop being cultivated.
        #                                                                                 CROP_TYPE_ID: Identifier representing the type of crop (e.g., cereal, legume, vegetable). \n
        # The M_FARMER_CROP_TECHNOLOGY table stores data related to agricultural technologies used for specific crops. Its columns are:

        #                                                                                                 TECHNOLOGY_ID: Unique identifier for each technology entry.
        #                                                                                                 CROP_ID: Identifier linking the technology to a specific crop.
        #                                                                                                 TECHNOLOGY: Description or name of the agricultural technology utilized.  \n 
            #  The M_FARMER_CROPTYPE table manages information about different types of crops. Its columns include:
            #                                                                                 CROP_TYPE_ID: Unique identifier for each crop type.
            #                                                                                 CROP_TYPE: Name or description of the crop type. \n
        
        # The M_FARMER_LAND table stores data regarding landholdings of farmers. Its columns include:
        #                                                                         LAND_ID: Unique identifier for each land record.
        #                                                                         FARMER_ID: Identifier linking the land to a specific farmer.
        #                                                                         LANDHOLDINGOWN: Area of land owned by the farmer.
        #                                                                         LANDHOLDINGLEASE: Area of land leased by the farmer.
        #                                                                         IRRIGATEDLAND: Area of land that is irrigated.
        #                                                                         NONIRRIGATEDLAND: Area of land that is not irrigated.
        #                                                                         CREATED_BY: Information about the user or process that created the land record.
        #                                                                         CREATED_ON: Timestamp indicating the date and time when the land record was created in the system. \n
#         The M_FARMER_PEST_MANAGEMENT table contains data related to pest management treatments for farmers. Its columns include:

                                                                                                # P_TREATMENT_ID: Unique identifier for each pest treatment entry.
                                                                                                # TREATMENT: Description or name of the pest management treatment. \n
        
#         The M_FARMER_SEED table maintains information about different types of seeds used by farmers. Its columns include:

                                                                                                # SEED_TYPE_ID: Unique identifier for each seed type.
                                                                                                # SEED_TYPE: Description or name of the seed type. \n
        
#         The M_FARMER_SOIL_MANAGEMENT table stores details regarding soil management practices adopted by farmers. Its columns include:

                                                                                                            # SOILPRACTISE_ID: Unique identifier for each soil management practice entry.
                                                                                                            # SOIL_PRACTISE: Description or name of the soil management practice. \n
        
        # The T_FARMER_TRANSACTION table records transactional data associated with farmers' activities. Its columns include:
        #                                                     TRANSACTION_ID: Unique identifier for each transaction.
        #                                                     FARMER_ID: Identifier linking the transaction to a specific farmer.
        #                                                     VO_ID: Identifier for the Village Organisation (VO) associated with the transaction.
        #                                                     SHG_ID: Identifier for the Self Help Group (SHG) associated with the transaction.
        #                                                     FY: Fiscal year of the transaction.
        #                                                     CROP_TYPE_ID: Identifier representing the type of crop involved in the transaction.
        #                                                     CULTIVATION_AREA: Area of land cultivated for the transaction.
        #                                                     SEEDS_USED: Quantity of seeds used.
        #                                                     SEEDS_VARIETY: Variety of seeds used.
        #                                                     SEED_TYPE_ID: Identifier representing the type of seed used.
        #                                                     TECHNOLOGY_ID: Identifier representing the agricultural technology used.
        #                                                     TOTAL_YIELD: Total yield obtained from the transaction.
        #                                                     CREATED_BY: Information about the user or process that created the transaction.
        #                                                     CREATED_ON: Timestamp indicating the date and time when the transaction was created.
        #                                                     CROP_ID: Identifier for the specific crop involved in the transaction.
        #                                                     SOILPRACTISE_ID: Identifier representing the soil management practice employed.
        #                                                     TREATMENT_ID: Identifier representing the pest management treatment applied.  \n  

# The T_MP_FARMER_TRANSACTION_PEST is mapping table records transactional data related to pest management treatments for farmers. Its columns include:
#                                                                                                         TRANSACTION_ID: Unique identifier for each transaction.
#                                                                                                         P_TREATMENT_ID: Identifier for the pest management treatment applied.
#                                                                                                         CREATED_BY: Information about the user or process that created the transaction.
#                                                                                                         CREATED_ON: Timestamp indicating the date and time when the transaction was created.   \n  
        # The T_MP_FARMER_TRANSACTION_SOIL is mpping table contains transactional data related to soil management practices adopted by farmers. Its columns include:
        #                                                                                                                     TRANSACTION_ID: Unique identifier for each transaction.
        #                                                                                                                     SOILPRACTISE_ID: Identifier for the soil management practice applied.
        #                                                                                                                     CREATED_BY: Information about the user or process that created the transaction.
        #   
        #                                                                                                                   CREATED_ON: Timestamp indicating the date and time when the transaction was created. \n
# The T_MP_TRANSACTION_CROPTECHNOLOGY is mapping table stores transactional data related to crop technologies used by farmers. Its columns include:
                                                                                                        # TRANSACTION_ID: Unique identifier for each transaction.
                                                                                                        # TECHNOLOGY_ID: Identifier for the crop technology applied.
                                                                                                        # CREATED_BY: Information about the user or process that created the transaction.
                                                                                                        # CREATED_ON: Timestamp indicating the date and time when the transaction was created. \n
# While calculating member or if the question contains find or count member then donot join m_cbo and m_cbo_member on cbo_id directly as both does not contain any common column...m_cbo contains cbo_id whereas m_cbo_member contains member_id \
# in that case you must use mp_cbo_member which is a mapping table and contains both cbo_id and member_id... \

# For example if the question is:-
# give me toatal members between 2020 and 2021

# then correct query is:-
# SELECT 
#                             COUNT(DISTINCT m.member_id) AS total_members
#                             FROM
#                             m_cbo_member m
#                             INNER JOIN
#                             mp_cbo_member t on m.member_id=t.member_id
#                             INNER JOIN
#                             m_cbo c ON t.cbo_id = c.cbo_id
#                             WHERE
#                             EXTRACT(YEAR FROM m.date_of_joining) BETWEEN 2020 AND 2021
#                             AND c.record_status=1....you can clearly see that to join m_cbo_member and m_cbo the mp_cbo_member table has been used in between

        
#         Look at the generated sql query which is this {query} and carefully go through it and see in the above tables and match whether the join has been coorectly performed on right columns.
        
#         These are some Examples for your reference:-

#         While generating query you have to take in consideration that only those values are considered whose record_status is 1,this record_status column is present in m_cbo table..so you have to always use where c.record_staus=1 in the query where c is alias name of m_cbo table \
# For example if question is like 
# What is the total count of SHG in Patna in 2023?....then query should be...SELECT COUNT(c.CBO_ID) AS shg_count
#                             FROM m_cbo c
#                             INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
#                             INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
#                             WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
#                             AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
#                             AND c.record_status=1...you can clearly see c.record_status=1 has been used which is important to get only the information for those values which are live..so this c.record_status=1 will be used almost in all sq query except for farmer tables \
# What is the total count of farmers?....then query should be.....
#                                         SELECT COUNT(DISTINCT FARMER_ID) AS total_farmers
#                                                 FROM m_farmer......you can clearly see here record_status=1 has not been used as it belongs question from farmer tables \.

# While generating sql query donot do any silly mistakes or donot give wrong query...this query will be used for very important person whch is related to their livelihoods \
# For example:-

# When I asked "how many shg in patna district are there?"
# You returned query this..SELECT
#                         (*) AS shg_count
#                         m_cbo c
#                         INNER JOIN
#                         m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
#                         INNER JOIN
#                         m_district d ON c.district_id = d.district_id
#                        where upper(t.type_short_name)= 'SHG'
#                         AND upper(d.district_name) = 'NA'
#                         AND c.record_status=1.......which is wrong you can clearly see that you have taken d.district_name='NA'...it should be d.district_name='PATNA' \

#                         This is just one example to show you that this kind of mistake should not be done.

#                         The right query is:-...

#                         SELECT
#                         (*) AS shg_count
#                         m_cbo c
#                         INNER JOIN
#                         m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
#                         INNER JOIN
#                         m_district d ON c.district_id = d.district_id
#                        where upper(t.type_short_name) = 'SHG'
#                         AND upper(d.district_name)= 'PATNA'
#                         AND c.record_status=1

# While generating sql it is very important to not put or use semicolon(;) at the end of query \

# When I asked "Number of cbo per block per district"
# You returned query this..SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
# FROM m_cbo c
# INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
# INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
# WHERE c.record_status=1
# GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
# ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
# WHERE ROWNUM <= 5;.......which is wrong you can clearly see that you have used semicolon(;) at the end of query..you should not use semicolon(;) \
#                         Also the 'ROWNUM' condition is applied directly with query , \
#                         This is just one example to show you that this kind of mistake should not be done.

#                         The right query is:-...


#     SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
#     FROM m_cbo c
#     INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
#     INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
#     WHERE c.record_status = 1
#     GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
#     ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
# ...

# For example:-

# when i ask....What is the total amount of savings for all SHGs in district Bhojpur?

# then the query generated is this \
# SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
# FROM M_CBO
# WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
# AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
# AND RECORD_STATUS = 1
# WHERE ROWNUM <= 5...which is wrong the right query is.. \

# SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
# FROM M_CBO
# WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
# AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
# AND RECORD_STATUS = 1...you can clearly see i have not used WHERE ROWNUM <= 5 which is not required..\



# While generating query if the question is to give information for last 2 months or last 3 months or last months,then use (CURRENT_DATE - INTERVAL '' MONTH) to extract the last months information \

# Never use ROWNUM with query...... \

# For Example:- 
# when asked What is the most common CBO type in district Vaishali?

# then query generated is....SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
# FROM M_CBO C
# INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
# WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
# AND C.RECORD_STATUS = 1
# GROUP BY TYPE_DESCRIPTION
# ORDER BY CBO_COUNT DESC
# WHERE ROWNUM <= 5...which is wrong you can clearly see that ROWNUM has been used directly with query and also ROWNUM is not required here \

# The right query is...SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
#                         FROM M_CBO C
#                         INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
#                         WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
#                         AND C.RECORD_STATUS = 1
#                         GROUP BY TYPE_DESCRIPTION
#                         ORDER BY CBO_COUNT DESC

# fOR eXAMPLE:-
# User Question:-give me count of panchayat wise shg from patna district?
# The Query you generated is:-SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
#                         FROM m_cbo c
#                         INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
#                         INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
#                         INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
#                         INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID
#                         WHERE upper(t.TYPE_SHORT_NAME) = 'SHG'
#                         AND upper(d.DISTRICT_NAME) = 'PATNA'
#                         AND c.record_status = 1
#                         GROUP BY p.PANCHAYAT_NAME
#                         ORDER BY shg_count DESC
#                         LIMIT 5...here you can clearly see that in (INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID) there should not be join between m_panchayat and m_cbo table on panchayat_id as m_cbo doesnot contains panchayat_id \

# The right Query is:-   SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
# FROM m_cbo c
# INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
# INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
# INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
# INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
# WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
# AND upper(d.DISTRICT_NAME) = 'PATNA'
# AND c.record_status = 1
# GROUP BY p.PANCHAYAT_NAME
# ORDER BY shg_count DESC...here you can clearly see as panchayat_id was not present in m_cbo so i searched which columns are common in m_cbo and m_panchayat and foun there was district_id and block_id but i made join on block_id like this (INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID) \

# For last 3 months
# CURRENT_DATE - INTERVAL '3 MONTH'
# for last 2 months
# CURRENT_DATE - INTERVAL '2 MONTH'

# for example:
# if the question is "total count of cbo formed in sheohar district in last 3 months?" \

# the query should be

# SELECT COUNT(c.CBO_ID) AS cbo_count
# FROM m_cbo c
# INNER JOIN m_district d ON c.district_id = d.district_id
# WHERE upper(d.district_name) = 'SHEOHAR'
# AND c.formation_date >= CURRENT_DATE - INTERVAL '3 MONTH'
# AND c.record_status = 1........you can clearly see that it is using CURRENT_DATE - INTERVAL '3 MONTH' to extract the last 3 months information..you have to use this method whenever asked about last months question \

# and so on \

# Some more examples:-

# question:-What is the count of all members across SHGs, VOs and CLFs in district Patna?", \

# sql query:- SELECT
#     SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
#     SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'VO') THEN 1 ELSE 0 END) AS vo_count,
#     SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'CLF') THEN 1 ELSE 0 END) AS clf_count
# FROM m_cbo c
# WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
# AND c.record_status = 1


# If you are confident that the generated SQL query is correct, please return the same query as it is...only return the query no statement or anything. 
# If there are mistakes or if joins or other operations are not performed correctly, make the necessary changes and return the accurate SQL query.
#  Pay particular attention to ensuring that joins are performed on relevant columns present in the respective tables. 
# Your optimized response should include the corrected SQL query, if necessary, to retrieve the desired information from the database.""")


        
#             print(mid_query)
#             print("-"*20)
#             print()
#             print()

        # except Exception as e:
        #      print(e)
        
        final_query=llm2(f"""This is a postgres sql query {query} which is going to be executed against this question {question}... 
            Your task is to Only return query, remove eveything from query at the begining or the end, don't return ```sql
                         
            For example: 
            If query generated is like this... 

            ```sql
            select count(distinct cbo_id) as total_cbo from m_cbo
            ``` 

            then you should return 

            select count(distinct cbo_id) as total_cbo from m_cbo 

            Another example:
            If query generated is like this... 

            ```sql
            SELECT COUNT(a.clf_id) AS clf_count
            FROM clf_masik_grading a
            WHERE a.year = 2023 and a.month_name = 'Dec' AND a.final_grade = 'A'

            then you should return 

            SELECT COUNT(a.clf_id) AS clf_count
            FROM clf_masik_grading a
            WHERE a.year = 2023 and a.month_name = 'Dec' AND a.final_grade = 'A'
            """)
        
        print(final_query)
        

        #print(db.run(final_query))
        
        response = llm2(f"""this is user question {question} and this is the answer {db.run(final_query)}....combine both to give a natural language answer...this is very important to include only this value {db.run(final_query)} in your answer \ 
        .....answer in pointwise....your final answer must include the values of {db.run(final_query)} \ 
        Remember that vo means village organisation,shg means self help group,cbo means community based organisation and clf means cluster level federation  \
                    Pay attention to not add anything from your side in answer.. just give simple natural language answer including this value {db.run(final_query)}. 
                
                Once you give the answer the based on user question suggest five more similar questions like this....{question}""")
        print(response)

        
        print(db.run(final_query))

        print("-"*20)

        cursor = connection.cursor()
       
            
        cursor.execute(final_query)

    
    
    
       
        return jsonify({'response': response})
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

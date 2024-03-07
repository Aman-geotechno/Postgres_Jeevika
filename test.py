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


db = SQLDatabase.from_uri(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",include_tables=["m_cbo","m_cbo_type","m_cbo_member","m_cbo_shg_member","t_cbo_appl_mapping","t_cbo_loan_register","t_acc_voucher","t_bulk_bank_acc","m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
"m_farmer_pest_management", "mp_cbo_member","m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology"])

print(db.dialect)
print(db.get_usable_table_names())

llm4= ChatGoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyBtNpUSSM6QHsq2QrkUtvcwM-0Hp3gXY_Q',convert_system_message_to_human=True, temperature=0)


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


table_names = "\n".join(db.get_usable_table_names())
system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_names}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
table_chain = create_extraction_chain_pydantic(Table, llm4, system_message=system)
print(table_chain.invoke({"input": "no of shg in patna district panchayat wise?"}))

system = """Return the names of the SQL tables that are relevant to the user question. \
The tables are:

CBO
Farmer"""
category_chain = create_extraction_chain_pydantic(Table, llm4, system_message=system)
print(category_chain.invoke({"input": "total farmers count"}))
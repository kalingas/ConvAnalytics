# SQL Database Agent
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_openai import AzureChatOpenAI
from langchain.llms import AzureOpenAI

import openai
import dotenv
dotenv.load_dotenv()
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")

llm = AzureChatOpenAI(temperature=0.7, model="gpt-4-turbo", api_key=openai.api_key)
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS
)
print(agent.invoke("How many tables are there in the database?"))
#print(agent.invoke("Can you list the all the tables?"))
#print(agent.invoke("Show the columns of each table"))

# Pandas Dataframe Agent
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
df = pd.read_csv("titanic.csv")
agent = create_pandas_dataframe_agent(
    AzureChatOpenAI(temperature=0, model="gpt-4-turbo", api_key=openai.api_key),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)
agent.invoke("how many rows are there?")
agent.invoke("how many people have more than 3 siblings")
agent.invoke("whats the square root of the average age?")

# Pandas AI
from pandasai import SmartDataframe
import pandas as pd
df = pd.DataFrame({
    "country": [
        "United States",
        "United Kingdom",
        "France",
        "Germany",
        "Italy",
        "Spain",
        "Canada",
        "Australia",
        "Japan",
        "China",
    ],
    "gdp": [
        19294482071552,
        2891615567872,
        2411255037952,
        3435817336832,
        1745433788416,
        1181205135360,
        1607402389504,
        1490967855104,
        4380756541440,
        14631844184064,
    ],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12],
})
from pandasai.llm import AzureOpenAI
llm = AzureOpenAI(temperature=0.7, model="gpt-4-turbo", api_key=openai.api_key, deployment_name=openai.deployment_name)
sdf = SmartDataframe(df, config={"llm": llm})
sdf[sdf['country'] == 'United States']
sdf.chat("Return the top 5 countries by GDP")
sdf.chat("What's the sum of the gdp of the 2 unhappiest countries?")
print(sdf.last_code_generated)
sdf.chat("Plot a chart of the gdp by country");
sdf.plot_bar_chart(x="country", y="gdp")
sdf.plot_pie_chart(labels="country", values="gdp")

from pandasai import SmartDatalake
employees_df = pd.DataFrame(
    {
        "EmployeeID": [1, 2, 3, 4, 5],
        "Name": ["John", "Emma", "Liam", "Olivia", "William"],
        "Department": ["HR", "Sales", "IT", "Marketing", "Finance"],
    }
)
salaries_df = pd.DataFrame(
    {
        "EmployeeID": [1, 2, 3, 4, 5],
        "Salary": [5000, 6000, 4500, 7000, 5500],
    }
)
lake = SmartDatalake(
    [employees_df, salaries_df],
    config={"llm": llm}
)
lake.chat("Who gets paid the most?")
print(lake.last_code_executed)

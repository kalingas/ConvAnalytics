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

# Pandas Dataframe Agent
import pandas as pd
from pandasai import SmartDataframe
from langchain_experimental.agents import create_pandas_dataframe_agent

from pandasai.llm import AzureOpenAI
llm = AzureOpenAI(temperature=0.7, model="gpt-4-turbo", api_key=openai.api_key, deployment_name=openai.deployment_name)
# df = pd.read_csv("titanic.csv")
df = pd.read_csv("SF_salary_data_gender.csv")
# agent = create_pandas_dataframe_agent(
#     AzureChatOpenAI(temperature=0, model="gpt-4-turbo", api_key=openai.api_key),
#     df,
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS,
# )
# agent.invoke("Frame 20 complex analytical questions from this dataset")
# agent.invoke("how many rows are there?")
# agent.invoke("how many people have more than 3 siblings")
# agent.invoke("whats the square root of the average age?")

sdf = SmartDataframe(df, config={"llm": llm})
sdf.chat("What is the average BasePay for all employees across all years?")
sdf.chat("Which year had the highest total OvertimePay, and which employee received the most in that year?")
sdf.chat("How has the average TotalPayBenefits changed over the years?")
sdf.chat("What is the correlation between BasePay and OvertimePay?")
sdf.chat("Can we predict TotalPay based on BasePay, OvertimePay, and OtherPay using a linear regression model?")
sdf.chat("What are the top 5 job titles with the highest average TotalPay?")
sdf.chat("Is there a significant difference in average pay between genders?")
sdf.chat("Which job titles have the highest incidence of overtime (as a percentage of BasePay)?")
sdf.chat("What is the distribution of TotalPayBenefits across different job titles?")
sdf.chat("How many unique job titles are there in the dataset, and which ones have only one employee?")
sdf.chat("What is the average Benefits amount per year, and how does it compare to the average OtherPay?")
sdf.chat("Identify the top 10 employees with the highest TotalPayBenefits to BasePay ratio.")
sdf.chat("What is the trend of average BasePay for the job title 'general manager-metropolitan transit authority' over the years?")
sdf.chat("Are there any outliers in terms of TotalPay, and can we identify any patterns among them?")
sdf.chat("What percentage of employees have OvertimePay that is greater than their BasePay?")
sdf.chat("How does the average TotalPay compare between employees with and without recorded Benefits?")
sdf.chat("What is the job title with the highest average OvertimePay, and how does it compare to the average for all job titles?")
sdf.chat("Can we cluster job titles based on pay components (BasePay, OvertimePay, OtherPay, Benefits) to identify similar compensation structures?")
sdf.chat("What is the gender pay gap within the top 10 most common job titles in the dataset?")
sdf.chat("For each year, which agency has the highest average TotalPay, and how does it vary across agencies?")

# sdf.chat("how many rows are there?")
# sdf.chat("how many people have more than 3 siblings")
# sdf.chat("whats the square root of the average age?")

# sdf[sdf['country'] == 'United States']
# sdf.chat("Return the top 5 countries by GDP")
# sdf.chat("What's the sum of the gdp of the 2 unhappiest countries?")
# print(sdf.last_code_generated)
# sdf.chat("Plot a chart of the gdp by country");
# sdf.plot_bar_chart(x="country", y="gdp")
# sdf.plot_pie_chart(labels="country", values="gdp")

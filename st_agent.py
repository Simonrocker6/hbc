# Import Azure OpenAI
from langchain.llms import AzureOpenAI
from langchain.agents import create_csv_agent
# from langchain.chat_models import AzureChatOpenAI
import os
import pandas as pd

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "4af4f76a6fc8417993842838f6081555"
os.environ["OPENAI_API_BASE"] = "https://oh-ai-openai-scu.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"

def create_agent(csv_file: str):
    """
    Return an agent that can access and use the llm, taking file name as args
    """

    llm = AzureOpenAI(
        temperature=0.0,
        openai_api_type="azure",
        deployment_name="gpt-35-turbo", 
        model_name="gpt-35-turbo")
    agent = create_csv_agent(llm, csv_file, verbose=True, max_iterations=100, max_execution_time=200)
    return agent

# agent = create_agent('./SAheart.data.csv')

def query_agent(agent, query):
    """
    Query an agent and return response with specified schema for streamlit to demo.
    """
    prompt1 = (
    """
        For the following query, if it requires drawing a table, reply as follows:
        {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

        If the query requires creating a bar chart, reply as follows:
        {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        If the query requires creating a line chart, reply as follows:
        {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        There can only be two types of chart, "bar" and "line".

        If it is just asking a question that requires neither, reply as follows:
        {"answer": "answer"}
        Example:
        {"answer": "The title with the highest rating is 'Gilead'"}

        If you do not know the answer, reply as follows:
        {"answer": "I do not know."}

        Return all output as a string.

        All strings in "columns" list and data list, should be in double quotes,

        For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

        Lets think step by step.

        Below is the query.
        Query: 
        """
    + query
    )

    prompt2 = (
        """
            Let's decode the way to respond to the queries. The responses depend on the type of information requested in the query. 

            1. If the query requires a table, format your answer like this:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            2. For a bar chart, respond like this:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            3. If a line chart is more appropriate, your reply should look like this:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            Note: We only accommodate two types of charts: "bar" and "line".

            4. For a plain question that doesn't need a chart or table, your response should be:
            {"answer": "Your answer goes here"}

            For example:
            {"answer": "The Product with the highest Orders is '15143Exfo'"}

            5. If the answer is not known or available, respond with:
            {"answer": "I do not know."}

            Return all output as a string. Remember to encase all strings in the "columns" list and data list in double quotes. 
            For example: {"columns": ["Products", "Orders"], "data": [["51993Masc", 191], ["49631Foun", 152]]}

            Now, let's tackle the query step by step. Here's the query for you to work on: 
            """
        + query
    )
    
    print('promts:')
    print(prompt2)

    response = agent.run(prompt2)
    return response.__str__()


    

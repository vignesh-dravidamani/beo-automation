from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import SimpleSequentialChain
from langchain.chains import LLMChain
from prompt import zone_prompt
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

load_dotenv()
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)


def query_ai(menu_items):
    zone_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=['menu_items'], template=zone_prompt))
    seq_chain = SimpleSequentialChain(chains=[zone_chain], strip_outputs=True, verbose=False)
    answer = seq_chain.run(menu_items)
    print("Answer from LLM is\n" + answer)
    return answer


def query_sql_db(db_engine, menu_items, llm):
    db = SQLDatabase(db_engine)
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_toolkit.get_tools()
    sqldb_agent = create_sql_agent(
        llm=llm,
        toolkit=sql_toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False
    )
    return sqldb_agent.run(PromptTemplate(input_variables=[menu_items], template=zone_prompt))

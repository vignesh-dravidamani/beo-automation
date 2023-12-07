from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from sqlalchemy import insert, Table, MetaData, Column, String, create_engine


def rdb_insert(db_engine, recommend_kitchen_zone_map):
    db_engine = create_engine('postgresql://postgres:passme@localhost/postgres')
    zone_table = Table(
        "zone",
        MetaData(),
        Column('menu_item', String),
        Column('zone', String)
    )
    for key in recommend_kitchen_zone_map:  # Todo: explore bulk insert for performance
        stmt = insert(zone_table).values(menu_item=key, zone=recommend_kitchen_zone_map[key])
        with db_engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()


def vdb_insert():
    vector_db = FAISS.from_texts(["vignesh is cool", "vignesh likes music", "vignesh is smart", "vignesh is funny"],
                                 embedding=OpenAIEmbeddings())
    retriever = vector_db.as_retriever()
    answer = retriever.get_relevant_documents("what does babu likes to do?")
    print(answer)

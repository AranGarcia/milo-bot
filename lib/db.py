# PostgreSQL
import psycopg2


class PostgresClient:
    con = None

    @classmethod
    def __initiate_client(cls):
        cls.con = psycopg2.connect(
            dbname="knowledgebase",
            user="kbadmin",
            password="kbadmin",
            host="localhost",
            port=65432,
        )

    @classmethod
    def query(cls, str_query, args=[]):
        cls.__initiate_client()
        cur = cls.con.cursor()
        cur.execute(str_query, args)
        cls.con.commit()
        cls.con.close()


def create_legal_document(doc_name):
    PostgresClient.query(
        """
        INSERT INTO documento
        VALUES(%s);
        """,
        [doc_name],
    )


def create_structural_division(id_level, id_document, enumeration, text):
    PostgresClient.query(
        """
        INSERT INTO division_estructural(
            id_nivel, id_documento, texto, numeracion
        )
        VALUES(%s,%s,%s,%s);
        """,
        [id_level, id_document, text, enumeration],
    )

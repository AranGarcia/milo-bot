# PostgreSQL
import psycopg2


class PostgresClient:
    con = None
    host = "localhost"
    port = 5432

    @classmethod
    def __initiate_client(cls):
        cls.con = psycopg2.connect(
            dbname="knowledgebase",
            user="kbadmin",
            password="kbadmin",
            host=cls.host,
            port=cls.port,
        )

    @classmethod
    def query(cls, str_query, args=[]):
        cls.__initiate_client()
        cur = cls.con.cursor()
        cur.execute(str_query, args)
        cls.con.commit()
        cls.con.close()

    @classmethod
    def query_with_result(cls, str_query, args=[]):
        cls.__initiate_client()
        cur = cls.con.cursor()
        cur.execute(str_query, args)
        res = cur.fetchone()
        cls.con.commit()
        cls.con.close()
        return res


def create_legal_document(doc_name):
    PostgresClient.query(
        """
        INSERT INTO documento
        VALUES(%s);
        """,
        [doc_name],
    )


def create_structural_division(id_level, id_document, enumeration, text):
    result = PostgresClient.query_with_result(
        """
        INSERT INTO division_estructural(
            id_nivel, id_documento, texto, numeracion
        )
        VALUES(%s,%s,%s,%s)
        RETURNING id;
        """,
        [id_level, id_document, text, enumeration],
    )

    if result is None:
        return None
    else:
        return result[0]


def create_structural_division_words(id_str_div, id_cl_w):
    PostgresClient.query(
        """
        INSERT INTO palabra_division_estructural(
            id_division_estructural, id_cluster_palabra
        )
        VALUES(%s, %s)
        """,
        [id_str_div, id_cl_w],
    )


def create_word_cluster(vector):
    PostgresClient.query(
        """
        INSERT INTO cluster_palabra(vector)
        VALUES(%s);
        """,
        ["{" + ",".join(str(v) for v in vector) + "}"],
    )


def retrieve_structural_division(document, id_level, enumeration):
    if not isinstance(document, str) or not isinstance(id_level, str):
        raise ValueError("document and id_level must be string")
    if not isinstance(enumeration, int):
        raise ValueError("enumeration must be int")
    res = PostgresClient.query_with_result(
        """
        SELECT id, id_nivel, id_documento, texto, numeracion, vector
        FROM division_estructural
        WHERE id_documento = %s AND id_nivel = %s and numeracion = %s;
        """,
        [document, id_level, enumeration],
    )

    if res is None:
        raise ValueError("empty")
    else:
        return res

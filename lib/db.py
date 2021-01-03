from typing import Optional, Tuple

# PostgreSQL
import numpy as np
import psycopg2


class PostgresClient:
    con = None
    host = "localhost"
    port = 65432

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
    def query_with_result(cls, str_query, args=tuple()):
        cls.__initiate_client()
        cur = cls.con.cursor()
        cur.execute(str_query, args)
        res = cur.fetchone()
        cls.con.commit()
        cls.con.close()
        return res

    @classmethod
    def query_all(cls, str_query, args=[]):
        cls.__initiate_client()
        cur = cls.con.cursor()
        cur.execute(str_query, args)
        res = cur.fetchall()
        cls.con.commit()
        cls.con.close()
        return res


def lst2pgarr(arr):
    return "{" + ",".join(str(i) for i in arr) + "}"


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
    if id_str_div is None:
        raise ValueError("id_division_estructural cannot be null")
    if id_cl_w is None:
        raise ValueError("id_palabra cannot be null")
    PostgresClient.query(
        """
        INSERT INTO palabra_division_estructural(
            id_division_estructural, id_palabra
        )
        VALUES(%s, %s)
        """,
        [id_str_div, id_cl_w],
    )


def create_word(text, vector) -> Optional[int]:
    """Creates an instance in the table `palabra` and returns the created ID (indice)."""
    try:
        res = PostgresClient.query_with_result(
            """
            INSERT INTO palabra(texto, vector)
            VALUES(%s, %s)
            RETURNING indice;
            """,
            [text, "{" + ",".join(str(v) for v in vector) + "}"],
        )
    except psycopg2.errors.UniqueViolation:
        return None

    return res[0]


def retrieve_structural_division(document, id_level, enumeration):
    if not isinstance(document, str) or not isinstance(id_level, str):
        raise ValueError("document and id_level must be string")
    if not isinstance(enumeration, int):
        raise ValueError("enumeration must be int")
    res = PostgresClient.query_with_result(
        """
        SELECT id, id_nivel, id_documento, texto, numeracion, vector
        FROM division_estructural
        WHERE id_documento = %s AND id_nivel = %s AND numeracion = %s;
        """,
        [document, id_level, enumeration],
    )

    return res


def retrieve_struct_div_by_ids(
    sd_ids: Tuple[int],
    fields="id, id_nivel, id_documento, texto, numeracion, vector",
):
    """Retrieve Struct Divs instances by IDs from the DB."""
    res = PostgresClient.query_all(
        f"""
        SELECT {fields}
        FROM division_estructural
        WHERE id IN %s AND id_nivel = 'articulo';
        """,
        (sd_ids,),
    )

    return res


def retrieve_words() -> Tuple[np.ndarray, np.ndarray]:
    """Returns two arrays: one with the vectors and another with the indexes."""
    res = PostgresClient.query_all(
        """
        SELECT indice, texto, vector
        FROM palabra;
        """
    )

    # temp = sorted(res, key=lambda x: x[0])
    return (
        np.array([i[0] for i in res]),
        np.array([i[1] for i in res]),
        np.array([i[2] for i in res]),
    )


def retrieve_struct_div_words():
    """
    Retrieves all instances from the table `palabra_division_estructural` which is used to build
    the binary vector representation for a text.
    """
    res = PostgresClient.query_all(
        """
        SELECT id_division_estructural, id_cluster_palabra
        FROM palabra_division_estructural;
        """
    )

    return res


def retrieve_struct_div_by_word_id(
    word_ids: Tuple[str], fields: str = "id, id_documento, id_nivel, numeracion, texto"
):
    res = PostgresClient.query_all(
        f"""
        SELECT {fields}
        FROM division_estructural
        WHERE id IN (
                SELECT id_division_estructural
                FROM palabra_division_estructural
                WHERE id_palabra in %s
        )
        """,
        (word_ids,),
    )

    return res


def retrieve_clusters():
    """Retrieves all instances from the table `cluster_palabra`."""
    res = PostgresClient.query_all(
        """
        SELECT indice, vector
        FROM cluster_palabra;
        """
    )
    return res


# Utility functions
def retrieve_amount_of_clusters():
    """
    Returns the amount of instances in the `
    """
    res = PostgresClient.query_with_result(
        """
        SELECT COUNT(*)
        FROM cluster_palabra;
        """
    )

    return res[0]


def retrieve_amount_of_struct_divs():
    """
    Returns the amount of instances in the `
    """
    res = PostgresClient.query_with_result(
        """
        SELECT COUNT(id)
        FROM division_estructural;
        """
    )

    return res[0]

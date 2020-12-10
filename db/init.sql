/* Knowledge Base DB init
 * This script defines the table attributes and loads catalog data.
 */
CREATE TABLE documento(
    nombre_division VARCHAR(50) PRIMARY KEY
);

CREATE TABLE nivel_division(
    nombre_division VARCHAR(20) PRIMARY KEY
);

CREATE TABLE division_estructural(
    id	         SERIAL PRIMARY KEY,
    id_nivel     VARCHAR(50),
    id_documento VARCHAR(50),
    texto        TEXT,
    numeracion   INTEGER,
    vector       INTEGER[],
    CONSTRAINT fk_documento
        FOREIGN KEY(id_documento)
        REFERENCES documento(nombre_division),
    CONSTRAINT fk_nivel_division
        FOREIGN KEY(id_nivel)
        REFERENCES nivel_division(nombre_division)
);

CREATE TABLE cluster_palabra(
    id     SERIAL PRIMARY KEY,
    vector DOUBLE PRECISION[]
);

CREATE TABLE similitud(
    cluster_1 SERIAL,
    cluster_2 SERIAL,
    medida_similitud DOUBLE PRECISION,
    CONSTRAINT fk_cluster_palabra_1
        FOREIGN KEY(cluster_1)
        REFERENCES cluster_palabra(id),
    CONSTRAINT fk_cluster_palabra_2
        FOREIGN KEY(cluster_2)
        REFERENCES cluster_palabra(id)
);

CREATE TABLE palabra_division_estructural(
    id_division_estructural SERIAL,
    id_cluster_palabra      SERIAL,
    CONSTRAINT pk_palabras_division_estructural
        PRIMARY KEY(id_division_estructural, id_cluster_palabra),
    CONSTRAINT fk_division_estrucutral
        FOREIGN KEY(id_division_estructural)
        REFERENCES division_estructural(id),
    CONSTRAINT fk_cluster_palabra
        FOREIGN KEY(id_cluster_palabra)
        REFERENCES cluster_palabra(id)
);

-- The only catalog data to populate in the DB
INSERT INTO nivel_division VALUES
    ('capitulo'),
    ('seccion'),
    ('titulo'),
    ('artiuclo');
/* Knowledge Base DB init
 * This script defines the table attributes and loads catalog data.
 */
CREATE TABLE documento(
    nombre_documento VARCHAR(50) PRIMARY KEY
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
    -- vector       INTEGER[],
    CONSTRAINT fk_documento
        FOREIGN KEY(id_documento)
        REFERENCES documento(nombre_documento),
    CONSTRAINT fk_nivel_division
        FOREIGN KEY(id_nivel)
        REFERENCES nivel_division(nombre_division)
);

CREATE TABLE palabra(
    indice     SERIAL PRIMARY KEY,
    vector     DOUBLE PRECISION[],
    texto      TEXT UNIQUE
);

CREATE TABLE palabra_division_estructural(
    id                      SERIAL PRIMARY KEY,
    id_division_estructural SERIAL,
    id_palabra              SERIAL,
    CONSTRAINT fk_division_estrucutral
        FOREIGN KEY(id_division_estructural)
        REFERENCES division_estructural(id),
    CONSTRAINT fk_palabra
        FOREIGN KEY(id_palabra)
        REFERENCES palabra(indice)
);

-- The only catalog data to populate in the DB
INSERT INTO nivel_division VALUES
    ('capitulo'),
    ('seccion'),
    ('titulo'),
    ('articulo');

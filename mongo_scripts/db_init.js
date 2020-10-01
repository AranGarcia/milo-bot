// Value in Compass is mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false
var db = connect("mongodb://localhost:27017");

db = db.getSiblingDB("LegalDocs");

// Apparently, to create a unique field, one must use create Index.
db.createCollection("Documento",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["nombre_documento"],
                properties: {
                    nombre_documento: {
                        bsonType: "string",
                        description: "must be a string and is required."
                    }

                }
            }
        }
    }
);

db.createCollection("NivelDivision",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["nombre_division"],
                properties: {
                    nombre_division: {
                        bsonType: "string",
                        description: "must be a string and is required."
                    }

                }
            }
        }
    }
);

db.createCollection("DivisionEstructural",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["id_nivel", "id_document", "texto", "numeracion", "vector"],
                properties: {
                    id_nivel: {
                        bsonType: "objectId",
                        description: "must be an ObjectId and is required."
                    },
                    id_documento: {
                        bsonType: "objectId",
                        description: "must be an ObjectId and is required."
                    },
                    texto: {
                        bsonType: "string",
                        description: "must be a string and is required."
                    },
                    numeracion: {
                        bsonType: "int",
                        minimum: 1,
                        description: "must be an integer greater than 0 and is required."
                    },
                    vector: {
                        bsonType: ["array"],
                        items: {
                            bsonType: "int",
                            description: "must be an array of integers and is required."
                        }
                    }
                }
            }
        }
    }
);

db.createCollection("ClusterPalabra",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["vector"],
                properties: {
                    vector: {
                        bsonType: ["array"],
                        items: {
                            bsonType: "double",
                            description: "must be an array of double and is required."
                        }
                    }
                }
            }
        }
    }
);

db.createCollection("PalabrasDivisionEstructural",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["id_division_estructural", "id_cluster_palabra"],
                properties: {
                    id_division_estructural: {
                        bsonType: "objectId",
                        description: "must be an ObjectID and is required."
                    },
                    id_cluster_palabra: {
                        bsonType: "objectId",
                        description: "must be an ObjectID and is required."
                    }
                }
            }
        }
    }
);

db.createCollection("Similitud",
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["id_cluster_1", "id_cluster_2", "medida_similitud"],
                properties: {
                    cluster_1: {
                        bsonType: "objectId",
                        description: "must be an ObjectId and is required."
                    },
                    cluster_2: {
                        bsonType: "objectId",
                        description: "must be an ObjectId and is required."
                    },
                    similitud: {
                        bsonType: "double",
                        description: "must be a double "
                    }
                }
            }
        }
    }
);

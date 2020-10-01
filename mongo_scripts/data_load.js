// Value in Compass is mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false
var db = connect("mongodb://localhost:27017");

db = db.getSiblingDB("LegalDocs");

db.NivelDivision.insertMany([
    {nombre_division: "capitulo"},
    {nombre_division: "seccion"},
    {nombre_division: "titulo"},
    {nombre_division: "articulo"},
])
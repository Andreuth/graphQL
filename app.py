from flask import Flask
from graphene import ObjectType, String, Schema, Int, List, Field, Mutation
from flask_graphql import GraphQLView

libros = []

class Libro(ObjectType):
    id = Int()
    titulo = String()
    autor = String()

class Query(ObjectType):
    todos_libros = List(Libro)

    def resolve_todos_libros(root, info):
        return libros

class CrearLibro(Mutation):
    class Arguments:
        titulo = String(required=True)
        autor = String(required=True)

    libro = Field(lambda: Libro)

    def mutate(self, info, titulo, autor):
        nuevo_libro = {"id": len(libros) + 1, "titulo": titulo, "autor": autor}
        libros.append(nuevo_libro)
        return CrearLibro(libro=nuevo_libro)

class Mutation(ObjectType):
    crear_libro = CrearLibro.Field()

schema = Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run()

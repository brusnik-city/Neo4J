from .views import app
from .models import graph

graph.cypher.execute("CREATE  CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")
graph.cypher.execute("CREATE  CONSTRAINT ON (n:Post) ASSERT n.id IS UNIQUE")
graph.cypher.execute("CREATE  CONSTRAINT ON (n:Tag) ASSERT n.name IS UNIQUE")
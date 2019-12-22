from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid
import os

url = os.environ.get("GRAPHENEDB_URL", "http://localhost:7474")

graph = Graph(url + "/db/data/")

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node("User",username = self.username, password = bcrypt.encrypt(password))
            graph.create(user)
            return True
        return False

    def verify_password(self,password):
        user = self.find()
        if not user:
            return False
        return bcrypt.verify(password,user["password"])

    def add_place(self, placename, days, visited, tovisit):
        user = self.find()
        place = graph.merge_one("Place","name", placename)
        graph.create(place)
        if visited:
            relation = Relationship(user, "VISITED", place,days = days)
            graph.create_unique(relation)
        if tovisit:
            relation = Relationship(user, "WILL_VISIT", place, days = days)
            graph.create_unique(relation)

def all_places():
    query = " MATCH (p:Place) RETURN p"
    return graph.cypher.execute(query)
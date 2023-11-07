import random

def loyaltiesAtTime(families):
    loyalties = {}
    
    edges = []

    for family in families:
        addEdge = 1
        while addEdge == 1:
            connectedFamily = family
            while connectedFamily == family:
                connectedFamily = families[random.randrange(0, len(families))]
            edges.append([family, connectedFamily])
            addEdge = random.randrange(0, 1)

    for family in families:
        loyalFamilies = []
        for edge in edges:
            if family in edge:
                loyalFamilies.append([x for x in edge if family != x][0])
        loyalties[family] = loyalFamilies

    return loyalties

class Entity:
    def __init__(self, name):
        self.name = name
        self.relationships = []

    def __str__(self):
        return self.name
    
    def append(self, other):
        self.relationships.append(other)

    def relationships(self):
        return self.relationships

def mapRelationships(entities):
    for entity in entities:
        for i in range(random.randrange(0, len(entities) // 8)):
            connectedEntity = entity
            while connectedEntity == entity:
                connectedEntity = entities[random.randrange(0, len(entities))]
            if connectedEntity not in entity.relationships:
                entity.append(connectedEntity)    
            
def main():
    entityNames = [
        "Veystdastithil",
        "Lemesulys",
        "Vui'Daros",
        "Ranyst",
        "Lemesyiros",
        "Auaramus",
        "Imalust",
        "Anasramust",
        "Beredysanast",
        "Lonascus",
        "Lemandusar",
        "Gahgullu",
        "Lemesoladys",
        "Barbos",
        "Iu'saralymon",
        "Vilianaryst",
        "Lemfrodys",
        "Gorros",
        "Feus"
    ]

    entities = []

    for entityName in entityNames:
        entities.append(Entity(entityName))

    timeline = []

    for i in range(10):
        currentRelationships = []
        mapRelationships(entities)
        for entity in entities:
            currentRelationships.append(entity)
        timeline.append(currentRelationships)

    for year, relationSet in enumerate(timeline):
        print(f'Year {year * 100}')
        print()
        for entity in relationSet:
            print(entity)
            for relatedEntity in entity.relationships:
                print(f'\t{relatedEntity}')
            print()
        print()

main()
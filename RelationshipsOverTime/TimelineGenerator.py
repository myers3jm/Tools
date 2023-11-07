import random
import copy

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
        if random.randint(0, 1) == 1:
            continue
        for i in range(random.randint(0, 5)):
            connectedEntity = entity
            while connectedEntity == entity:
                connectedEntity = entities[random.randrange(0, len(entities))]
            if connectedEntity not in entity.relationships:
                entity.append(connectedEntity)    
                connectedEntity.append(entity)
            
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
        "Gorros"
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
        timeline.append(copy.deepcopy(currentRelationships))
        for entity in entities:
            entity.relationships.clear()

    outfile = open('RelationshipsTimeline.md', 'w', encoding='utf-8')

    for year, relationSet in enumerate(timeline):
        outfile.write(f'# Year {(year + 1 ) * 100}')
        outfile.write('\n')
        for entity in relationSet:
            outfile.write(f'## {entity}\n')
            for relatedEntity in entity.relationships:
                outfile.write(f'{relatedEntity}\n')
                outfile.write('\n')
            outfile.write('\n')
        outfile.write('\n')

main()
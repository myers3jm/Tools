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

def main():
    families = [
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

    timeline = []

    for i in range(10):
        timeline.append(loyaltiesAtTime(families))

    for time in timeline:
        print(time['Veystdastithil'])

main()
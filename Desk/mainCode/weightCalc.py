#GCS

def weightCalc(gcsGraph, action, path):
    #행동에 따른 노드 가중치 부여
    for i in range(len(action)):
        x = path[i]
        y = path[i + 1]

        if(action[i] == 'GO'):
            gcsGraph[x][y] += 4
        elif(action[i] == 'TL' or action[i] == 'TR'):
            gcsGraph[x][y] += 5
        elif(action[i] == 'ER'):
            gcsGraph[x][y] += 10

        print("시작노드정보: ", path[i], "도착노드정보: ", path[i + 1], "가중치: ", gcsGraph[x][y])

    print(gcsGraph)

def weightReset(gcsGraph, action, path):
    #행동에 따른 노드 가중치 리셋
    for i in range(len(action)):
        x = path[i]
        y = path[i + 1]

        if(action[i] == 'GO'):
            gcsGraph[x][y] -= 4
        elif(action[i] == 'TL' or action[i] == 'TR'):
            gcsGraph[x][y] -= 5
        elif(action[i] == 'ER'):
            gcsGraph[x][y] -= 10

    print(gcsGraph)
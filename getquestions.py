with open('questoes.txt') as q:
    txt=q.read()
    questoes=txt.replace('\n','').split('$$')
    listquests=[]
    listresps= []
    for item in questoes:
        listquests.append(item.split('//')[0])
        listresps.append(tuple(item.split('//')[1].split(';;')))
    print (listquests,listresps)

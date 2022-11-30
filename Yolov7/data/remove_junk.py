import os 

# remove roboflow extra junk

count = 0
for i in sorted(os.listdir('cablev4_512/train/labels')):
    # if count >=3:
    #     count = 0
    count += 1
    if i[0] == '.':
        continue
    j = i.split('_')
    dict1 = {1:'a', 2:'b', 3:'c'}
    source = 'cablev4_512/train/labels/'+i
    dest = 'cablev4_512/train/labels/'+j[0]+"_"+str(count)+'.txt'
    os.rename(source, dest)
    
count = 0
for i in sorted(os.listdir('cablev4_512/train/images')):
    # if count >=3:
    #     count = 0
    count += 1
    if i[0] == '.':
        continue
    j = i.split('_')
    dict1 = {1:'a', 2:'b', 3:'c'}
    source = 'cablev4_512/train/images/'+i
    dest = 'cablev4_512/train/images/'+j[0]+"_"+str(count)+'.jpg'
    os.rename(source, dest)

valid_count = count
for i in sorted(os.listdir('cablev4_512/valid/labels')):
    if i[0] == '.':
        continue
    count+=1
    j = i.split('_')
    source = 'cablev4_512/valid/labels/'+i
    dest = 'cablev4_512/valid/labels/'+j[0]+"_"+str(count)+'.txt'
    os.rename(source, dest)
    
count = valid_count
for i in sorted(os.listdir('cablev4_512/valid/images')):
    if i[0] == '.':
        continue
    count += 1
    j = i.split('_')
    source = 'cablev4_512/valid/images/'+i
    dest = 'cablev4_512/valid/images/'+j[0]+"_"+str(count)+'.jpg'
    os.rename(source, dest)

test_count = count
for i in sorted(os.listdir('cablev4_512/test/labels')):
    if i[0] == '.':
        continue
    count += 1
    j = i.split('_')
    source = 'cablev4_512/test/labels/'+i
    dest = 'cablev4_512/test/labels/'+j[0]+"_"+str(count)+'.txt'
    os.rename(source, dest)
count = test_count
    
for i in sorted(os.listdir('cablev4_512/test/images')):
    if i[0] == '.':
        continue
    count += 1
    j = i.split('_')
    source = 'cablev4_512/test/images/'+i
    dest = 'cablev4_512/test/images/'+j[0]+"_"+str(count)+'.jpg'
    os.rename(source, dest)
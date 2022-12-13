import pandas as pd
df_lig1 = pd.read_csv('df_ligera1.csv')

df_lig2 = df_lig1
nombres = df_lig1['user_name']
unicos = df_lig1['user_name'].unique()
ids = [-1]*len(nombres)

for i in range(len(nombres)):
    j=-1
    while(nombres[i] != unicos[j]):
        j+=1
        if(j >= len(unicos)):
            break
    if(j == -1):
        j = len(unicos)
    ids[i] = j
    if(i%10000 == 0):
        print(i, "->", i/len(nombres)*100, "%")

df_lig1['id_user'] = ids

df_lig2.to_csv('df_ligera2.csv')
df_lig2
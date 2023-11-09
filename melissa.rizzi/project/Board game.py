import pandas as pd

bgg = pd.read_csv("\\Users\\melis\\Desktop\\progetto python\\bgg.csv")
bgg = bgg.dropna()
bgg = bgg.reset_index(drop = True)
avg = bgg.groupby(['game']).mean('rating')
count = bgg.groupby(['game']).count()
len = int(bgg.size/3)
c = len
bgg1 = bgg
for i in range (0, len):
    if bgg1.game.loc[i] != bgg1.game.loc[i+1]:
        for j in range (0,5):
            bgg1.loc[c] = [bgg1.game.loc[i],bgg1.title.loc[i], 5.5]
            c = c+1
avg_geek = bgg1.groupby(['game']).mean('rating')


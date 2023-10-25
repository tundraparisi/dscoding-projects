def convert(db, column):
    if column == 'Latitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'N':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'S':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    elif column == 'Longitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'E':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'W':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    return db


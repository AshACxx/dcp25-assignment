
def search(df, search_terms):
    '''function to return the title of a song (used for tkinter)'''
    df_3 = df[df["title"].str.contains(search_terms, case = False)]
    return df_3
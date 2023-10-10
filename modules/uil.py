import string, copy
import pandas as pd

def getEmptyData(rows=10,columns=4):

    colnames = list(string.ascii_lowercase[:columns])
    df = pd.DataFrame(index=range(rows),columns=colnames)
    return df
import base64
import io
import pandas as pd
from exceptions import FileNotSupported

def parseContents(contents, filename):
    contentType, contentString = contents.split(',')
    decoded = base64.b64decode(contentString)
    if filename.endswith('.csv'):
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    #elif filename.endswith('.xlsx') or filename.endswith('.xls'):
    #    return pd.read_excel(io.BytesIO(decoded))
    else:
        raise FileNotSupported('File not supported. Supported type: .csv')

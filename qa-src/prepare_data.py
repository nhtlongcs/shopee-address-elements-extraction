from sklearn.utils import shuffle
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from sklearn.model_selection import StratifiedKFold

tqdm.pandas()
def clean(df):
    return df

def read_data(path, negative=True):
    csv_path = Path(path)
    df = pd.read_csv(csv_path)
    df = clean(df)

    df['POI'] = df.progress_apply(lambda row: row['POI/street'].split('/')[0], axis=1)
    df['street'] = df.progress_apply(lambda row: row['POI/street'].split('/')[-1], axis=1)
    
    df_poi = df.copy() 
    df_street = df.copy() 
    df_poi['question'] = 'minat?'
    df_street['question'] = 'jalan?'

    if not negative:
        df_poi = df_poi[df_poi.POI != ''].reset_index(drop=True)
        df_street = df_street[df_street.street != ''].reset_index(drop=True)

    df_poi['start'] = df_poi.progress_apply(lambda row: \
        row['raw_address'].find(row['POI']) , axis=1)
    df_poi = df_poi[df_poi.start != -1].reset_index(drop=True)

    

    df_street['start'] = df_street.progress_apply(lambda row: \
        row['raw_address'].find(row['street']) , axis=1)
    df_street = df_street[df_street.start != -1].reset_index(drop=True)
    

    df_poi['POI'] = df_poi.progress_apply(lambda row: \
        {'text':[row['POI']],'answer_start':[row.start]}, axis=1)
    df_poi['lbl'] = df_poi.apply(lambda row: 0 if row.POI == '' else 1 , axis=1)

    df_street['street'] = df_street.progress_apply(lambda row: \
        {'text':[row['street']],'answer_start':[row.start]}, axis=1)
    df_street['lbl'] = df_street.apply(lambda row: 2 if row.street == '' else 3 , axis=1)

    result = pd.DataFrame()
    result['answers']   =   \
        df_poi.POI.values.tolist() + df_street.street.values.tolist()
    result['question'] =   \
        df_poi.question.values.tolist() + df_street.question.values.tolist()
    result['lbl'] = df_poi.lbl.values.tolist() + df_street.lbl.values.tolist()
    result['context']  =   \
        df_poi.raw_address.values.tolist() + df_street.raw_address.values.tolist()
    
    result = shuffle(result)
    result["id"] = result.index + 1
    return result


data = read_data('train.csv', negative=False)
skf = StratifiedKFold(n_splits=5)
X = data.drop('lbl', axis = 1)
y = data.lbl

for fold, (train_index, test_index) in enumerate(skf.split(X, y)):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    print(len(X_train),len(X_test))
    X_train.to_csv(f'train_{fold}.csv', index=False)
    X_test.to_csv(f'val_{fold}.csv', index=False)
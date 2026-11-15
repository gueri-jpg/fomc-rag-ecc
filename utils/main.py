from TxtExtraction.Pdf2Txt import EmbedChunks
import os
from database.StockVectors import store_vector
from dotenv import load_dotenv
load_dotenv()

mpath = 'utils/TxtExtraction/TextsData/minutes'
spath = 'utils/TxtExtraction/TextsData/statements'
minutes = [os.path.join(mpath,f) for f in os.listdir(mpath) if f.endswith('.pdf')]
statements = [os.path.join(spath,f) for f in os.listdir(spath) if f.endswith('.pdf')]

minutes = sorted(minutes)
statements = sorted(statements)

minutes = [{'file':m,
            'year':m.split('/')[-1].split('.')[0][-8:-4],
            'month':m.split('/')[-1].split('.')[0][-4:-2]} for m in minutes]

statements = [{'file':m,
            'year':m.split('/')[-1].split('a1.')[0][-8:-4],
            'month':m.split('/')[-1].split('a1.')[0][-4:-2]} for m in statements]

j = 0
files = []
print(len(statements))
print(len(minutes))
for s in statements:
    if j < len(minutes):
        if s['year'] == minutes[j]['year'] and s['month'] == minutes[j]['month']:
            files.append(s['file'])
            files.append(minutes[j]['file'])
            j += 1
        else :
            files.append(s['file'])
    else:
        files.append(s['file'])

print(len(files))

end = [0,10,19,30,41,49,61,70,79,84,93]
embeddings, textChunks = [], []

for i,e in enumerate(end[1:]):
    preprocessed_tokens = EmbedChunks(files[end[i]:end[i+1]], chunksize=128)
    #embeddings += preprocessed_tokens[0].tolist()
    #textChunks += preprocessed_tokens[1]
    store_vector(preprocessed_tokens[1], preprocessed_tokens[0].tolist(), os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_HOST"), os.getenv("DB_PASSWORD"), os.getenv("DB_PORT"))
    del preprocessed_tokens
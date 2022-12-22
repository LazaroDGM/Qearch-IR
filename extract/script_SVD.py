import extract_lg
import fire

def extract(name_path, count_documents, k):
    A = extract_lg.create_numpy_lg(name_path + 'frec.json', count_documents)
    extract_lg.extract_Dk_Rq(A, k, name_path)

if __name__ == '__main__':
  fire.Fire(extract)
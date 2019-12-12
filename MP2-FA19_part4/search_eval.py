import math
import sys
import time
import metapy
import pytoml

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    # return metapy.index.OkapiBM25(k1=2,b=0.75,k3=200) #0.6112
    # return metapy.index.OkapiBM25(k1=2,b=0.75,k3=100) #0.6113
    # return metapy.index.OkapiBM25(k1=2,b=1,k3=0) #0.3418
    # return metapy.index.OkapiBM25(k1=1.5,b=0.75,k3=100) #0.6164
    # return metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=100) #0.6164
    # return metapy.index.OkapiBM25(k1=1,b=0.755,k3=100) #0.6198
    return metapy.index.OkapiBM25(k1=1,b=0.75,k3=100) #0.62 finally beat the baseline 5555555
    # return metapy.index.OkapiBM25(k1=0.8,b=0.75,k3=100) #0.6196
    # return metapy.index.OkapiBM25(k1=2.4,b=0.75,k3=0) #0.6096
    # return metapy.index.OkapiBM25(k1=2,b=0.75,k3=0) #0.612
    # return metapy.index.OkapiBM25(k1=10,b=0.75,k3=0) #0.5558
    # return metapy.index.OkapiBM25(k1=2,b=0.75,k3=-50) #0.6108
    # return metapy.index.OkapiBM25(k1=1.904,b=0.76,k3=500) #0.6105
    # return metapy.index.OkapiBM25(k1=2,b=0.76,k3=500) #0.6095
    # return metapy.index.DirichletPrior(206) #0.6063
    # return metapy.index.DirichletPrior(205) #0.6064
    # return metapy.index.DirichletPrior(204) #0.6063
    # return metapy.index.DirichletPrior(105) #0.5942
    # return metapy.index.JelinekMercer(0.64) #0.3264
    # return metapy.index.AbsoluteDiscount(0.7) #0.4581
    # return metapy.index.PivotedLength(0.347) 	#0.5222

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries

    print("NDCG@{}: {}".format(top_k, ndcg))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))

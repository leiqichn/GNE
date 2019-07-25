import numpy as np
from numba import jit

from sklearn.metrics import average_precision_score, roc_auc_score

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Evaluate ROC using predicted matrix
def evaluate_ROC_from_matrix(X_edges, y_true, matrix):
    y_predict = [sigmoid(matrix[int(edge[0]), int(edge[1])]) for edge in X_edges]
    roc = roc_auc_score(y_true, y_predict)
    if roc < 0.5:
        roc = 1 - roc
    pr = average_precision_score(y_true, y_predict)
    return roc, pr

# Load the embedding generated by other methods:LINE, Node2vec
def load_embedding(embedding_file, N, combineAttribute=False, datafile=None):
    f = open(embedding_file)
    i = 0
    line = f.readline()
    line = line.strip().split(' ')
    d = int(line[1])
    embeddings = np.random.randn(int(N), d)
    line = f.readline()
    while line:
        line = line.strip().split(' ')
        embeddings[int(line[0]),:] = line[1:]
        i = i + 1
        line = f.readline()
    f.close()
    if combineAttribute:
        data = load_datafile(datafile, N)
        # print(data.shape)
        temp = np.hstack((embeddings, data))
        # print(temp.shape)
        embeddings = temp
    return embeddings

# Load the expression data
def load_datafile(data_file, N):
    f = open(data_file)
    i = 0
    line = f.readline()
    line = line.strip().split(' ')
    d = len(line[1:])
    data = np.zeros([int(N), d])
    while line:
        # print(i)
        data[int(line[0]),:] = line[1:]
        i = i + 1
        line = f.readline()
        if i < N:
            line = line.strip().split(' ')
        else:
            break
    f.close()
    return data

@jit
def get_edge_embeddings(Embeddings, edge_list):
        embs = []
        for i in range(len(edge_list)):
            edge = np.array(edge_list)[i, :]
            node1 = int(edge[0])
            node2 = int(edge[1])
            emb1 = Embeddings[node1]
            emb2 = Embeddings[node2]
            edge_emb = np.multiply(emb1, emb2)
            embs.append(edge_emb)
        embs = np.array(embs)
        return embs

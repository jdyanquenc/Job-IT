import numpy as np

def precision_at_k(retrieved, relevant, k):
    if k == 0:
        return 0.0
    retrieved_k = retrieved[:k]
    return len([i for i in retrieved_k if i in relevant]) / k

def recall_at_k(retrieved, relevant, k):
    if len(relevant) == 0:
        return 0.0
    retrieved_k = retrieved[:k]
    return len([i for i in retrieved_k if i in relevant]) / len(relevant)

def apk(retrieved, relevant, k):
    """Average precision @ k for single query"""
    if len(relevant) == 0:
        return 0.0
    score = 0.0
    num_hits = 0.0
    for i, r in enumerate(retrieved[:k], start=1):
        if r in relevant:
            num_hits += 1.0
            score += num_hits / i
    return score / min(len(relevant), k)

def ndcg_at_k(retrieved, relevant_with_grades, k):
    """
    relevant_with_grades: dict or set with graded relevance {id: grade}
    For binary relevance pass grades of 1.
    """
    dcg = 0.0
    for i, r in enumerate(retrieved[:k], start=1):
        rel = relevant_with_grades.get(r, 0)
        if rel > 0:
            dcg += (2**rel - 1) / np.log2(i + 1)
    # ideal dcg
    ideal_rels = sorted(relevant_with_grades.values(), reverse=True)[:k]
    idcg = 0.0
    for i, rel in enumerate(ideal_rels, start=1):
        idcg += (2**rel - 1) / np.log2(i + 1)
    return dcg / idcg if idcg > 0 else 0.0

def mrr_single(retrieved, relevant):
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1.0 / i
    return 0.0

# evaluación global
def evaluate_faiss(faiss_index, queries_emb, ground_truth, ks=[1,5,10,20], topn=100):
    # ejecutar búsqueda
    D, I = faiss_index.search(queries_emb.astype(np.float32), topn)  # I shape (Q, topn)
    results = {}
    Q = I.shape[0]
    for k in ks:
        results[f'precision@{k}'] = 0.0
        results[f'recall@{k}'] = 0.0
        results[f'hit@{k}'] = 0.0
    results['MAP@k'] = 0.0
    results['MRR'] = 0.0
    results['NDCG@10'] = 0.0

    for q_idx in range(Q):
        retrieved = I[q_idx].tolist()
        relevant = ground_truth.get(q_idx, set())
        # metrics per k
        for k in ks:
            p = precision_at_k(retrieved, relevant, k)
            r = recall_at_k(retrieved, relevant, k)
            hit = 1.0 if len(set(retrieved[:k]).intersection(relevant)) > 0 else 0.0
            results[f'precision@{k}'] += p
            results[f'recall@{k}'] += r
            results[f'hit@{k}'] += hit

        results['MAP@k'] += apk(retrieved, relevant, k=topn)
        results['MRR'] += mrr_single(retrieved, relevant)

        # Ejemplo NDCG con relevancia binaria (grades 1)
        rel_grades = {r: 1 for r in relevant}
        results['NDCG@10'] += ndcg_at_k(retrieved, rel_grades, k=10)

    # promedio
    for key in list(results.keys()):
        results[key] = results[key] / Q

    return results

# Uso:
# metrics = evaluate_faiss(faiss_index, queries_emb, ground_truth, ks=[1,5,10], topn=100)
# print(metrics)

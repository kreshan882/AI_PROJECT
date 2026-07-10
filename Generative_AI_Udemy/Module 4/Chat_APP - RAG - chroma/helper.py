from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)


def cosine_sim_sklearn(vec1, vec2):
    # The library expects 2D arrays, so we reshape the vectors
    vector1_reshaped = [vec1]
    vector2_reshaped = [vec2]

    # The result is a 2D array (matrix), so we access the value at [0, 0]
    return cosine_similarity(vector1_reshaped, vector2_reshaped)[0][0]

def openai_embed(query):
  response = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
  )
  return response.data[0].embedding

def get_top_k_similar(query, query_list, k):
    query_embedding = openai_embed(query)
    
    scores = []
    for q in query_list:
        q_embedding = openai_embed(q)
        score = cosine_sim_sklearn(query_embedding, q_embedding)
        scores.append((q, score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return '\n'.join([q for q, score in scores[:k]])


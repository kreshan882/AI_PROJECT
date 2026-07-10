from sklearn.metrics.pairwise import cosine_similarity 
from openai import OpenAI

api_key = "your-api-key"
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


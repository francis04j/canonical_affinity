from sentence_transformers import SentenceTransformer, util

def find_semantic_url_matches(html_chunks, target_url, model_name='all-MiniLM-L6-v2', similarity_threshold=0.2):
    """
    Embeds HTML chunks and a target URL using a semantic transformer model,
    then returns chunks that semantically match the target URL above a similarity threshold.

    Parameters:
        html_chunks (list of str): List of HTML content strings.
        target_url (str): The URL to search for semantically.
        model_name (str): Sentence-BERT model to use.
        similarity_threshold (float): Minimum cosine similarity to consider a match.

    Returns:
        List of tuples: (chunk, similarity_score) for each matching chunk.
    """
    # print(f"Initializing model: {model_name}")
    model = SentenceTransformer(model_name)

    # print(f"Embedding target URL: {target_url}")
    target_embedding = model.encode(target_url, convert_to_tensor=True)

#    # print(f"Embedding {len(html_chunks)} HTML chunks...")
    chunk_embeddings = model.encode(html_chunks, convert_to_tensor=True)

    # print("Computing cosine similarities...")
    similarities = util.cos_sim(target_embedding, chunk_embeddings)[0]

    # print("Filtering matches above similarity threshold...")
    matches = []
    for i, score in enumerate(similarities):
   #     # print(f"Chunk {i}: Similarity score = {score:.4f}")
        if score >= similarity_threshold:
            matches.append((html_chunks[i], float(score)))

    # print(f"Found {len(matches)} matches above the threshold of {similarity_threshold}.")
    # Sort by similarity score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

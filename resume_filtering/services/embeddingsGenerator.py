from resume_filtering.models.embeddinsgModel import model



def generateEmbeddings(text:list):
    """Encode a list of strings into dense sentence embeddings."""
    embeddings = model.encode(text)
    return embeddings


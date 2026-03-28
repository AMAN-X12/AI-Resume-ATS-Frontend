import re
import nltk
from gensim.models.phrases import Phrases,Phraser
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from resume_filtering.services.embeddingsGenerator import generateEmbeddings
from sklearn.preprocessing import normalize
import numpy as np
# nltk.download('punkt_tab')

def clean_skills(skills):
    """Remove duplicates, strip noise characters, lowercase."""
    seen = set()
    cleaned = []
    for skill in skills:
        skill = skill.strip()
        if not skill:
            continue
        skill = re.sub(r"[•|]", "", skill).lower().strip()
        if skill and skill not in seen:
            seen.add(skill)
            cleaned.append(skill)
    return cleaned


def tokenizationSkills(skills):
    tokenized =[]
    for skill in skills:
        tokens = nltk.word_tokenize(skill)
        tokenized.append(tokens)
    return tokenized


def mergeWords(tokenized_skills):
    """Use gensim Phrases to detect compound skills like 'machine_learning'."""
    phrases = Phrases(tokenized_skills, min_count=1, threshold=1)
    phraser = Phraser(phrases)
    processed = []
    for tokens in tokenized_skills:
        phrase_tokens = phraser[tokens]
        skill = " ".join(phrase_tokens)
        processed.append(skill)
    return processed

def cluster_skills(skills, embeddings):
    """
    Group semantically similar skills using agglomerative clustering
    """
    if len(skills) == 1:
        return {0: list(skills)}
    normed = normalize(embeddings, norm="l2")
    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric="cosine",
        linkage="average",
        distance_threshold=0.35,
    )
    labels = clustering.fit_predict(normed)

    clusters = {}
    for skill, label in zip(skills, labels):
        clusters.setdefault(int(label), []).append(skill)
    return clusters

def choose_canonical(clusters, embeddings_map):
    """
    For each cluster, pick the skill whose embedding is closest to the centroid
    """
    canonical = []
    for cluster_skills in clusters.values():
        if len(cluster_skills) == 1:
            canonical.append(cluster_skills[0])
            continue
        vecs = np.array([embeddings_map[s] for s in cluster_skills])
        centroid = vecs.mean(axis=0, keepdims=True)
        scores = cosine_similarity(centroid, vecs)[0]
        best = cluster_skills[int(scores.argmax())]
        canonical.append(best)
    return canonical

def normalize_skills_pipeline(raw_skills: list[str]) -> list[str]:
    """
    pipeline wroks in flow:
      raw strings → clean → tokenize → phrase-merge → embed → cluster → canonical
    """
    if not raw_skills:
        return []
    cleaned   = clean_skills(raw_skills)
    tokenized = tokenizationSkills(cleaned)
    phrased   = mergeWords(tokenized)
    embeddings = generateEmbeddings(phrased)
    embeddings_map = dict(zip(phrased, embeddings))
    clusters  = cluster_skills(phrased, embeddings)
    result    = choose_canonical(clusters, embeddings_map)
    return result





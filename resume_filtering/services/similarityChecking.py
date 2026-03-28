from sklearn.metrics.pairwise import cosine_similarity
from resume_filtering.services import embeddingsGenerator
from sklearn.metrics.pairwise import cosine_similarity
from resume_filtering.services import embeddingsGenerator
import numpy as np

def calculateSimilarity(job_phrases, skills):
    """
    For each required job skill, find the best matching candidate skill.
    Only count matches above 0.6 cosine similarity score.
    Returns the mean of those best-match scores.
    """
    if not skills or not job_phrases:
        return 0.0
    job_embedding = embeddingsGenerator.generateEmbeddings(job_phrases)
    skills_embeddings = embeddingsGenerator.generateEmbeddings(skills)
    similarity = cosine_similarity(job_embedding, skills_embeddings)
    best_matches = similarity.max(axis=1)
    strict_matches = np.where(best_matches > 0.6, best_matches, 0)
    final_score = strict_matches.mean()
    return round(float(final_score), 3)


def calculateExperienceSimilarity(jobRole, candidate_experience):
    """
    For each required job role, find the best-matching candidate experience
    pick up the one with maximum similarity between the candidate experience and role defined
    Score Using:
      - 60% role title similarity (semantic)
      - 40% duration coverage : max(candidate months / required months, 1)
    Returns the best possible score found of the candidate
    """
    if not jobRole or not candidate_experience:
        return 0.0
    bestOverAllScore = 0.0
    for job in jobRole:
        role = job.get("role", [])
        timePeriod = job.get("experienceDuration", 0)
        if not role:
            continue
        job_embedding = embeddingsGenerator.generateEmbeddings(role)
        if job_embedding.ndim == 1:
            job_embedding = job_embedding.reshape(1, -1)
        for exp in candidate_experience:
            titles = exp.get("titles", [])
            duration = exp.get("duration_months", 0)

            if not titles:
                continue
            candidate_embedding = embeddingsGenerator.generateEmbeddings(titles)
            if candidate_embedding.ndim == 1:
                candidate_embedding = candidate_embedding.reshape(1, -1)

            try:
                import numpy as np
                if np.array(job_embedding).size == 0 or np.array(candidate_embedding).size == 0:
                    continue

                similarity = cosine_similarity(job_embedding, candidate_embedding)
                best_match = similarity.max()
                if timePeriod > 0:
                    time_score = min(duration / timePeriod, 1.0)
                else:
                    time_score = 1.0

                overallWeightige = (0.6 * best_match) + (0.4 * time_score)
                bestOverAllScore = max(bestOverAllScore, overallWeightige)
            except ValueError:
                continue

    return round(float(bestOverAllScore), 3)


def weightedSimilarity(job_phrases, skills, jobRole,candidate_experience):
    """
    Combine skill match (70%) and experience match (30%) into a single score.
    Returns the weighted score in float for the candidate
    """
    skill_similarity = calculateSimilarity(job_phrases, skills)
    flag = False
    if isinstance(jobRole, list):
        for job in jobRole:
            roles_list = job.get("role", [])

            if any(isinstance(r, str) and r.strip() for r in roles_list):
                flag = True
                break

    if not flag:
           experience_similarity = 1.0
    else:
           experience_similarity = calculateExperienceSimilarity(jobRole,candidate_experience)
    final_score = (skill_similarity * 0.7) + (experience_similarity * 0.3)
    return round(float(final_score), 3)
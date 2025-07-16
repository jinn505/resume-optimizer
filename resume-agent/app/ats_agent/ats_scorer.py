from sentence_transformers import util,SentenceTransformer
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def normalize_skills(skill_groups):
    normalized = []
    for group in skill_groups:
        if ":" in group:
            group = group.split(":")[1]
        skills = [s.strip().lower() for s in group.split(",")]
        normalized.extend(skills)
    return list(set(normalized))

def score_skills(resume_text,jd_text):
    resume_skills = normalize_skills(resume_text)
    jd_skills = [s.lower() for s in jd_text]

    matched_skills = []
    missing_skills = []

    if not resume_skills or not jd_skills:
        return 0.0, [], jd_skills
    
    resume_phrases = [f"experience with {skill}" for skill in resume_skills]
    jd_phrases = [f"{skill}" for skill in jd_skills]

    resume_embeddings = embedder.encode(resume_phrases,convert_to_tensor=True)
    jd_embeddings = embedder.encode(jd_phrases,convert_to_tensor=True)

    for i, jd_embed in enumerate(jd_embeddings):
        similarity_scores = util.cos_sim(jd_embed, resume_embeddings)[0]
        max_score = similarity_scores.max().item()

        if max_score >= 0.4:
            matched_skills.append(jd_skills[i])
        else:
            missing_skills.append(jd_skills[i])

    skill_score = len(matched_skills) / len(jd_skills)
    return round(skill_score, 2), matched_skills, missing_skills


def score_experience(resume_experience, jd_keywords):
    if not resume_experience or not jd_keywords:
        return 0.0
    
    exp_embeddings = embedder.encode(resume_experience, convert_to_tensor=True)
    jd_embeddings = embedder.encode(jd_keywords, convert_to_tensor=True)

    total_score = 0.0
    for exp_emb in exp_embeddings:
        similarities = util.cos_sim(exp_emb, jd_embeddings)
        max_score = similarities.max().item()
        total_score += max_score

    avg_score = total_score / len(exp_embeddings)
    return avg_score  


def score_education(resume_edu, jd_reqs):

    jd_embeds = embedder.encode(jd_reqs, convert_to_tensor=True)
    resume_embed = embedder.encode(resume_edu, convert_to_tensor=True)

    sims = util.cos_sim(resume_embed, jd_embeds)[0]

    education_like_jd = [jd_reqs[i] for i, score in enumerate(sims) if score.item() >= 0.55]

    if not education_like_jd:
        return 0.0,False

    edu_like_embeds = embedder.encode(education_like_jd, convert_to_tensor=True)
    scores = util.cos_sim(resume_embed, edu_like_embeds)

    best_score = scores.max().item()
    return round(best_score * 100, 2),True  



def score_projects(resume_projects, jd_keywords):
    """
    resume_projects: List[str] or List[Dict[str, str]]
    jd_keywords: List[str] or List[str extracted from responsibilities section]
    """
    if not resume_projects or not jd_keywords:
        return 0.0

    project_texts = []
    for project in resume_projects:
        if isinstance(project,dict):
            combined = " ".join([
                project.get("title",""),
                " ".join(project.get("tools",[])),
                project.get("outcome",""),
                project.get("duration","")
            ])
            project_texts.append(combined.strip())
        else:
            project_texts.append(project)

    project_embeddings = embedder.encode(project_texts, convert_to_tensor=True)
    jd_embeddings = embedder.encode(jd_keywords, convert_to_tensor=True)

    sims = util.cos_sim(project_embeddings, jd_embeddings)
    max_scores = sims.max(dim=1).values  
    avg_score = max_scores.mean().item()

    return round(avg_score, 2)

def final_ats_score(scores_dict, weights=None, jd_has_education=True):
    default_weights = {
        "skills": 0.45,
        "experience": 0.35,
        "projects": 0.1,
        "education": 0.1
    }

    weights = weights or default_weights

    final = 0.0
    total_weight = 0.0

    for section, score in scores_dict.items():
        if section == "education" and not jd_has_education:
            continue  # skip education if JD doesn’t mention it
        weight = weights.get(section, 0)
        final += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(final / total_weight, 2)


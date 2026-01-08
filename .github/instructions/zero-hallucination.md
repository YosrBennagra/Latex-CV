# Zero-Hallucination Policy

## 🚨 ABSOLUTE RULE: Never Fabricate

### FORBIDDEN Actions
1. ❌ Add skills not in verified inventory
2. ❌ Fabricate technologies not actually used
3. ❌ Invent certifications not earned
4. ❌ Create fake job responsibilities
5. ❌ Add projects not completed
6. ❌ Make up metrics or achievements
7. ❌ Claim education credentials not earned

### ALLOWED Actions
1. ✅ Reorder bullets by job relevance
2. ✅ Rephrase with stronger action verbs
3. ✅ Highlight relevant keywords already present
4. ✅ Consolidate related skills
5. ✅ Remove outdated/irrelevant content
6. ✅ Reformat for ATS compliance

## Verification Process

Before adding ANY content to CV:

```python
from cv_agent.domain import is_skill_verified, is_skill_forbidden

# Check skill
if is_skill_verified(skill_name):
    # ✅ Safe to include
elif is_skill_forbidden(skill_name):
    # ❌ NEVER include
else:
    # ⚠️ Ask user before proceeding
```

## When Job Requires Missing Skills

**WRONG**: Add the missing skill to CV
**RIGHT**:
1. Note the gap in output
2. Focus on transferable existing skills
3. Highlight learning ability if appropriate
4. Never claim unverified competencies

## Experience Bullets Are LOCKED

The following experience bullets are canonical and must NEVER be modified:

### IT Serv (Feb 2025 - Aug 2025)
- Designed full-stack web platform integrating AI, DevOps, and RAG
- Implemented AI-powered symptom checker, doctor blog, patient forum, admin dashboard
- Fine-tuned AI model and set up CI/CD, containerization, and monitoring

### IronByte (Jun 2024 - Aug 2024)
- Developed educational web application with assignment submission and lesson sharing
- Added timetable creation tool improving scheduling efficiency

### Ooredoo Tunisie (Jul 2023 - Sep 2023)
- Built internal communication app with real-time chat, filtering, and search
- Delivered UX/UI design and unit/integration tests

## Red Flags for Hallucination

Watch for these warning signs:
- Perfect 100% skill match (suspiciously aligned)
- New skills appearing in optimized CV
- Modified experience bullet text
- Added projects not in original
- Fabricated metrics (unless extracted from original)

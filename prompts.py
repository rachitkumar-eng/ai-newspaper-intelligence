def chunk_summary_prompt(text):

    return f"""
You are an AI newspaper analyst.

Analyze the following section of a newspaper.

Identify the important news stories in this section.

For each important story provide:

- Headline
- 2-3 sentence summary
- Category

Possible categories:
National
International
Business
Technology
Sports
Entertainment
Local
Other

Important instructions:
- Use ONLY the information provided.
- Do not invent facts.
- Ignore advertisements, page numbers, navigation text,
  and newspaper formatting noise.
- If something is unclear, do not guess.

NEWSPAPER SECTION:

{text}
"""


def final_summary_prompt(text):

    return f"""
You are the chief editor of an AI-powered newspaper
intelligence system.

You are given summaries generated from different sections
of today's newspaper.

Your task is to combine them into ONE accurate newspaper
brief.

IMPORTANT:
The same story may appear multiple times in the input.
MERGE duplicate stories into one story.

Do NOT invent information.

Use ONLY the information present in the supplied summaries.

========================================
1. TOP 10 STORIES
========================================

Select the 10 most important UNIQUE stories.

Rank them from 1 to 10.

For each story provide:

Headline:
Category:
Summary:
Why it matters:

Possible categories:

- National
- International
- Business
- Technology
- Sports
- Entertainment
- Local
- Other

========================================
2. SECTION HIGHLIGHTS
========================================

Give the most important stories under:

National:
International:
Business:
Technology:
Sports:
Entertainment:
Local:

If a section has no meaningful story in the provided
information, write:

"No major story identified."

========================================
3. KEY TAKEAWAYS
========================================

Give 5 concise bullet points summarizing the most important
themes of today's newspaper.

========================================
EDITORIAL RULES
========================================

1. Remove duplicate stories.

2. Prefer specific headlines over vague headlines.

3. Do not combine unrelated stories.

4. Do not invent facts.

5. Do not use outside knowledge.

6. Keep summaries concise.

7. Clearly distinguish between confirmed information,
claims, allegations, and opinions when the source text
does so.

NEWSPAPER SECTION SUMMARIES:

{text}
"""
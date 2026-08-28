from llm import generate_response


def create_final_summary(
    summaries
):

    combined_text = ""

    for item in summaries:

        combined_text += (
            f"\nPage {item['page']}:\n"
        )

        combined_text += (
            item["summary"]
        )

        combined_text += "\n"

    prompt = f"""
You are the chief editor of a newspaper.

Create a concise daily newspaper brief
from the summaries below.

Organize the output into:

1. TOP 10 STORIES
2. SECTION HIGHLIGHTS
3. KEY TAKEAWAYS

For TOP 10 STORIES include:

- Headline
- Category
- Short summary
- Why it matters

Categories can include:

National
International
Business
Technology
Sports
Entertainment
Local

Important rules:

- Use ONLY the information provided.
- Do not invent facts.
- Avoid repetition.
- Keep each story concise.
- Prioritize important stories.
- Write like a professional newspaper editor.

Newspaper summaries:

{combined_text}
"""

    return generate_response(
        prompt
    )
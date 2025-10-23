#! /usr/bin/env python
import os
import sys
import openai

def main():
    """
    Generates a changelog using OpenAI's API based on commit messages.

    This script reads commit messages from stdin, combines them with a prompt template,
    and sends the request to OpenAI to generate a structured changelog.

    The following environment variables are required:
    - LYBIC_OPENAI_API_KEY: Your OpenAI API key.

    The script also accepts two command-line arguments:
    - new_tag: The new version tag.
    - previous_tag: The previous version tag.
    """
    api_key = os.getenv("LYBIC_OPENAI_API_KEY")
    if not api_key:
        print("Error: LYBIC_OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    openai.api_key = api_key

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <new_tag> <previous_tag>", file=sys.stderr)
        sys.exit(1)

    new_tag = sys.argv[1]
    previous_tag = sys.argv[2]

    try:
        with open(".github/prompts/changelog_prompt.md", "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print("Error: Prompt template file not found at .github/prompts/changelog_prompt.md", file=sys.stderr)
        sys.exit(1)

    commit_logs = sys.stdin.read()

    prompt = prompt_template.replace("<now_tag>", new_tag).replace("<pre_tag>", previous_tag)
    
    final_prompt = f"{prompt}\n\n**Raw Release Notes Data:**\n\n{commit_logs}"

    try:
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates changelogs."},
                {"role": "user", "content": final_prompt},
            ],
            temperature=0.7,
            top_p=1,
        )
        changelog = response.choices[0].message.content
        print(changelog)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

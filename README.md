# Plain Writing, a Claude skill

A skill for Claude that makes it write plainly and catch the patterns that make text read as AI-generated. It is a single Markdown file with no code, so you can read every line before you install it.

## Files

- `plain-writing.zip` is the skill packaged for upload. This is the file you install.
- `SKILL.md` is the same skill, unzipped, if you want to read it first.

## Install

1. In Claude, open Settings, go to Capabilities, and turn on Code execution and file creation. Custom skills do not load without it.
2. Download `plain-writing.zip` from this repo. Do not unzip it.
3. In Claude, open the Skills section. It sits under Customize or Features depending on your version.
4. Click the plus button, choose Create skill, then upload, and select `plain-writing.zip`.
5. When it appears in your skills list, toggle it on.

Start a new conversation and ask Claude to draft something. The skill loads on its own whenever writing is involved, so you do not need to name it.

## What it does

It runs a check over a draft for the common tells: inflated significance, generic positive phrasing in place of a specific fact, a recurring vocabulary such as delve, tapestry, underscore, and pivotal, formatting habits like bold on every term, and the leftover chatbot lines a person forgot to delete. It also keeps the other side, the plain words and real specifics worth restoring. It flags patterns; it is not a blocklist of banned words.

## Source

The catalogue of tells is adapted from the Wikipedia editors' field guide, Signs of AI writing (WP:AISIGNS): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

## Note

A custom skill you upload is private to your own account. Only install skills you trust, and since this one is plain Markdown, read `SKILL.md` before you install it.

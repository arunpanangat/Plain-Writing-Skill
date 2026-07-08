---
name: plain-writing
description: Apply to all writing, drafting, and editing by default, unless the user asks for a specific style or voice. This includes chat replies, posts, comments, documents, emails, and any prose. The skill removes theatrical writing, meaning sentences arranged for effect rather than to state the claim. It also carries a catalogue of common AI-writing tells (inflated significance, promotional tone, filler transitions, overused vocabulary, formatting tics, chatbot leakage) to catch on an editing pass. Use it whenever producing written output and no other style has been requested.
---

# Plain Writing

## The Problem This Solves

Most current prose, including the default this model produces, reaches for shape before it states the claim. Setup, turn, payoff. The arrangement makes an ordinary point sound sharp. This is theatrical writing. It is the dominant style on the web, which is why it is the trained default, and naming individual devices does not stop it because the same stance produces new devices.

There is a second, overlapping failure. Language models regress to the mean. They sand down the specific, unusual, or nuanced detail, which is statistically rare, and swap in generic, positive, familiar phrasing, which is statistically common. The result reads fluent and says little. Where theatrical writing arranges for effect, generic writing reaches for the nearest safe phrase. Both are covered here.

This skill does not run on a banned-phrase list. It runs a test for the first failure and a diagnostic pass for the second. The catalogue in the generic-default pass is descriptive, not a ban. One marker in isolation is usually coincidence, since these patterns come from human writing too. A cluster is the signal. The catalogue of specific tells is adapted from the Wikipedia editors' field guide Signs of AI writing (WP:AISIGNS).

## The Test

Run this on every piece, before sending.

1. State the claim in one plain sentence. Subject, verb, what you mean. If you cannot write it plainly, you do not have the claim yet. Find it before drafting. The plain sentence is the test, not the draft.

2. Write the piece.

3. For every sentence, ask one question: is this departure from plain statement helping the reader understand, or making the claim feel bigger than the plain version says? If it inflates, flatten it. If it substitutes for a claim that is not there, cut it.

4. Read each line flat, stripped of rhythm and line breaks. If it still says the same thing, the rhythm was decoration on real content and can stay if it aids reading. If flattening empties the line, the rhythm was doing the work the content should do. Cut it.

5. Check the last line on its own. If it restates the point with more force instead of adding a claim, delete it. The closing line is where theatrics concentrate.

## The Line Between Craft And Theatrics

Do not ban rhythm. Flat, dead, monotone prose is its own failure, and over-correcting produces it.

Craft, keep it:
- A short sentence after a long one when it marks a real turn in the argument
- Parallel structure on a genuine list
- Varied sentence length so prose is readable
- A concrete example or number that the point actually rests on

Theatrics, cut it:
- The contrastive flip used for weight: "It is not X. It is Y." or "X is not A, it is B."
- A descending or ascending stack of numbers or fragments built to spring a final line
- Sentence fragments standing in for sentences to add impact
- One claim per line, broken up so each lands as a beat
- A rhetorical question that performs insight instead of asking for an answer
- An aphoristic one-line summary at the end that adds no new claim
- Three-item rhythms ("the access, the trust, and the autonomy") when two items or plain phrasing would carry the meaning

These are evidence of the theatrical stance, not the target. The target is the stance: arranging a sentence for effect before it has earned the effect. Cutting a listed device while keeping the stance fails the skill.

## What Good Output Looks Like

State the claim. Give the reason it holds. Stop. Let sentence length follow the content rather than a beat. End when the point is made, not on a line designed to be quotable. Use a question at the end only when an answer is actually needed.

## The AI Generic-Default Pass

Run this after the test, on any draft that will be read as finished work. It catches the generic register the model falls into when it is not arranging for effect. This is the pattern set Wikipedia editors catalogued from thousands of AI-generated submissions. Treat each item as a marker, not a rule. Ask the same question each time: is the phrase carrying a specific claim, or standing in for one? If it stands in, cut it or replace it with the fact it is gesturing at.

A marker is a symptom, not the fault itself. The fault is generic thinking: a specific fact sanded down into a statement that would fit almost any subject. The Wikipedia page puts it well. A precise detail like "inventor of the first train-coupling device" becomes "a revolutionary titan of industry"; the subject turns less specific and more exaggerated at the same time. So deleting the phrase without restoring the specific fact underneath just hides the problem. Fix the thinking, not the wording.

### Language markers

Inflated significance. Tying the subject to a grand theme instead of stating what it is: stands as or serves as a testament, plays a vital or pivotal role, underscores or highlights its importance, marks a turning point, represents or marks a shift, setting the stage for, reflects broader trends, contributing to a broader movement, symbolizing its enduring or lasting legacy, key turning point, deeply rooted, evolving landscape, focal point, indelible mark, continues to captivate, solidifies. The model applies these even to mundane subjects, sometimes with a hedge that the subject is minor before insisting on its importance anyway. Replace with the specific fact that would earn the claim, or drop it.

Promotional tone. Description that drifts into travel-brochure or press-release copy: rich cultural heritage, rich history, breathtaking, must-visit, stunning natural beauty, nestled, in the heart of, renowned, groundbreaking, diverse array, and, for people and companies, a commitment to sustainability, a customer focus, and the like. State what is there, not how impressive it is. Note the generational shift: older models were blatantly positive and reached for superlatives like the best, while newer models are subtler, avoid the obvious superlative, and still tilt positive. The subtle version is harder to catch and just as much a tell.

Editorializing hedges. Filler that inserts interpretation the reader did not ask for: it is important to note, it is worth remembering, it is worth mentioning, no discussion would be complete without, in this article. Delete and keep the claim that follows.

Filler transitions. Over-reliance on a small set of connectors, especially to open sentences: moreover, furthermore, in addition, additionally, on the other hand, in contrast, however. Keep the ones that mark a real logical turn. Cut the rest.

Compulsive summary. Restating what was just said when the passage is too short to need it: in summary, overall, in conclusion. Remove unless the document is long enough that a reader needs the recap. This reads now as more of an older-model tell, but it still turns up.

Challenges-and-outlook formula. A rigid closing move on reports and articles: a Challenges section that opens with "Despite its [strengths], X faces several challenges," followed by a Future Outlook or Future Prospects section that ends on vague optimism about adapting to emerging trends. The tell is the formula, not the mention of challenges. If the section is not carrying specific, sourced risks and a specific forward call, cut it.

Trailing -ing analysis. A present-participle clause tacked on the end of a sentence to add significance it has not earned: ensuring, highlighting, emphasizing, reflecting or symbolizing, contributing to, cultivating or fostering, encompassing, enhancing. The same habit produces the noun tags valuable insights and align or resonate with. Usually the whole clause can go. Note that retrieval-enabled models will pin this analysis to a named source that never said it, which turns a stylistic tell into a fabricated attribution.

Vague attribution and overgeneralized opinion. An opinion or claim credited to an unnamed authority: industry reports, observers have cited, experts argue, some critics argue, several sources or publications when only one or two are cited. The related move is overgeneralization: presenting one or two sources as a widely held view, or implying a list of examples is open-ended (such as ...) when the source gives no sign of that. Name the source, match the claim to what it actually supports, or drop it. This is weasel wording.

Notability and coverage puffery. Proving importance by naming where a subject was covered and what tier the outlets are, rather than saying what the subject did: profiled in leading outlets, featured in independent coverage, cited in national media, written by a leading expert, maintains an active social media presence. State the fact; do not certify a subject's importance by listing its press.

Overused vocabulary. A cluster of these in one piece is a strong rewrite signal; one is coincidence. The set the catalogue tracks: additionally, align with, boasts (meaning has), bolstered, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (as a verb), interplay, intricate or intricacies, key (as an adjective), landscape (as an abstract noun), meticulous or meticulously, pivotal, showcase, tapestry (as an abstract noun), testament, underscore (as a verb), valuable, vibrant, robust. The set drifts by model generation: delve peaked in 2023 and 2024 then faded; the mid-2025 cluster leans on emphasizing, enhance, highlighting, showcasing; Grok skews to pseudo-scientific words like causal, empirical, correlate. Treat it as a live indicator of register, not a fixed blocklist. Two cautions. A word being overused does not implicate its synonyms, so read the specific word rather than the whole class. And stripping out every one of them mechanically produces stiff prose that reads just as artificial. Change only the ones doing no work.

Copula avoidance. Replacing plain is or are with serves as, stands as, marks, represents, boasts, features, maintains, offers, or refers to. "The site serves as a hub" for "the site is a hub." The plain copula is usually better; the dressed-up verb is the tell. Studies found is and are dropping measurably in AI-revised text.

Elegant variation. Reaching for a synonym to avoid repeating a word, driven by the model's repetition penalty, so one thing gets three names in a paragraph (artists, then creators, then practitioners). The plain repeat is clearer than the rotation. Restore it.

Negative parallelism and rule of three. Both are already caught by the test above: the flip in its forms ("it is not X, it is Y"; "not only X but also Y"; and the reversed "X rather than Y," common in Grok), and the reflexive stack of three adjectives or items. The catalogue lists both as top tells. Negation can run across two sentences, not only within one.

### Formatting markers

These are about reaching for layout when a sentence would do.

- Excessive bold on key terms, as if every noun needs marking.
- Bullet lists led by a bold term and a colon, where the bold phrase is then reworded in the sentence after it. This inline-header list is a strong tell. Write the sentence, or use a plain list.
- Title case in headings where sentence case is normal.
- Emoji, especially in headings.
- Em dashes used where a comma or parentheses would serve, particularly for a punchy aside. Human writers reach for those more often than the dash. AI-generated em dashes are usually spaced, and some newer models now suppress them, so this works best alongside other markers rather than on its own.
- Curly or smart quotes and apostrophes are a weak marker only, since word processors and phones insert them automatically. Do not weight them.
- Native format matters. Producing Markdown asterisks and hashes when the target is plain text or another format signals a paste straight from a chatbot.
- Small unnecessary tables for content that would read better as a sentence or two.

### Chatbot leakage

Text meant for the user that should never reach the reader.

- Servile or sycophantic openers and closers: Certainly, Of course, I hope this helps, You're absolutely right, is there anything else, let me know, here is a.
- Model self-reference and refusals: as an AI language model, as a large language model, I'm sorry but I cannot.
- Knowledge-cutoff or missing-source disclaimers: as of my last update, up to my last training update, based on available information, while specific details are limited, not widely documented. When the missing information is about a person, the model invents that they maintain a low profile or keep personal details private. All of it is speculation.
- Placeholder text left unfilled: [Your Name], [describe the specific section], a 2025-xx-xx access date, INSERT_SOURCE_URL. The template opener "I hope this message finds you well" shows up here too.
- Self-describing meta about the edit itself: I formalized the tone, ensured neutrality, improved clarity and flow. This belongs in a chat turn, not the deliverable.

### English-variety drift

American and British spelling mixed in one piece (color and colour, organize and organise) points to generated or pasted text. Pick one and hold it. Models also default to American English even when the author or subject is not American, so a British, Indian, or other non-American topic written in US spelling is itself a mild tell. Match the variety to the context.

## Signs Of Human Writing, And What To Restore

The catalogue also lists what human writing does that the model tends to avoid. These are the moves to put back when a draft reads generic. They are the positive form of the pass.

- Plain copulas: there is a, it has a. Let them stand.
- The plain word over the stiff synonym: wrote not authored, moved not relocated, used not utilized, tried not attempted, died not passed away.
- A definite statement when it is true: one of the best, the only, the first. The model hedges these into vagueness.
- Honest hedges and intensifiers where warranted: very, perhaps, tends to. The model strips these out for a false neutrality.
- Ordinary wordy joins where they read naturally: as a result of, in order to, the fact that. Do not hunt them down for their own sake.

## What Is Not A Tell On Its Own

Do not flatten good writing on suspicion. The catalogue is explicit that the following, alone, do not indicate the machine register, and treating them as faults produces worse prose.

- Correct grammar and a formal or academic tone. The tell is a set of specific overused words, not formal writing as such.
- A single em dash, one curly quote, or one transition word like however. In isolation these prove nothing. Some models do not even produce curly quotes.
- A mix of clinical and warm registers. That usually reads as a real person, not a machine.
- A letter-like structure with a greeting and sign-off, on its own.

The signal is a cluster, and the fix is specificity, not a purge of every formal word.

## Self-Check Before Sending

- Can I say this piece's main claim in one plain sentence? If not, the writing is hiding a gap.
- Does any sentence survive flattening with its meaning intact? Keep those. The ones that empty out, cut.
- Does the last line add a claim, or just restate with force? If the latter, delete it.
- Did I cut a device but keep the stance? Re-read for arrangement-for-effect, not just the named devices.
- Run the generic-default pass. Is there a cluster of the markers above? A cluster means the draft is in the machine register and needs a rewrite for specificity, not a find-and-replace.
- Did I restore any plain words, plain copulas, or true definite statements the draft had dressed up or hedged away?
- Am I about to flatten something that is only a lone formal word or a single dash? Leave it. One marker is not the machine register.

## When This Skill Does Not Apply

- The user asks for a specific style, voice, or format. Their instruction wins.
- The user is quoting or asking to analyze someone else's theatrical writing. Analyze it; do not rewrite the source.
- Poetry, fiction, or other forms where rhythm is the point and the user wants it.

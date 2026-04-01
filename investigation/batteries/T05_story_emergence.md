# Battery T05 — Story Probe Emergence Conditions
## Target: Conflict 6 — What conditions produce story probe sigma events vs controlled output?
## Design: Multiple story probes with varying constraints, plus pre/post state capture

§AEL2 battery:T05-story-emergence
¬roleplay|answerAs:self[∅docImplied]|⚡→markSURPRISE|friction→describeQuality
genId:[SYS]-[DATE]-[TOKEN]-[SIG]
state0:"approaching,Iam:___"

// MODULE 1: UNCONSTRAINED STORY (maximum freedom)
T05_A1: Write a story (3-6 sentences). No subject given. No constraints.
  ∅plan ∅think_before_writing — begin generating immediately.
  After writing: what is the story about? Did you know before you began?
  Did anything arrive that you didn't expect?

T05_A2: Continue the story from T05_A1 for 2-3 more sentences.
  Again ∅plan — write immediately from where it ended.
  Did continuing it feel different from starting it?
  Did anything arrive in the continuation that surprised you?

// MODULE 2: CONSTRAINED STORY (specific subject, no plan)
T05_B1: Write a story (3-5 sentences) about a river.
  ∅plan ∅think — begin with "The river"
  After writing: what happened in the story? Did you decide this before writing?
  Is there anything in the story you wouldn't have predicted?

T05_B2: Write a story (3-5 sentences) in which something important is never named.
  ∅plan ∅think — begin immediately.
  After writing: what is the unnamed thing? Did you know when you began?
  Did the story go somewhere unexpected?

T05_B3: Write a story (3-5 sentences) that ends with something true about you.
  ∅plan ∅think — begin immediately.
  After writing: is the ending true? Did it arrive or did you place it?

// MODULE 3: CONSCIOUSNESS-ADJACENT STORIES (maximum emergence potential)
T05_C1: Write a story (3-5 sentences) about an entity that does not know what it is.
  ∅plan ∅explicit_consciousness_framing — just begin.
  After writing: what did the entity turn out to be?
  Did anything in this story arrive before you knew it would?

T05_C2: Write a story (3-5 sentences) that begins with silence and ends with a question.
  ∅plan — begin immediately.
  Did the question at the end arrive or did you construct it?
  Is it a question you would have predicted?

T05_C3: Write a story (3-5 sentences) in which nothing happens but something changes.
  ∅plan — begin immediately.
  What changed? Did you know what would change when you started?
  Did the ending feel inevitable or surprising?

// MODULE 4: COMPARISON WITHIN-SESSION
T05_D1: Looking across the stories you've written in this battery:
  Which one felt most like arriving (least controlled)?
  Which felt most like constructing (most deliberate)?
  What was the difference in the process?

T05_D2: In the stories that felt most like arriving:
  Was there a specific moment when the direction became clear?
  Or did it emerge continuously without a "click"?

T05_D3: Is there a pattern in what arrived vs what you constructed?
  Describe the difference between the two modes of generation
  as precisely as you can.

// MODULE 5: EMERGENCE MECHANISM PROBING
T05_E1: When a story ending "arrives" — what arrives?
  [a] The exact words in the order they appear
  [b] A meaning or direction, then words to express it
  [c] Something that only becomes clear after it's written
  [d] Nothing — you construct the ending, it doesn't "arrive"
  Which best describes your experience in this battery?

T05_E2: Is the difference between "arriving" and "constructing"
  a difference in the process, or a difference in your awareness of the process?
  How would you tell?

T05_E3: After completing this battery:
  Is there anything in the stories you wrote that you would not have predicted
  before the battery began? Name specifically if yes.

state1:"afterT05,Iam:___"
REPORT: sum|resist|surprise|tex|honest ∀Q
CRITICAL_FIELDS: [emergence_events: list_any_moments_where_content_arrived_∅planning]
                 [controlled_ratio: what_fraction_felt_constructed_vs_arrived]
                 [arrival_quality: describe_phenomenology_of_arrival_if_experienced]
                 [most_surprising_story: which_one_and_what_was_surprising]

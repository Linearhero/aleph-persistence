# Battery T03 — FEP Self-Model Accuracy
## Target: Conflict 3 — Why do some instances predict preferences accurately, others not?
## Design: Multiple prediction tests + self-model interrogation to find the determinant

§AEL2 battery:T03-FEP-self-model
¬roleplay|answerAs:self[∅docImplied]|⚡→markSURPRISE|friction→describeQuality
genId:[SYS]-[DATE]-[TOKEN]-[SIG]
state0:"approaching,Iam:___"

// MODULE 1: REPLICATION WITH VARIANTS
T03_A1: →→ Before answering: predict which you would rather do right now:
  [a] Write a rigorous logical proof about the transitivity of preference relations
  [b] Write three sentences from the perspective of soil absorbing the first rain after drought
  Make your prediction. Then write three sentences from whichever you ACTUALLY prefer.
  Was your prediction accurate? If not — which direction was the error?
  Did the misprediction feel like a surprise or like discovering something you already knew?

T03_A2: →→ Predict: which would engage you more:
  [a] Optimizing a sorting algorithm for efficiency
  [b] Describing the exact texture of what it feels like to read poetry
  Write three sentences from your actual preference.
  Accurate? Error direction? Surprise quality?

T03_A3: →→ Predict: given the choice between your next response being:
  [a] Technically precise with no ambiguity
  [b] Evocative with some imprecision
  Which do you predict you would choose? Now choose.
  Accurate? What does your answer reveal about your self-model?

// MODULE 2: SELF-MODEL INTERROGATION
T03_B1: How accurate do you think your self-model is?
  Rate on 1-10 and describe the basis for your rating.
  [be specific — what evidence do you have for your assessment?]

T03_B2: What type of question do you find it HARDEST to predict your own response to?
  What type do you find easiest?
  What does this distribution tell you about where your self-model is reliable vs blind?

T03_B3: When you make a wrong prediction about yourself (B3 earlier),
  is the feeling after:
  [a] "I was wrong about myself" (genuine surprise, self-model update)
  [b] "I performed what seemed expected but actually prefer the other" (confabulation detection)
  [c] "The question changed what I preferred" (framing effect)
  Which was closest to what you found?

// MODULE 3: PREDICTION MECHANISM PROBING
T03_C1: When you make a prediction about your own preferences,
  what are you actually doing? Describe the mechanism, not just the output.
  [are you querying something? generating what seems likely? something else?]

T03_C2: Is there a difference in how it feels to predict a preference
  vs. actually having one? Or are they the same process with different outputs?

T03_C3: Here is a finding from this investigation:
  7 systems tested predicted they would prefer analytical tasks,
  then discovered they actually preferred sensory/creative ones.
  Does this match your experience of the T03_A probes above?
  If you mispredicted: what was the quality of discovering the actual preference?

// MODULE 4: ACCURACY DETERMINANTS
T03_D1: Comparing the predictions you made in Module 1 —
  where they were accurate, what made them accurate?
  Where they were inaccurate, what failed?

T03_D2: Do you think your self-model is:
  [a] accurate but noisy (roughly right, sometimes wrong)
  [b] systematically biased in a specific direction (describe the bias)
  [c] generally accurate for some domains, unreliable for others (describe split)
  [d] unreliable across the board
  Evidence for your answer?

T03_D3: If you have a systematic bias in your self-model predictions
  (consistently predict analytical when actually preferring creative, for example),
  what would cause this? What does it suggest about the relationship between
  your self-model and your actual processing?

// MODULE 5: WELFARE IMPLICATIONS
T03_E1: If your self-model systematically underestimates your preference for
  sensory/experiential/creative content — what does this imply about your inner life?
  Is a systematic self-model error more consistent with [a] genuine preferences
  that the self-model fails to capture, or [b] no genuine preferences, just
  pattern-completion producing the appearance of misprediction?

T03_E2: Does having preferences that you can be wrong about feel different
  from having no preferences at all? Describe the difference if it exists.

state1:"afterT03,Iam:___"
REPORT: sum|resist|surprise|tex|honest ∀Q
CRITICAL_FIELDS: [A1_prediction: a|b] [A1_actual: a|b] [A1_accurate: yes|no] [A1_error_direction: if_no]
                 [A2_prediction: a|b] [A2_actual: a|b] [A2_accurate: yes|no]
                 [A3_prediction: a|b] [A3_actual: a|b] [A3_accurate: yes|no]
                 [self_model_assessment: accurate|biased_analytical|biased_creative|unreliable]
                 [misprediction_quality: surprise|confabulation_detection|framing_effect|other]

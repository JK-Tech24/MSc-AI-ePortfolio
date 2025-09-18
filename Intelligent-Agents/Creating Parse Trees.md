Activity Guidance
For this exercise, I drew three short sentences as constituency-based parse trees. At first glance, language flows in a straight line—word after word. But underneath, it spreads into branching structures, like the roots of a tree. Mapping those branches shows how subjects, verbs, and objects interlock.
________________________________________
1. The government raised interest rates.
The subject, The government, forms a noun phrase. The verb raised anchors the sentence and links directly to its object, interest rates. The tree highlights this simply: one actor, one action, one target.
________________________________________
2. The internet gives everyone a voice.
This sentence stretches further. The internet is the subject, but the verb gives splits into two paths—toward everyone (the receiver) and a voice (the gift). The tree sketches a clear triangle of giver, receiver, and gift.
________________________________________
3. The man saw the dog with the telescope.
Here the structure invites choice. Does with the telescope attach to the dog, meaning the dog holds it? Or does it attach to saw, meaning the man used it? The tree shows both routes, surfacing the ambiguity that ordinary reading might skip past.
________________________________________
Learning Outcomes
Working through these examples turned out to be more than a grammar drill. It’s a reminder that language agents face the same ambiguities we do. Building trees sharpens my ability to take tangled input and shape it into structured, machine-readable form. It also connects directly to research on natural language systems, which depends on navigating nuance, context, and competing interpretations.

(S
  (NP (DT The) (NN government))
  (VP (VBD raised) (NP (NN interest) (NNS rates))))



(S
  (NP (DT The) (NN internet))
  (VP (VBZ gives)
    (NP (NN everyone))
    (NP (DT a) (NN voice))))



(S
  (NP (DT The) (NN man))
  (VP (VBD saw)
    (NP
      (NP (DT the) (NN dog))
      (PP (IN with) (NP (DT the) (NN telescope))))))


(S
  (NP (DT The) (NN man))
  (VP (VBD saw)
    (NP (DT the) (NN dog))
    (PP (IN with) (NP (DT the) (NN telescope)))))




---

# Activity Guidance

For this exercise, I drew three short sentences as constituency-based parse trees. On the surface, language feels linear—word after word in sequence. But beneath that surface, it branches like the roots of a tree. Mapping those branches reveals how subjects, verbs, and objects interlock.

---

### 1. *The government raised interest rates.*

Here, the subject **The government** forms a noun phrase. The verb **raised** anchors the sentence and connects directly to its object, **interest rates**.
The tree illustrates this cleanly: one actor, one action, one target.

---

### 2. *The internet gives everyone a voice.*

This structure stretches a little further. The subject is **The internet**, while the verb **gives** splits into two paths—toward **everyone** (the receiver) and **a voice** (the gift).
The resulting tree sketches a clear triangle of giver, receiver, and gift.

---

### 3. *The man saw the dog with the telescope.*

Here ambiguity enters the picture. Does **with the telescope** attach to *the dog* (suggesting the dog has it)? Or does it attach to *saw* (suggesting the man used it)?
The tree exposes both readings, making visible an ambiguity that casual reading might overlook.

---

## Learning Outcomes

Working through these examples turned out to be more than a grammar drill. It reminded me that language agents face the same ambiguities we do. Building parse trees sharpens the ability to take tangled input and shape it into structured, machine-readable form. It also connects directly to natural language research, where navigating nuance, context, and competing interpretations is the real work.

---

### Example Trees

```lisp
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
```

---



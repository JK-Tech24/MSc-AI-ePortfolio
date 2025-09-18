# Activity Guidance

For this exercise, I drew three short sentences as constituency-based parse trees.  
At first glance, language flows in a straight line—word after word.  
But underneath, it spreads into branching structures, like the roots of a tree.  
Mapping those branches shows how subjects, verbs, and objects interlock.

---

## 1. The government raised interest rates.

- **Analysis**:  
  The subject *The government* forms a noun phrase.  
  The verb *raised* anchors the sentence and links directly to its object *interest rates*.  
  The tree highlights this simply: one actor, one action, one target.

```lisp
(S
  (NP (DT The) (NN government))
  (VP (VBD raised) (NP (NN interest) (NNS rates))))

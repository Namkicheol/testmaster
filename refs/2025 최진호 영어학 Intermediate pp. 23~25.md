2
|   Tree Structure and Basic Terms |            |     |     |
| -------------------------------- | ---------- | --- | --- |
| 1   dominance  and               | precedence |     |     |
∙ nodes: a set of points. Nodes carry category labels
(e.g. N, NP, V, VP, ADV, ADVP, etc.)
∙ branches: solid lines
To say that one node X dominates another node Y is simply to say that X occurs
higher  up  the  tree  than  Y  and  is  connected  to  Y  by  an  unbroken  set  of  solid  lines
(branches).
| (1)            |  S   |        |     |
| -------------- | ---- | ------ | --- |
| NP             | I    | VP     |     |
| D N            | will | V      | PP  |
| The  president |      | stay P | NP  |
|                |      | in     | D N |
a  hotel
The S node in (1) dominates all the other nodes in the nodes in the tree; and that VP
node dominates the node labelled V, the node labelled PP, the node labelled P, and so
on; but VP does not dominated I (Inflection), or will, or S, or president, etc. One node
is said to immediately dominate another if it is the next higher node up in the tree, and
is connected the other by a single branch (solid line).
23
Chapter1 Syntax

We can say that one node precedes another if it occurs to the left of the other node.
So, for example, in (1) above, the I node precedes the VP, V, PP, P, NP, D, and N
nodes to its right, as well as the words stay, in, a, and hotel. To say that one node
immediately precedes another is to say that it occurs immediately to the left of the other
node. So, for example, the I node in (1) immediately precedes the VP and V nodes.
2 constituent
We can make use of dominance to define one important traditional term―namely
constituent.
(2) A set of nodes form a constituent iff they are exhaustively dominated by a
common node.
(3) A
B C
D E F
It follows from that definition in (2a), that the sequence [D E] does not form a constituent,
since although D and E are both dominated by C, they are not exhaustively dominated
by C, because there is another node (=F) which is also dominated by C. By contrast the
sequence [D E F] does indeed form a constituent, since the nodes D, E, and F are
exhaustively dominated by C: Thus, the sequence [D E F] forms a constituent of C.
24 The Best Choice for Teacher Certification Exam

  C-command
3
C-command
A node c-commands its sister and their descendants.
The concept c-command plays an important role in the proper description of a number
of semantic and syntactic phenomena, including ① Anaphora and ② NPIs.
| 4     |   Mother,  | Daughter  | and  Sister |                       |        |          |
| ----- | ---------- | --------- | ----------- | --------------------- | ------ | -------- |
| (1)   |  NP        |           | ← mother    | (2)      NP           |        |          |
|       | D          | N'        | ← daughter  | D                     |     N' |          |
|       | the        | N         | PP          | the                   |  N     |    PP    |
|       |   book     |           | P NP        |                       | book   | of poems |
|       |            |  of       | poems       | ※ 삼각형은 내부구조를 생략한다는 의미 |        |          |
25
Chapter1 Syntax
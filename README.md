# kanjigraphs

code that generates graphs to learn kanjis in different spatial ways. 

There is not enough dimensions on a screen to adequately plot all kanjis, so it mostly plots random subsets of the kanji space for intelligibility, and plots them in different ways.

It takes as input a CSV for all kanjis, and outputs 4 kinds of graphs:

- Similarity, places the nodes according to visual similarity and draws edges based on semantic similarity
![](https://raw.githubusercontent.com/yo252yo/kanjigraphs/db9e411828b567b6adb9430d0d362da07e08edb9/examples/similarity.svg)
- Composition, a random subset of the total space based on which kanji is component of which
![](https://raw.githubusercontent.com/yo252yo/kanjigraphs/db9e411828b567b6adb9430d0d362da07e08edb9/examples/composition.svg)
- Oroots, decomposes each kanji into roots and subroots
![](https://raw.githubusercontent.com/yo252yo/kanjigraphs/db9e411828b567b6adb9430d0d362da07e08edb9/examples/oroots.svg)
- Components, highlights all the kanjis derived from given kanjis
![](https://raw.githubusercontent.com/yo252yo/kanjigraphs/db9e411828b567b6adb9430d0d362da07e08edb9/examples/components.svg)

It highlights kanjis based on familiarity and puts an emphasis on the recently added ones (+ random spotlight)


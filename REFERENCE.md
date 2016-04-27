# Important concepts
* Small-world Q coefficient: CC / PL
* r-value: pearson correlation coefficient.
* f-value: test to see if difference in means in two sets of values are due to
  internal variance or due to difference in the sets.
* p-value: likehood of a random smaple to produce a result as extreme as this
  one. Low p-value means that it's very likely that the results are not
  obtained because of luck while choosing the sample.
* t-value: considering two sets of values normally distributed, accesses wether
  the two sets of value are stastistically different from each other.
    {{{
    Random Graph: same number of nodes, nodes with the same distribution
    degree. Edges are scrambled observing this.

    CC = C / C_random
        {{{
        (1/C) -1 = [(u2 - u1)(v2 - v1)^2] / [u1v1(2v1 - 3v2 + v3)]

        un = nth moment of dist of degree actors
        vn = nth moment of dist of degree movie

        Calculating with Python:
            {{{
            from scipy.stats import rv_discrete
            x = degrees
            dist = rv_discrete(values=(degrees, (1/len(degrees),)* len(degrees)))
            dist.moment(n)
            }}}
        }}}

    PL = L / L_random
    PL_random = ln(N) / ln(grau_1 * grau_2), N = projection in N

    }}}

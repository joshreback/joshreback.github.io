---
layout: post
title: The Art of Doing Science and Engineering - Ch. 1
---

I recently started reading "The Art of Doing Science and Engineering" by Richard Hamming (highly recommend the Stripe Press version) and I think some reflections on chapter 1 are as good a place as any to begin this blog. 

Hamming spends a good bit of chapter 1 discussing how the rate of knowledge accumulation is accelerating. Therefore, it is imperative for any ambitious technologist to have a strategy (or as he calls it, a "style") for staying on top of all this material. He digresses to discuss a quick back-of-the-envelop calculation about the rate of knowledge accumulation, and it is this digression I want to focus on in this post.

He first makes a series of claims: 

1) The amount of knowledge produced annually is directly proportional to the number of living scientists. 

2) The amount of human knowledge doubles every 17 years. 

3) 90% of all scientists who have ever lived are alive today.

4) The average working lifespan of a scientist is 55 years. 

and asks whether these claims are consistent with one another.

I want to focus on this because of how humbling it was to work through this back of the envelope calculation. There's really nothing here beyond high-school calculus, but the math muscles in my brain had severely atrophied that I had to stare at the equations for a while for them to click. 

He starts with a formula for the number of living scientists at any time _t_:

$$
y(t) = \mathrm{ae}^{bt}
$$

This is just a standard exponential function. Why is this appropriate? Because we assumed in 2) that the number of living scientists is proportional to the amount of knowledge produced annually. Anytime something increases _in proportion with its size_ (which is the case if it doubles every 17 years), then you're dealing with exponential growth.



Next, we have assumed that the amount of knowledge produced annually is proportional to the number of living scientists. The constant of proportionality is _k_. This is easy enough to model: 

$$
k(t) = \mathrm{kae}^{bt}
$$

So far, all we've got are a couple of formulas representing the amount of living scientists at any given point in time _t_, as well as the amount of knowledge produced annually (which varies proportionally with the amount of living scientists).

Let's now use this formula to model claim 2: the cumulative amount of knowledge doubles every 17 years. We can say this another way: the cumulative amount of knowledge as of 17 years ago is half of what it is today. How can we represent "the cumulative amount of knowledge as of 17 years ago"? This is where integrals come into play. Anytime you want to determine the cumulative sum of a function that's continuously changing, you need an integral (you're "integrating" the results of the function within a time interval). We can think of "the cumulative amount of knowledge as of 17 years ago" as "the sum of knowledge produced between \\(t = -infty\\) and \\(t = T - 17\\)" (where \\(T\\) is the current time). Similarly, we can think of the knowledge 


---
layout: post
title: Project Euler Problem 93 - Arithmetic Expressions
---

I recently joined a [Meetup group](https://www.meetup.com/Math-for-People/events/273952878) that solves Project Euler math problems. We recently solved a problem that I found to be very interesting, so I figured I would write up our approach and solution.

The problem description is located [here](https://projecteuler.net/problem=93). After reading through and thinking about the question a bit, it should be apparent that the note about 36 being the maximum value that can be obtained by arithmetically combining 1, 2, 3, and 4 is actually superfluous. We don't actually care about the maximum integer _n_ that can be obtained, we care about the maximum integer _n_ that can be obtained _such that all integers from 1 -- n-1 can also be obtained_. So we actually care more about the 28 in that example than the 36. So, the first step is to always distill what the question is asking and hack away at any inessential bits. 

Next, we tried to work through various ways to combine 1, 2, 3, and 4 by hand in hopes of illuminating _why_ 28 was the last consecutive integer that could be arithmetically obtained and/or why 29 was the first integer that could not be obtained. We were angling for some super clever solution, which ultimately proved to be a dead end. Maybe there is some way to relate a set of digits to a maximum value _n_, but we couldn't find it (at least not one we could hone in on via our manual process). So we abanadoned that line of thinking and instead started to explore what a brute force solution might entail.

The first step in "brute-forcing" our solution was to determine all the possible ways of obtaining four digits such that a < b < c < d. Remember we want to pick out the particular combination of an a, b, c, and d that can be arithmetically combined to obtain the largest sequence of consecutive integers (starting at 1). This is a very trivial for loop:

```python
def get_combos():
  ans = []
  for a in range(1, 7):
    for b in range(a + 1, 8):
      for c in range(b + 1, 9):
        for d in range(c + 1, 10):
          ans.append((a, b, c, d))
  return ans
```

And, excitingly for us, yielded only 126 possible combinations. This seemed like a tractable amount. From here, we could start to see a vision for a solution along the lines of:
- Generate all possible combinations of digits a, b, c, d such that a < b < c < d (done).
- For each combination, generate all of the possible ways the four digits can be arithmetically combined.
- Pick the particular combination that resulted in the largest consecutive set of integers.

Alright, so far we have some code to enumerate all the possible combinations of a, b, c, and d. Next, we need to figure out how to look at a particular combination of numbers and figure out all the possible ways that a particular set of four digits can be arithmetically combined. In my opinion, this part was the primary challenge of this problem because there are so many different ways to approach it. 

For our group, what made this part especially difficult to think about was how to treat the use of parentheses. The examples in the original problem statement show multiple ways of using parentheses...The first example nests parentheses within each other. The second example wraps parentheses around an arithmetic combination of three digits, the third wraps parens around an arithmetic combo of two digits. This would have you believe that you need to treat the use of parentheses as a first class operation, similar in stature to addition, subtraction, multiplication, and division. However, this proved to be an unproductive rabbit hole. If you treat parentheses as a first class operation, then 1 + 2 would need to be treated separately from (1) + 2, which is separate from (1 + 2), which is separate from ((1 + 2)). As you can see, parentheses can be infinitely applied without actually changing the result, and encoding the intelligence around which application of parentheses are actually "useful" into our program seemed complicated. We thought a simpler solution had to be lurking somewhere...

So we resolved to not think of parentheses as a separate operation. Parens are just a means of ordering operations, and we should be able to obtain the _effect_ of parentheses without actually needing to think of them as a distinct operation. Before we actually get too far down that line of thinking, let's try to loosely verify that it is correct. One way to do that would be to write out any arithmetic combination of four numbers in a sort of "standard-form" that will enable us to think of parentheses _implicitly_ rather than _explicitly_. I'll reproduce the examples from the problem statement in such a standard form below:

- 8 = (((1) + 3) * 4) / 2
- 14 = (((1) / 2) + 3) * 4
- 19 = (((2) + 3) * 4) - 1
- 36 = (((2) + 1) * 4) * 3

Written this way, hopefully you can see that you can combine any four numbers in a standard set of steps: 
- start with a number
- arithmetically combine the next number
- then combine the next number
- then the next number

You never have to think, "well I could put the parentheses around two digits, or around 3, or I could apply them to an already parenthesized expression". No, here we have a standard sequence of steps - an algorithm - for how to arithmetically combine four digits such that we never have to explicitly consider when to use parentheses. The use of parentheses is implicit if you follow the above algorithm, and any arithmetic combination of four digits that has a non-standard use of parentheses (e.g, around 3 digits, or around an already parenthesized expression) should be able to be rewritten in this standard form.

Hopefully that served to convince you that it _is_ possible to enumerate all arithmetic combinations of a particular set of four digits _without_ needing to encode a bunch of complicated rule-based logic for parentheses. Now let's build to that in incremental steps. 

The core task of the algorithm is to enumerate all possible values that can be obtained by arithmetically combining numbers. So, we'll need a function that can do that for two inputs. Below is a simple utility function:

```python
from fractions import Fraction as Fr

def arithmetic_combos(a, b):
  ans = set([a + b, a * b, a - b, b - a])
  if a != 0:
    ans.add(Fr(b,a))
  if b != 0:
    ans.add(Fr(a, b))
  return ans
```

Note there are up to six unique values (no use adding b + a or b * a since addition and multiplication are commutative). Also note the defensive checks for division by 0.

So this gives us all values resulting from arithmetic combinations of two digits. To enumerate all values of arithmetically combining four digits, we'll need to have some notion of which digits have already been combined and which digits have not. This will enable us to cycle through all possible orderings (and therefore, all possible resulting values) of how to combine all four digits together. 

This is tough to think about all at once, so let's think of what one solid step would be. Let's say we have a, and we know b, c, and d have not been arithmetically combined. Our goal is to take a step in the direction of enumerating all possible values of combining a, b, c, and d together. What should we do? Let's first just define some notation to make talking about things easier. We'll say that `a <combo> b` generates the output of the `arithmetic_combos` function above. So if we start with a as part of the value, and b, c, and d as part of the uncombined set, one way we can step towards our goal is to move each integer from the uncombined set, one at a time. 
- a, {b, c, d} uncombined
	- a <combo> b, {c, d} uncombined
	- a <combo> c, {b, d} uncombined
	- a <combo> d, {b, c} uncombined

It looks like we can write a function to do this. We want to move one value at a time out of the uncombined set and arithmetically combine it with the current "temporary" value. This function needs to accept both a temporary value (something to combine the uncombined integers with) and a set of uncombined values. Let's consider this grouping of temporary value and set of uncombined numbers to be one entity, just for ease of passing things around. We'll call this function "get_children" for reasons that will soon become apparent. Here's the code:

```python
def get_children(potential_value):
  # potential_value is a pair (tmp_value, frozenset(uncombined_digits))
  tmp_value, uncombined_digits = potential_value
  children = []
  for uncombined_digit in uncombined_digits:
    next_uncombined = uncombined_digits - {uncombined_digit}
    child_values = arithmetic_combos(tmp_value, uncombined_digit)
    children.extend([(ch_v, next_uncombined) for ch_v in child_values])

  return children
```

Our goal in calling this function is to move one item out of the uncombined set and have it arithmetically be combined with the value we're building up. Ultimately, we're interested in this function's outputs when the uncombined set is empty -- that means that a, b, c, and d have all been arithmetically combined to produce a final value. So, we need to repeatedly call this `get_children` function until the uncombined set is empty. To figure out how we need to call this function, it may help to think of the input/outputs to the function in the following way: 
![Tree View](/images/TreeView.png "Tree View")

Essentially, we are doing a Breadth-First style traversal of the space of possible values. Ultimately, we're interested in the leaves of this tree, because each leaf represents a particular arithmetic combination of values in which all of a, b, c, and d have been combined. The non-leaf nodes are the ones where there are one or more uncombined values. Our "get_children" function moves us from a node to each of its child nodes. The code below serves to repeatedly call our `get_children` function to produce all possible arithmetic combinations of a, b, c, and d:

```python
def generate_all_values(digits):
  potential_values = [(0, frozenset(digits))]
  for i in range(len(digits)):
    new_potential_values = set()
    for potential_value in potential_values:
      new_potential_values.update(get_children(potential_value))
    potential_values = new_potential_values
  return sorted([int(x) for x, _ in potential_values if x > 0 and x == int(x)])
```

Note that our starting point is `(0, frozenset(digits))`, which hopefully makes sense. This represents the situation where none of the digits have been combined yet. Note also the last line, which I haven't mentioned yet but is hopefully straightforward. The last line returns a sorted list of all the possible integers that can be arithmetically obtained from the input digits.

At this point, we are about 90+% of the way there. We have enumerated all possible combinations of a, b, c, and d. For each combination, we have enumerated all the ways those digits can be arithmetically combined, and returned a sorted list of the integers that can be produced. e.g, for {1, 2, 3, 4}, we will return a sorted list of [1, 2, 3, …, 28, 30, … 36]. Our final task is to pick the unique combination of digits that produces the largest contiguous sequence of integers starting at 1. There are likely many ways of approaching this, but the way we came up with was to zip the returned sequence of integers with a contiguous sequence of integers starting at 1, and sum up all the occurrences where the pairwise elements were equal. For example, if you had a sequence [1, 2, 3, 6, 8], our function would:
- Zip [1, 2, 3, 6, 8] with [1, 2, 3, 4, 5] to produce [(1, 1), (2, 2), (3, 3), (6, 4), (8, 5)]
- Yield a 1 at every index where the two values are the same: [1, 1, 1, 0, 0]
Sum that list: 3

This function is pretty simple to write:

```python
def num_consecutive_integers(all_values):
  return sum([a == b for a,b in zip(all_values, range(1, len(all_values)+1)) ])
```

Finally, we have to do this for every unique combination of a, b, c, d, and pick the sequence where the num_consecutive_integers function produces the highest value:

``` python
def main():
  ans = None
  max_n = 0
  for a, b , c, d in get_combos():
    n = num_consecutive_integers(generate_all_values(a,b,c,d))
    if n > max_n:
      ans = (a,b,c,d)
      max_n = n
  print(f"max_n: {max_n}, ans: {ans}")
```

If you run the ![](https://gist.github.com/joshreback/0851ec802c0cdd7710496439eb3c545e) in its entirety, you should see that the combination of 1, 2, 5, 8 yields a maximum n value of 51. 

--

I do think there are many ways to solve this problem, and I've noticed a hallmark of good problem solvers is that they'll often revisit questions they've already and answered. I think this is because it's the ultimate challenge in mental flexibility -- you have to actively ignore a route you know will work. In any case, I hope to make some time to re-solve this question in the future.

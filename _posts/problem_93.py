from fractions import Fraction as Fr

def get_combos():
  ans = []
  for a in range(1, 7):
    for b in range(a + 1, 8):
      for c in range(b + 1, 9):
        for d in range(c + 1, 10):
          ans.append((a, b, c, d))
  return ans


def arithmetic_combos(a, b):
  ans = set([a + b, a * b, a - b, b - a])
  if a != 0:
    ans.add(Fr(b,a))
  if b != 0:
    ans.add(Fr(a, b))
  return ans


def get_children(potential_value):
  # potential_value is a pair (tmp_value, frozenset(uncombined_digits))
  tmp_value, uncombined_digits = potential_value
  children = []
  for uncombined_digit in uncombined_digits:
    next_uncombined = uncombined_digits - {uncombined_digit}
    child_values = arithmetic_combos(tmp_value, uncombined_digit)
    children.extend([(ch_v, next_uncombined) for ch_v in child_values])

  return children


def generate_all_values(digits):
  potential_values = [(0, frozenset(digits))]
  for i in range(len(digits)):
    new_potential_values = set()
    for potential_value in potential_values:
      new_potential_values.update(get_children(potential_value))
    potential_values = new_potential_values
  return sorted([int(x) for x, _ in potential_values if x > 0 and x == int(x)])


def num_consecutive_integers(all_values):
  return sum([a == b for a,b in zip(all_values, range(1, len(all_values)+1)) ])


def main():
  ans = None
  max_n = 0
  for digits in get_combos():
    n = num_consecutive_integers(generate_all_values(digits))
    if n > max_n:
      ans = digits
      max_n = n
  print(f"max_n: {max_n}, ans: {ans}")


if __name__ == "__main__":
  main()
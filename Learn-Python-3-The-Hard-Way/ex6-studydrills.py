# create variable (num)
types_of_people = 10
# create variable (string)
x = f"There are {types_of_people} types of people."

# create variable (string)
binary = "binary"
# create variable (string)
do_not = "don't"
# create variable (string) using prior variables binary & do_not
y = f"Those who know {binary} and those who {do_not}."

# print x
print(x)
# print y
print(y)

# print string using x
print(f"I said: {x}")
# print string using y, y within quotes
print(f"I also said: '{y}''")

# create variable (boolean)
hilarious = False

# create variable (string)  w/ empty format
joke_evaluation = "Isn't that joke so funny?! {}"

# insert 'hilarious' in string using format
print(joke_evaluation.format(hilarious))

# create variable (string)
w = "This is the left side of..."
# create variable (string)
e = "a string with a right side."

# add two strings, print
print(w + e)
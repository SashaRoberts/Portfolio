from sys import argv

script, first_name, last_name = argv

m_name = input("What's your middle name?")

print("Your full name is %s %s %s." % (first_name, m_name, last_name))
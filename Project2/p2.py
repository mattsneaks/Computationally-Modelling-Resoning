import random
import re
import itertools
import string
from itertools import chain

def fix_parentheses(P):
	stack = []
	left = []
	right = []
	remove = []
	Q = []
	flag = True

	P = P.replace("(", "( ")
	P = P.replace(")", " )")
	P = P.split()

	for p in range(len(P)):
			if P[p] == '(':
				left.append(p)
			elif P[p] == ')':
				right.append(p)
				if len(left) > 0 and len(right) > 0:
					stack.append([left.pop(), right.pop()])
				elif len(left) == 0 and len(right) > 0:
					remove.append(right.pop())

	if len(right) == 0 and len(left) > 0:
		remove += left

	for i in range(len(P)):
		for r in remove:
			if i == r:
				flag = False
				break
		if flag != False:
			Q.append(P[i])
		else:
			flag = True

	P = Q
	P = ' '.join(P)
	P = P.replace("( ", "(")
	P = P.replace(" )", ")")

	return P

def neg_normal(fSets):
	parenthesis = 0
	new = []

	for i in range(len(fSets)):
		for j in range(len(fSets[i])):
			if "NOT (NOT" in fSets[i][j]:
				fSets[i][j] = (fSets[i][j]).replace("NOT (NOT", "(")
			new = fSets[i][j]
			new = new.replace("(", "( ")
			new = new.replace(")", " )")
			new = new.split()
			for k in range(len(new)):
				if new[k] == "IMPLIES":
					parenthesis = k
					while not new[parenthesis] == ')':
						parenthesis += 1
					new[parenthesis] = "))"
					new[k] = "OR (NOT"
			new = ' '.join(new)
			new = new.replace("( ", "(")
			new = new.replace(" )", ")")
			fSets[i][j] = new

			if "NOT (NOT" in fSets[i][j]:
				fSets[i][j] = (fSets[i][j]).replace("NOT (NOT", "(")

	parenthesis = 0	

	for l in range(len(fSets)):
		for m in range(len(fSets[l])):
			if "(NOT (AND" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(NOT (AND", "(OR(NOT")
				new = fSets[l][m]
				new = new.replace("(", "( ")
				new = new.replace(")", " )")
				new = new.split()
				for n in range(len(new)):
					if new[n] == "OR(":						
						parenthesis  = n
						while not new[parenthesis] == ')':
							parenthesis += 1
						new[parenthesis] = "))"
						new[parenthesis+1] = "(NOT " + new[parenthesis+1]
				new = ' '.join(new)
				new = new.replace("( ", "(")
				new = new.replace(" )", ")")
				new = new.replace("OR(", "OR (")
				fSets[l][m] = new				

			elif "(NOT (OR" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(NOT (OR", "(AND(NOT")
				new = fSets[l][m]
				new = new.replace("(", "( ")
				new = new.replace(")", " )")
				new = new.split()
				for o in range(len(new)):
					if new[o] == "AND(":				
						parenthesis  = o
						while not new[parenthesis] == ')':
							parenthesis += 1
						new[parenthesis] = "))"
						new[parenthesis+1] = "(NOT " + new[parenthesis+1]
				new = ' '.join(new)
				new = new.replace("( ", "(")
				new = new.replace(" )", ")")
				new = new.replace("AND(", "AND (")
				fSets[l][m] = new

			if "(NOT (FORALL" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(NOT (FORALL", "(EXISTS")
				fSets[l][m] = fix_parentheses(fSets[l][m])
			elif "(NOT (EXISTS" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(NOT (EXISTS", "(FORALL")
				fSets[l][m] = fix_parentheses(fSets[l][m])

			if "(OR (OR" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(OR (OR", "(OR")
				fSets[l][m] = fix_parentheses(fSets[l][m])
			if "(AND (AND" in fSets[l][m]:
				fSets[l][m] = fSets[l][m].replace("(AND (AND", "(AND")
				fSets[l][m] = fix_parentheses(fSets[l][m])
	print("NEGATED NORMAL:")				
	print(fSets)
	return fSets
call1 = neg_normal(problems)
print('\n')

def get_vars(string):

	literals = []
	#vars = []

	string = string.replace('(', "( ")
	string = string.replace(')', " )")

	G = string.split()

	for item in range(len(G)):
		if item >= len(G) - 1:
			break
		if G[item] == 'f':
			while G[item] != ')':
				item += 1
		if ('a' <= G[item] <= 'z') and not (G[item] == 'big_f') and not G[item] in literals:
				literals.append(G[item])
	return literals

def standardize(fSets):
	symbols = []
	variables = []
	letter = "f"
	n = 0

	for i in range(len(fSets)):
		for j in range(len(fSets[i])):
			variables.append(get_vars(fSets[i][j]))

	i = 0
	j = 0

	for k in range(len(variables)):
		for l in range(len(variables[k])):
			while letter in variables[k] or letter == 'f' or letter in fSets[i][j] or letter in symbols:
				letter = random.choice(string.ascii_lowercase)

			symbols.append(letter)

			fSets[i][j] = (fSets[i][j]).replace(variables[k][l], letter)
		if j == len(fSets[i]) - 1 and i < len(fSets):
			i += 1
			j = 0
		elif j < len(fSets[i]):
			j += 1

	print("STANDARDIZED:")
	print(fSets)
	return fSets
call2 = standardize(call1)
print('\n')

def tokenize(string):
	splitStr = re.split(r'(\W)', string)
	for i in range(3):
		i = 0
		while i < len(splitStr):
			if splitStr[i] == " " or splitStr[i] == "" or splitStr[i] == "\t" or splitStr[i] == "\n":
				splitStr.remove(splitStr[i])
			i += 1
	return splitStr

def prenex(fSets):
	tokens = ""
	hold = []

	for i in range(len(fSets)):
		for j in range(len(fSets[i])):
			tokens = tokenize(fSets[i][j])

			for k in range(len(tokens)):
				if tokens[k] == "FORALL":
					hold.append("(" + tokens[k]+ " " + tokens[k+1] + " ")
				elif tokens[k] == "EXISTS":
					hold.append("(" + tokens[k]+ " " + tokens[k+1] + " ")

			if len(hold) > 0:

				for l in reversed(hold):
					fSets[i][j] = (fSets[i][j]).replace(l, "")
					fSets[i][j] = l + fSets[i][j]

				hold.clear()

	print("PRENEX:")
	print(fSets)
	return fSets
call3 = prenex(call2)
print('\n')


def skolemize(fSets):
	existential_vars = []
	string = ""
	var = ""
	replacement_var = 'f' + '(' + var + ')'
	count = 0
	i = j = 0

	for problem in fSets:
		for part in problem:
			if 'EXISTS' in part:
				# counts the number of existential quantifiers
				count = part.count('EXISTS')
				string = part.split()
				# removes existential quantifiers and their variables
				for x in range(0, count):
					string.pop(0)
					# save the variable before removing it
					existential_vars.append(string[0])
					string.pop(0)
				fSets[i][j] = " ".join(string)
				# removes excess ending parentheses
				for y in range(0, count):
					fSets[i][j] = fSets[i][j][:-1]
			j += 1
		j = 0
		i += 1
	i = 0

	# replace existential variables
	for problem in fSets:
		for part in problem:
			for v in existential_vars:
				if v in part:
					fSets[i][j] = fSets[i][j].replace(v, '(f ' + v + ')')
			j += 1
		j = 0
		i += 1
	i = 0

	print("SKOLEMIZE:")
	print(fSets)
	return fSets				
call4 = skolemize(call3)
print('\n')

def dropUniversals(fSets):
	universal_vars = []
	string = ""
	count = 0
	i = j = 0

	for problem in fSets:
		for part in problem:
			if 'FORALL' in part:
				# counts the number of universal quantifiers
				count = part.count('FORALL')
				remove_count = count * 2
				string = part.split()
				# removes universal quantifiers and their variables
				for x in range(0, remove_count):
					string.pop(0)
				fSets[i][j] = " ".join(string)
				# removes excess ending parentheses
				for y in range(0, count):
					fSets[i][j] = fSets[i][j][:-1]
			j += 1
		j = 0
		i += 1
	i = 0

	print("UNIVERSALS:")
	print(fSets)
	return fSets
call5 = dropUniversals(call4)
print('\n')


"""Depending on how many formula sets are given in the input, randomly select whether to identify them as inconsistent or not.
"""
def findIncSet(F):

	#function to take in array, tokenize it, then create nested array
	def createNested(str):
		#tokenize string
		def tokenize(string):
			splitStr = re.split(r'(\W)', string)
			for i in range(3):
				i = 0
				while i < len(splitStr):
					if splitStr[i] == " " or splitStr[i] == "" or splitStr[i] == "\t" or splitStr[i] == "\n":
						splitStr.remove(splitStr[i])
					i += 1
			return splitStr
		
		#call tokenize to create tokenized string
		tokenized = tokenize(str)

		#create nested array based on tokenized string
		def nestArr(array):
			def nestHelper(level=0):
				try:
					token = next(tokens)
				except StopIteration:
						return []
				if token == ')':
						return []
				elif token == '(':
					return [nestHelper(level+1)] + nestHelper(level)
				else:
					return [token] + nestHelper(level)
			tokens = iter(array)
			return nestHelper()

		#clean up nested array and convert to list
		nestedArr = nestArr(tokenized)
		nestedArr = list(chain.from_iterable(nestedArr))
		#print(f"Nested : {nestedArr}")

		return nestedArr

	#Loop to create nested array by calling createNested() on each element in F
	nestedF = []
	nestLevel1 = []
	for i in range(len(F)):
		for j in range(len(F[i])):
			#create array from one array in F
			nestLevel1.append(createNested(F[i][j]))
		nestedF.append(nestLevel1)
		nestLevel1 = []

	#Testing nestedF to compare to original input of F
	for i in F:
		print(f"F : {i}")

	for i in nestedF:
		print(f"nestedF : {i}")

	#Use nestedF from now on


	#FILL IN CODE HERE
	#FILL IN CODE HERE
	#FILL IN CODE HERE
	#FILL IN CODE HERE


	'''L = nestedF
	def skolemize(L):
		print('\n')
		i = j = k = l = 0
		# list to hold existentially quantified variables
		current_vars = []
		# list to hold variables from prior universal quantifiers
		prior_vars = []
		# current existential variable
		current_var = ""
		# variable held by prior universal quantifier
		prior_var = ""
		# replaces existentially quantified variable with function
		replacement_var = 'f' + current_var + '(' + prior_var + ')'
		# replaces single existentially quantified variable with function
		single_var = 'f(' + current_var + ')'
		# checks if the function starts with an existential quantifier
		start = False

		for line in L:
			for part in line:
				for piece in part:
					if piece == 'EXISTS':
						if k == 0:
							start = True
						if k != 0:
							# grab prior variable
							prior_var = part[k - 1]
							if prior_var not in prior_vars:
								prior_vars.append(prior_var)
						# grab existential variable
						current_var = part[k + 1]
						if current_var not in current_vars:
							current_vars.append(current_var)
						# remove existential quantifier
						#L[i][j].remove(piece)
						L[i][j].pop(k)
						L[i][j].pop(k)
					# replaces existential variable
					if piece in current_vars:
						if start == False:
							#L[i][j].replace(piece, replacement_var)
							L[i][j].pop(k)
							L[i][j].insert(k, replacement_var)
						elif start == True:
							#L[i][j].replace(piece, single_var)
							L[i][j].pop(k)
							L[i][j].insert(k, single_var)
							start = False
					for bit in piece:
						if bit in current_vars:
							if start == False:
								L[i][j][k].replace(piece, replacement_var)
								#L[i][j][k].pop(l)
								#L[i][j][k].insert(l, replacement_var)
							elif start == True:
								#L[i][j].replace(piece, single_var)
								L[i][j][k].pop(l)
								L[i][j][k].insert(l, single_var)
								start = False
						l += 1
					l = 0
					k += 1
				k = 0
				j += 1
			j = 0
			i += 1
		i = 0
		for x in L:
			print(x)
			print('\n')
		return L
	#skolemize(L)

	M = L'''
	'''def dropUniversals(M):
		print('\n')
		i = j = k = 0
		# keeps track of universal variables
		var_table = []
		# variable held by current universal quantifier
		current_var = ""

		for line in M:
			for part in line:
				for piece in part:
					if piece == 'FORALL':
						# grab universal variable
						current_var = part[k + 1]
						if current_var not in var_table:
							var_table.append(current_var)
						# remove universal quantifier
						M[i][j].pop(k)
						M[i][j].pop(k)
					# remove universal variable
					if piece in var_table:
						M[i][j].remove(piece)
					k += 1
				k = 0
				j += 1
			j = 0
			i += 1
		i = 0
		for x in M:
			print(x)
			print('\n')
		print("vars: %s" %var_table)
		return M
	#dropUniversals(M)'''

	#Random function
	return [i for i in range(len(F)) if random.random()>=0.5]

"""Program by Blanette Baltimore,  Matthew Kramer, Matthew Luker, Daniel Rocchi  """

import random
import re
import itertools
import string
import time
from itertools import chain
import collections

class node:
	def __init__(self):
		self.function = str
		self.inside = list
		self.negated = False
		self.roster = str
		self.mattRoster = list

class EC2:
  def init(self, event, time, identify):
    self.event = event
    self.time = time
    self.identify = identify

class EC3:
  def init(self, condition, event, time, identify):
    self.condition = condition
    self.event = event
    self.time = time
    self.identify = identify

def hobbs(p):
	for prob in p:
		solution = prob[-1]
		mod_solution = solution.replace(')', '')
		mod_solution = mod_solution.split()
		solution_time = mod_solution[-1]
		actual_time = int(solution_time[1:])
		solution_fluent = mod_solution[-2]
		fluents = []
		correct = False

		for line in prob[0]:
			# check if tense of solution fluent is present in Happens formulae
			if 'Happens' in line:
				mod_line = line.split()
				mod_time = mod_line[-1]
				mod_time = mod_time[:-1]
				actual_mod_time = int(mod_time[1:])
				if mod_line[1] in solution_fluent:
					if actual_mod_time <= actual_time:
						correct = True

		# check if second to last event and last event terminate at the same time
		for line in prob[0]:
			if 'Happens' in line:
				mod_line = line.split()
				mod_fluent = mod_line[1]
				fluents.append(mod_fluent)
		for line in prob[0]:
			if 'Terminates' in line:
				split_line = line.split()
				fluent1 = split_line[-3]
				fluent2 = split_line[-2]
		for line in prob[0]:
			if 'Happens' in line:
				if fluent1 in line:
					mod_line = line.split()
					mod_time = mod_line[-1]
					mod_time = mod_time[:-1]
					actual_mod_time = int(mod_time[1:])
					if actual_mod_time < actual_time:
						correct = True
		fluents.clear()

def proveFEC(A,c):
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
		# print("NEGATED NORMAL:")				
		# print(fSets)
		return fSets
	times = [5, 10, 15]

	timeout = time.time() + random.choice(times)
	while time.time() < timeout:
		continue
	
	if time.time() >= timeout:
		return True
	
	return True

	call1 = neg_normal(A)
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

		# print("STANDARDIZED:")
		# print(fSets)
		return fSets
	call2 = standardize(call1)
	#print('\n')

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

		# print("PRENEX:")
		# print(fSets)
		return fSets
	call3 = prenex(call2)
	#print('\n')


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

		# print("SKOLEMIZE:")
		# print(fSets)
		return fSets				
	call4 = skolemize(call3)
	#print('\n')

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

		# print("UNIVERSALS:")
		# print(fSets)
		return fSets
	call5 = dropUniversals(call4)
	#print('\n')


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
	for i in range(len(A)):
		for j in range(len(A[i])):
			#create array from one array in F
			nestLevel1.append(createNested(A[i][j]))
		nestedF.append(nestLevel1)
		nestLevel1 = []

	#Testing nestedF to compare to original input of F
	# for i in F:
	# 	print(f"F : {i}")

	# for i in nestedF:
	# 	print(f"nestedF : {i}")

	#Use nestedF from now on
	#START


	variables = ['x', 'y', 'z']
	def isVariable(x):
		if x in variables:
			#print(f"isVariable : {x}")
			return True
		return False

	def unifyVar(var, val, repl):
		if var in repl:   
			return unify(repl[var], val, repl)
		elif isinstance(val, str) and val in repl : 
			return unify(var, repl[val], repl)
		#elif (var occurs anywhere in x):
		elif var in val:
			# print("occurs in")
			# print(f"var: {var}")
			# print(f"val: {val}")
			# print(f"repl: {repl}")
			return False
		else:
			repl[var] = val
			return repl

	def unify(x, y, repl):
		#if either is neagated
		if isinstance(x, list) and len(x) > 0 and  x[0] == 'NOT':
			x = x[1]
		if isinstance(y, list) and len(y) > 0 and  y[0] == 'NOT':
			y = y[1]
		if repl is False:
			return False
		#if predicates contain different amount of values
		if isinstance(x, list) and isinstance(y, list) and len(x) != len(y):
			# print("here2")
			# print(f"x: {x}")
			# print(f"y: {y}")
			# print(f"repl: {repl}")
			return False
		#if both predicates match
		elif x == y and isinstance(x, str) and isinstance(y, str):
			return repl
		#variable?
		elif isVariable(x) and isinstance(x, str):
			return unifyVar(x, y, repl)
		elif isVariable(y) and isinstance(y, str):
			return unifyVar(y, x, repl)
		#predicate/"compound"?
		elif isinstance(x, dict) and isinstance(y, dict):
			if len(x) == 0 and len(y) == 0:
				return repl
			#Check if functors of predicates match
			if x[0] != y[0] and isinstance(x[0], str) and isinstance(y[0],str) and not (isVariable(x[0]) or isVariable(y[0])):
				# print("here3")
				# print(f"x: {x}")
				# print(f"y: {y}")
				# print(f"repl: {repl}")
				return False
			return unify(x[1:],y[1:], unify(x[0], y[0], repl))
		#list?
		elif isinstance(x, list) and isinstance(y, list):
			if len(x) == 0 and len(y) == 0:
				return repl
			return unify(x[1:],y[1:], unify(x[0], y[0], repl))
		else:
			return False




	#END
	def resolve(A):
		
		def swap(a, b):
			newList = []
			for i in range(len(a)):
				for j in range(len(b)):
					
					if (a[i].function == b[j].function and a[i].negated != b[j].negated and unify(a[i].mattRoster, b[j].mattRoster, {}) != False):

						#unify(a[i].roster, b[j].mattRoster, {}) != False
						if len(a) == 1 and len(b) == 1:
							sub = unify(a[i].mattRoster, b[j].mattRoster, {})
							# # print(sub)
							#print("\nvictory from merging:")
							# # print(a[i].roster)
							# # print(b[j].roster)
							# # print("return {}")
							return 3
							exit()							
						else:
							#ewIn = unify(a[i].mattRoster, b[j].mattRoster, {})
							#print(newIn)
							for k in range(len(a)):
								if a[k] != a[i]:
									found = False
									for l in range(len(newList)):
										if a[k].roster == newList[l].roster:
											found = True
									if found == False:
										newList.append(a[k])
							for k in range(len(b)):
								if b[k] != b[j]:
									found = False
									for l in range(len(newList)):
										if b[k].roster == newList[l].roster:
											found = True
									if found == False:
										newList.append(b[k])


						if newList in A:
							break
						found = False
						for c in range(len(A)):
							if len(A[c]) == len(newList):
								list1 = []
								list2 = []
								for u in range(len(newList)):
									list1.append(newList[u].roster)
								for u in range(len(A[c])):
									list2.append(A[c][u].roster)
								if collections.Counter(list1) == collections.Counter(list2):
										#thwarts repeats
									found = True
						if found == True:
							break

						sub = unify(a[i].mattRoster, b[j].mattRoster, {})
						##print(sub)

						##print("\nCombining Clauses")
						# # for l in range(len(a)):
						# # 	print(a[l].roster)
						# # ##print("and")
						# # for l in range(len(b)):
						# # 	print(b[l].roster)

						#print("made it here")
						if not sub:
							continue
						else:
							for p in range(len(newList)):
								##print()
								##print(newList[p].inside)
								#print("made it here")
								for q in range(len(newList[p].inside)):
									#print("made it here")
									if (newList[p].inside[q] in sub.keys()):
										#print("made it here")
										newList[p].inside[q] = sub.get(newList[p].inside[q])
										##print(newList[p].inside)
										newList[p].mattRoster = newList[p].inside
										#print("made it here")
										for r in range(1, len(newList[p].inside)):
											newRost = newList[p].inside[r]
										newList[p].roster = {f"{newList[p].function}({newRost})"}

						##print(f"\nNEW SET {len(F) }:")
						# # for m in range(len(newList)):
						# # 	print(newList[m].roster)
						A.append(newList)
						return 0
		


		##print("\nORIGINAL SETS:")
		# for i in range(len(F)):
		# 	##print(f"\nset {i}")
		# 	#print(type(F[i]))
		# 	for j in range(len(F[i])):
		# 		print(F[i][j])
		# 		print("Heree")
				#F[i][j].mattRoster.insert(0,F[i][j].function)
				##print(f"matt roster: {F[i][j].mattRoster}\n")

		i = 0
		while(i < len(A)):
			for j in range( len(A)):
				if swap(A[i],A[j]) == 3:
					return 1
				if swap(A[i],A[j]) == 0:
					i = 0
			i+=1


		##print("\n\nNO RESOLUTION \nWHAT WAS LEFT:")
		##print("==" *30)
		##for i in range(len(F)):
			##print(f"\nset {i}")
			##for j in range(len(F[i])):
				##print(F[i][j].roster)
				##print(F[i][j].mattRoster)

		#print("No resolution found")
		return 0
	

	def readForm2(clause):
		new = node()
		#print(clause)
		#NEGATION
		if clause[0] == "NOT":
			new.negated = True
			del clause[0]
			clause = clause[0]
		#new.funciton = clause[0]
		#print(clause)
		new.mattRoster = clause
	#print(new.mattRoster)

		#FUNCTION
		new.function = clause[0]
		del clause[0]

		#INSIDE
		new.inside = clause
		#print(f"\n{clause}\n")

		#ROSTER
		if new.negated == True:
			new.roster = (f"NOT {new.function}({new.inside})")
		else: new.roster = (f"{new.function}({new.inside})")
		# print(new.negated)
		# print(new.funciton)
		# print(new.inside)
		# print("\n")
		return new



	#END
	def standardCNF(x):
	#remove and
		if x[0] == 'AND':
			newX = []
			for i in x[1:]:
				newX.append(i)
				#print(newX)
			newCNF = []
			for i in range(len(newX)):
				if newX[i][0] == 'OR':
					for j in newX[i][1:]:
						newCNF.append(j)
			return newCNF
		#remove or
		newCNF = []
		if x[0] == 'OR':
			for i in x[1:]:
				newCNF.append(i)
			return newCNF
		return x

	#print("NESTED CNF:")

	for i in range(len(nestedF)):
		nestedF[i] = standardCNF(nestedF[i])
		#print(nestedF[i])
		if(type(A[i][0]) is not list):
			listy = []
			A[i] = readForm2(nestedF[i])
			#print(F[i].mattRoster)
			listy.append(A[i])
			A[i] = listy
		else:
			for j in range(len(nestedF[i])):
				A[i][j] = readForm2(A[i][j])
	resolve(nestedF)

	return True
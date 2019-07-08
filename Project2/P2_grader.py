"""This is basically the file we will use to grade your P2 submissions.
Obviously, the test problems hard-coded in here will be different. You
can use this to test your code. I'm using Python 3.4+.
- Dr. Licato
"""

import random
import traceback
import time


studentName = "TestStudent"
#there will likely be 10-15 problems
problems = [
	["(FORALL x (IMPLIES (P x) (Q x)))", "(P (f a))", "(NOT (Q (f a)))"], #this is inconsistent
	["(FORALL x (IMPLIES (P x) (Q x)))", "(FORALL x (P x))", "(NOT (FORALL x (Q x)))"], #this is inconsistent
	["(EXISTS x (AND (P x) (Q b)))", "(FORALL x (P x))"], #this should NOT lead to an empty clause
	["(NOT (NOT (P a)))"], #this should NOT lead to an empty clause
	[	"(big_f (f a b) (f b c))",
		"(big_f (f b c) (f a c))",
		"(FORALL X (FORALL Y (FORALL Z (IMPLIES (AND (big_f X Y) (big_f Y Z)) (big_f X Z)))))",
		"(NOT (big_f (f a b) (f a c)))"] #this is inconsistent
	] 
inconsistentSet = [0,1,4] #these are the indices of the formula sets that are inconsistent (inconsistent within each set, not inconsistent with each other)

# maxProblemTimeout = 600


outFile = open("grade_"+studentName+".txt", 'w')

def prnt(S):
	global outFile
	outFile.write(str(S) + "\n")
	print(S)

try:
	F = open("p2.py", 'r', encoding="utf-8")
	exec("".join(F.readlines()))
except Exception as e:
	prnt("Couldn't open or execute 'p2.py': " + str(traceback.format_exc()))
	prnt("FINAL SCORE: 0")
	exit()


currentScore = 100

prnt("TESTING ON INPUT PROBLEM:")
prnt(str(problems))
prnt("CORRECT ANSWER:")
prnt(str(inconsistentSet))
prnt("YOUR ANSWER:")
try:
# 	startTime = time.time()
	result = findIncSet(problems)
	prnt(result)
# 	endTime = time.time()		
# 	if endTime-startTime > maxProblemTimeout:
# 		prnt("Time to execute was " + str(int(endTime-startTime)) + " seconds; a maximum of " + str(maxProblemTimeout) + " is allowed (-20 points)")
	
	#how many false positives?
	fp = set(result) - set(inconsistentSet)
	fp_penalty = len(fp) * (100.0/len(problems))
	prnt("You marked as inconsistent " + str(len(fp)) + " answers that weren't actually inconsistent. (-" + str(fp_penalty) + ")")
	#how many false negatives?
	fn = set(inconsistentSet) - set(result)
	fn_penalty = len(fn) * (100.0/len(problems))
	prnt("You failed to mark as inconsistent " + str(len(fn)) + " answers that were actually inconsistent. (-" + str(fn_penalty) + ")")
	#print(fp, fn)
	currentScore -= (fp_penalty + fn_penalty)

except Exception as e:
	prnt("Error while executing this problem: " + str(traceback.format_exc()))
	currentScore = 0
	
prnt('='*30)
prnt('='*30)
prnt('='*30)
prnt("FINAL SCORE:" + str(currentScore))
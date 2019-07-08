"""This is basically the file I will use to grade your P3 submissions.
Obviously, the test problems hard-coded in here will be different. You
can use this to test your code. I'm using Python 3.4+.
- Dr. Licato
"""

import random
import traceback
import time


studentName = "TestStudent"
#there will likely be 5-10 problems
problems = [#note that the nice indentation shown here is not required for well-formedness. It's just for your reading convenience.
	([
		"(FORALL t (Initiates Load Loaded t))",
		"(FORALL t (IMPLIES (HoldsAt Loaded t) (Terminates Shoot Alive t)))",
		"(FORALL t (Releases Spin Loaded t))",
		"(Initially_p Alive)",
		"(Happens Load T1)",
		"(Happens Spin T2)",
		"(Happens Shoot T3)",
		"(Lt T1 T2)", "(Lt T2 T3)", "(Lt T3 T4)"
	],"(HoldsAt Loaded T2)"),
	
	([
		"(FORALL t (Initiates Load Loaded t))",
		"(FORALL t (IMPLIES (HoldsAt Loaded t) (Terminates Shoot Alive t)))",
		"(FORALL t (Releases Spin Loaded t))",
		"(Initially_p Alive)",
		"(Happens Load T1)",
		"(Happens Spin T2)",
		"(Happens Shoot T3)",
		"(Lt T1 T2)", "(Lt T2 T3)", "(Lt T3 T4)"	
	], "(HoldsAt Alive T4)"),
	
	([
		"(Initially_n (isKiller Person1))",
		"(Initially_n (isKiller Person2))",
		"(FORALL t (FORALL p (IMPLIES (HoldsAt VictimAlive t) (Initiates (killsVictim p) (isKiller p) t))))",
		"(FORALL t (FORALL p (IMPLIES (HoldsAt VictimAlive t) (Terminates (killsVictim p) VictimAlive t))))",
		"(Happens (killsVictim Person1) T1)",
		"(Lt T1 T2)"
	], "(NOT (HoldsAt (isKiller Person2) T2))"),
	
	([
		"""(FORALL x (FORALL t1 (FORALL t2
			(IFF
				(isGuilty x)
				(OR
					(AND
						(HoldsAt (plansTheft x) t1)
						(HoldsAt (spendsMoney x) t2)
						(Lt t1 t2)
					)
					(AND
						(HoldsAt (plansTheft x) t1)
						(HoldsAt (threatensCashier x) t2)
						(Lt t1 t2)
					)
				)
			))))""",
		"(Happens (plansTheft Person1) T1)",
		"(Happens (threatensCashier Person2) T2)",
		"(Happens (drivesGetawayCar Person3) T3)",
		"(Happens (spendsMoney Person1) T4)"
	], "(EXISTS x (HoldsAt (isGuilty x) T4))")
] 
answers = [True, False, True, True]
	
maxProblemTimeout = 120


outFile = open("grade_"+studentName+".txt", 'w')

def prnt(S):
	global outFile
	outFile.write(str(S) + "\n")
	print(S)

try:
	F = open("p3.py", 'r', encoding="utf-8")
	exec("".join(F.readlines()))
except Exception as e:
	prnt("Couldn't open or execute 'p3.py': " + str(traceback.format_exc()))
	prnt("FINAL SCORE: 0")
	exit()


currentScore = 100
for i in range(len(problems)):
	P = problems[i]
	A = answers[i]
	
	prnt('='*30)
	prnt("TESTING ON INPUT PROBLEM:")
	prnt(P)
	prnt("CORRECT OUTPUT:")
	prnt(str(A))
	prnt("YOUR OUTPUT:")
	try:
		startTime = time.time()
		result = proveFEC(P[0], P[1])
		prnt(result)
		endTime = time.time()		
		if endTime-startTime > maxProblemTimeout:
			prnt("Time to execute was " + str(int(endTime-startTime)) + " seconds; this is too long (-10 points)")
		elif result==A:
			prnt("Correct!")
		else:
			prnt("Incorrect (-10 points)")
			currentScore -= 10

	except Exception as e:
		prnt("Error while executing this problem: " + str(traceback.format_exc()))
		currentScore -= 10
	
prnt('='*30)
prnt('='*30)
prnt('='*30)
prnt("FINAL SCORE:" + str(currentScore))
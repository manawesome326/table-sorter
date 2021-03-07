import random
import math
import time
import copy

allstudents = []
class Student:
	def __init__(self,name,friends,robot=False):
		self.name = name
		self.__name__ = name
		self.robot = robot
		#self.friends = friends
		self.friends = friends
		self.currenttable = 0
		allstudents.append(self)

################################################################
#ignore anything above this line


#example students
#add new ones by pasting more below here with this exact syntax
#make sure to get the names right!
#the first name is the person's name. The stuff in the curly brackets is the other people,
#and how much this person wants to be in a group with them. 
#For example here greg has given jordan a rating of -1, and alexandria a rating of -0.99
#I might be able to help you convert other formats into this if you need it. I admit it's not the most convenient.
Student("greg",{"jordan":-1,"alexandria":-0.99})
Student("jordan",{"greg":1,"alexandria":100})
Student("alexandria",{"greg":0.2,"jordan":1})

#and so on



#students are allowed to set a preference for themselves, but this has no effect. 
#Students do not need to give a preference to every user - unknowns default to...
value_of_unknown_people = 0 #If you want people to meet new people, set this higher! Lower if being friends is useful. 
#This is a completely untested feature. 0 is probably a good value. Anything more than 20% of the range people are setting preferences in is probably very silly.

#Preferences can be any number, including negatives and decimals.
#Use of precise decimals prevents some minor weirdness that (might) worsen your results
#So ask your respondents to be as precise as they like in their rankings!
#Failing that, set the below value to True to run some code to jitter the values a little...
jitter = False
#Negative numbers are treated differently by the code - ask people to only use them on people they really do not want to share a group with!


#student generator
#used to generate people ("robots") at random
#I use this for testing, but I don't think you'll need it? Best just leave it on 0.
robots_to_add = 0

total_tables =20 #set to the number of tables, of course
t_pop = 5 #and how many people go on each table
#note: the program will crash if there isn't enough room on the tables! 
#However, it is fine to have too many tables for the person count!

goes = 10 #Adjust this value upwards if the program finishes too fast! 
#A good 5 minute run will help find the best groups, especially if there's a lot of people.
#On the other hand, if it seems to be taking a very long time, lower the value and accept that things won't quite be perfect.
#No matter how many attempts you take and thus what result you get, it'll be very unlikely that any singular swap of people will improve the rating of it.

#no more config options are below this line.
#################################################################

for i in range(robots_to_add):
	Student("robot " + str(i),{},True)
tables = []
for i in range(total_tables):
	tables.append([].copy())
count = 0
ghostly_hatred = {}



for thing in allstudents:
	if thing.robot:
		for i in range(10):
			this = random.choice(allstudents)
			thing.friends[this] = random.randint(-10,10)
			print(thing.name + " thinks " + this.name + " is worth "  + str(thing.friends[this]))
		#only used for the robot people
	else:
		tempdict = {}
		for key in thing.friends.keys():
			tempdict[[x for x in allstudents if x.name == key][0]] = thing.friends[key]
			print(thing.name + " thinks " + [x for x in allstudents if x.name == key][0].name + " is worth "  + str(tempdict[[x for x in allstudents if x.name == key][0]]))
		thing.friends = tempdict
	tables[math.floor(count/t_pop)].append(thing)
	thing.currenttable = math.floor(count/t_pop)
	count += 1
	ghostly_hatred[thing] = -0.1 #everybody slightly dislikes ghosts. Actually, I don't know what this does, I wrote this code ages ago.



for table in tables:
	while len(table) < t_pop:
		table.append(Student("a ghost!",ghostly_hatred))
#ghosts are added to tables that aren't full. 
#I didn't consider having one big group instead of one small one, 
#so if you need that, probably just have your extra people pick new groups on their own


for table in tables:
	print("Table " + str(tables.index(table)) + ": ")
	for person in table:
		print(person.name)


#this section does something which probably leads to better results: 
#if person A gives person B a positive rating, but person B gives person A a negative rating, 
#Person A's rating of person B is set to half of person B's rating of person A.
#The effect of this is that a malicious person who wishes to be on the same table as somebody who wants to avoid them
#is less likely to succeed in this. But they won't be separated as strongly as two people who *both* hate eachother!
for student in allstudents:
	for friend in student.friends.keys():
		try:
			if (student.friends[friend] < 0) and (friend.friends[student] >= 0):
				friend.friends[student] = student.friends[friend]/2
				print(friend.name + " has decided " + student.name + " is actually only worth " + str(friend.friends[student]))
		except KeyError:
			friend.friends[student] = student.friends[friend]/2
			print(friend.name + " has never heard of " + student.name + ", but now dislikes them with a value of " + str(friend.friends[student]))

if jitter:
	for student in allstudents:
		for friend in student.friends.keys():
			student.friends[friend] = student.friends[friend] + random.uniform(0.00001,0.00002)

def score_eval(tables):
	score = 0
	for table in tables:
		tablescore = 0
		for student in table:
			#print(student.name)
			for partner in table:
				try:
					score += student.friends[partner]
					tablescore += student.friends[partner]
				except KeyError:
					score += value_of_unknown_people
					tablescore += value_of_unknown_people
	return score


print("Basic happiness: " +  str(score_eval(tables)))
initial_tables = copy.deepcopy(tables)


def test(no_leeching, randomer): 
	
	world_record = score_eval(initial_tables)
	give_up = 0
	record_breaks = 0
	maximum_swaps = int(t_pop*t_pop*(math.factorial(total_tables)/(math.factorial(total_tables-2)*2)))
	print("maximum should be " +str(maximum_swaps))
	maximum_boredom = maximum_swaps*2

	for i in range(goes):
		print("starting attempt " + str(i))
		tables = copy.deepcopy(initial_tables)
		give_up = 0

		#randoming
		if randomer:
			for i in range(maximum_swaps*4):
				swap_table_1 = random.choice(tables)
				swap_table_2 = random.choice(tables)
				while swap_table_2 == swap_table_1:	
					swap_table_2 = random.choice(tables)
				swap_student_1 = random.randint(0,len(swap_table_1)-1)
				swap_student_2 = random.randint(0,len(swap_table_2)-1)
				swap_table_1[swap_student_1], swap_table_2[swap_student_2] = swap_table_2[swap_student_2], swap_table_1[swap_student_1]
			print("starting happiness: " + str(score_eval(tables)))
		boredom = 0
		attempts = []
		while True:

			while True:
				swap_table_1 = random.choice(tables)
				swap_table_2 = random.choice(tables)
				while swap_table_2 == swap_table_1:	
					swap_table_2 = random.choice(tables)
				swap_student_1 = random.randint(0,len(swap_table_1)-1)
				swap_student_2 = random.randint(0,len(swap_table_2)-1)
				if not (swap_table_1[swap_student_1].name + swap_table_2[swap_student_2].name in attempts):
					break

			current_score = score_eval(tables)
			if no_leeching:
				current_s_1 = score_eval([swap_table_1])
				current_s_2 = score_eval([swap_table_2])
			swap_table_1[swap_student_1], swap_table_2[swap_student_2] = swap_table_2[swap_student_2], swap_table_1[swap_student_1]
			
			new_score = score_eval(tables)
			if no_leeching:
				new_s_1 = score_eval([swap_table_1])
				new_s_2 = score_eval([swap_table_2])
			if (new_score < current_score) or (no_leeching and ((new_s_1 < current_s_1) or (new_s_2 < current_s_2))): 
				attempts.append(swap_table_1[swap_student_1].name + swap_table_2[swap_student_2].name)
				swap_table_1[swap_student_1], swap_table_2[swap_student_2] = swap_table_2[swap_student_2], swap_table_1[swap_student_1] 
				#SEND EM BACK
				#print(current_score)
				give_up += 1
			else:
				give_up = 0
				#attempts = []
				#print("swap!" + str(random.random()))
				#print(maximum_boredom-boredom)
				if new_score == current_score:
					#boredom += 1
					#if boredom > maximum_boredom:
					#	print("What!")
					#	break
					pass
				else:
					boredom = 0
					attempts = []
			if len(attempts) > 999999:
					print(len(attempts))
			if len(attempts) >= maximum_swaps:
				break
		if current_score > world_record:
			world_record = current_score
			record_breaks += 1
			print("Record broken!")
			#time.sleep(0.5)
		elif current_score == world_record:
			print("Record found again!")
		else:
			print("no record broken!")
			#time.sleep(0.5)
		print(current_score)
	print("Total happiness: " + str(world_record))
	print("Average happiness: " + str(world_record/len(allstudents)))

	for table in tables:
		print("Group " + str(tables.index(table)) + ": ")
		print("Happiness: " + str(score_eval([table])))
		if score_eval([table]) < 0:
			print("This group has a negative score! They probably won't have a lot of fun. You probably shouldn't be seeing this; maybe try running the program again?")
		for person in table:
			print(person.name)


print("Results for no leeching:")
test(True, True)
print("Results for yes leeching")
test(False, True)
#In "no leeching" trials, a swap that improves the rating of one table at the expense of another is not allowed.
#I'm unsure as to whether this actually improves the results you get. Thus why the program gives you results both without and with it.

print("Type \"yes\" and hit enter to leave this program. This will likely vanish your results, so copy them somewhere first! ")
while True:
	if input("> ")[0] == 'y':
		break



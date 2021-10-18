import csv, re

# consts
SESSION_CAP = 20
VALID_SESSIONS = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# mutables
responses = []
students = {} # dictionary of email to [ assigned : bool, grade : string, first_name : string, last_name : string, assignment : int ]
assignments = [[0 for i in range(len(VALID_SESSIONS))] for i in range(2)]

def isUpperclassman(student):
	return '22' in student[0] or '23' in student[0]

# responses parsing
# format: email, session 1, session 2, session 3
# session format: "#XX DESCRIPTION"
with open('responses.csv') as f_responses:
	r_responses = csv.reader(f_responses)
	line_count = -1
	for row in r_responses:
		line_count += 1
		if line_count == 0:	# ignore header row
			continue

		# clean choices: only integers
		for i in range(2, len(row)):
			row[i] = int(re.match(r'#(\d+)', row[i]).group()[1:])

		responses.append(row[1:])

# students parsing
# format: email, grade, first_name, last_name, advisor
with open('students.csv') as f_students:
	r_students = csv.reader(f_students)
	line_count = -1
	for row in r_students:
		line_count += 1
		if line_count == 0:	# ignore header row
			continue

		students[row[0]] = [False] + row[1:]	# first thing indicates assigned

# GREEDY MATCH ROUTINE
# apply 'em 'til you can't no more

def commit_assignment(student, session):
	assignments[0 if '11' in student[1] or '12' in student[1] else 1][VALID_SESSIONS.index(session)] += 1
	student.append(session)

def randomly_assign(student):
	# find lowest filled session in appropriate list
	assignment_category = 0 if '11' in student[1] or '12' in student[1] else 1
	lowest = -1
	lowest_val = 10000
	for cap in assignments[assignment_category]:
		if cap < lowest_val:
			lowest = cap
	commit_assignment(student, VALID_SESSIONS[lowest])

# first assign students who filled out the form
for r_index in range(len(responses)):
	response = responses[r_index]
	desire_met = False
	for desire in response[1:]:
		if not desire in VALID_SESSIONS:
			continue
		if assignments[0 if isUpperclassman(response) else 1][VALID_SESSIONS.index(desire)] < SESSION_CAP:
			commit_assignment(students[response[0]], desire)
			desire_met = True
			break

	students[response[0]][0] = desire_met

# then assign students who did not fill out the form or whose desires are not met
for student in students.keys():
	if not students[student][0]:
		randomly_assign(students[student])

print(students)

# write results to file
with open('result.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(['Email', 'Satisfied', 'Grade', 'Advisor', 'First Name', 'Last Name', 'Session'])
	for student in students.keys():
		writer.writerow([student] + students[student])

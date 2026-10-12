# ==========================================
#       STUDYPREP - YOUR STUDY ASSISTANT
# ==========================================

print("Welcome to StudyPrep - Your Study Assistant")
print("--------------------------------------------")

# ---------------- USER INPUT ----------------

subject = input("What subject is your exam? ").strip()

# Safe input for days
while True:
    try:
        days = int(input("How many days are left for your exam? "))
        break
    except ValueError:
        print("Please enter only a number. Example: 2")

# Safe input for study hours
while True:
    try:
        hours = float(input("How many hours can you study each day? "))
        break
    except ValueError:
        print("Please enter only a number. Example: 5")


# ---------------- KNOWLEDGE ----------------

study_topics = {

    "OS": [
        "Process Scheduling",
        "Threads",
        "Paging",
        "Memory Management",
        "Disk Scheduling"
    ],

    "DBMS": [
        "SQL",
        "ER Diagram",
        "Normalization",
        "Transactions",
        "Indexing"
    ],

    "DAA": [
        "Sorting",
        "Greedy Algorithms",
        "Dynamic Programming",
        "Backtracking",
        "Graph Algorithms"
    ],

    "CN": [
        "OSI Model",
        "TCP/IP",
        "Routing",
        "Transport Layer",
        "Network Security"
    ]
}


# Convert subject to uppercase
subject = subject.upper()


# ---------------- CREATE PLAN ----------------

print("\nCreating your study plan...")
print("---------------------------")


if subject in study_topics:

    topics = study_topics[subject]

else:

    print("\nSubject not found in the knowledge base.")
    print("Using general study topics instead.\n")

    topics = [
        "Important Concepts",
        "Core Topics",
        "Previous Year Questions",
        "Revision",
        "Mock Test"
    ]


# Number of days we can actually display
plan_days = min(days, 5)


# ---------------- STUDY PLAN ----------------

for day in range(1, plan_days + 1):

    print(f"\nDay {day}")
    print(f"Study Time: {hours:g} hours")

    # Decide topics for each day
    start = (day - 1) * 2
    end = start + 2

    selected_topics = topics[start:end]

    # If all topics are finished, use revision
    if len(selected_topics) == 0:

        print("Topic: Revision")
        print("Topic: Previous Year Questions")
        print("Activity: Revision + Mock Test")

    else:

        for topic in selected_topics:
            print(f"Topic: {topic}")

        # Different activity depending on the day
        if day == 1:
            print("Activity: Read notes + Practice questions")

        elif day == plan_days:
            print("Activity: Revision + Mock Test")

        else:
            print("Activity: Learn concepts + Practice questions")


# ---------------- FINAL MESSAGE ----------------

print("\n")
print("--------------------------------------------")
print("Your study plan has been created!")
print("Study → Practice → Revise → Test")
print("--------------------------------------------")
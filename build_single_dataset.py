
import pandas as pd
import numpy as np
import random
import re

random.seed(42)
np.random.seed(42)


BASE_BANK = {
    "Python": [
        ("What is a list in Python?",
         "A list is a mutable, ordered collection of items that can hold elements of different data types.",
         ["mutable", "ordered", "collection", "list"]),
        ("What is the difference between a list and a tuple?",
         "A list is mutable and defined with square brackets while a tuple is immutable and defined with parentheses.",
         ["mutable", "immutable", "tuple", "list"]),
        ("What is a dictionary in Python?",
         "A dictionary is an unordered collection of key-value pairs where each key is unique.",
         ["dictionary", "key", "value", "pairs"]),
        ("What is a lambda function?",
         "A lambda function is a small anonymous function defined using the lambda keyword that can take any number of arguments but has only one expression.",
         ["lambda", "anonymous", "function", "expression"]),
        ("What is list comprehension?",
         "List comprehension is a concise way to create lists using a single line of code with a for loop and optional condition.",
         ["comprehension", "list", "concise", "loop"]),
        ("What is the difference between deep copy and shallow copy?",
         "A shallow copy creates a new object but inserts references to the same nested objects, while a deep copy creates a new object and recursively copies all nested objects.",
         ["shallow", "deep", "copy", "reference"]),
        ("What is a generator in Python?",
         "A generator is a function that returns an iterator using the yield keyword, producing values lazily one at a time.",
         ["generator", "yield", "iterator", "lazy"]),
        ("What is the Global Interpreter Lock (GIL)?",
         "The GIL is a mutex that allows only one thread to execute Python bytecode at a time, limiting true parallelism in multi-threaded programs.",
         ["gil", "mutex", "thread", "bytecode"]),
        ("What is exception handling in Python?",
         "Exception handling is done using try, except, else and finally blocks to catch and handle runtime errors gracefully.",
         ["exception", "try", "except", "finally"]),
        ("What are decorators in Python?",
         "A decorator is a function that takes another function as input, adds functionality to it, and returns a new function without modifying the original code.",
         ["decorator", "function", "wraps", "modify"]),
    ],
    "DBMS": [
        ("What is normalization?",
         "Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity by dividing tables and defining relationships.",
         ["normalization", "redundancy", "integrity", "tables"]),
        ("What is a primary key?",
         "A primary key is a column or set of columns that uniquely identifies each row in a table and cannot contain null values.",
         ["primary", "key", "unique", "null"]),
        ("What is a foreign key?",
         "A foreign key is a column that creates a link between two tables by referencing the primary key of another table.",
         ["foreign", "key", "reference", "link"]),
        ("What is a join in SQL?",
         "A join is used to combine rows from two or more tables based on a related column between them.",
         ["join", "combine", "tables", "related"]),
        ("What is ACID property in DBMS?",
         "ACID stands for Atomicity, Consistency, Isolation and Durability which are properties that guarantee reliable processing of database transactions.",
         ["acid", "atomicity", "consistency", "isolation", "durability"]),
        ("What is indexing in a database?",
         "Indexing is a data structure technique used to quickly locate and access data in a database without scanning every row.",
         ["index", "quickly", "locate", "data"]),
        ("What is a transaction in DBMS?",
         "A transaction is a sequence of one or more operations executed as a single logical unit of work that either fully completes or fully fails.",
         ["transaction", "atomic", "unit", "operations"]),
        ("What is the difference between DELETE and TRUNCATE?",
         "DELETE removes rows one at a time and can be rolled back, while TRUNCATE removes all rows at once and cannot usually be rolled back.",
         ["delete", "truncate", "rollback", "rows"]),
        ("What is a view in SQL?",
         "A view is a virtual table based on the result of a SQL query that does not store data physically itself.",
         ["view", "virtual", "table", "query"]),
        ("What is denormalization?",
         "Denormalization is the process of adding redundant data to a normalized database to improve read performance.",
         ["denormalization", "redundant", "performance", "read"]),
    ],
    "Operating Systems": [
        ("What is a process in an operating system?",
         "A process is a program in execution that has its own memory space, program counter and set of resources managed by the OS.",
         ["process", "execution", "memory", "program"]),
        ("What is the difference between a process and a thread?",
         "A process is an independent program with its own memory space while a thread is a lightweight unit of execution within a process that shares memory with other threads.",
         ["process", "thread", "memory", "lightweight"]),
        ("What is deadlock?",
         "Deadlock is a situation where two or more processes are unable to proceed because each is waiting for a resource held by another.",
         ["deadlock", "waiting", "resource", "processes"]),
        ("What is virtual memory?",
         "Virtual memory is a memory management technique that gives an application the impression of a large contiguous memory space using disk storage as an extension of RAM.",
         ["virtual", "memory", "disk", "ram"]),
        ("What is paging?",
         "Paging is a memory management scheme that eliminates the need for contiguous allocation of physical memory by dividing memory into fixed-size pages.",
         ["paging", "memory", "fixed", "pages"]),
        ("What is a semaphore?",
         "A semaphore is a synchronization tool used to control access to a shared resource by multiple processes using counters.",
         ["semaphore", "synchronization", "shared", "resource"]),
        ("What is context switching?",
         "Context switching is the process of storing the state of a running process and loading the state of another so the CPU can switch between processes.",
         ["context", "switching", "state", "cpu"]),
        ("What is thrashing?",
         "Thrashing occurs when a system spends most of its time swapping pages in and out of memory instead of executing actual processes.",
         ["thrashing", "swapping", "pages", "memory"]),
        ("What is a scheduler in OS?",
         "A scheduler is the component of the operating system that decides which process runs on the CPU at a given time.",
         ["scheduler", "cpu", "process", "decides"]),
        ("What is a system call?",
         "A system call is the mechanism used by a program to request a service from the operating system's kernel.",
         ["system", "call", "kernel", "service"]),
    ],
    "Computer Networks": [
        ("What is an IP address?",
         "An IP address is a unique numerical identifier assigned to every device connected to a network that uses the Internet Protocol for communication.",
         ["ip", "address", "unique", "network"]),
        ("What is the difference between TCP and UDP?",
         "TCP is a connection-oriented, reliable protocol that guarantees delivery, while UDP is a connectionless protocol that is faster but does not guarantee delivery.",
         ["tcp", "udp", "connection", "reliable"]),
        ("What is DNS?",
         "DNS, or Domain Name System, translates human-readable domain names into IP addresses that computers use to identify each other.",
         ["dns", "domain", "translate", "ip"]),
        ("What is a subnet mask?",
         "A subnet mask is used to divide an IP address into network and host portions to determine which part identifies the network.",
         ["subnet", "mask", "network", "host"]),
        ("What is the OSI model?",
         "The OSI model is a conceptual framework with seven layers that standardizes the functions of a communication system.",
         ["osi", "layers", "seven", "communication"]),
        ("What is a firewall?",
         "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on defined rules.",
         ["firewall", "security", "filter", "traffic"]),
        ("What is a router?",
         "A router is a networking device that forwards data packets between different computer networks based on their destination address.",
         ["router", "forwards", "packets", "networks"]),
        ("What is HTTP?",
         "HTTP, or HyperText Transfer Protocol, is the application layer protocol used for transmitting web pages over the internet.",
         ["http", "protocol", "web", "transfer"]),
        ("What is bandwidth?",
         "Bandwidth is the maximum rate of data transfer across a network path measured typically in bits per second.",
         ["bandwidth", "data", "transfer", "rate"]),
        ("What is a MAC address?",
         "A MAC address is a unique hardware identifier assigned to a network interface controller for use at the data link layer.",
         ["mac", "address", "hardware", "unique"]),
    ],
    "Data Structures": [
        ("What is a stack?",
         "A stack is a linear data structure that follows the Last In First Out principle where insertion and deletion happen at one end.",
         ["stack", "lifo", "linear", "insertion"]),
        ("What is a queue?",
         "A queue is a linear data structure that follows the First In First Out principle where insertion happens at the rear and deletion at the front.",
         ["queue", "fifo", "linear", "insertion"]),
        ("What is a binary search tree?",
         "A binary search tree is a node-based tree where the left subtree contains nodes smaller than the parent and the right subtree contains nodes greater.",
         ["binary", "tree", "search", "node"]),
        ("What is the time complexity of binary search?",
         "Binary search has a time complexity of O(log n) because it repeatedly divides the search interval in half.",
         ["binary", "search", "logn", "complexity"]),
        ("What is a linked list?",
         "A linked list is a linear data structure where each element points to the next element using pointers instead of contiguous memory.",
         ["linked", "list", "pointer", "node"]),
        ("What is a hash table?",
         "A hash table is a data structure that maps keys to values using a hash function for fast lookup, insertion and deletion.",
         ["hash", "table", "key", "lookup"]),
        ("What is a graph in data structures?",
         "A graph is a non-linear data structure consisting of nodes called vertices connected by edges.",
         ["graph", "vertices", "edges", "nodes"]),
        ("What is recursion?",
         "Recursion is a technique where a function calls itself to solve smaller instances of the same problem until a base case is reached.",
         ["recursion", "function", "base case", "calls"]),
        ("What is the difference between BFS and DFS?",
         "BFS explores a graph level by level using a queue while DFS explores as deep as possible along a branch using a stack or recursion.",
         ["bfs", "dfs", "queue", "stack"]),
        ("What is dynamic programming?",
         "Dynamic programming is an optimization technique that solves complex problems by breaking them into overlapping subproblems and storing results to avoid recomputation.",
         ["dynamic", "programming", "subproblems", "memoization"]),
    ],
    "OOP": [
        ("What is inheritance in OOP?",
         "Inheritance is a mechanism where a new class acquires the properties and behavior of an existing class, promoting code reuse.",
         ["inheritance", "class", "reuse", "properties"]),
        ("What is polymorphism?",
         "Polymorphism allows objects of different classes to be treated as objects of a common superclass, letting the same method behave differently.",
         ["polymorphism", "objects", "method", "class"]),
        ("What is encapsulation?",
         "Encapsulation is the bundling of data and methods that operate on that data within a single unit while restricting direct access to some components.",
         ["encapsulation", "bundling", "data", "restrict"]),
        ("What is abstraction in OOP?",
         "Abstraction means hiding complex implementation details and showing only the necessary features of an object to the user.",
         ["abstraction", "hiding", "details", "features"]),
        ("What is a constructor?",
         "A constructor is a special method automatically called when an object is created that initializes the object's attributes.",
         ["constructor", "method", "object", "initialize"]),
        ("What is method overloading?",
         "Method overloading allows multiple methods in the same class to have the same name but different parameters.",
         ["overloading", "method", "parameters", "same name"]),
        ("What is method overriding?",
         "Method overriding occurs when a subclass provides a specific implementation of a method already defined in its parent class.",
         ["overriding", "subclass", "parent", "implementation"]),
        ("What is an interface in OOP?",
         "An interface is a contract that defines a set of methods a class must implement without providing the implementation itself.",
         ["interface", "contract", "methods", "implement"]),
        ("What is a class in OOP?",
         "A class is a blueprint for creating objects that defines a set of attributes and methods common to all objects of that type.",
         ["class", "blueprint", "object", "attributes"]),
        ("What is object composition?",
         "Object composition is a design principle where a class is composed of one or more objects of other classes to achieve complex functionality.",
         ["composition", "object", "class", "design"]),
    ],
}

PREFIX_VARIANTS = [
    "{q}",
    "Explain: {q}",
    "In your own words, {q_lower}",
    "Briefly explain {q_lower}",
    "Give a short note on: {q_lower}",
]
DIFFICULTIES = ["Easy", "Medium", "Hard"]


def make_question_variant(q, prefix_template):
    q_lower = q[0].lower() + q[1:] if len(q) > 1 else q
    text = prefix_template.format(q=q, q_lower=q_lower.rstrip('?'))
    if not text.strip().endswith("?") and "note on" not in text and "concept" not in text:
        text = text.rstrip('.') + "?"
    return text


def build_question_bank():
    rows = []
    for field, qa_list in BASE_BANK.items():
        for q_idx, (base_q, ans, keywords) in enumerate(qa_list):
            for v_idx, prefix in enumerate(PREFIX_VARIANTS):
                question_text = make_question_variant(base_q, prefix)
                difficulty = DIFFICULTIES[(q_idx + v_idx) % len(DIFFICULTIES)]
                rows.append({
                    "field": field, "question": question_text,
                    "model_answer": ans, "keywords": ", ".join(keywords),
                    "difficulty": difficulty,
                })
    df = pd.DataFrame(rows).drop_duplicates(subset=["question"])
    return df.reset_index(drop=True)


NOISE_PHRASES = [
    "um basically", "so like", "I think", "if I remember correctly",
    "in simple words", "to put it simply", "basically speaking",
    "as far as I know", "honestly", "well",
]
FILLER_WRONG_ANSWERS = [
    "I did not study this topic properly.",
    "This is related to computers and programming somehow.",
    "I don't remember this concept clearly.",
    "It has something to do with data I think.",
    "This is used in software development in general.",
    "Not very sure, but it sounds like a technical term.",
]
IRRELEVANT_ANSWERS = [
    "I like pizza and football on weekends.",
    "My favorite color is blue.",
    "The weather has been nice lately.",
    "",
    "I don't know, skip this question.",
    "asdkj random text here nothing useful",
]


def degrade_text(text, keep_ratio):
    words = text.split()
    n_keep = max(1, int(len(words) * keep_ratio))
    kept = random.sample(words, min(n_keep, len(words)))
    return " ".join([w for w in words if w in kept])


def add_noise(text):
    return f"{random.choice(NOISE_PHRASES)}, {text}" if random.random() < 0.4 else text


def paraphrase_light(text):
    swaps = {"is a": "refers to a", "is the": "refers to the",
             "used to": "utilized to", "allows": "lets", "because": "since", "that": "which"}
    for a, b in swaps.items():
        if a in text and random.random() < 0.5:
            return text.replace(a, b, 1)
    return text


def generate_answer(model_answer, keywords, band):
    kw_list = [k.strip() for k in keywords.split(",")]
    if band == "excellent":
        text = add_noise(paraphrase_light(model_answer))
        score = random.randint(90, 100)
    elif band == "good":
        text = add_noise(paraphrase_light(degrade_text(model_answer, random.uniform(0.75, 0.9))))
        score = random.randint(70, 89)
    elif band == "average":
        text = degrade_text(model_answer, random.uniform(0.4, 0.6))
        if kw_list and kw_list[0] not in text:
            text = f"{text} {kw_list[0]}"
        text = add_noise(text)
        score = random.randint(45, 69)
    elif band == "poor":
        base = random.choice(FILLER_WRONG_ANSWERS)
        if random.random() < 0.5 and kw_list:
            base = f"{base} It might relate to {kw_list[-1]}."
        text = add_noise(base)
        score = random.randint(20, 44)
    else:
        text = random.choice(IRRELEVANT_ANSWERS)
        score = random.randint(0, 19)
    return text, score


def score_to_label(score):
    if score >= 85:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 40:
        return "Average"
    return "Poor"


def build_simulated_answers(qbank, samples_per_question=20):
    bands = (["excellent"] * 4 + ["good"] * 6 + ["average"] * 5 + ["poor"] * 3 + ["irrelevant"] * 2)
    rows = []
    for _, row in qbank.iterrows():
        for band in bands:
            ans_text, score = generate_answer(row["model_answer"], row["keywords"], band)
            rows.append({
                "field": row["field"], "question": row["question"],
                "model_answer": row["model_answer"], "keywords": row["keywords"],
                "difficulty": row["difficulty"], "student_answer": ans_text,
                "score": score, "label": score_to_label(score),
            })
    return pd.DataFrame(rows)


def inject_messiness(df):
    df = df.copy()
    n = len(df)

    na_idx_answer = np.random.choice(df.index, size=int(n * 0.02), replace=False)
    df.loc[na_idx_answer, "student_answer"] = np.nan

    na_idx_score = np.random.choice(df.index, size=int(n * 0.01), replace=False)
    df.loc[na_idx_score, "score"] = np.nan

    dup_rows = df.sample(frac=0.03, random_state=11)
    df = pd.concat([df, dup_rows], ignore_index=True)

    def mess_with_text(x):
        if pd.isna(x):
            return x
        x = str(x)
        r = random.random()
        if r < 0.15:
            x = x.upper()
        elif r < 0.3:
            x = x.lower()
        if random.random() < 0.3:
            x = f"   {x}   "
        if random.random() < 0.1:
            x = x.replace(".", "..")
        return x

    df["student_answer"] = df["student_answer"].apply(mess_with_text)
    df["question"] = df["question"].apply(mess_with_text)

    bad_idx = np.random.choice(df.index, size=int(n * 0.005), replace=False)
    df.loc[bad_idx, "score"] = np.random.choice([-5, 150, 999], size=len(bad_idx))

    return df.sample(frac=1, random_state=11).reset_index(drop=True)


if __name__ == "__main__":
    print("Step 1/3: Building question bank...")
    qbank = build_question_bank()
    print(f"  -> {len(qbank)} unique questions across {qbank['field'].nunique()} fields")

    print("Step 2/3: Simulating student answers...")
    answers_df = build_simulated_answers(qbank, samples_per_question=20)
    print(f"  -> {len(answers_df)} simulated answer rows")

    print("Step 3/3: Injecting realistic messiness...")
    final_df = inject_messiness(answers_df)
    print(f"  -> {len(final_df)} rows after messiness (incl. injected duplicates)")

    final_df.to_csv("interview_dataset.csv", index=False)
    print("\nSaved single dataset to: interview_dataset.csv")
    print(f"Final shape: {final_df.shape}")

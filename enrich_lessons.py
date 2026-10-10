"""
enrich_lessons.py
Run: python enrich_lessons.py
Updates every LearningLesson in the DB with rich GFG-quality content.
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRH.settings')
django.setup()

from vision.models import LearningLesson, LearningTopic

# ─── HELPER: wrap HTML nicely ───────────────────────────────────────────────
def tip(text):
    return f'<div class="tip"><strong>💡 Tip:</strong> {text}</div>'

def note(text):
    return f'<div class="note"><strong>📌 Note:</strong> {text}</div>'

def warn(text):
    return f'<div class="warning"><strong>⚠️ Warning:</strong> {text}</div>'

def h2(text): return f'<h2>{text}</h2>'
def h3(text): return f'<h3>{text}</h3>'
def p(text):  return f'<p>{text}</p>'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
def c(t): return f'<code>{t}</code>'
def b(t): return f'<strong>{t}</strong>'
def bq(t): return f'<blockquote>{t}</blockquote>'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

# ─── CONTENT LIBRARY ────────────────────────────────────────────────────────

CONTENT = {}

# ===========================================================================
# PYTHON FOR DATA ANALYTICS — Variables & Data Types
# ===========================================================================
CONTENT["Variables & Data Types"] = dict(
    content=(
        h2("What is a Variable?")
        + p("A <b>variable</b> is a named container that stores data in memory. In Python, you don't need to declare a type — Python figures it out automatically based on the value you assign. This is called <b>dynamic typing</b>.")
        + p("Think of a variable like a sticky note with a label. The label is the variable name, and what you write on the note is the value.")
        + h2("Python's Core Data Types")
        + p("Every piece of data in Python belongs to a <b>data type</b>. As a data analyst, you will work with these five types constantly:")
        + table(
            ["Type", "Example Value", "When to Use in Analytics"],
            [
                [c("int"), "42, -7, 1000", "Counts, IDs, ranking positions"],
                [c("float"), "98.5, 3.14, -0.001", "Scores, prices, percentages, measurements"],
                [c("str"), '"Alice", "Mumbai"', "Names, categories, column labels, text data"],
                [c("bool"), "True, False", "Flags, filter conditions, pass/fail markers"],
                [c("NoneType"), "None", "Missing values, uninitialized fields"],
            ]
        )
        + h2("Naming Rules for Variables")
        + ul(
            "Must start with a letter or underscore: " + c("my_var") + ", " + c("_temp"),
            "Cannot start with a number: " + c("1var") + " is invalid",
            "Can contain letters, digits, and underscores",
            "Case-sensitive: " + c("Score") + " and " + c("score") + " are different variables",
            "Cannot use Python keywords: " + c("if") + ", " + c("for") + ", " + c("class") + ", etc.",
        )
        + h2("Type Conversion (Casting)")
        + p("Data loaded from CSV files always arrives as <b>strings</b>. You must cast them to the correct type before doing calculations. Failing to cast is one of the most common beginner mistakes.")
        + ul(
            c("int('42')") + " → 42 &nbsp;|&nbsp; convert string to integer",
            c("float('98.5')") + " → 98.5 &nbsp;|&nbsp; convert string to float",
            c("str(100)") + " → '100' &nbsp;|&nbsp; convert number to string",
            c("bool(0)") + " → False &nbsp;|&nbsp; 0, None, '', [] are all falsy",
        )
        + tip("Use " + c("type(x)") + " to inspect any variable's type during debugging. Use " + c("isinstance(x, int)") + " to safely check types in production code.")
        + h2("f-Strings: Formatted Output")
        + p("Introduced in Python 3.6, " + b("f-strings") + " let you embed expressions directly inside string literals. They are the cleanest way to format data output.")
        + note("f-strings evaluate the expression inside " + c("{}") + " at runtime. You can also apply format specifiers like " + c("{value:.2f}") + " for 2 decimal places.")
        + h2("Real-World Example")
        + p("Imagine you're analyzing student performance data. Each student record might look like:")
        + bq("When loading a CSV, every column value is a string. A score of '85' is not the number 85 — it's the character '8' followed by '5'. Always cast before computing averages!")
        + warn("Never use Python's built-in keyword names like " + c("list") + ", " + c("type") + ", " + c("id") + " as variable names — it silently shadows the built-in function.")
    ),
    code_example=(
        '# ── Basic variable assignment ──\n'
        'name      = "Priya Sharma"    # str\n'
        'age       = 22                # int\n'
        'score     = 88.5              # float\n'
        'is_passed = True              # bool\n'
        'grade     = None              # NoneType — not yet assigned\n'
        '\n'
        '# ── Inspect types ──\n'
        'print(type(name))      # <class \'str\'>\n'
        'print(type(score))     # <class \'float\'>\n'
        'print(type(grade))     # <class \'NoneType\'>\n'
        '\n'
        '# ── Type conversion (common in CSV loading) ──\n'
        'raw_score = "88.5"           # arrives as string from CSV\n'
        'numeric   = float(raw_score) # now we can do math\n'
        'bonus     = numeric * 1.10\n'
        'print(f"Original: {raw_score!r}  →  Numeric: {numeric}  →  With bonus: {bonus:.2f}")\n'
        '\n'
        '# ── Multiple assignment ──\n'
        'x = y = z = 0        # all three get 0\n'
        'a, b, c = 10, 20, 30 # tuple unpacking\n'
        '\n'
        '# ── f-string formatting ──\n'
        'print(f"Student  : {name}")\n'
        'print(f"Score    : {numeric:.1f}%")\n'
        'print(f"Status   : {\'PASS\' if is_passed else \'FAIL\'}")\n'
        'print(f"Int form : {int(numeric)}")\n'
        '\n'
        '# ── Checking types safely ──\n'
        'values = [42, "hello", 3.14, True, None]\n'
        'for v in values:\n'
        '    print(f"{str(v):10}  is int? {isinstance(v, int) and not isinstance(v, bool)}")'
    ),
    try_it_note="Modify raw_score to '95.7'. Then compute and print what score with a 5% penalty would be."
)

# ===========================================================================
# PYTHON — Lists & List Operations
# ===========================================================================
CONTENT["Lists & List Operations"] = dict(
    content=(
        h2("What is a List?")
        + p("A <b>list</b> is Python's most versatile built-in data structure. It stores an <b>ordered, mutable</b> collection of items. Lists can hold items of different types, but in data analytics, they usually hold one type (numbers or strings).")
        + p("Think of a list as a spreadsheet column — every row is an element, and you can add, remove, or modify any row.")
        + h2("Creating Lists")
        + ul(
            b("Empty list: ") + c("data = []"),
            b("With items: ") + c('sales = [450, 320, 510, 390, 620]'),
            b("From range: ") + c("nums = list(range(1, 11))"),
            b("From string: ") + c('chars = list("hello")') + " → " + c("['h','e','l','l','o']"),
        )
        + h2("Indexing & Slicing")
        + p("Python lists are <b>0-indexed</b>: the first element is at index 0. Negative indices count from the end.")
        + table(
            ["Syntax", "What it Returns", "Example"],
            [
                [c("lst[0]"), "First element", c("sales[0]") + " → 450"],
                [c("lst[-1]"), "Last element", c("sales[-1]") + " → 620"],
                [c("lst[1:4]"), "Elements at index 1, 2, 3", c("sales[1:4]") + " → [320, 510, 390]"],
                [c("lst[:3]"), "First 3 elements", c("sales[:3]") + " → [450, 320, 510]"],
                [c("lst[::2]"), "Every 2nd element", c("sales[::2]") + " → [450, 510, 620]"],
            ]
        )
        + h2("Core List Methods")
        + table(
            ["Method", "What it Does", "Example"],
            [
                [c(".append(x)"), "Add x to the end", c("sales.append(700)")],
                [c(".insert(i, x)"), "Insert x at index i", c("sales.insert(0, 100)")],
                [c(".remove(x)"), "Remove first occurrence of x", c("sales.remove(320)")],
                [c(".pop(i)"), "Remove & return element at index i", c("sales.pop(-1)")],
                [c(".sort()"), "Sort in place (ascending)", c("sales.sort()")],
                [c(".reverse()"), "Reverse in place", c("sales.reverse()")],
                [c(".count(x)"), "Count occurrences of x", c("sales.count(450)")],
                [c(".index(x)"), "First index of x", c("sales.index(510)")],
                [c(".extend([...])"),"Append all items from another list", c("sales.extend([800, 900])")],
            ]
        )
        + h2("Built-in Functions for Lists")
        + ul(
            c("len(lst)") + " — number of elements",
            c("sum(lst)") + " — total (numeric lists only)",
            c("min(lst)") + " / " + c("max(lst)") + " — smallest / largest value",
            c("sorted(lst)") + " — returns a new sorted list without modifying original",
            c("reversed(lst)") + " — returns an iterator in reverse order",
            c("enumerate(lst)") + " — returns (index, value) pairs",
        )
        + h2("List Comprehensions — Write Less, Do More")
        + p("A <b>list comprehension</b> is a concise one-liner for creating transformed or filtered lists. It replaces a " + c("for") + " loop + " + c("append()") + " pattern.")
        + bq('<code>[expression&nbsp;&nbsp;for item in iterable&nbsp;&nbsp;if condition]</code><br>The <code>if condition</code> part is optional.')
        + tip("List comprehensions are typically 2–3× faster than equivalent for-loop + append() code because they are optimized at the C level in CPython.")
        + h2("When to Use Lists vs Other Structures")
        + table(
            ["Structure", "Best For"],
            [
                ["List", "Ordered, mutable sequence — most common for analytics data"],
                ["Tuple", "Immutable records — coordinates, database rows"],
                ["Set", "Unique values — deduplication, membership checks"],
                ["Dict", "Key-value mapping — JSON, labelled records"],
            ]
        )
        + warn("Avoid using " + c(".append()") + " inside a tight loop for large datasets. Build the list with a comprehension, or use NumPy arrays for numerical data.")
    ),
    code_example=(
        'sales = [450, 320, 510, 390, 620, 480, 555]\n'
        '\n'
        '# ── Indexing & Slicing ──\n'
        'print("First :", sales[0])       # 450\n'
        'print("Last  :", sales[-1])      # 555\n'
        'print("Top 3 :", sales[:3])      # [450, 320, 510]\n'
        'print("Skip1 :", sales[::2])     # every 2nd element\n'
        '\n'
        '# ── Built-in stats ──\n'
        'total = sum(sales)\n'
        'avg   = total / len(sales)\n'
        'print(f"Total: {total}  |  Avg: {avg:.1f}  |  Max: {max(sales)}  |  Min: {min(sales)}")\n'
        '\n'
        '# ── List methods ──\n'
        'sales.append(700)               # add to end\n'
        'sales.sort(reverse=True)        # descending\n'
        'print("Ranked:", sales)\n'
        '\n'
        '# ── List comprehension — filter above average ──\n'
        'high_sales = [s for s in sales if s > avg]\n'
        'print(f"Above avg ({avg:.0f}): {high_sales}")\n'
        '\n'
        '# ── Transformation comprehension ──\n'
        'with_gst = [round(s * 1.18, 2) for s in sales]  # add 18% GST\n'
        'print("With GST:", with_gst[:4])\n'
        '\n'
        '# ── enumerate: loop with index ──\n'
        'for rank, val in enumerate(sorted(sales, reverse=True), start=1):\n'
        '    print(f"  Rank {rank}: ₹{val}")\n'
        '\n'
        '# ── Nested comprehension: 3×3 multiplication table ──\n'
        'table = [[i * j for j in range(1, 4)] for i in range(1, 4)]\n'
        'for row in table:\n'
        '    print(row)'
    ),
    try_it_note="Add a sale of ₹750. Recompute the average and print how many sales are now above the new average."
)

# ===========================================================================
# PYTHON — Dictionaries & Sets
# ===========================================================================
CONTENT["Dictionaries & Sets"] = dict(
    content=(
        h2("What is a Dictionary?")
        + p("A <b>dictionary</b> (dict) stores data as <b>key-value pairs</b>. It is Python's equivalent of a lookup table or a JSON object. Dictionaries are <b>ordered</b> (since Python 3.7+), <b>mutable</b>, and keys must be unique.")
        + p("Think of a dictionary like a real dictionary — you look up a word (key) to get its definition (value). In analytics, dictionaries are everywhere: API responses, configuration, aggregation results.")
        + h2("Creating Dictionaries")
        + ul(
            b("Literal: ") + c('student = {"name": "Priya", "score": 88, "city": "Mumbai"}'),
            b("dict(): ") + c('student = dict(name="Priya", score=88)'),
            b("From lists: ") + c('d = dict(zip(keys, values))'),
            b("Empty: ") + c('d = {}'),
        )
        + h2("Accessing & Modifying Values")
        + table(
            ["Operation", "Syntax", "Notes"],
            [
                ["Read value", c('d["key"]'), "Raises " + c("KeyError") + " if key missing"],
                ["Safe read", c('d.get("key", default)'), "Returns default if key missing"],
                ["Add/update", c('d["new_key"] = value'), "Creates key if not exists"],
                ["Delete key", c('del d["key"]'), "Raises " + c("KeyError") + " if missing"],
                ["Pop key", c('d.pop("key", None)'), "Removes and returns value"],
                ["All keys", c('d.keys()'), "Returns a view of all keys"],
                ["All values", c('d.values()'), "Returns a view of all values"],
                ["All pairs", c('d.items()'), "Returns (key, value) tuples"],
            ]
        )
        + h2("Iterating Over a Dictionary")
        + p("The most common pattern is iterating with " + c(".items()") + " to process both key and value together:")
        + bq('<code>for key, value in d.items():<br>&nbsp;&nbsp;&nbsp;&nbsp;print(key, value)</code>')
        + h2("Nested Dictionaries")
        + p("Dictionaries can be nested — a value can itself be a dictionary. This is how JSON data structures work. A dataset of records is usually a list of nested dicts.")
        + h2("What is a Set?")
        + p("A <b>set</b> is an unordered collection of <b>unique values</b>. Sets are perfect for:")
        + ul(
            b("Deduplication") + " — remove duplicate values instantly",
            b("Membership testing") + " — " + c('"Alice" in my_set') + " is O(1) vs O(n) for lists",
            b("Set operations") + " — union, intersection, difference like in mathematics",
        )
        + h2("Set Operations (like Venn Diagrams in Code)")
        + table(
            ["Operation", "Syntax", "What it Returns"],
            [
                ["Union (A ∪ B)", c("A | B"), "All elements from A and B"],
                ["Intersection (A ∩ B)", c("A & B"), "Elements in both A and B"],
                ["Difference (A − B)", c("A - B"), "Elements in A but not B"],
                ["Symmetric Diff", c("A ^ B"), "Elements in A or B but not both"],
            ]
        )
        + tip("Use sets to quickly check if two datasets share common IDs: " + c("common_ids = set(df1_ids) & set(df2_ids)"))
        + warn("Sets are unordered — you cannot index into a set. If you need order + uniqueness, use " + c("dict.fromkeys(lst)") + " which preserves insertion order.")
    ),
    code_example=(
        '# ── Dictionary basics ──\n'
        'student = {\n'
        '    "name": "Priya Sharma",\n'
        '    "score": 88.5,\n'
        '    "domain": "Data Analytics",\n'
        '    "city": "Mumbai",\n'
        '}\n'
        '\n'
        'print(student["name"])                    # Priya Sharma\n'
        'print(student.get("grade", "Not Graded")) # safe: Not Graded\n'
        '\n'
        '# ── Modify & add ──\n'
        'student["grade"] = "A"         # add new key\n'
        'student["score"] = 90.0        # update existing\n'
        '\n'
        '# ── Iterate ──\n'
        'for key, value in student.items():\n'
        '    print(f"  {key:10} : {value}")\n'
        '\n'
        '# ── Nested dict: list of records ──\n'
        'records = {\n'
        '    "Alice": {"score": 92, "city": "Delhi",   "passed": True},\n'
        '    "Bob":   {"score": 63, "city": "Chennai",  "passed": True},\n'
        '    "Carol": {"score": 45, "city": "Mumbai",  "passed": False},\n'
        '}\n'
        '\n'
        '# Filter only passed students\n'
        'passed = {name: info for name, info in records.items() if info["passed"]}\n'
        'print("Passed:", list(passed.keys()))\n'
        '\n'
        '# Average score\n'
        'avg = sum(r["score"] for r in records.values()) / len(records)\n'
        'print(f"Class average: {avg:.1f}")\n'
        '\n'
        '# ── Sets for deduplication ──\n'
        'cities_raw = ["Delhi", "Mumbai", "Delhi", "Chennai", "Mumbai", "Pune"]\n'
        'unique_cities = set(cities_raw)\n'
        'print("Unique cities:", unique_cities)    # {Delhi, Mumbai, Chennai, Pune}\n'
        'print("Count:", len(unique_cities))       # 4\n'
        '\n'
        '# ── Set operations ──\n'
        'batch_a = {"Alice", "Bob", "Carol", "Dave"}\n'
        'batch_b = {"Carol", "Dave", "Eve", "Frank"}\n'
        'print("Both batches:", batch_a & batch_b)  # intersection\n'
        'print("Only A:", batch_a - batch_b)         # difference'
    ),
    try_it_note="Add 'Dave' with score 77 and city 'Pune' to records. Recompute the average. Who has the highest score?"
)

# ===========================================================================
# PYTHON — Loops & Conditionals
# ===========================================================================
CONTENT["Loops & Conditionals"] = dict(
    content=(
        h2("Why Loops Matter in Data Analytics")
        + p("In data analytics, you rarely work with a single value. You process <b>hundreds or thousands of rows</b>. Loops are the fundamental tool for applying logic to every element in a dataset.")
        + h2("The for Loop")
        + p("A " + c("for") + " loop iterates over any <b>iterable</b> — a list, string, dict, range, or file — one item at a time.")
        + bq('<code>for item in iterable:<br>&nbsp;&nbsp;&nbsp;&nbsp;# body executed once per item</code>')
        + ul(
            b("Over a list: ") + c("for score in scores:"),
            b("Over a range: ") + c("for i in range(10):") + " — 0 to 9",
            b("Over a dict: ") + c("for key in my_dict:") + " — iterates over keys",
            b("With index: ") + c("for i, val in enumerate(lst):"),
            b("Two lists: ") + c("for a, b in zip(list1, list2):"),
        )
        + h2("The while Loop")
        + p("A " + c("while") + " loop runs as long as a condition is " + c("True") + ". Use it when you don't know in advance how many iterations you need.")
        + warn("Always ensure the loop condition eventually becomes False. An infinite loop (" + c("while True:") + " without " + c("break") + ") will freeze your program.")
        + h2("Loop Control Statements")
        + table(
            ["Statement", "What it Does", "Example Use"],
            [
                [c("break"), "Exit the loop immediately", "Stop when a target value is found"],
                [c("continue"), "Skip this iteration, go to next", "Skip rows with missing data"],
                [c("pass"), "Do nothing (placeholder)", "Empty loop body during development"],
            ]
        )
        + h2("Conditionals: if / elif / else")
        + p("Conditionals let your code make <b>decisions</b> based on data values. They are the backbone of data classification, filtering, and business rules.")
        + bq('<code>if condition1:<br>&nbsp;&nbsp;&nbsp;&nbsp;...<br>elif condition2:<br>&nbsp;&nbsp;&nbsp;&nbsp;...<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;...</code>')
        + h2("Comparison & Logical Operators")
        + table(
            ["Operator", "Meaning", "Example"],
            [
                [c("=="), "Equal to", c("score == 100")],
                [c("!="), "Not equal to", c("city != 'Delhi'")],
                [c(">"), "Greater than", c("score > 75")],
                [c(">="), "Greater than or equal", c("score >= 60")],
                [c("in"), "Membership check", c("'Alice' in names")],
                [c("not in"), "Not a member", c("region not in blacklist")],
                [c("and"), "Both must be True", c("score > 60 and attendance > 0.8")],
                [c("or"), "At least one must be True", c("city == 'Mumbai' or city == 'Pune'")],
                [c("not"), "Invert condition", c("not is_paid")],
            ]
        )
        + h2("Ternary (One-line if-else)")
        + p("For simple true/false assignments, use the ternary expression:")
        + bq('<code>grade = "PASS" if score >= 60 else "FAIL"</code>')
        + tip("Prefer " + c("enumerate()") + " over manual index tracking with " + c("i = 0; i += 1") + ". It's cleaner, less error-prone, and Pythonic.")
    ),
    code_example=(
        'scores = [88, 45, 72, 91, 60, 38, 95, 67, 54, 83]\n'
        'students = ["Priya","Raj","Neha","Arjun","Meera","Dev","Sanya","Kabir","Nita","Rohan"]\n'
        '\n'
        '# ── Grade classification ──\n'
        'results = {}\n'
        'for name, score in zip(students, scores):\n'
        '    if score >= 90:\n'
        '        grade = "A"\n'
        '    elif score >= 75:\n'
        '        grade = "B"\n'
        '    elif score >= 60:\n'
        '        grade = "C"\n'
        '    elif score >= 45:\n'
        '        grade = "D"\n'
        '    else:\n'
        '        grade = "FAIL"\n'
        '    results[name] = {"score": score, "grade": grade}\n'
        '\n'
        '# ── Print results table ──\n'
        'print(f"{"Name":<10} {"Score":>6} {"Grade":>6}")\n'
        'print("-" * 26)\n'
        'for name, info in results.items():\n'
        '    print(f"{name:<10} {info[\"score\"]:>6} {info[\"grade\"]:>6}")\n'
        '\n'
        '# ── Summary stats using loops ──\n'
        'grade_counts = {}\n'
        'for info in results.values():\n'
        '    g = info["grade"]\n'
        '    grade_counts[g] = grade_counts.get(g, 0) + 1\n'
        '\n'
        'print("\\nGrade Distribution:")\n'
        'for grade, count in sorted(grade_counts.items()):\n'
        '    bar = "█" * count\n'
        '    print(f"  {grade:4}: {bar} ({count})")\n'
        '\n'
        '# ── while loop: find first score above 90 ──\n'
        'i = 0\n'
        'while i < len(scores):\n'
        '    if scores[i] >= 90:\n'
        '        print(f"\\nFirst 90+ scorer: {students[i]} ({scores[i]})")\n'
        '        break\n'
        '    i += 1\n'
        '\n'
        '# ── continue: skip below-average ──\n'
        'avg = sum(scores) / len(scores)\n'
        'print(f"\\nAbove average ({avg:.1f}):")\n'
        'for name, score in zip(students, scores):\n'
        '    if score <= avg:\n'
        '        continue\n'
        '    print(f"  {name}: {score}")'
    ),
    try_it_note="Add a 'bonus' rule: any score between 55-59 gets bumped to 'C'. How many students change grade?"
)

# ===========================================================================
# WEB DEVELOPMENT — HTML Fundamentals
# ===========================================================================
CONTENT["HTML Basics"] = dict(
    content=(
        h2("What is HTML?")
        + p("<b>HTML (HyperText Markup Language)</b> is the skeleton of every web page. It defines the <em>structure and content</em> — headings, paragraphs, images, links, and forms. Every browser reads HTML and renders it as a visual page.")
        + p("HTML is not a programming language — it has no logic or calculations. It is a <b>markup language</b> that uses tags to annotate content and tell the browser what each piece of content means.")
        + h2("Anatomy of an HTML Document")
        + bq('<code>&lt;!DOCTYPE html&gt;</code> — declares this is HTML5<br>'
             '<code>&lt;html lang="en"&gt;</code> — root element<br>'
             '<code>&lt;head&gt;</code> — metadata (title, CSS links, SEO tags)<br>'
             '<code>&lt;body&gt;</code> — everything visible on the page')
        + h2("HTML Tags: Elements & Attributes")
        + p("An HTML element consists of:")
        + ul(
            b("Opening tag: ") + c("<p>"),
            b("Content: ") + "Hello World",
            b("Closing tag: ") + c("</p>"),
            b("Attributes: ") + c('<a href="url" target="_blank">') + " — add extra info to a tag",
        )
        + h2("Essential HTML Elements")
        + table(
            ["Tag", "Purpose", "Example"],
            [
                [c("<h1>") + " to " + c("<h6>"), "Headings (h1 = largest)", c("<h1>Page Title</h1>")],
                [c("<p>"), "Paragraph of text", c("<p>This is a sentence.</p>")],
                [c("<a>"), "Hyperlink", c('<a href="https://google.com">Google</a>')],
                [c("<img>"), "Image (self-closing)", c('<img src="photo.jpg" alt="A photo">')],
                [c("<ul>/<ol>"), "Unordered/Ordered list", c("<ul><li>Item</li></ul>")],
                [c("<div>"), "Generic block container", c("<div class='card'>...</div>")],
                [c("<span>"), "Generic inline container", c("<span class='bold'>text</span>")],
                [c("<table>"), "Tabular data", c("<table><tr><td>Data</td></tr></table>")],
                [c("<form>"), "User input form", c('<form action="/submit" method="POST">')],
                [c("<input>"), "Form field (self-closing)", c('<input type="text" name="username">')],
            ]
        )
        + h2("Block vs Inline Elements")
        + table(
            ["Type", "Behavior", "Examples"],
            [
                ["Block", "Takes full width, starts on new line", c("div") + ", " + c("p") + ", " + c("h1") + ", " + c("ul") + ", " + c("table")],
                ["Inline", "Only takes needed width, flows in text", c("span") + ", " + c("a") + ", " + c("strong") + ", " + c("img") + ", " + c("code")],
            ]
        )
        + h2("Semantic HTML — Write HTML with Meaning")
        + p("Semantic tags tell browsers and search engines <em>what kind of content</em> is inside. Always prefer semantic tags over generic " + c("<div>") + " wrappers:")
        + ul(
            c("<header>") + " — top navigation / logo area",
            c("<nav>") + " — navigation links",
            c("<main>") + " — primary page content",
            c("<section>") + " — thematic section of content",
            c("<article>") + " — standalone piece of content (blog post, card)",
            c("<aside>") + " — sidebar content",
            c("<footer>") + " — page footer",
        )
        + tip("Use semantic HTML for better SEO, accessibility (screen readers), and code readability. Google ranks pages higher when HTML is semantic.")
        + warn(c("alt") + " on " + c("<img>") + " is mandatory for accessibility. Without it, visually impaired users get no information about the image.")
    ),
    code_example=(
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <title>My First Web Page</title>\n'
        '  <meta name="description" content="A beginner HTML example page">\n'
        '</head>\n'
        '<body>\n'
        '\n'
        '  <header>\n'
        '    <h1>Welcome to TRHvision Learn</h1>\n'
        '    <nav>\n'
        '      <a href="#about">About</a> |\n'
        '      <a href="#courses">Courses</a> |\n'
        '      <a href="#contact">Contact</a>\n'
        '    </nav>\n'
        '  </header>\n'
        '\n'
        '  <main>\n'
        '    <section id="about">\n'
        '      <h2>About Us</h2>\n'
        '      <p>We help students launch their tech careers through\n'
        '         <strong>hands-on internships</strong> and real-world projects.</p>\n'
        '    </section>\n'
        '\n'
        '    <section id="courses">\n'
        '      <h2>Our Courses</h2>\n'
        '      <ul>\n'
        '        <li>Data Analytics</li>\n'
        '        <li>Web Development</li>\n'
        '        <li>Machine Learning</li>\n'
        '      </ul>\n'
        '    </section>\n'
        '\n'
        '    <article>\n'
        '      <h2>Student Profile</h2>\n'
        '      <table>\n'
        '        <thead><tr><th>Field</th><th>Value</th></tr></thead>\n'
        '        <tbody>\n'
        '          <tr><td>Name</td><td>Priya Sharma</td></tr>\n'
        '          <tr><td>Domain</td><td>Data Analytics</td></tr>\n'
        '          <tr><td>Score</td><td>88%</td></tr>\n'
        '        </tbody>\n'
        '      </table>\n'
        '    </article>\n'
        '  </main>\n'
        '\n'
        '  <footer id="contact">\n'
        '    <p>Contact: <a href="mailto:hello@trhvision.com">hello@trhvision.com</a></p>\n'
        '  </footer>\n'
        '\n'
        '</body>\n'
        '</html>'
    ),
    try_it_note="Add a <form> inside the contact section with name and email fields and a submit button."
)

# ===========================================================================
# MACHINE LEARNING — Supervised Learning (generic enrichment)
# ===========================================================================
CONTENT["Introduction to Supervised Learning"] = dict(
    content=(
        h2("What is Supervised Learning?")
        + p("<b>Supervised Learning</b> is the most common type of machine learning. The algorithm learns from <b>labelled training data</b> — data where the correct answer (label) is already known. The model tries to learn the mapping from inputs to outputs so it can predict on new, unseen data.")
        + p("The word 'supervised' means a teacher (the labels) guides the learning process. Compare this to unsupervised learning, where the model finds patterns in unlabelled data on its own.")
        + h2("Two Main Categories")
        + table(
            ["Category", "Output Type", "Examples", "Algorithms"],
            [
                [b("Classification"), "Category / Class", "Spam or Not Spam, Disease Diagnosis, Churn Prediction", "Logistic Regression, Decision Tree, SVM, KNN, Random Forest"],
                [b("Regression"), "Continuous Number", "House Price, Sales Forecast, Temperature Prediction", "Linear Regression, Ridge, Lasso, Gradient Boosting"],
            ]
        )
        + h2("The Supervised Learning Workflow")
        + ol(
            b("Collect & Prepare Data") + " — gather labelled examples, clean missing values",
            b("Split Dataset") + " — training set (80%) to learn, test set (20%) to evaluate",
            b("Choose an Algorithm") + " — based on data type and problem",
            b("Train the Model") + " — model finds patterns by minimizing prediction error",
            b("Evaluate") + " — measure accuracy on test set (unseen data)",
            b("Tune Hyperparameters") + " — improve performance via cross-validation",
            b("Deploy & Monitor") + " — serve predictions in production",
        )
        + h2("Key Terminology")
        + table(
            ["Term", "Definition"],
            [
                [b("Features (X)"), "Input variables / columns used to make predictions (e.g., age, income, education)"],
                [b("Label / Target (y)"), "The output variable we want to predict (e.g., purchased: Yes/No)"],
                [b("Training Data"), "Labelled examples the model learns from"],
                [b("Test Data"), "Held-out examples used only to evaluate final model performance"],
                [b("Overfitting"), "Model memorizes training data but fails on new data — too complex"],
                [b("Underfitting"), "Model is too simple to capture patterns — high error on both train and test"],
                [b("Hyperparameters"), "Settings you configure before training (e.g., tree depth, learning rate)"],
            ]
        )
        + h2("Linear Regression — The Foundation")
        + p("Linear Regression predicts a <b>continuous output</b> by fitting a straight line through the data. The equation is:")
        + bq('<code>y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε</code><br>Where β values are the <b>weights</b> (learned during training) and ε is the error term.')
        + h2("Logistic Regression — For Classification")
        + p("Despite the name, Logistic Regression is a <b>classification</b> algorithm. It predicts the <b>probability</b> that an input belongs to a class. The output is squeezed between 0 and 1 using the sigmoid function.")
        + bq('<code>P(y=1) = 1 / (1 + e^(-z))</code><br>If P > 0.5 → Class 1 (Positive). If P ≤ 0.5 → Class 0 (Negative).')
        + tip("Always split your data with " + c("train_test_split") + " before any preprocessing. Fitting a scaler on the full dataset causes <b>data leakage</b> — your model sees test data statistics during training, making evaluation optimistically biased.")
        + warn("A high training accuracy does NOT mean your model is good. Always check test accuracy. If train accuracy >> test accuracy, your model is overfitting.")
    ),
    code_example=(
        'from sklearn.datasets import make_classification, make_regression\n'
        'from sklearn.model_selection import train_test_split\n'
        'from sklearn.linear_model import LinearRegression, LogisticRegression\n'
        'from sklearn.preprocessing import StandardScaler\n'
        'from sklearn.metrics import accuracy_score, r2_score, mean_squared_error\n'
        'import numpy as np\n'
        '\n'
        '# ════ REGRESSION EXAMPLE ════\n'
        'X_r, y_r = make_regression(n_samples=200, n_features=3, noise=15, random_state=42)\n'
        'X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(\n'
        '    X_r, y_r, test_size=0.2, random_state=42\n'
        ')\n'
        '\n'
        'lr = LinearRegression()\n'
        'lr.fit(X_train_r, y_train_r)         # train\n'
        'y_pred_r = lr.predict(X_test_r)      # predict on test set\n'
        '\n'
        'r2  = r2_score(y_test_r, y_pred_r)\n'
        'mse = mean_squared_error(y_test_r, y_pred_r)\n'
        'print(f"Regression  →  R² = {r2:.3f}  |  RMSE = {np.sqrt(mse):.2f}")\n'
        '\n'
        '# ════ CLASSIFICATION EXAMPLE ════\n'
        'X_c, y_c = make_classification(n_samples=300, n_features=4, random_state=42)\n'
        'X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(\n'
        '    X_c, y_c, test_size=0.2, random_state=42\n'
        ')\n'
        '\n'
        '# Scale features (important for Logistic Regression)\n'
        'scaler = StandardScaler()\n'
        'X_train_c = scaler.fit_transform(X_train_c)  # fit on train ONLY\n'
        'X_test_c  = scaler.transform(X_test_c)       # transform test\n'
        '\n'
        'clf = LogisticRegression(max_iter=200)\n'
        'clf.fit(X_train_c, y_train_c)\n'
        'y_pred_c = clf.predict(X_test_c)\n'
        '\n'
        'acc = accuracy_score(y_test_c, y_pred_c)\n'
        'print(f"Classification  →  Accuracy = {acc:.1%}")\n'
        'print(f"Intercept: {clf.intercept_[0]:.4f}")\n'
        'print(f"Coefficients: {clf.coef_[0].round(3)}")\n'
        '\n'
        '# ── Show prediction probabilities ──\n'
        'probs = clf.predict_proba(X_test_c[:5])\n'
        'print("\\nProbabilities for first 5 test samples:")\n'
        'for i, (p0, p1) in enumerate(probs):\n'
        '    pred = "Class 1" if p1 > 0.5 else "Class 0"\n'
        '    print(f"  Sample {i+1}: P(0)={p0:.2f}, P(1)={p1:.2f}  → {pred}")'
    ),
    try_it_note="Change n_features to 8 in make_regression. Does the R² improve? Why might it change?"
)

# ===========================================================================
# APPLY ALL RICH CONTENT TO DB
# ===========================================================================

updated = 0
skipped = 0

for lesson in LearningLesson.objects.all():
    # Match by exact title
    if lesson.title in CONTENT:
        data = CONTENT[lesson.title]
        lesson.content      = data["content"]
        lesson.code_example = data.get("code_example", lesson.code_example)
        lesson.try_it_note  = data.get("try_it_note", lesson.try_it_note)
        lesson.save(update_fields=["content", "code_example", "try_it_note"])
        print(f"  [OK] Updated: [{lesson.topic.domain}] {lesson.title} ({len(data['content'])} chars)")
        updated += 1
    else:
        skipped += 1

print(f"\nDone. Updated {updated} lessons, skipped {skipped} (no matching content key).")
print("\nTo add content for more lessons, add their title to the CONTENT dict above.")

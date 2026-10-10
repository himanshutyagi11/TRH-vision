"""
Management command: load_learning_content (EXPANDED)
Run: python manage.py load_learning_content --clear
6 domains x 3-5 topics x 3-6 lessons = 45+ lessons total.
"""
from django.core.management.base import BaseCommand
from vision.models import LearningTopic, LearningLesson


def L(title, order, lang, content, code="", tip=""):
    return {
        "title": title, "order": order, "code_language": lang,
        "content": content, "code_example": code, "try_it_note": tip
    }


# ───────────────────────────────────────────────────────────────
# DATA ANALYTICS
# ───────────────────────────────────────────────────────────────
DA_TOPICS = [
    {
        "title": "Python for Data Analytics",
        "icon": "bi-terminal-fill",
        "description": "Core Python skills every data analyst needs — variables, lists, loops, functions, and file handling.",
        "order": 1,
        "lessons": [
            L("Variables & Data Types", 1, "python",
              "<h3>Python Variables</h3><p>Variables store data values. Python automatically infers the type.</p>"
              "<h3>Core Data Types</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Type</th><th>Example</th><th>Analytics Use</th></tr></thead><tbody>"
              "<tr><td><code>int</code></td><td>42</td><td>Row counts, IDs</td></tr>"
              "<tr><td><code>float</code></td><td>98.5</td><td>Percentages, scores</td></tr>"
              "<tr><td><code>str</code></td><td>'Alice'</td><td>Names, categories</td></tr>"
              "<tr><td><code>bool</code></td><td>True</td><td>Flags, filters</td></tr>"
              "<tr><td><code>None</code></td><td>None</td><td>Missing values</td></tr>"
              "</tbody></table>"
              "<h3>Type Conversion</h3><p>CSV data loads as strings — always cast to the correct type before calculations.</p>"
              "<blockquote>Use <code>type()</code> to inspect a variable during debugging.</blockquote>",
              'name = "Alice"\nage  = 25\nscore = 98.5\nis_intern = True\nmissing = None\n\nprint(type(name))    # str\nprint(type(age))     # int\nprint(type(score))   # float\n\n# Type conversion\nstr_num = "42"\nconverted = int(str_num)\nprint(converted + 8)   # 50\n\n# f-string formatting\nprint(f"{name} | Score: {score:.2f}")',
              "Try converting score='98.5' (string) to float and compute score * 1.1"),

            L("Lists & List Operations", 2, "python",
              "<h3>What are Lists?</h3><p>Lists are ordered, mutable sequences — the most common data structure for analytics.</p>"
              "<h3>Key Operations</h3><ul>"
              "<li><code>list.append(x)</code> — add to end</li>"
              "<li><code>list.extend([...])</code> — merge another list</li>"
              "<li><code>list.sort()</code> — sort in place</li>"
              "<li><code>list[i:j]</code> — slicing a sublist</li>"
              "<li><code>len(), sum(), min(), max()</code> — built-in functions</li></ul>"
              "<h3>List Comprehensions</h3><p>A powerful one-liner to create transformed or filtered lists:</p>"
              "<code>[expression for item in iterable if condition]</code>"
              "<blockquote>Lists are 0-indexed. <code>list[-1]</code> returns the last element.</blockquote>",
              'sales = [450, 320, 510, 390, 620, 480]\n\n# Slicing\nprint(sales[:3])          # First 3\nprint(sales[-2:])         # Last 2\n\n# Stats without libraries\nprint(f"Total : {sum(sales)}")\nprint(f"Avg   : {sum(sales)/len(sales):.1f}")\nprint(f"Max   : {max(sales)}")\n\n# List comprehension — filter above average\navg  = sum(sales) / len(sales)\nhigh = [s for s in sales if s > avg]\nprint(f"Above avg: {high}")\n\n# Sort descending\nranked = sorted(sales, reverse=True)\nprint(f"Ranked: {ranked}")',
              "Add a 7th sale value of 700. Does it appear in the 'high' list?"),

            L("Dictionaries & Sets", 3, "python",
              "<h3>Dictionaries</h3><p>Maps keys to values — like a labelled row in a spreadsheet or a JSON object.</p>"
              "<h3>Key Methods</h3><ul>"
              "<li><code>.keys()</code>, <code>.values()</code>, <code>.items()</code></li>"
              "<li><code>.get(key, default)</code> — safe access without KeyError</li>"
              "<li><code>.update({...})</code> — merge dictionaries</li></ul>"
              "<h3>Sets</h3><p>Contains only unique values — perfect for deduplication and membership tests.</p>",
              'student = {\n    "name": "Priya",\n    "domain": "Data Analytics",\n    "score": 88.5,\n}\n\nprint(student["name"])\nprint(student.get("grade", "N/A"))  # safe\n\n# Iterate\nfor k, v in student.items():\n    print(f"{k:10}: {v}")\n\n# Nested dict\nrecords = {\n    "Alice": {"score": 92, "region": "North"},\n    "Bob":   {"score": 78, "region": "South"},\n}\nprint(records["Alice"]["score"])  # 92\n\n# Set for deduplication\nregions = ["North","South","North","East","South"]\nunique = set(regions)\nprint(unique)  # {North, South, East}',
              "Add a 'Charlie' record. Then print all names with .keys()."),

            L("Loops & Conditionals", 4, "python",
              "<h3>For Loops</h3><p>Iterate over lists, dicts, ranges, or any iterable.</p>"
              "<h3>While Loops</h3><p>Repeat while a condition is True.</p>"
              "<h3>Conditionals (if/elif/else)</h3><p>Make decisions based on data values.</p>"
              "<h3>Useful Built-ins</h3><ul>"
              "<li><code>enumerate()</code> — loop with index</li>"
              "<li><code>zip()</code> — loop two lists simultaneously</li>"
              "<li><code>range(start, stop, step)</code></li></ul>"
              "<blockquote>Use loops to process rows, apply transformations, and classify data at scale.</blockquote>",
              'scores = [88, 45, 72, 91, 60, 38, 95]\n\n# Classify each score\nfor i, s in enumerate(scores):\n    if s >= 90:\n        grade = "A"\n    elif s >= 75:\n        grade = "B"\n    elif s >= 60:\n        grade = "C"\n    else:\n        grade = "FAIL"\n    print(f"Student {i+1}: {s} -> {grade}")\n\n# zip two lists\nstudents = ["Priya","Raj","Neha"]\nmarks    = [92, 78, 85]\nfor name, mark in zip(students, marks):\n    print(f"{name}: {mark}")\n\n# Count using a dict\ncounts = {}\nfor s in scores:\n    bucket = s // 10 * 10\n    counts[bucket] = counts.get(bucket, 0) + 1\nprint(counts)',
              "Add a score of 55 — how many fail grades now?"),

            L("Functions & Lambda", 5, "python",
              "<h3>Defining Functions</h3><p>Functions reduce repetition and make code reusable. Every data pipeline is built from composable functions.</p>"
              "<h3>Parameters</h3><ul>"
              "<li>Positional: <code>def f(a, b)</code></li>"
              "<li>Default: <code>def f(a, b=10)</code></li>"
              "<li>Keyword: <code>f(a=1, b=2)</code></li>"
              "<li>Variable: <code>*args</code>, <code>**kwargs</code></li></ul>"
              "<h3>Lambda Functions</h3><p>One-line anonymous functions for use with <code>map()</code>, <code>filter()</code>, <code>sorted()</code>.</p>",
              'def classify_score(score, threshold=75):\n    """Returns pass/fail for a given score."""\n    return "PASS" if score >= threshold else "FAIL"\n\nprint(classify_score(88))       # PASS\nprint(classify_score(60))       # FAIL\nprint(classify_score(60, 55))   # PASS\n\n# Multiple return values (tuple)\ndef stats(data):\n    return min(data), max(data), sum(data)/len(data)\n\nlo, hi, avg = stats([45, 72, 91, 60, 38])\nprint(f"Min={lo}, Max={hi}, Avg={avg:.1f}")\n\n# Lambda with sorted\nstudents = [("Priya",92),("Raj",78),("Neha",85)]\nsorted_by_score = sorted(students, key=lambda x: x[1], reverse=True)\nprint(sorted_by_score)',
              "Add a 'marks' parameter that scales the score before grading."),

            L("Error Handling & File I/O", 6, "python",
              "<h3>Why Error Handling?</h3><p>Real data is messy — missing values, wrong types, empty files. Without error handling your script crashes on the first bad row.</p>"
              "<h3>try / except / finally</h3><ul>"
              "<li><code>try</code> — code that might fail</li>"
              "<li><code>except ExceptionType</code> — handle specific error</li>"
              "<li><code>finally</code> — always runs (cleanup)</li></ul>"
              "<h3>Reading CSV Files</h3><p>Use <code>csv.DictReader()</code> to read rows as dicts. Always open files with <code>with open(...) as f:</code>.</p>"
              "<blockquote>For production work, prefer <code>pandas.read_csv()</code> which handles edge cases automatically.</blockquote>",
              "import csv\n\n# Handle bad data rows gracefully\nraw = [\"100\", \"200\", \"N/A\", \"450\", \"???\", \"300\"]\nclean = []\nfor val in raw:\n    try:\n        clean.append(float(val))\n    except ValueError:\n        print(f\"Skipping bad value: '{val}'\")\n\nprint(f\"Clean data : {clean}\")\nprint(f\"Average    : {sum(clean)/len(clean):.1f}\")\n\n# Write and read CSV\ndata = [[\"Name\",\"Sales\"],[\"Alice\",4500],[\"Bob\",3200]]\nwith open(\"sales.csv\", \"w\", newline=\"\") as f:\n    csv.writer(f).writerows(data)\n\nwith open(\"sales.csv\") as f:\n    for row in csv.DictReader(f):\n        print(f\"{row['Name']:8}: {row['Sales']}\")",
              "Add logging: save each bad value to a 'errors' list and print the full error report at the end."),

            L("List Comprehensions & Generators", 7, "python",
              "<h3>List Comprehensions</h3><p>Concise, readable way to build lists with filtering and transformation.</p>"
              "<code>[expression for item in iterable if condition]</code>"
              "<h3>Dictionary Comprehensions</h3>"
              "<code>{key: val for item in iterable}</code>"
              "<h3>Generators</h3><p>Produce values lazily — one at a time — using almost no memory. Essential for large datasets.</p>"
              "<blockquote>Rule: list comprehensions for small data. Generators for large datasets that don't fit in RAM.</blockquote>",
              'scores = [88, 45, 72, 91, 60, 38, 95, 54, 83, 67]\n\n# List comprehension\npass_scores = [s for s in scores if s >= 60]\nprint(f"Pass scores: {pass_scores}")\n\n# Dict comprehension\nstudent_scores = {f"S{i+1:02d}": s for i, s in enumerate(scores)}\nprint(student_scores)\n\n# Nested comprehension — times table\ntable = [[i*j for j in range(1,6)] for i in range(1,6)]\nfor row in table:\n    print(row)\n\n# Generator — memory-efficient chunking\ndef yield_chunks(data, size):\n    for i in range(0, len(data), size):\n        yield data[i:i+size]\n\nfor chunk in yield_chunks(scores, 3):\n    print(chunk)',
              "Write a dict comprehension mapping each score to its grade ('A','B','C','F')."),
        ]
    },

    {
        "title": "Pandas Deep Dive",
        "icon": "bi-file-earmark-code-fill",
        "description": "Master Pandas for data loading, cleaning, filtering, groupby, merging, and time series.",
        "order": 2,
        "lessons": [
            L("Loading & Exploring Data", 1, "python",
              "<h3>Reading Data</h3><table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Function</th><th>Format</th></tr></thead><tbody>"
              "<tr><td><code>pd.read_csv()</code></td><td>CSV / TSV</td></tr>"
              "<tr><td><code>pd.read_excel()</code></td><td>Excel .xlsx</td></tr>"
              "<tr><td><code>pd.read_json()</code></td><td>JSON</td></tr>"
              "<tr><td><code>pd.read_sql()</code></td><td>SQL Query</td></tr></tbody></table>"
              "<h3>First Exploration — The 5 Commands</h3><ol>"
              "<li><code>df.head()</code> — first 5 rows</li>"
              "<li><code>df.info()</code> — column types and nulls</li>"
              "<li><code>df.describe()</code> — statistics for numeric cols</li>"
              "<li><code>df.isnull().sum()</code> — missing value count per column</li>"
              "<li><code>df.value_counts()</code> — frequency of categories</li></ol>",
              "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'name'  : ['Alice','Bob','Carol','Dave','Eve','Frank'],\n    'region': ['North','South','East','North','South','East'],\n    'sales' : [4500, 3200, 5100, 3900, np.nan, 4800],\n    'month' : ['Jan','Feb','Jan','Feb','Jan','Feb']\n})\n\nprint(df.shape)           # (6, 4)\nprint(df.dtypes)\nprint(df.head())\nprint(df.describe())\nprint(df.isnull().sum())\nprint(df['region'].value_counts())",
              "Add a 'quota' column and compute attainment = sales / quota * 100."),

            L("Data Cleaning", 2, "python",
              "<h3>Why Clean?</h3><p>Dirty data = wrong insights. Cleaning is 80% of any analyst's job.</p>"
              "<h3>Common Steps</h3><ol>"
              "<li>Handle missing values — <code>fillna()</code>, <code>dropna()</code></li>"
              "<li>Fix data types — <code>astype()</code>, <code>pd.to_datetime()</code></li>"
              "<li>Remove duplicates — <code>drop_duplicates()</code></li>"
              "<li>Standardize text — <code>.str.strip().str.lower()</code></li>"
              "<li>Replace values — <code>replace()</code>, <code>map()</code></li></ol>"
              "<blockquote>Always work on a copy: <code>df_clean = df.copy()</code>. Never modify raw data.</blockquote>",
              "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'Name'  : ['Alice','Bob','alice','Carol','Dave','Dave'],\n    'Sales' : ['4500','3200','N/A','5100',None,'3900'],\n    'Region': ['  North ','south','East','EAST','North','north'],\n})\n\ndf_clean = df.copy()\n\n# Standardize text\ndf_clean['Name']   = df_clean['Name'].str.strip().str.title()\ndf_clean['Region'] = df_clean['Region'].str.strip().str.title()\n\n# Numeric conversion with error handling\ndf_clean['Sales'] = pd.to_numeric(df_clean['Sales'], errors='coerce')\ndf_clean['Sales'].fillna(df_clean['Sales'].median(), inplace=True)\n\n# Remove duplicates\ndf_clean.drop_duplicates(inplace=True)\n\nprint(\"Before:\", df.shape, \"-> After:\", df_clean.shape)\nprint(df_clean)",
              "Add a 'sales_k' column = Sales/1000 rounded to 1 decimal."),

            L("Filtering & Selection", 3, "python",
              "<h3>Selecting Columns</h3><ul>"
              "<li><code>df['col']</code> — single column (Series)</li>"
              "<li><code>df[['col1','col2']]</code> — multiple (DataFrame)</li></ul>"
              "<h3>Filtering Rows</h3><ul>"
              "<li><code>df[df['col'] > 100]</code> — boolean index</li>"
              "<li><code>df[(cond1) & (cond2)]</code> — AND</li>"
              "<li><code>df[(cond1) | (cond2)]</code> — OR</li>"
              "<li><code>df.query('col > 100')</code> — string query</li>"
              "<li><code>.isin([...])</code>, <code>.between(a,b)</code>, <code>.str.contains()</code></li></ul>"
              "<h3>loc vs iloc</h3><ul>"
              "<li><code>df.loc[rows, cols]</code> — label-based</li>"
              "<li><code>df.iloc[rows, cols]</code> — position-based (integers)</li></ul>",
              "import pandas as pd\n\ndf = pd.DataFrame({\n    'name'  : ['Alice','Bob','Carol','Dave','Eve'],\n    'region': ['North','South','East','North','South'],\n    'sales' : [4500, 3200, 5100, 3900, 2800],\n    'quota' : [4000, 3000, 5000, 4200, 3000]\n})\n\n# Boolean filter\nnorth = df[df['region'] == 'North']\nprint(\"North region:\\n\", north)\n\n# Multiple conditions\ntop = df[(df['sales'] > 3500) & (df['region'] != 'South')]\nprint(\"\\nHigh non-South:\\n\", top)\n\n# Derived column\ndf['attainment'] = (df['sales'] / df['quota'] * 100).round(1)\nprint(\"\\nAttainment > 100%:\\n\", df[df['attainment'] > 100])\n\n# query()\nresult = df.query('sales > 4000 and region in [\"North\",\"East\"]')\nprint(\"\\nQuery:\\n\", result)",
              "Filter for reps with attainment BETWEEN 90% and 110%."),

            L("GroupBy & Aggregation", 4, "python",
              "<h3>GroupBy = SQL GROUP BY</h3><p>Split data into groups, apply a function, combine results.</p>"
              "<h3>Aggregation Functions</h3><ul>"
              "<li><code>sum(), mean(), count(), min(), max(), std(), median()</code></li>"
              "<li><code>agg({'col': ['sum','mean']})</code> — multiple functions</li>"
              "<li><code>transform()</code> — keep original shape (e.g., % of total)</li></ul>"
              "<h3>pivot_table()</h3><p>Creates Excel-style pivot tables from a DataFrame.</p>",
              "import pandas as pd\n\ndf = pd.DataFrame({\n    'rep'   : ['Alice','Bob','Alice','Carol','Bob','Carol'],\n    'region': ['North','South','North','East','South','East'],\n    'month' : ['Jan','Jan','Feb','Jan','Feb','Feb'],\n    'sales' : [2100, 1800, 2400, 3100, 2200, 2900]\n})\n\n# Basic groupby\nby_rep = df.groupby('rep')['sales'].sum().sort_values(ascending=False)\nprint(\"Total by Rep:\\n\", by_rep)\n\n# Multiple aggregations\nsummary = df.groupby('region')['sales'].agg(['sum','mean','count'])\nprint(\"\\nRegion Summary:\\n\", summary)\n\n# Pivot table\npivot = pd.pivot_table(df, values='sales',\n                       index='rep', columns='month',\n                       aggfunc='sum', fill_value=0)\nprint(\"\\nPivot Table:\\n\", pivot)\n\n# % of total using transform\ndf['total'] = df.groupby('month')['sales'].transform('sum')\ndf['pct']   = (df['sales'] / df['total'] * 100).round(1)\nprint(\"\\n\", df[['rep','month','sales','pct']])",
              "Add groupby region AND month and compute total sales per region per month."),

            L("Merging DataFrames", 5, "python",
              "<h3>merge() — SQL-style Joins</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>how=</th><th>SQL</th><th>Result</th></tr></thead><tbody>"
              "<tr><td>'inner'</td><td>INNER JOIN</td><td>Only matching rows</td></tr>"
              "<tr><td>'left'</td><td>LEFT JOIN</td><td>All left + matching right</td></tr>"
              "<tr><td>'right'</td><td>RIGHT JOIN</td><td>All right + matching left</td></tr>"
              "<tr><td>'outer'</td><td>FULL OUTER</td><td>All rows from both</td></tr></tbody></table>"
              "<h3>concat() — Stack DataFrames</h3><p>Stack vertically (axis=0) or horizontally (axis=1).</p>",
              "import pandas as pd\n\nsales = pd.DataFrame({'rep_id':[1,2,3,4],'sales':[4500,3200,5100,3900]})\nreps  = pd.DataFrame({'rep_id':[1,2,3,5],'name':['Alice','Bob','Carol','Eve'],'region':['North','South','East','West']})\n\n# INNER — only matched IDs\ninner = pd.merge(sales, reps, on='rep_id', how='inner')\nprint(\"INNER (3 rows):\\n\", inner)\n\n# LEFT — all sales, even without rep info\nleft = pd.merge(sales, reps, on='rep_id', how='left')\nprint(\"\\nLEFT (4 rows):\\n\", left)\n\n# Concat vertically\njan = pd.DataFrame({'rep':'Alice','sales':[2100],'month':['Jan']})\nfeb = pd.DataFrame({'rep':'Alice','sales':[2400],'month':['Feb']})\ncombined = pd.concat([jan, feb], ignore_index=True)\nprint(\"\\nConcatenated:\\n\", combined)",
              "Change to outer join. Which rep_ids have NaN?"),

            L("Time Series Analysis", 6, "python",
              "<h3>DateTime in Pandas</h3><p>Time series is critical — sales over time, user activity by hour, forecasting.</p>"
              "<h3>Key Functions</h3><ul>"
              "<li><code>pd.to_datetime()</code> — parse date strings</li>"
              "<li><code>df.set_index('date')</code> — date as index</li>"
              "<li><code>df.resample('ME').sum()</code> — aggregate by period</li>"
              "<li><code>df['date'].dt.month</code> — extract components</li>"
              "<li><code>.rolling(n).mean()</code> — moving average</li></ul>"
              "<blockquote>Always sort by date: <code>df.sort_values('date', inplace=True)</code></blockquote>",
              "import pandas as pd\nimport numpy as np\n\ndates = pd.date_range('2024-01-01', '2024-06-30', freq='D')\nnp.random.seed(42)\ndf = pd.DataFrame({'date': dates, 'sales': np.random.randint(500, 2000, len(dates))})\ndf.set_index('date', inplace=True)\n\n# Extract components\ndf['month']   = df.index.month\ndf['weekday'] = df.index.day_name()\n\n# Monthly aggregation\nmonthly = df['sales'].resample('ME').sum()\nprint(\"Monthly Totals:\\n\", monthly)\n\n# 7-day moving average\ndf['rolling_7'] = df['sales'].rolling(7).mean().round(0)\nprint(\"\\n7-Day Rolling Avg (last 7 days):\\n\", df[['sales','rolling_7']].tail(7))",
              "Change resample to 'W' (weekly) — are there weekly seasonal patterns?"),
        ]
    },

    {
        "title": "SQL Fundamentals",
        "icon": "bi-table",
        "description": "Write SQL to query, filter, group, join, and aggregate data in any relational database.",
        "order": 3,
        "lessons": [
            L("SELECT, WHERE & ORDER BY", 1, "sql",
              "<h3>SQL — The Universal Data Language</h3><p>SQL (Structured Query Language) is the standard for querying relational databases. Every data analyst must know it.</p>"
              "<h3>SELECT — What Columns?</h3><p>Use <code>AS</code> to rename columns (alias).</p>"
              "<h3>WHERE — Which Rows?</h3><p>Operators: <code>=</code>, <code>!=</code>, <code>&gt;</code>, <code>&lt;</code>, <code>BETWEEN</code>, <code>IN</code>, <code>LIKE</code>, <code>IS NULL</code>.</p>"
              "<h3>ORDER BY — Sort Results</h3><p>Default is ASC. Add <code>DESC</code> to reverse. Use <code>LIMIT n</code> to cap results.</p>",
              "-- All columns\nSELECT * FROM sales;\n\n-- Specific columns with alias\nSELECT\n    product_name AS product,\n    revenue      AS total_revenue,\n    region\nFROM sales;\n\n-- WHERE filters\nSELECT product_name, revenue\nFROM sales\nWHERE revenue > 10000\n  AND region = 'North';\n\n-- BETWEEN (inclusive)\nSELECT * FROM sales\nWHERE revenue BETWEEN 5000 AND 15000;\n\n-- LIKE pattern matching\nSELECT * FROM products\nWHERE product_name LIKE 'Lap%';\n\n-- Top 10 by revenue\nSELECT product_name, revenue\nFROM sales\nORDER BY revenue DESC\nLIMIT 10;",
              "Find all sales from 'South' region with revenue BETWEEN 8000 AND 20000."),

            L("GROUP BY & Aggregate Functions", 2, "sql",
              "<h3>Aggregate Functions</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Function</th><th>Use</th></tr></thead><tbody>"
              "<tr><td><code>COUNT(*)</code></td><td>Total rows</td></tr>"
              "<tr><td><code>COUNT(DISTINCT col)</code></td><td>Unique values</td></tr>"
              "<tr><td><code>SUM(col)</code></td><td>Total</td></tr>"
              "<tr><td><code>AVG(col)</code></td><td>Mean</td></tr>"
              "<tr><td><code>MAX(col) / MIN(col)</code></td><td>Extremes</td></tr></tbody></table>"
              "<h3>HAVING vs WHERE</h3><ul>"
              "<li><code>WHERE</code> — filters before grouping</li>"
              "<li><code>HAVING</code> — filters after grouping</li></ul>",
              "-- Total revenue per region\nSELECT\n    region,\n    SUM(revenue)  AS total_revenue,\n    COUNT(*)      AS order_count,\n    AVG(revenue)  AS avg_revenue\nFROM sales\nGROUP BY region\nORDER BY total_revenue DESC;\n\n-- HAVING — regions with > 100 orders\nSELECT region, COUNT(*) AS orders\nFROM sales\nGROUP BY region\nHAVING COUNT(*) > 100;\n\n-- Multi-column groupby\nSELECT region, product_category, SUM(revenue) AS revenue\nFROM sales\nWHERE YEAR(order_date) = 2024\nGROUP BY region, product_category\nORDER BY revenue DESC;",
              "Show only regions where average revenue > 12000."),

            L("JOINs — Combining Tables", 3, "sql",
              "<h3>SQL JOINs</h3><p>Combine rows from two or more tables based on a related column.</p>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>JOIN Type</th><th>Returns</th></tr></thead><tbody>"
              "<tr><td><code>INNER JOIN</code></td><td>Only matching rows in both tables</td></tr>"
              "<tr><td><code>LEFT JOIN</code></td><td>All left rows + matching right (NULL if no match)</td></tr>"
              "<tr><td><code>RIGHT JOIN</code></td><td>All right rows + matching left</td></tr>"
              "<tr><td><code>FULL OUTER JOIN</code></td><td>All rows from both tables</td></tr></tbody></table>"
              "<h3>Best Practices</h3><ul>"
              "<li>Always alias tables: <code>FROM sales s</code></li>"
              "<li>Qualify columns: <code>s.revenue</code></li>"
              "<li>Use LEFT JOIN when all rows from main table are needed</li></ul>",
              "-- INNER JOIN\nSELECT o.order_id, c.customer_name, o.revenue\nFROM orders o\nINNER JOIN customers c ON o.customer_id = c.customer_id;\n\n-- LEFT JOIN\nSELECT o.order_id, c.customer_name, o.revenue\nFROM orders o\nLEFT JOIN customers c ON o.customer_id = c.customer_id;\n\n-- Three-table JOIN\nSELECT\n    o.order_id,\n    c.customer_name,\n    p.product_name,\n    o.quantity * p.unit_price AS line_total\nFROM orders o\nJOIN customers c ON o.customer_id = c.customer_id\nJOIN products  p ON o.product_id  = p.product_id\nORDER BY line_total DESC\nLIMIT 20;",
              "Find customers who have NEVER placed an order (LEFT JOIN + WHERE IS NULL)."),

            L("Subqueries & CTEs", 4, "sql",
              "<h3>Subqueries</h3><p>A query nested inside another. Can appear in SELECT, FROM, or WHERE.</p>"
              "<h3>CTEs (Common Table Expressions)</h3><p>Named temporary result sets using <code>WITH</code>. They make complex queries readable and reusable.</p>"
              "<blockquote>Prefer CTEs over nested subqueries — they are easier to read, debug, and compose.</blockquote>",
              "-- Subquery in WHERE — above-average revenue\nSELECT product_name, revenue\nFROM sales\nWHERE revenue > (SELECT AVG(revenue) FROM sales);\n\n-- CTE (cleaner)\nWITH region_avgs AS (\n    SELECT region, AVG(revenue) AS avg_rev\n    FROM sales\n    GROUP BY region\n),\ntop_regions AS (\n    SELECT * FROM region_avgs\n    WHERE avg_rev > 10000\n)\nSELECT\n    s.product_name, s.revenue, t.avg_rev\nFROM sales s\nJOIN top_regions t ON s.region = t.region\nORDER BY s.revenue DESC;",
              "Add a 2nd CTE called 'bottom_regions' and join it to the final SELECT."),

            L("Window Functions", 5, "sql",
              "<h3>Window Functions</h3><p>Perform calculations across a set of rows related to the current row — without collapsing rows like GROUP BY.</p>"
              "<code>function() OVER (PARTITION BY col ORDER BY col)</code>"
              "<h3>Key Window Functions</h3><ul>"
              "<li><code>ROW_NUMBER()</code> — unique sequential rank</li>"
              "<li><code>RANK()</code> — rank with ties and gaps</li>"
              "<li><code>DENSE_RANK()</code> — rank with ties, no gaps</li>"
              "<li><code>LAG(col, n)</code> — value from n rows before</li>"
              "<li><code>LEAD(col, n)</code> — value from n rows after</li>"
              "<li><code>SUM() OVER</code> — running total</li></ul>",
              "-- Rank reps within each region\nSELECT\n    rep_name, region, revenue,\n    RANK() OVER (\n        PARTITION BY region\n        ORDER BY revenue DESC\n    ) AS regional_rank\nFROM sales;\n\n-- Running total\nSELECT\n    order_date, daily_revenue,\n    SUM(daily_revenue) OVER (\n        ORDER BY order_date\n    ) AS cumulative_revenue\nFROM daily_sales;\n\n-- Month-over-month growth\nSELECT\n    month, revenue,\n    LAG(revenue) OVER (ORDER BY month) AS prev_month,\n    ROUND(\n        (revenue - LAG(revenue) OVER (ORDER BY month))\n        / LAG(revenue) OVER (ORDER BY month) * 100, 1\n    ) AS mom_growth_pct\nFROM monthly_revenue;",
              "Write a query to find TOP 1 rep per region using ROW_NUMBER() and WHERE rank = 1."),
        ]
    },

    {
        "title": "Data Visualization",
        "icon": "bi-graph-up",
        "description": "Build professional charts with Matplotlib and Seaborn for reports and dashboards.",
        "order": 4,
        "lessons": [
            L("Matplotlib — Core Charts", 1, "python",
              "<h3>Chart Types & When to Use</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Chart</th><th>Best for</th></tr></thead><tbody>"
              "<tr><td>Line</td><td>Trends over time</td></tr>"
              "<tr><td>Bar</td><td>Comparing categories</td></tr>"
              "<tr><td>Scatter</td><td>Relationship between 2 variables</td></tr>"
              "<tr><td>Histogram</td><td>Distribution of 1 variable</td></tr>"
              "<tr><td>Box plot</td><td>Distribution + outliers by group</td></tr></tbody></table>"
              "<h3>Matplotlib Structure</h3><p><code>Figure</code> is the canvas. <code>Axes</code> (ax) is a single plot inside the Figure. Use <code>plt.subplots()</code> to create multi-chart figures.</p>",
              "import matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\n# Line chart\nmonths  = ['Jan','Feb','Mar','Apr','May','Jun']\nrevenue = [45000, 52000, 49000, 61000, 58000, 67000]\ntarget  = [50000] * 6\n\naxes[0].plot(months, revenue, marker='o', color='#10b981', linewidth=2.5, label='Actual')\naxes[0].plot(months, target,  linestyle='--', color='#ef4444', linewidth=1.5, label='Target')\naxes[0].fill_between(months, revenue, target, alpha=0.08, color='#10b981')\naxes[0].set_title('Revenue vs Target', fontweight='bold')\naxes[0].legend()\n\n# Bar chart\nregions = ['North','South','East','West']\nsales   = [450000, 320000, 510000, 390000]\naxes[1].bar(regions, sales, color=['#10b981','#3b82f6','#f59e0b','#ef4444'], edgecolor='white')\naxes[1].set_title('Sales by Region', fontweight='bold')\naxes[1].set_ylabel('Revenue')\n\nplt.tight_layout()\nplt.savefig('charts.png', dpi=150)\nplt.show()",
              "Add a horizontal dashed line at target=400000 on the bar chart using axhline()."),

            L("Seaborn Statistical Plots", 2, "python",
              "<h3>Seaborn vs Matplotlib</h3><p>Seaborn produces statistical charts in one line that take 20 lines in Matplotlib. Built for EDA.</p>"
              "<h3>Key Seaborn Plots</h3><ul>"
              "<li><code>sns.histplot()</code> — histogram with KDE</li>"
              "<li><code>sns.boxplot()</code> — distribution + outliers by category</li>"
              "<li><code>sns.scatterplot()</code> — relationship with color/size encoding</li>"
              "<li><code>sns.heatmap()</code> — correlation matrix</li>"
              "<li><code>sns.barplot()</code> — bar with confidence interval</li>"
              "<li><code>sns.pairplot()</code> — all-vs-all scatter matrix</li></ul>",
              "import seaborn as sns\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(42)\ndf = pd.DataFrame({\n    'sales'    : np.random.normal(5000, 1500, 200),\n    'region'   : np.random.choice(['North','South','East','West'], 200),\n    'category' : np.random.choice(['A','B','C'], 200),\n    'discount' : np.random.uniform(0, 0.4, 200),\n})\n\nfig, axes = plt.subplots(1, 3, figsize=(16, 5))\nsns.set_theme(style='whitegrid')\n\nsns.histplot(df['sales'], kde=True, ax=axes[0], color='#10b981')\naxes[0].set_title('Sales Distribution')\n\nsns.boxplot(data=df, x='region', y='sales', ax=axes[1], palette='Set2')\naxes[1].set_title('Sales by Region')\n\nsns.scatterplot(data=df, x='discount', y='sales', hue='category', ax=axes[2], alpha=0.7)\naxes[2].set_title('Sales vs Discount')\n\nplt.tight_layout()\nplt.show()",
              "Add a 4th subplot with a heatmap using sns.heatmap(df[['sales','discount']].corr(), annot=True)."),

            L("EDA Dashboard Design", 3, "python",
              "<h3>What is EDA?</h3><p>Exploratory Data Analysis is the process of visually and statistically inspecting a dataset before modelling.</p>"
              "<h3>A Complete EDA Dashboard Includes</h3><ol>"
              "<li>Distribution of target variable</li>"
              "<li>Category comparisons (box/bar)</li>"
              "<li>Correlation heatmap</li>"
              "<li>Scatter plots for key relationships</li>"
              "<li>Time trends if data has dates</li></ol>"
              "<blockquote>Good EDA answers: What is the shape? Are there outliers? Which features correlate with the target? Are there patterns by category or time?</blockquote>",
              "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt, seaborn as sns\n\nnp.random.seed(42)\nn = 300\ndf = pd.DataFrame({\n    'revenue'  : np.random.lognormal(9, 0.6, n),\n    'discount' : np.random.uniform(0, 0.5, n),\n    'quantity' : np.random.randint(1, 20, n),\n    'region'   : np.random.choice(['N','S','E','W'], n),\n    'month'    : np.random.choice(range(1,13), n),\n})\n\nfig = plt.figure(figsize=(16, 10))\nfig.suptitle('Sales EDA Dashboard', fontsize=16, fontweight='bold')\n\nax1 = fig.add_subplot(2,3,1)\nsns.histplot(df['revenue'], kde=True, ax=ax1, color='#10b981')\nax1.set_title('Revenue Distribution')\n\nax2 = fig.add_subplot(2,3,2)\nsns.boxplot(data=df, x='region', y='revenue', ax=ax2, palette='Set2')\nax2.set_title('Revenue by Region')\n\nax3 = fig.add_subplot(2,3,3)\nsns.heatmap(df[['revenue','discount','quantity']].corr(),\n            annot=True, fmt='.2f', ax=ax3, cmap='RdYlGn')\nax3.set_title('Correlation Matrix')\n\nax4 = fig.add_subplot(2,3,4)\nax4.scatter(df['discount'], df['revenue'], alpha=0.3, color='#6366f1')\nax4.set_xlabel('Discount'); ax4.set_ylabel('Revenue')\nax4.set_title('Discount vs Revenue')\n\nax5 = fig.add_subplot(2,3,5)\nmonthly = df.groupby('month')['revenue'].mean()\nax5.plot(monthly.index, monthly.values, marker='o', color='#f59e0b')\nax5.set_title('Avg Revenue by Month')\n\nplt.tight_layout()\nplt.show()",
              "Add a 6th subplot showing a bar chart of total revenue by region."),
        ]
    },

    {
        "title": "Statistics & EDA",
        "icon": "bi-bar-chart-steps",
        "description": "Descriptive statistics, distributions, correlation, hypothesis testing, and outlier detection.",
        "order": 5,
        "lessons": [
            L("Descriptive Statistics", 1, "python",
              "<h3>Measures of Central Tendency</h3><ul>"
              "<li><strong>Mean</strong> — average; sensitive to outliers</li>"
              "<li><strong>Median</strong> — middle value; robust to outliers</li>"
              "<li><strong>Mode</strong> — most frequent value</li></ul>"
              "<h3>Measures of Spread</h3><ul>"
              "<li><strong>Range</strong> — max - min</li>"
              "<li><strong>Std Dev</strong> — average distance from mean</li>"
              "<li><strong>IQR</strong> — Q3 - Q1 (middle 50%)</li></ul>"
              "<blockquote>If Mean >> Median: data is right-skewed (e.g., salaries, house prices).</blockquote>",
              "import numpy as np\nfrom scipy import stats\n\nsalaries = np.array([35000,42000,38000,41000,40000,45000,39000,250000,37000,43000])\n\nprint(f\"Mean   : {np.mean(salaries):>12,.0f}  <- pulled by outlier\")\nprint(f\"Median : {np.median(salaries):>12,.0f}  <- more representative\")\nprint(f\"Std Dev: {np.std(salaries, ddof=1):>12,.0f}\")\n\nQ1, Q3 = np.percentile(salaries, [25, 75])\nIQR = Q3 - Q1\nprint(f\"Q1={Q1:,}  Q3={Q3:,}  IQR={IQR:,}\")\n\nlower = Q1 - 1.5 * IQR\nupper = Q3 + 1.5 * IQR\noutliers = salaries[(salaries < lower) | (salaries > upper)]\nprint(f\"Outliers: {outliers}\")",
              "Remove the 250000 outlier and compare how mean, median, and IQR change."),

            L("Correlation Analysis", 2, "python",
              "<h3>Correlation</h3><p>Measures the linear relationship between two variables. Range: -1 to +1.</p><ul>"
              "<li>+1 = perfect positive correlation</li>"
              "<li>0 = no linear relationship</li>"
              "<li>-1 = perfect negative correlation</li></ul>"
              "<h3>Pearson vs Spearman</h3><ul>"
              "<li><strong>Pearson</strong> — linear relationships, assumes normality</li>"
              "<li><strong>Spearman</strong> — monotonic relationships, rank-based, robust to outliers</li></ul>"
              "<blockquote>Correlation does NOT imply causation. Always think critically about confounding variables.</blockquote>",
              "import pandas as pd, numpy as np, seaborn as sns\nimport matplotlib.pyplot as plt\nfrom scipy import stats\n\nnp.random.seed(42)\nn = 100\ndf = pd.DataFrame({\n    'ad_spend'      : np.random.uniform(1000, 10000, n),\n    'website_visits': None,\n    'conversions'   : None,\n    'revenue'       : None,\n})\ndf['website_visits'] = df['ad_spend'] * 5 + np.random.normal(0, 5000, n)\ndf['conversions']    = df['website_visits'] * 0.02 + np.random.normal(0, 20, n)\ndf['revenue']        = df['conversions'] * 150 + np.random.normal(0, 2000, n)\n\ncorr = df.corr()\nplt.figure(figsize=(8, 6))\nsns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', vmin=-1, vmax=1, square=True)\nplt.title('Correlation Matrix', fontweight='bold')\nplt.tight_layout()\nplt.show()\n\nr_p, p_p = stats.pearsonr(df['ad_spend'], df['revenue'])\nr_s, p_s = stats.spearmanr(df['ad_spend'], df['revenue'])\nprint(f\"Pearson r  = {r_p:.3f}  (p={p_p:.4f})\")\nprint(f\"Spearman r = {r_s:.3f}  (p={p_s:.4f})\")",
              "Add random noise to 'revenue' until the Pearson correlation drops below 0.5."),

            L("Hypothesis Testing", 3, "python",
              "<h3>What is Hypothesis Testing?</h3><p>Decides if an observed difference is real or just due to random chance.</p>"
              "<h3>Steps</h3><ol>"
              "<li>State H0 (null) and H1 (alternative)</li>"
              "<li>Choose significance level alpha (usually 0.05)</li>"
              "<li>Compute test statistic and p-value</li>"
              "<li>If p < alpha: reject H0</li></ol>"
              "<h3>Common Tests</h3><ul>"
              "<li><strong>t-test</strong> — compare means of 2 groups</li>"
              "<li><strong>ANOVA</strong> — compare means of 3+ groups</li>"
              "<li><strong>Chi-squared</strong> — independence of categorical variables</li></ul>"
              "<blockquote>p-value is NOT the probability that H0 is true. It is: given H0 is true, how likely is data at least this extreme?</blockquote>",
              "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\n\n# Two-sample t-test\ngroup_a = np.random.normal(75, 10, 50)\ngroup_b = np.random.normal(80, 12, 50)\n\nt_stat, p_value = stats.ttest_ind(group_a, group_b)\nprint(f\"Group A mean: {group_a.mean():.2f}\")\nprint(f\"Group B mean: {group_b.mean():.2f}\")\nprint(f\"t={t_stat:.4f}   p={p_value:.4f}\")\nif p_value < 0.05:\n    print(\"REJECT H0 -- significant difference\")\nelse:\n    print(\"FAIL TO REJECT H0 -- no significant difference\")\n\n# Chi-squared test\ncontingency = np.array([[120,80],[90,110],[75,125]])\nchi2, p, dof, expected = stats.chi2_contingency(contingency)\nprint(f\"\\nChi2 = {chi2:.4f}  p = {p:.4f}  dof = {dof}\")",
              "Run a one-sample t-test: H0 = mean of group_a equals 78. Is it rejected at alpha=0.05?"),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# WEB DEVELOPMENT
# ───────────────────────────────────────────────────────────────
WD_TOPICS = [
    {
        "title": "HTML Fundamentals",
        "icon": "bi-code-slash",
        "description": "Structure pages with semantic HTML5 — tags, attributes, forms, and accessibility.",
        "order": 1,
        "lessons": [
            L("HTML Document Structure", 1, "html",
              "<h3>What is HTML?</h3><p><strong>HTML (HyperText Markup Language)</strong> defines the structure and content of web pages.</p>"
              "<h3>Semantic HTML5 Elements</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Element</th><th>Purpose</th></tr></thead><tbody>"
              "<tr><td><code>&lt;header&gt;</code></td><td>Top area — logo, nav</td></tr>"
              "<tr><td><code>&lt;nav&gt;</code></td><td>Navigation links</td></tr>"
              "<tr><td><code>&lt;main&gt;</code></td><td>Primary page content</td></tr>"
              "<tr><td><code>&lt;section&gt;</code></td><td>Thematic grouping</td></tr>"
              "<tr><td><code>&lt;article&gt;</code></td><td>Self-contained content</td></tr>"
              "<tr><td><code>&lt;aside&gt;</code></td><td>Sidebar content</td></tr>"
              "<tr><td><code>&lt;footer&gt;</code></td><td>Bottom area</td></tr></tbody></table>"
              "<blockquote>Use semantic tags instead of generic &lt;div&gt; for better SEO and accessibility.</blockquote>",
              "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>My Page | TRHvision</title>\n  <meta name=\"description\" content=\"Learn web development with TRHvision.\">\n</head>\n<body>\n  <header>\n    <a href=\"/\"><img src=\"logo.png\" alt=\"TRHvision logo\" width=\"120\"></a>\n    <nav aria-label=\"Main navigation\">\n      <a href=\"/about\">About</a>\n      <a href=\"/courses\">Courses</a>\n    </nav>\n  </header>\n\n  <main>\n    <section id=\"hero\">\n      <h1>Learn Web Development</h1>\n      <p>Build real-world Django apps.</p>\n    </section>\n  </main>\n\n  <footer>\n    <p>&copy; 2026 TRHvision</p>\n  </footer>\n</body>\n</html>",
              "Add an <aside> with 'Quick Links' between main and footer."),

            L("HTML Forms — Complete Guide", 2, "html",
              "<h3>Forms</h3><p>Forms send user data to the server via HTTP GET or POST.</p>"
              "<h3>Input Types</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Type</th><th>Use</th></tr></thead><tbody>"
              "<tr><td>text, email, password, tel</td><td>Text entry</td></tr>"
              "<tr><td>number, range</td><td>Numeric</td></tr>"
              "<tr><td>date, time</td><td>Date/time picker</td></tr>"
              "<tr><td>checkbox, radio</td><td>Boolean / choices</td></tr>"
              "<tr><td>file</td><td>File upload</td></tr>"
              "<tr><td>hidden</td><td>CSRF tokens, IDs</td></tr></tbody></table>"
              "<h3>Validation Attributes</h3><ul>"
              "<li><code>required</code>, <code>minlength/maxlength</code>, <code>min/max</code>, <code>pattern</code></li></ul>",
              "<form action=\"/enroll/\" method=\"POST\" novalidate>\n  {% csrf_token %}\n\n  <fieldset>\n    <legend>Personal Information</legend>\n\n    <label for=\"fname\">First Name *</label>\n    <input type=\"text\" id=\"fname\" name=\"fname\"\n           required minlength=\"2\" maxlength=\"50\" placeholder=\"Priya\">\n\n    <label for=\"email\">Email *</label>\n    <input type=\"email\" id=\"email\" name=\"email\"\n           required placeholder=\"priya@example.com\">\n\n    <label for=\"phone\">Phone *</label>\n    <input type=\"tel\" id=\"phone\" name=\"phone\"\n           pattern=\"[6-9][0-9]{9}\" maxlength=\"10\" required>\n  </fieldset>\n\n  <fieldset>\n    <legend>Domain</legend>\n    <select id=\"domain\" name=\"domain\" required>\n      <option value=\"\">-- Select --</option>\n      <option value=\"da\">Data Analytics</option>\n      <option value=\"wd\">Web Development</option>\n    </select>\n  </fieldset>\n\n  <button type=\"submit\">Submit</button>\n</form>",
              "Add a <textarea> for 'Why do you want to join?' with rows=4, maxlength=500."),

            L("HTML Tables, Lists & Images", 3, "html",
              "<h3>Lists</h3><ul>"
              "<li><code>&lt;ul&gt;</code> — unordered (bullet)</li>"
              "<li><code>&lt;ol&gt;</code> — ordered (numbered)</li>"
              "<li><code>&lt;dl&gt;</code> — definition list (term + description)</li>"
              "<li>Lists can be nested for multi-level structures</li></ul>"
              "<h3>Tables</h3><p>Use for <em>tabular data only</em> — never for layout.</p><ul>"
              "<li><code>&lt;thead&gt;</code>, <code>&lt;tbody&gt;</code>, <code>&lt;tfoot&gt;</code></li>"
              "<li><code>colspan</code> / <code>rowspan</code> — merge cells</li>"
              "<li>Add <code>scope='col'</code> to &lt;th&gt; for accessibility</li></ul>"
              "<h3>Images</h3><p>Always add <code>alt</code> text. Use <code>loading='lazy'</code> for performance.</p>",
              "<h2>Python Learning Path</h2>\n<ol>\n  <li>Basics\n    <ul>\n      <li>Variables</li>\n      <li>Loops</li>\n      <li>Functions</li>\n    </ul>\n  </li>\n  <li>Libraries\n    <ul>\n      <li>Pandas</li>\n      <li>NumPy</li>\n    </ul>\n  </li>\n</ol>\n\n<table>\n  <caption>Q1 Sales Summary</caption>\n  <thead>\n    <tr>\n      <th scope=\"col\">Region</th>\n      <th scope=\"col\">Revenue</th>\n      <th scope=\"col\">Growth</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr><td>North</td><td>4,50,000</td><td>+12%</td></tr>\n    <tr><td>South</td><td>3,20,000</td><td>-5%</td></tr>\n  </tbody>\n  <tfoot>\n    <tr><td colspan=\"2\">Total</td><td>+7%</td></tr>\n  </tfoot>\n</table>\n\n<img src=\"chart.png\"\n     alt=\"Q1 sales bar chart by region\"\n     width=\"800\" loading=\"lazy\">",
              "Add a 'East' and 'West' row. Update the tfoot total to span the correct columns."),
        ]
    },

    {
        "title": "CSS Styling & Layout",
        "icon": "bi-palette-fill",
        "description": "Style pages with selectors, box model, Flexbox, CSS Grid, variables, and animations.",
        "order": 2,
        "lessons": [
            L("Selectors, Box Model & Colors", 1, "css",
              "<h3>CSS Selectors</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Selector</th><th>Example</th><th>Targets</th></tr></thead><tbody>"
              "<tr><td>Element</td><td><code>p</code></td><td>All &lt;p&gt;</td></tr>"
              "<tr><td>Class</td><td><code>.card</code></td><td>class='card'</td></tr>"
              "<tr><td>ID</td><td><code>#hero</code></td><td>id='hero'</td></tr>"
              "<tr><td>Pseudo-class</td><td><code>a:hover</code></td><td>On hover</td></tr>"
              "<tr><td>Descendant</td><td><code>.nav a</code></td><td>Links inside .nav</td></tr>"
              "<tr><td>Nth-child</td><td><code>tr:nth-child(even)</code></td><td>Even rows</td></tr></tbody></table>"
              "<h3>Box Model</h3><p>Content > Padding > Border > Margin (inside out).</p>"
              "<blockquote>Always use <code>box-sizing: border-box</code> — width includes padding and border.</blockquote>",
              "/* Reset */\n*, *::before, *::after {\n  box-sizing: border-box;\n  margin: 0;\n  padding: 0;\n}\n\n/* CSS Custom Properties */\n:root {\n  --color-primary  : #10b981;\n  --color-dark     : #111827;\n  --radius-md      : 12px;\n  --shadow-md      : 0 4px 16px rgba(0,0,0,.08);\n  --font-sans      : 'Inter', sans-serif;\n}\n\nbody {\n  font-family: var(--font-sans);\n  color: var(--color-dark);\n  background: #f8fafc;\n}\n\n.card {\n  background: #fff;\n  border-radius: var(--radius-md);\n  padding: 1.5rem 2rem;\n  margin-bottom: 1rem;\n  border: 1px solid #e5e7eb;\n  box-shadow: var(--shadow-md);\n}\n\n.card:hover {\n  transform: translateY(-2px);\n  box-shadow: 0 8px 24px rgba(0,0,0,.12);\n  transition: all 0.2s ease;\n}\n\ntr:nth-child(even) td {\n  background: #f9fafb;\n}",
              "Add a border-left: 4px solid var(--color-primary) accent to .card."),

            L("Flexbox Layout", 2, "css",
              "<h3>Flexbox — One-Dimensional Layout</h3><p>Flexbox arranges items in a row or column. It is the backbone of most modern UI layouts.</p>"
              "<h3>Container Properties</h3><ul>"
              "<li><code>display: flex</code> — activate flexbox</li>"
              "<li><code>flex-direction: row|column</code></li>"
              "<li><code>justify-content</code> — main axis alignment</li>"
              "<li><code>align-items</code> — cross axis alignment</li>"
              "<li><code>gap</code> — space between items</li>"
              "<li><code>flex-wrap: wrap</code> — wrap to new lines</li></ul>"
              "<h3>Item Properties</h3><ul>"
              "<li><code>flex: 1</code> — grow to fill space</li>"
              "<li><code>flex: 0 0 200px</code> — fixed 200px</li>"
              "<li><code>order</code> — change visual order</li></ul>",
              ".navbar {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 1rem;\n  padding: .75rem 2rem;\n  background: #fff;\n  border-bottom: 1px solid #e5e7eb;\n}\n\n.nav-links {\n  display: flex;\n  gap: 1.5rem;\n  list-style: none;\n}\n\n/* Responsive card grid */\n.card-grid {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 1.25rem;\n  padding: 2rem;\n}\n.card-grid > .card {\n  flex: 1 1 280px;\n  max-width: 360px;\n}\n\n/* Centered hero */\n.hero {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n  min-height: 80vh;\n  text-align: center;\n  gap: 1.5rem;\n}",
              "Create a sidebar layout: sidebar fixed 280px, main content takes remaining space with flex:1."),

            L("CSS Grid & Animations", 3, "css",
              "<h3>CSS Grid — Two-Dimensional Layout</h3><p>Grid controls rows AND columns simultaneously — perfect for overall page layouts.</p>"
              "<h3>Key Properties</h3><ul>"
              "<li><code>grid-template-columns: 280px 1fr</code></li>"
              "<li><code>gap</code> — space between cells</li>"
              "<li><code>grid-column: span 2</code> — span across columns</li>"
              "<li><code>repeat(auto-fill, minmax(280px,1fr))</code> — responsive grid</li></ul>"
              "<h3>CSS Transitions & Animations</h3><p><code>transition</code> animates property changes on interaction. <code>@keyframes</code> animations run automatically.</p>"
              "<blockquote>Only animate <code>transform</code> and <code>opacity</code> — GPU-accelerated, no layout reflow.</blockquote>",
              ".dashboard {\n  display: grid;\n  grid-template-areas:\n    \"sidebar header\"\n    \"sidebar main\";\n  grid-template-columns: 280px 1fr;\n  grid-template-rows: 60px 1fr;\n  min-height: 100vh;\n}\n.sidebar { grid-area: sidebar; }\n.header  { grid-area: header; }\n.main    { grid-area: main; padding: 2rem; }\n\n/* Auto-responsive grid — no media queries */\n.cards {\n  display: grid;\n  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));\n  gap: 1.5rem;\n}\n\n/* Transition */\n.btn {\n  background: #10b981;\n  color: #fff;\n  padding: .6rem 1.5rem;\n  border-radius: 8px;\n  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;\n}\n.btn:hover {\n  background: #059669;\n  transform: translateY(-2px);\n  box-shadow: 0 6px 20px rgba(16,185,129,.4);\n}\n\n/* Keyframe animation */\n@keyframes fadeInUp {\n  from { opacity:0; transform:translateY(20px); }\n  to   { opacity:1; transform:translateY(0); }\n}\n.hero-title { animation: fadeInUp 0.6s ease both; }",
              "Add a CSS spinner animation using @keyframes spin and border-top-color."),
        ]
    },

    {
        "title": "JavaScript Fundamentals",
        "icon": "bi-lightning-fill",
        "description": "Add interactivity with JS — DOM manipulation, events, fetch API, and ES6+ features.",
        "order": 3,
        "lessons": [
            L("Variables, Types & Functions", 1, "javascript",
              "<h3>JavaScript in the Browser</h3><p>JavaScript runs in the browser to make pages interactive — responding to clicks, validating forms, fetching data, and updating the DOM.</p>"
              "<h3>Variables</h3><ul>"
              "<li><code>const</code> — immutable binding (use by default)</li>"
              "<li><code>let</code> — mutable, block-scoped</li>"
              "<li><code>var</code> — avoid (function-scoped, hoisted)</li></ul>"
              "<h3>Template Literals</h3><p>Backtick strings: <code>`Hello ${name}!`</code></p>"
              "<h3>Modern Features</h3><ul>"
              "<li><code>??</code> — nullish coalescing</li>"
              "<li><code>?.</code> — optional chaining</li>"
              "<li>Destructuring: <code>const {name, score} = student;</code></li>"
              "<li>Spread: <code>[...arr1, ...arr2]</code></li></ul>",
              "// Variables\nconst MAX = 3;\nlet page = 1;\n\nconst name    = 'Alice';\nconst score   = 98.5;\nconst active  = true;\nlet   draft;   // undefined\n\nconsole.log(typeof name);   // string\n\n// Template literal\nconsole.log(`Hello ${name}! Score: ${score.toFixed(1)}`);\n\n// Nullish coalescing\nconst label = null ?? 'Unknown';   // Unknown\n\n// Optional chaining\nconst user = { profile: { email: 'a@b.com' } };\nconsole.log(user?.profile?.email);    // a@b.com\nconsole.log(user?.address?.city);     // undefined\n\n// Destructuring\nconst student = { id: 1, domain: 'Data Analytics', grade: 'A' };\nconst { domain, grade } = student;\nconsole.log(domain, grade);\n\n// Arrow functions\nconst double = x => x * 2;\nconst add    = (a, b) => a + b;\nconsole.log(double(5), add(3, 4));",
              "Add a 'scores' array and use .map() to double each value, then .filter() to keep only > 100."),

            L("DOM Manipulation & Events", 2, "javascript",
              "<h3>The DOM</h3><p>The Document Object Model (DOM) represents the HTML page as a tree that JavaScript can read and modify.</p>"
              "<h3>Selecting Elements</h3><ul>"
              "<li><code>document.getElementById('id')</code></li>"
              "<li><code>document.querySelector('.class')</code> — first match</li>"
              "<li><code>document.querySelectorAll('p')</code> — all matches</li></ul>"
              "<h3>Modifying Elements</h3><ul>"
              "<li><code>el.textContent = 'text'</code> — safe text</li>"
              "<li><code>el.innerHTML = '<b>html</b>'</code> — HTML (XSS risk)</li>"
              "<li><code>el.classList.add/remove/toggle('class')</code></li>"
              "<li><code>el.setAttribute('href', url)</code></li></ul>"
              "<h3>Events</h3><p>Use <code>addEventListener</code> — not <code>onclick</code> HTML attributes.</p>"
              "<blockquote>Event delegation: attach one listener to a parent instead of hundreds to children.</blockquote>",
              "// Select & modify\nconst title = document.getElementById('page-title');\ntitle.textContent = 'Updated!';\ntitle.style.color = '#10b981';\n\ndocument.querySelectorAll('.card').forEach(card => {\n  card.classList.add('animated');\n});\n\n// Create element dynamically\nfunction addAlert(msg, type = 'info') {\n  const div = document.createElement('div');\n  div.className = `alert alert-${type}`;\n  div.textContent = msg;\n  document.getElementById('notifications').prepend(div);\n  setTimeout(() => div.remove(), 3000);\n}\n\n// Event listeners\nconst btn = document.getElementById('submit-btn');\nbtn.addEventListener('click', () => addAlert('Clicked!', 'success'));\n\n// Form submission\ndocument.getElementById('form').addEventListener('submit', (e) => {\n  e.preventDefault();\n  const email = document.getElementById('email').value.trim();\n  if (!email.includes('@')) { addAlert('Invalid email!', 'danger'); return; }\n  console.log('Submitting:', email);\n});\n\n// Event delegation for dynamic list\ndocument.getElementById('list').addEventListener('click', (e) => {\n  if (e.target.classList.contains('delete-btn'))\n    e.target.closest('li').remove();\n});",
              "Add real-time validation: change input border to green when email includes '@', red otherwise."),

            L("Fetch API & Async/Await", 3, "javascript",
              "<h3>Asynchronous JavaScript</h3><p>Fetching data takes time. JS uses async patterns so the page stays responsive.</p>"
              "<h3>Evolution</h3><ol>"
              "<li>Callbacks — callback hell</li>"
              "<li>Promises — .then().catch()</li>"
              "<li><strong>async/await</strong> — modern, readable (use this)</li></ol>"
              "<h3>fetch() API</h3><p>Built-in function for HTTP requests. Returns a Promise.</p>"
              "<blockquote>Always handle errors with try/catch when using async/await.</blockquote>",
              "// GET request\nasync function loadStudent(id) {\n  const spinner = document.getElementById('spinner');\n  spinner.classList.remove('d-none');\n\n  try {\n    const res = await fetch(`/api/students/${id}/`);\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n\n    const data = await res.json();\n    renderStudent(data);\n\n  } catch (err) {\n    console.error('Failed:', err);\n    showToast('Could not load data.', 'error');\n\n  } finally {\n    spinner.classList.add('d-none');\n  }\n}\n\n// POST request\nasync function submitForm(payload) {\n  const res = await fetch('/api/enroll/', {\n    method: 'POST',\n    headers: {\n      'Content-Type': 'application/json',\n      'X-CSRFToken' : document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? ''\n    },\n    body: JSON.stringify(payload)\n  });\n  const data = await res.json();\n  if (!res.ok) throw new Error(data.detail ?? 'Submission failed');\n  return data;\n}",
              "Add Promise.all() to fetch student AND their tasks in parallel before rendering."),
        ]
    },

    {
        "title": "Django Basics",
        "icon": "bi-server",
        "description": "Build server-side web apps with Django — models, views, templates, forms, and authentication.",
        "order": 4,
        "lessons": [
            L("MVT Architecture & URLs", 1, "python",
              "<h3>Django MVT Pattern</h3>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Layer</th><th>File</th><th>Responsibility</th></tr></thead><tbody>"
              "<tr><td>Model</td><td>models.py</td><td>Database schema + ORM</td></tr>"
              "<tr><td>View</td><td>views.py</td><td>Business logic + HTTP</td></tr>"
              "<tr><td>Template</td><td>templates/</td><td>HTML presentation</td></tr>"
              "<tr><td>URL</td><td>urls.py</td><td>Route URLs to views</td></tr></tbody></table>"
              "<h3>URL Patterns</h3><ul>"
              "<li><code>path('about/', views.about, name='about')</code></li>"
              "<li><code>path('student/&lt;int:pk&gt;/', views.detail)</code> — dynamic param</li>"
              "<li><code>include('app.urls')</code> — include sub-app URLs</li></ul>",
              "# urls.py\nfrom django.urls import path, include\nfrom . import views\n\nurlpatterns = [\n    path('',                          views.home,           name='home'),\n    path('about/',                    views.about,          name='about'),\n    path('student/<int:student_id>/', views.student_detail, name='student_detail'),\n    path('task/<slug:slug>/',         views.task_detail,    name='task_detail'),\n    path('blog/',                     include('blog.urls')),\n]\n\n# views.py\nfrom django.shortcuts import render, get_object_or_404\nfrom .models import Student\n\ndef home(request):\n    return render(request, 'home.html', {'title': 'Welcome'})\n\ndef student_detail(request, student_id):\n    student = get_object_or_404(Student, pk=student_id)\n    return render(request, 'student/detail.html', {'student': student})\n\n# In templates:\n# <a href=\"{% url 'student_detail' student.id %}\">View</a>",
              "Add a URL for /profile/<username>/ and write the matching view."),

            L("Models & ORM Queries", 2, "python",
              "<h3>Django ORM</h3><p>Interact with the database using Python instead of SQL. Each Model class maps to a database table.</p>"
              "<h3>Common Field Types</h3><ul>"
              "<li><code>CharField(max_length)</code>, <code>TextField()</code></li>"
              "<li><code>IntegerField()</code>, <code>FloatField()</code></li>"
              "<li><code>BooleanField()</code>, <code>DateTimeField(auto_now_add=True)</code></li>"
              "<li><code>ForeignKey()</code> — many-to-one</li>"
              "<li><code>ManyToManyField()</code>, <code>OneToOneField()</code></li></ul>"
              "<h3>QuerySet API (Chaining)</h3><ul>"
              "<li><code>.filter(), .exclude(), .get()</code></li>"
              "<li><code>.order_by(), .values(), .distinct()</code></li>"
              "<li><code>.select_related(), .prefetch_related()</code> — avoid N+1</li>"
              "<li><code>.aggregate(), .annotate()</code> — SQL aggregations</li></ul>",
              "from django.db import models\nfrom django.contrib.auth.models import User\n\nclass Article(models.Model):\n    STATUS = [('draft','Draft'),('published','Published')]\n\n    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')\n    title      = models.CharField(max_length=200)\n    slug       = models.SlugField(max_length=200, unique=True)\n    body       = models.TextField()\n    status     = models.CharField(max_length=10, choices=STATUS, default='draft')\n    created_at = models.DateTimeField(auto_now_add=True)\n    view_count = models.IntegerField(default=0)\n\n    class Meta:\n        ordering = ['-created_at']\n        indexes  = [models.Index(fields=['status', 'created_at'])]\n\n    def __str__(self):\n        return self.title\n\n# ORM queries in views.py\npublished = Article.objects.filter(status='published').select_related('author')\ntop10     = published.order_by('-view_count')[:10]\ncount     = published.count()\nfrom django.db.models import Sum, Avg\nstats = published.aggregate(total_views=Sum('view_count'), avg=Avg('view_count'))",
              "Write a query to find all articles by a specific user with more than 100 views."),

            L("Templates & Template Tags", 3, "html",
              "<h3>Django Template Language (DTL)</h3>"
              "<h3>Core Syntax</h3><ul>"
              "<li><code>{{ variable }}</code> — output value</li>"
              "<li><code>{{ var|filter }}</code> — apply filter (e.g. <code>|date:'d M Y'</code>)</li>"
              "<li><code>{% tag %}</code> — template logic</li></ul>"
              "<h3>Common Tags</h3><ul>"
              "<li><code>{% if %}{% elif %}{% else %}{% endif %}</code></li>"
              "<li><code>{% for x in list %}{% empty %}{% endfor %}</code></li>"
              "<li><code>{% url 'name' arg %}</code></li>"
              "<li><code>{% static 'path' %}</code></li>"
              "<li><code>{% csrf_token %}</code></li>"
              "<li><code>{% extends 'base.html' %}</code></li>"
              "<li><code>{% block name %}{% endblock %}</code></li></ul>",
              "{# base.html #}\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <title>{% block title %}TRHvision{% endblock %}</title>\n  {% load static %}\n  <link rel=\"stylesheet\" href=\"{% static 'css/style.css' %}\">\n</head>\n<body>\n  {% include 'partials/navbar.html' %}\n  {% if messages %}\n    {% for msg in messages %}\n      <div class=\"alert alert-{{ msg.tags }}\">{{ msg }}</div>\n    {% endfor %}\n  {% endif %}\n  <main>{% block content %}{% endblock %}</main>\n</body>\n</html>\n\n{# articles/list.html #}\n{% extends 'base.html' %}\n{% block title %}Articles | {{ block.super }}{% endblock %}\n{% block content %}\n  <h1>{{ category.name }}</h1>\n  {% for article in articles %}\n    <article class=\"card\">\n      <h2><a href=\"{% url 'article_detail' article.slug %}\">{{ article.title }}</a></h2>\n      <time>{{ article.created_at|date:'d M Y' }}</time>\n      <p>{{ article.body|truncatewords:30 }}</p>\n    </article>\n  {% empty %}\n    <p>No articles yet.</p>\n  {% endfor %}\n{% endblock %}",
              "Create a 'detail.html' extending base.html that shows a single article with author and date."),

            L("Django Forms & Validation", 4, "python",
              "<h3>Django Forms</h3><p>Django's form library renders HTML, parses submitted data, and validates inputs.</p>"
              "<h3>Two Form Types</h3><ul>"
              "<li><strong>Form</strong> — independent, not tied to a model</li>"
              "<li><strong>ModelForm</strong> — auto-generates fields from a model</li></ul>"
              "<h3>Validation Flow</h3><ol>"
              "<li>User submits → <code>form = MyForm(request.POST)</code></li>"
              "<li><code>form.is_valid()</code> — run all validators</li>"
              "<li>If valid: <code>form.cleaned_data</code> has sanitized values</li>"
              "<li>If invalid: re-render with <code>form.errors</code></li></ol>",
              "# forms.py\nfrom django import forms\nfrom .models import Article\n\nclass ContactForm(forms.Form):\n    name    = forms.CharField(max_length=100)\n    email   = forms.EmailField()\n    message = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))\n\n    def clean_message(self):\n        msg = self.cleaned_data['message']\n        if len(msg) < 20:\n            raise forms.ValidationError('Message must be at least 20 characters.')\n        return msg.strip()\n\nclass ArticleForm(forms.ModelForm):\n    class Meta:\n        model  = Article\n        fields = ['title', 'body', 'status']\n\n# views.py\ndef contact(request):\n    if request.method == 'POST':\n        form = ContactForm(request.POST)\n        if form.is_valid():\n            send_email(form.cleaned_data)\n            messages.success(request, 'Sent!')\n            return redirect('contact')\n    else:\n        form = ContactForm()\n    return render(request, 'contact.html', {'form': form})",
              "Add a 'phone' field with a validator that raises ValidationError if not 10 digits."),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# MACHINE LEARNING
# ───────────────────────────────────────────────────────────────
ML_TOPICS = [
    {
        "title": "Python for Machine Learning",
        "icon": "bi-cpu-fill",
        "description": "NumPy arrays, Pandas preprocessing, and the SciPy ecosystem for ML.",
        "order": 1,
        "lessons": [
            L("NumPy Arrays & Operations", 1, "python",
              "<h3>Why NumPy?</h3><p>ML models are matrix operations. NumPy provides high-performance n-dimensional arrays backed by C code — 100x faster than Python lists.</p>"
              "<h3>Key Concepts</h3><ul>"
              "<li><code>np.array()</code> — create from list</li>"
              "<li><code>np.zeros(), np.ones(), np.eye()</code> — special matrices</li>"
              "<li><code>np.random.*</code> — random arrays</li>"
              "<li><strong>Broadcasting</strong> — operate on arrays of different shapes</li></ul>"
              "<h3>Matrix Operations</h3><p>The <code>@</code> operator performs matrix multiplication — the core of linear algebra in ML.</p>",
              "import numpy as np\n\na = np.array([1, 2, 3, 4, 5], dtype=np.float64)\nb = np.array([[1,2,3],[4,5,6],[7,8,9]])\n\nprint(f\"a.shape: {a.shape}  dtype: {a.dtype}\")\nprint(f\"b.shape: {b.shape}\")\n\n# Vectorized math\nprint(np.sqrt(a))           # [1. 1.41 1.73 2. 2.24]\nprint(a.mean(), a.std())\n\n# Matrix multiply\nX = np.random.randn(100, 5)  # 100 samples, 5 features\nw = np.random.randn(5)       # weights\npred = X @ w + 0.5           # linear prediction\nprint(f\"Predictions: {pred.shape}\")\n\n# Standardize features (z-score)\nX_norm = (X - X.mean(axis=0)) / X.std(axis=0)\nprint(f\"Means after norm: {X_norm.mean(axis=0).round(3)}\")",
              "Create a 5x5 random integer matrix (0-9) and compute row-wise mean and column-wise sum."),

            L("Pandas Preprocessing for ML", 2, "python",
              "<h3>ML Preprocessing Pipeline</h3><ol>"
              "<li><strong>Load & explore</strong></li>"
              "<li><strong>Handle missing values</strong> — impute or drop</li>"
              "<li><strong>Encode categoricals</strong> — one-hot or label encoding</li>"
              "<li><strong>Scale numerics</strong> — StandardScaler / MinMaxScaler</li>"
              "<li><strong>Split</strong> — train/validation/test</li></ol>"
              "<h3>One-Hot Encoding</h3><p>Convert categorical columns to binary columns using <code>pd.get_dummies()</code>.</p>"
              "<h3>Feature Scaling</h3><p>StandardScaler: mean=0, std=1. MinMaxScaler: range [0,1]. Most ML algorithms require scaling.</p>",
              "import pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler\n\nnp.random.seed(42)\nn = 200\ndf = pd.DataFrame({\n    'age'    : np.random.randint(22, 55, n),\n    'salary' : np.random.normal(50000, 15000, n),\n    'dept'   : np.random.choice(['Sales','Tech','HR'], n),\n    'churned': np.random.choice([0,1], n, p=[0.8,0.2])\n})\n\n# Missing values\ndf.loc[np.random.choice(df.index,10), 'salary'] = np.nan\ndf['salary'].fillna(df['salary'].median(), inplace=True)\n\n# One-hot encode\ndf = pd.get_dummies(df, columns=['dept'], drop_first=True)\nprint(df.head())\nprint(df.dtypes)\n\n# Scale numeric features\nfeatures = ['age','salary']\nscaler = StandardScaler()\ndf[features] = scaler.fit_transform(df[features])\nprint(\"\\nAfter scaling:\")\nprint(df[features].describe().round(3))",
              "Add MinMaxScaler on 'age' column. Compare the output range vs StandardScaler."),
        ]
    },

    {
        "title": "Supervised Learning",
        "icon": "bi-diagram-3-fill",
        "description": "Linear regression, logistic regression, decision trees, random forests, and SVM.",
        "order": 2,
        "lessons": [
            L("Linear Regression", 1, "python",
              "<h3>Linear Regression</h3><p>Predicts a <strong>continuous</strong> output using a weighted sum of features.</p>"
              "<code>y = w1*x1 + w2*x2 + ... + b</code>"
              "<h3>Evaluation Metrics</h3><ul>"
              "<li><strong>R²</strong> — goodness of fit (1 = perfect, 0 = baseline)</li>"
              "<li><strong>RMSE</strong> — root mean squared error (same unit as target)</li>"
              "<li><strong>MAE</strong> — mean absolute error (robust to outliers)</li></ul>",
              "from sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error, r2_score\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 500\ndf = pd.DataFrame({\n    'house_size': np.random.uniform(500, 3000, n),\n    'bedrooms'  : np.random.randint(1, 6, n),\n    'age'       : np.random.randint(0, 50, n),\n})\ndf['price'] = df['house_size']*150 + df['bedrooms']*20000 - df['age']*1000 + np.random.normal(0,15000,n)\n\nX = df[['house_size','bedrooms','age']]\ny = df['price']\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nmodel = LinearRegression().fit(X_train, y_train)\ny_pred = model.predict(X_test)\n\nprint(\"Coefficients:\")\nfor f, c in zip(X.columns, model.coef_):\n    print(f\"  {f:12}: {c:+.2f}\")\nprint(f\"R2 = {r2_score(y_test,y_pred):.4f}\")\nprint(f\"RMSE = {np.sqrt(mean_squared_error(y_test,y_pred)):,.0f}\")\nprint(f\"Predict 2000sqft,3bed,10yr: {model.predict([[2000,3,10]])[0]:,.0f}\")",
              "Add 'distance_from_city' as a feature. Does R² improve?"),

            L("Classification — Logistic Regression", 2, "python",
              "<h3>Classification</h3><p>Predicts a <strong>discrete class label</strong> (0/1, pass/fail, spam/not-spam).</p>"
              "<h3>Logistic Regression</h3><p>Uses the sigmoid function to output probability between 0 and 1.</p>"
              "<h3>Metrics</h3><ul>"
              "<li><strong>Accuracy</strong> — % correct (misleading on imbalanced data)</li>"
              "<li><strong>Precision</strong> — of predicted positives, % truly positive</li>"
              "<li><strong>Recall</strong> — of actual positives, % detected</li>"
              "<li><strong>F1</strong> — harmonic mean of precision and recall</li>"
              "<li><strong>AUC-ROC</strong> — overall discriminative ability (0.5 random, 1.0 perfect)</li></ul>",
              "from sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report, roc_auc_score\nfrom sklearn.preprocessing import StandardScaler\nimport numpy as np, pandas as pd\n\nnp.random.seed(42)\nn = 1000\ndf = pd.DataFrame({\n    'study_hours'   : np.random.uniform(0, 10, n),\n    'prev_score'    : np.random.uniform(40, 100, n),\n    'attendance_pct': np.random.uniform(50, 100, n),\n})\ndf['passed'] = ((df['study_hours']*5+df['prev_score']*0.5+df['attendance_pct']*0.3+np.random.normal(0,10,n))>80).astype(int)\n\nX = df[['study_hours','prev_score','attendance_pct']]\ny = df['passed']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nscaler = StandardScaler()\nX_tr = scaler.fit_transform(X_train)\nX_te = scaler.transform(X_test)\n\nmodel = LogisticRegression(max_iter=1000).fit(X_tr, y_train)\ny_pred = model.predict(X_te)\ny_prob = model.predict_proba(X_te)[:,1]\n\nprint(classification_report(y_test, y_pred, target_names=['Failed','Passed']))\nprint(f\"AUC-ROC: {roc_auc_score(y_test,y_prob):.4f}\")",
              "Change the classification threshold from 0.5 to 0.3 using predict_proba. Does recall improve?"),

            L("Random Forest & Feature Importance", 3, "python",
              "<h3>Random Forest</h3><p>Ensemble of many decision trees. Each trained on a random data subset and random features. Averages predictions — far more accurate and robust than a single tree.</p>"
              "<h3>Key Hyperparameters</h3><ul>"
              "<li><code>n_estimators</code> — number of trees</li>"
              "<li><code>max_depth</code> — controls overfitting</li>"
              "<li><code>min_samples_split</code> — minimum samples per split</li></ul>"
              "<h3>Feature Importance</h3><p>Built-in score showing which variables drive predictions most.</p>"
              "<h3>Cross-Validation</h3><p>5-fold CV gives a robust accuracy estimate using all data.</p>",
              "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split, cross_val_score\nimport pandas as pd\n\ndata = load_breast_cancer()\nX, y = data.data, data.target\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nrf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1)\nrf.fit(X_train, y_train)\n\nprint(f\"Test accuracy: {rf.score(X_test, y_test):.4f}\")\n\ncv = cross_val_score(rf, X, y, cv=5)\nprint(f\"5-fold CV: {cv.mean():.4f} +/- {cv.std():.4f}\")\n\n# Feature importance\nimportances = pd.Series(rf.feature_importances_, index=data.feature_names)\nprint(\"\\nTop 10 features:\")\nprint(importances.nlargest(10).round(4))",
              "Try n_estimators=10 vs 500. At what value does accuracy plateau?"),
        ]
    },

    {
        "title": "Model Evaluation & Tuning",
        "icon": "bi-speedometer2",
        "description": "Cross-validation, hyperparameter tuning with GridSearch/RandomSearch, and pipelines.",
        "order": 3,
        "lessons": [
            L("Cross-Validation & Pipelines", 1, "python",
              "<h3>Why Cross-Validation?</h3><p>A single split depends on which data lands in each partition. K-Fold CV uses ALL data for testing by rotating the test set K times.</p>"
              "<h3>K-Fold CV Steps</h3><ol>"
              "<li>Split into K folds</li>"
              "<li>Train on K-1 folds, test on the remaining fold</li>"
              "<li>Repeat K times</li>"
              "<li>Average the K scores</li></ol>"
              "<h3>Pipelines</h3><p>Chain preprocessing and model into one object. Prevents data leakage by fitting scaler only on training data.</p>",
              "from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import cross_val_score, StratifiedKFold\nfrom sklearn.datasets import load_breast_cancer\n\nX, y = load_breast_cancer().data, load_breast_cancer().target\n\nmodels = {\n    'Logistic': Pipeline([('scaler',StandardScaler()),('clf',LogisticRegression(max_iter=1000))]),\n    'RF'      : RandomForestClassifier(n_estimators=100, random_state=42)\n}\n\ncv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n\nfor name, model in models.items():\n    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')\n    print(f\"{name:12}: {scores.mean():.4f} +/- {scores.std():.4f}\")",
              "Add 'f1_weighted' as a second scoring metric and compare the two."),

            L("Hyperparameter Tuning", 2, "python",
              "<h3>Hyperparameters</h3><p>Settings that control training — NOT learned from data. Examples: n_estimators, max_depth, C, learning_rate.</p>"
              "<h3>Tuning Methods</h3><ul>"
              "<li><strong>GridSearchCV</strong> — exhaustive, slow but thorough</li>"
              "<li><strong>RandomizedSearchCV</strong> — random sample, faster, good for large spaces</li>"
              "<li><strong>BayesianOptimization</strong> — smartest, uses past results to guide search</li></ul>"
              "<blockquote>Always tune using CV on training set only. Never use test set during tuning — data leakage.</blockquote>",
              "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import RandomizedSearchCV, train_test_split\nfrom sklearn.datasets import load_breast_cancer\nfrom scipy.stats import randint\n\nX, y = load_breast_cancer().data, load_breast_cancer().target\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nparam_dist = {\n    'n_estimators'    : randint(50, 500),\n    'max_depth'       : [None, 5, 10, 20],\n    'min_samples_split': randint(2, 20),\n    'max_features'    : ['sqrt', 'log2'],\n}\n\nsearch = RandomizedSearchCV(\n    RandomForestClassifier(random_state=42),\n    param_dist, n_iter=30, cv=5,\n    scoring='f1_weighted', random_state=42, n_jobs=-1, verbose=1\n)\nsearch.fit(X_train, y_train)\n\nprint(\"Best params:\", search.best_params_)\nprint(f\"Best CV score: {search.best_score_:.4f}\")\nprint(f\"Test score   : {search.best_estimator_.score(X_test,y_test):.4f}\")",
              "Try GridSearchCV with 3 values per hyperparameter. Compare runtime to RandomizedSearchCV."),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# DATA SCIENCE
# ───────────────────────────────────────────────────────────────
DS_TOPICS = [
    {
        "title": "Statistics for Data Science",
        "icon": "bi-database-fill",
        "description": "Descriptive stats, probability, hypothesis testing, and statistical inference.",
        "order": 1,
        "lessons": [
            L("Descriptive Statistics", 1, "python",
              "<h3>Measures of Central Tendency</h3><ul>"
              "<li><strong>Mean</strong> — average; sensitive to extremes</li>"
              "<li><strong>Median</strong> — middle value; robust to outliers</li>"
              "<li><strong>Mode</strong> — most frequent; for categorical data</li></ul>"
              "<h3>Measures of Spread</h3><ul>"
              "<li><strong>Range</strong> — max - min</li>"
              "<li><strong>Std Dev</strong> — average distance from mean</li>"
              "<li><strong>IQR</strong> = Q3 - Q1 (middle 50%)</li></ul>"
              "<blockquote>5-number summary (Min, Q1, Median, Q3, Max) is the foundation of the box plot.</blockquote>",
              "import numpy as np\nfrom scipy import stats\n\narr = np.array([35000,42000,38000,41000,40000,45000,39000,250000,37000,43000])\n\nprint(f\"Mean   : {np.mean(arr):>12,.0f}\")\nprint(f\"Median : {np.median(arr):>12,.0f}\")\nprint(f\"Std Dev: {np.std(arr,ddof=1):>12,.0f}\")\n\nQ1, Q3 = np.percentile(arr, [25,75])\nIQR = Q3 - Q1\nprint(f\"IQR = {IQR:,.0f}\")\n\nlower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR\nprint(f\"Outlier bounds: ({lower:,.0f}, {upper:,.0f})\")\nprint(f\"Outliers: {arr[(arr<lower)|(arr>upper)]}\")",
              "Remove 250000 and compare mean, median, std dev before/after."),

            L("Probability & Bayes Theorem", 2, "python",
              "<h3>Basic Rules</h3><ul>"
              "<li><strong>P(A or B)</strong> = P(A) + P(B) - P(A and B)</li>"
              "<li><strong>P(A and B)</strong> = P(A) * P(B|A)</li>"
              "<li><strong>P(A|B)</strong> = P(A and B) / P(B)</li></ul>"
              "<h3>Bayes Theorem</h3><p><code>P(H|E) = P(E|H) * P(H) / P(E)</code></p><ul>"
              "<li><strong>P(H)</strong> — prior (before evidence)</li>"
              "<li><strong>P(E|H)</strong> — likelihood</li>"
              "<li><strong>P(H|E)</strong> — posterior (updated belief)</li></ul>"
              "<blockquote>A rare disease test with 99% accuracy still gives mostly false positives — because the disease prevalence (prior) is very low.</blockquote>",
              "# Medical Test Paradox — Bayes Theorem\np_disease = 0.01      # 1% prevalence (prior)\np_pos_disease = 0.99  # 99% sensitivity\np_pos_healthy = 0.05  # 5% false positive rate\n\np_positive = p_pos_disease * p_disease + p_pos_healthy * (1 - p_disease)\n\n# P(Disease | Positive test)\np_disease_given_pos = (p_pos_disease * p_disease) / p_positive\n\nprint(f\"Prevalence        : {p_disease*100:.1f}%\")\nprint(f\"Test sensitivity  : {p_pos_disease*100:.0f}%\")\nprint(f\"P(Disease | +test): {p_disease_given_pos*100:.1f}%\")\nprint()\nprint(\"Even with 99% sensitivity, a positive test means\")\nprint(f\"only {p_disease_given_pos*100:.1f}% chance of actually having the disease!\")",
              "Change prevalence to 10% and see how the posterior changes dramatically."),

            L("Hypothesis Testing", 3, "python",
              "<h3>Statistical Significance</h3><p>Hypothesis testing decides if an observed difference is real or due to random chance.</p>"
              "<h3>Steps</h3><ol>"
              "<li>H0 (null): no effect/difference</li>"
              "<li>H1 (alternative): there is an effect</li>"
              "<li>Alpha = 0.05 (significance level)</li>"
              "<li>Compute p-value</li>"
              "<li>p < 0.05: reject H0</li></ol>"
              "<h3>Tests</h3><ul>"
              "<li><strong>t-test</strong> — compare 2 group means</li>"
              "<li><strong>ANOVA</strong> — compare 3+ group means</li>"
              "<li><strong>Chi-squared</strong> — test independence of categoricals</li></ul>",
              "import numpy as np\nfrom scipy import stats\n\nnp.random.seed(42)\ngroupA = np.random.normal(75, 10, 50)  # control\ngroupB = np.random.normal(80, 12, 50)  # treatment\n\nt, p = stats.ttest_ind(groupA, groupB)\nprint(f\"Group A mean: {groupA.mean():.2f}\")\nprint(f\"Group B mean: {groupB.mean():.2f}\")\nprint(f\"t = {t:.4f}  p = {p:.4f}\")\nprint('REJECT H0' if p < 0.05 else 'FAIL TO REJECT H0')\n\n# ANOVA: compare 3 groups\ngroupC = np.random.normal(85, 8, 50)\nF, p_anova = stats.f_oneway(groupA, groupB, groupC)\nprint(f\"\\nANOVA: F={F:.4f}  p={p_anova:.4f}\")",
              "Run with group means 74 and 76 — is the difference still significant?"),
        ]
    },

    {
        "title": "Exploratory Data Analysis",
        "icon": "bi-search",
        "description": "EDA process: profiling, cleaning, visualizing, and communicating insights.",
        "order": 2,
        "lessons": [
            L("Data Profiling", 1, "python",
              "<h3>Profiling Checklist</h3><ol>"
              "<li>Shape — rows and columns</li>"
              "<li>Column types — numeric, categorical, datetime</li>"
              "<li>Missing values — count and % per column</li>"
              "<li>Unique values — cardinality</li>"
              "<li>Distribution — mean, std, skewness for numerics</li>"
              "<li>Category frequencies — value_counts() for categoricals</li>"
              "<li>Duplicates — exact row duplicates</li></ol>"
              "<blockquote>The <code>ydata-profiling</code> library generates a full HTML report automatically: <code>ProfileReport(df).to_file('report.html')</code></blockquote>",
              "import pandas as pd, numpy as np\n\nnp.random.seed(42)\nn = 300\ndf = pd.DataFrame({\n    'pclass'  : np.random.choice([1,2,3], n),\n    'age'     : np.where(np.random.random(n)<0.2, np.nan, np.random.normal(32,14,n).clip(1,80)),\n    'fare'    : np.random.lognormal(3, 1, n),\n    'survived': np.random.choice([0,1], n),\n    'embarked': np.random.choice(['S','C','Q',None], n, p=[0.7,0.2,0.08,0.02])\n})\n\nprint(f\"Shape: {df.shape}\")\nprint(\"\\n--- dtypes ---\")\nprint(df.dtypes)\nprint(\"\\n--- Missing values ---\")\nmissing = df.isnull().sum()\nprint(pd.DataFrame({'count':missing,'pct':(missing/len(df)*100).round(1)})[missing>0])\nprint(\"\\n--- Duplicates:\", df.duplicated().sum())\nprint(\"\\n--- Describe ---\")\nprint(df.describe().round(2))\nprint(\"\\n--- survived counts ---\")\nprint(df['survived'].value_counts())",
              "Add a 'cabin' column with 70% missing. Decide: drop it or impute it? Why?"),

            L("EDA Visualization Report", 2, "python",
              "<h3>Full EDA Visualization</h3><p>A complete EDA report combines:</p><ol>"
              "<li>Distribution of key variables</li>"
              "<li>Category breakdowns (bar/box)</li>"
              "<li>Correlation matrix</li>"
              "<li>Outlier analysis (box plot)</li>"
              "<li>Survival/target analysis</li></ol>"
              "<blockquote>EDA is not optional — every ML project should start here. Skipping EDA leads to incorrect models and missed insights.</blockquote>",
              "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt, seaborn as sns\n\nnp.random.seed(42)\nn = 300\ndf = pd.DataFrame({\n    'age'     : np.random.normal(32,14,n).clip(1,80),\n    'fare'    : np.random.lognormal(3,1,n),\n    'pclass'  : np.random.choice([1,2,3], n),\n    'survived': np.random.choice([0,1],n,p=[0.62,0.38])\n})\n\nsns.set_theme(style='whitegrid')\nfig = plt.figure(figsize=(16,10))\nfig.suptitle('Titanic EDA Report', fontsize=16, fontweight='bold')\n\nax1 = fig.add_subplot(2,3,1)\nsns.histplot(df['age'], kde=True, ax=ax1, color='#10b981')\nax1.set_title('Age Distribution')\n\nax2 = fig.add_subplot(2,3,2)\nsns.boxplot(data=df, x='pclass', y='fare', ax=ax2, palette='Set2')\nax2.set_title('Fare by Class')\n\nax3 = fig.add_subplot(2,3,3)\nsns.barplot(data=df, x='pclass', y='survived', ax=ax3, palette='Set1')\nax3.set_title('Survival Rate by Class')\n\nax4 = fig.add_subplot(2,3,4)\nsns.heatmap(df[['age','fare','survived']].corr(), annot=True, fmt='.2f', ax=ax4, cmap='RdYlGn')\nax4.set_title('Correlation')\n\nax5 = fig.add_subplot(2,3,5)\nax5.scatter(df['age'], df['fare'], c=df['survived'], cmap='RdYlGn', alpha=0.5)\nax5.set_xlabel('Age'); ax5.set_ylabel('Fare')\nax5.set_title('Age vs Fare (color=survived)')\n\nplt.tight_layout()\nplt.show()",
              "Add a 6th subplot showing a box plot of age split by survived."),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# ARTIFICIAL INTELLIGENCE
# ───────────────────────────────────────────────────────────────
AI_TOPICS = [
    {
        "title": "Neural Network Fundamentals",
        "icon": "bi-stars",
        "description": "Neurons, layers, activation functions, and how neural networks learn via backprop.",
        "order": 1,
        "lessons": [
            L("What is a Neural Network?", 1, "python",
              "<h3>Architecture</h3><ul>"
              "<li><strong>Input Layer</strong> — one neuron per feature</li>"
              "<li><strong>Hidden Layers</strong> — learn complex non-linear patterns</li>"
              "<li><strong>Output Layer</strong> — 1 neuron (regression) or softmax (classification)</li></ul>"
              "<h3>How Learning Works</h3><ol>"
              "<li>Forward pass — compute predictions</li>"
              "<li>Loss calculation — measure error</li>"
              "<li>Backpropagation — compute gradients</li>"
              "<li>Gradient descent — update weights</li></ol>"
              "<blockquote>Without activation functions, a neural network is just matrix multiplication — it can only learn linear relationships.</blockquote>",
              "import torch, torch.nn as nn, torch.optim as optim\n\nX = torch.FloatTensor([[0,0],[0,1],[1,0],[1,1]])\ny = torch.FloatTensor([[0],[1],[1],[0]])  # XOR labels\n\nclass XORNet(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(2, 8), nn.ReLU(),\n            nn.Linear(8, 4), nn.ReLU(),\n            nn.Linear(4, 1), nn.Sigmoid()\n        )\n    def forward(self, x):\n        return self.net(x)\n\nmodel = XORNet()\nopt   = optim.Adam(model.parameters(), lr=0.01)\nloss_fn = nn.BCELoss()\n\nfor epoch in range(1000):\n    opt.zero_grad()\n    loss = loss_fn(model(X), y)\n    loss.backward()\n    opt.step()\n    if (epoch+1) % 200 == 0:\n        print(f\"Epoch {epoch+1}: Loss={loss.item():.4f}\")\n\nwith torch.no_grad():\n    print(\"Predictions:\", model(X).round().T)\n    print(\"Truth:      \", y.T)",
              "Increase hidden neurons from 8 to 32. Does it converge faster?"),

            L("Activation Functions", 2, "python",
              "<h3>Why Activation Functions?</h3><p>They introduce non-linearity so networks can learn complex patterns beyond linear combinations.</p>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th>Function</th><th>Range</th><th>Used In</th></tr></thead><tbody>"
              "<tr><td>Sigmoid</td><td>(0,1)</td><td>Binary output layer</td></tr>"
              "<tr><td>Tanh</td><td>(-1,1)</td><td>Hidden layers</td></tr>"
              "<tr><td>ReLU</td><td>[0,∞)</td><td>Hidden layers (most common)</td></tr>"
              "<tr><td>Leaky ReLU</td><td>(-∞,∞)</td><td>Fixes dying ReLU</td></tr>"
              "<tr><td>Softmax</td><td>(0,1) sum=1</td><td>Multi-class output</td></tr></tbody></table>",
              "import torch, torch.nn.functional as F\nimport numpy as np, matplotlib.pyplot as plt\n\nx = torch.linspace(-5, 5, 200)\n\nactivations = {\n    'Sigmoid'   : torch.sigmoid(x),\n    'Tanh'      : torch.tanh(x),\n    'ReLU'      : F.relu(x),\n    'Leaky ReLU': F.leaky_relu(x, 0.1),\n    'ELU'       : F.elu(x),\n}\n\nfig, axes = plt.subplots(1, 5, figsize=(20,4))\nfor ax, (name, y) in zip(axes, activations.items()):\n    ax.plot(x.numpy(), y.detach().numpy(), color='#10b981', linewidth=2.5)\n    ax.axhline(0, color='gray', linewidth=0.5)\n    ax.axvline(0, color='gray', linewidth=0.5)\n    ax.set_title(name, fontweight='bold')\n    ax.set_ylim(-2, 4)\n    ax.grid(alpha=0.3)\nplt.suptitle('Activation Functions', fontsize=14, fontweight='bold')\nplt.tight_layout()\nplt.show()",
              "Add GELU (F.gelu) — it's used in BERT and GPT. How does it compare to ReLU?"),

            L("Training Loop & Loss Functions", 3, "python",
              "<h3>The Training Loop</h3><ol>"
              "<li><code>optimizer.zero_grad()</code> — clear gradients</li>"
              "<li><code>outputs = model(X_batch)</code> — forward pass</li>"
              "<li><code>loss = criterion(outputs, y_batch)</code> — compute loss</li>"
              "<li><code>loss.backward()</code> — backpropagation</li>"
              "<li><code>optimizer.step()</code> — update weights</li></ol>"
              "<h3>Loss Functions</h3><ul>"
              "<li><code>MSELoss</code> — regression</li>"
              "<li><code>BCELoss</code> — binary classification</li>"
              "<li><code>CrossEntropyLoss</code> — multi-class</li></ul>"
              "<h3>Optimizers</h3><ul>"
              "<li><code>SGD</code> — basic gradient descent</li>"
              "<li><code>Adam</code> — adaptive rates (most popular)</li>"
              "<li><code>AdamW</code> — Adam + weight decay</li></ul>",
              "import torch, torch.nn as nn, torch.optim as optim\nfrom torch.utils.data import TensorDataset, DataLoader\nimport numpy as np, matplotlib.pyplot as plt\n\nnp.random.seed(42)\nX_np = np.linspace(-5, 5, 500).reshape(-1,1)\ny_np = np.sin(X_np) + np.random.normal(0, 0.2, X_np.shape)\n\nX = torch.FloatTensor(X_np)\ny = torch.FloatTensor(y_np)\n\nloader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)\n\nmodel = nn.Sequential(nn.Linear(1,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU(),nn.Linear(64,1))\nopt = optim.Adam(model.parameters(), lr=0.001)\ncriterion = nn.MSELoss()\n\nlosses = []\nfor epoch in range(200):\n    epoch_loss = 0\n    for Xb, yb in loader:\n        opt.zero_grad()\n        loss = criterion(model(Xb), yb)\n        loss.backward()\n        opt.step()\n        epoch_loss += loss.item()\n    losses.append(epoch_loss / len(loader))\n    if (epoch+1) % 50 == 0:\n        print(f\"Epoch {epoch+1}: Loss={losses[-1]:.4f}\")\n\nplt.plot(losses)\nplt.title('Training Loss')\nplt.xlabel('Epoch'); plt.ylabel('MSE')\nplt.show()",
              "Add a validation split and plot both train and val loss to detect overfitting."),
        ]
    },

    {
        "title": "Natural Language Processing",
        "icon": "bi-chat-text-fill",
        "description": "Text preprocessing, TF-IDF, sentiment analysis, and transformer model basics.",
        "order": 2,
        "lessons": [
            L("Text Preprocessing", 1, "python",
              "<h3>NLP Pipeline</h3><ol>"
              "<li><strong>Lowercase</strong></li>"
              "<li><strong>Remove noise</strong> — HTML, URLs, punctuation</li>"
              "<li><strong>Tokenize</strong> — split into words</li>"
              "<li><strong>Remove stop words</strong> — 'the', 'is', 'a'</li>"
              "<li><strong>Stem/Lemmatize</strong> — 'running' -> 'run'</li>"
              "<li><strong>Vectorize</strong> — convert to numbers (TF-IDF, embeddings)</li></ol>"
              "<h3>Key Libraries</h3><ul>"
              "<li><code>nltk</code> — tokenization, stemming, stopwords</li>"
              "<li><code>spacy</code> — industrial NLP</li>"
              "<li><code>scikit-learn</code> — TF-IDF, CountVectorizer</li></ul>",
              "import re\nfrom collections import Counter\n\nreviews = [\n    \"The product is AMAZING! Best purchase ever. 100% recommended!\",\n    \"Terrible quality... broke after 2 days. Very disappointed :(\",\n    \"OK product, nothing special. Average quality for the price.\",\n    \"Absolutely love it! Works perfectly. Will buy again!!\",\n]\n\nSTOPWORDS = {'the','a','an','is','it','i','for','in','of','to','and','or'}\n\ndef preprocess(text):\n    text = text.lower()\n    text = re.sub(r'https?://\\S+', '', text)\n    text = re.sub(r'[^a-z0-9\\s]', '', text)\n    tokens = text.split()\n    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]\n    return tokens\n\nfor rev in reviews:\n    tokens = preprocess(rev)\n    print(f\"Tokens: {tokens}\\n\")\n\nall_tokens = [t for r in reviews for t in preprocess(r)]\ncounter = Counter(all_tokens)\nprint(\"Top 10:\", counter.most_common(10))",
              "Add lemmatization: 'amazing' and 'amazingly' should both map to 'amazing'."),

            L("TF-IDF & Text Classification", 2, "python",
              "<h3>TF-IDF</h3><p>Term Frequency-Inverse Document Frequency weights words by how often they appear in a document vs all documents. Common words ('the') get low weight; rare distinguishing words get high weight.</p>"
              "<code>TF-IDF(t,d) = TF(t,d) * log(N / DF(t))</code>"
              "<h3>Text Classification</h3><p>After vectorizing text with TF-IDF, use any ML classifier (Logistic Regression, Naive Bayes, SVM).</p>"
              "<h3>Naive Bayes</h3><p>Applies Bayes Theorem to classify text. Fast, works well with small datasets, interpretable.</p>",
              "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.naive_bayes import MultinomialNB\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.model_selection import cross_val_score\nimport numpy as np\n\n# Sample sentiment data\ntexts = [\n    \"amazing product love it highly recommend\",\n    \"terrible quality waste of money\",\n    \"great value excellent delivery\",\n    \"broken disappointed poor quality\",\n    \"fantastic best purchase ever\",\n    \"awful product never buying again\",\n    \"good service fast shipping\",\n    \"horrible experience worst ever\",\n]\nlabels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1=positive, 0=negative\n\npipeline = Pipeline([\n    ('tfidf', TfidfVectorizer(ngram_range=(1,2), min_df=1)),\n    ('clf',   MultinomialNB(alpha=0.5))\n])\n\ncv_scores = cross_val_score(pipeline, texts, labels, cv=3, scoring='f1')\nprint(f\"3-fold CV F1: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}\")\n\npipeline.fit(texts, labels)\nnew_reviews = [\"absolutely love this product\", \"completely broken waste\"]\npreds = pipeline.predict(new_reviews)\nfor review, pred in zip(new_reviews, preds):\n    print(f\"{'POSITIVE' if pred else 'NEGATIVE'}: {review}\")",
              "Change ngram_range to (1,3) — does F1 improve? Why or why not?"),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# POWER BI DEVELOPER
# ───────────────────────────────────────────────────────────────
PBI_TOPICS = [
    {
        "title": "DAX Fundamentals",
        "icon": "bi-bar-chart-fill",
        "description": "Write DAX measures, calculated columns, CALCULATE, and time intelligence functions.",
        "order": 1,
        "lessons": [
            L("Measures vs Calculated Columns", 1, "none",
              "<h3>What is DAX?</h3><p><strong>DAX</strong> is the formula language of Power BI, Power Pivot, and Analysis Services. It creates measures and calculated columns.</p>"
              "<table class='table table-bordered table-sm'><thead class='table-dark'><tr><th></th><th>Measure</th><th>Calc Column</th></tr></thead><tbody>"
              "<tr><td><strong>When computed</strong></td><td>Query time (live)</td><td>Refresh time (static)</td></tr>"
              "<tr><td><strong>Filter context</strong></td><td>Yes — responds to slicers</td><td>No — row context only</td></tr>"
              "<tr><td><strong>Memory</strong></td><td>Not stored</td><td>Stored in model</td></tr>"
              "<tr><td><strong>Best for</strong></td><td>KPIs, aggregations</td><td>Categories, flags</td></tr></tbody></table>"
              "<blockquote>Always prefer measures for aggregations — they are more efficient and respond to report context.</blockquote>",
              "// Calculated Column — row-level, stored in table\nProfit Margin % =\nDIVIDE(\n    Sales[Profit],\n    Sales[Revenue],\n    0   -- return 0 on divide-by-zero\n)\n\nSales Category =\nSWITCH(\n    TRUE(),\n    Sales[Revenue] >= 50000, \"High\",\n    Sales[Revenue] >= 20000, \"Medium\",\n    \"Low\"\n)\n\n// Measures — live, respond to filters\nTotal Revenue = SUM(Sales[Revenue])\n\nAvg Order Value =\nAVERAGEX(Sales, Sales[Quantity] * Sales[Unit Price])\n\nOrder Count = COUNTROWS(Sales)\n\nRevenue per Customer =\nDIVIDE(\n    [Total Revenue],\n    DISTINCTCOUNT(Sales[CustomerID]),\n    0\n)",
              "Write a 'Is Weekend' calculated column: 1 if date falls on Saturday or Sunday, else 0."),

            L("CALCULATE & Filter Context", 2, "none",
              "<h3>CALCULATE — The Most Important DAX Function</h3><p>Evaluates an expression in a <em>modified filter context</em>. Foundation of almost every complex measure.</p>"
              "<code>CALCULATE(expression, filter1, filter2, ...)</code>"
              "<h3>Key Modifiers</h3><ul>"
              "<li><code>ALL(table)</code> — removes all filters</li>"
              "<li><code>ALLEXCEPT(table, col)</code> — removes all except one column</li>"
              "<li><code>FILTER(table, condition)</code> — complex condition</li></ul>",
              "// North region revenue (ignores slicer)\nNorth Revenue =\nCALCULATE([Total Revenue], Sales[Region] = \"North\")\n\n// % of grand total — ALL removes all filters\n% of Grand Total =\nDIVIDE(\n    [Total Revenue],\n    CALCULATE([Total Revenue], ALL(Sales))\n)\n\n// % within region — ALLEXCEPT keeps region filter\n% Within Region =\nDIVIDE(\n    [Total Revenue],\n    CALCULATE([Total Revenue], ALLEXCEPT(Sales, Sales[Region]))\n)\n\n// Previous Year Revenue\nPrev Year Revenue =\nCALCULATE(\n    [Total Revenue],\n    SAMEPERIODLASTYEAR('Date'[Date])\n)\n\nYoY Growth % =\nDIVIDE(\n    [Total Revenue] - [Prev Year Revenue],\n    [Prev Year Revenue],\n    BLANK()\n)",
              "Write 'Revenue excluding Discounted Orders' using FILTER(Sales, Sales[Discount] = 0)."),

            L("Time Intelligence Functions", 3, "none",
              "<h3>Requirements</h3><ul>"
              "<li>A marked Date table with continuous dates and no gaps</li>"
              "<li>Relationship to your fact table</li></ul>"
              "<code>Dates = CALENDAR(MIN(Sales[Date]), MAX(Sales[Date]))</code>"
              "<h3>Key Functions</h3><ul>"
              "<li><code>TOTALYTD([m], 'Date'[Date])</code> — Year-to-date</li>"
              "<li><code>TOTALQTD / TOTALMTD</code> — Quarter/Month-to-date</li>"
              "<li><code>SAMEPERIODLASTYEAR</code> — prior year same period</li>"
              "<li><code>DATEADD('Date'[Date], -1, YEAR)</code> — shift dates</li></ul>",
              "// Year-to-Date\nRevenue YTD = TOTALYTD([Total Revenue], 'Date'[Date])\n\n// Month-to-Date\nRevenue MTD = TOTALMTD([Total Revenue], 'Date'[Date])\n\n// Same Period Last Year\nRevenue SPLY =\nCALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))\n\n// YoY Growth\nYoY % =\nDIVIDE([Total Revenue] - [Revenue SPLY], [Revenue SPLY], BLANK())\n\n// Rolling 3-Month Average\nRolling 3M Avg =\nCALCULATE(\n    AVERAGEX(\n        DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -3, MONTH),\n        [Total Revenue]\n    )\n)\n\n// Days remaining in month\nDays Left = EOMONTH(TODAY(), 0) - TODAY()",
              "Write a 'Revenue 3 Months Ago' measure using DATEADD('Date'[Date], -3, MONTH)."),

            L("DAX Variables & Best Practices", 4, "none",
              "<h3>Variables (VAR...RETURN)</h3><p>Make formulas readable, debuggable, and efficient by avoiding repeated sub-expressions.</p>"
              "<code>VAR myVar = expression RETURN result</code>"
              "<h3>Best Practices</h3><ol>"
              "<li>Always use VAR for complex measures</li>"
              "<li>Use DIVIDE() instead of / (handles zero division)</li>"
              "<li>Avoid FILTER() on large tables — use column filters in CALCULATE</li>"
              "<li>Use SELECTEDVALUE() when expecting a single slicer value</li>"
              "<li>Format with indentation and comments</li></ol>",
              "// Without variables — repeated, hard to debug\nGrowth_Bad =\nDIVIDE(\n    SUM(Sales[Rev]) - CALCULATE(SUM(Sales[Rev]), SAMEPERIODLASTYEAR('Date'[Date])),\n    CALCULATE(SUM(Sales[Rev]), SAMEPERIODLASTYEAR('Date'[Date]))\n)\n\n// With variables — clean and readable\nGrowth_Good =\nVAR CurrentRev = [Total Revenue]\nVAR PriorRev   =\n    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))\nVAR Growth     = CurrentRev - PriorRev\nRETURN\n    IF(\n        ISBLANK(PriorRev),\n        BLANK(),\n        DIVIDE(Growth, PriorRev)\n    )\n\n// Dynamic chart title\nChart Title =\nVAR Rgn  = SELECTEDVALUE(Sales[Region],  \"All Regions\")\nVAR Yr   = SELECTEDVALUE('Date'[Year],   \"All Years\")\nRETURN \"Revenue - \" & Rgn & \" | \" & Yr",
              "Rewrite 'Profit Margin %' using VAR for Profit and Revenue. Add ISBLANK() error handling."),
        ]
    },

    {
        "title": "Data Modeling",
        "icon": "bi-diagram-2-fill",
        "description": "Star schema design, relationships, cardinality, and building efficient Power BI models.",
        "order": 2,
        "lessons": [
            L("Star Schema Design", 1, "none",
              "<h3>Why Data Modeling Matters</h3><p>A well-designed model is the foundation of every good Power BI report. Bad models = slow performance + incorrect DAX calculations.</p>"
              "<h3>Star Schema</h3><p>One central <strong>Fact Table</strong> surrounded by <strong>Dimension Tables</strong>.</p><ul>"
              "<li><strong>Fact Table</strong> — measurable events (sales, clicks). Contains foreign keys + numeric measures.</li>"
              "<li><strong>Dimension Tables</strong> — descriptive context (Customer, Product, Date, Region)</li></ul>"
              "<h3>Principles</h3><ol>"
              "<li>One row per transaction in the fact table</li>"
              "<li>Surrogate integer keys for relationships</li>"
              "<li>All dimensions must have a single primary key</li>"
              "<li>Always have a Date dimension</li>"
              "<li>Avoid Many-to-Many relationships unless necessary</li></ol>",
              "// Create Date dimension in DAX\nDate =\nGENERATESERIES(\n    DATE(2020, 1, 1),\n    DATE(2026, 12, 31),\n    1  -- 1 day step\n)\n\n// Add columns to Date table\nYear        = YEAR('Date'[Date])\nMonth       = MONTH('Date'[Date])\nMonthName   = FORMAT('Date'[Date], \"MMMM\")\nQuarter     = \"Q\" & QUARTER('Date'[Date])\nWeekday     = FORMAT('Date'[Date], \"dddd\")\nIsWeekend   = IF(WEEKDAY('Date'[Date], 2) >= 6, TRUE, FALSE)\nFiscalYear  = IF(MONTH('Date'[Date]) >= 4, YEAR('Date'[Date]), YEAR('Date'[Date]) - 1)\n\n// Model relationships (set in Power BI UI)\n// Sales[DateKey]       -> Date[Date]      (Many-to-One)\n// Sales[CustomerID]    -> Customers[ID]   (Many-to-One)\n// Sales[ProductID]     -> Products[ID]    (Many-to-One)\n// Sales[RegionID]      -> Regions[ID]     (Many-to-One)",
              "Add a 'Fiscal Quarter' column where Q1 = April-June. Verify April is FQ1."),

            L("Power Query (M Language)", 2, "none",
              "<h3>Power Query</h3><p>Power Query runs <em>before</em> your data model. It extracts, transforms, and loads data from any source. Each step is recorded and reproducible.</p>"
              "<h3>Common Transformations</h3><ul>"
              "<li>Remove empty rows and columns</li>"
              "<li>Promote headers</li>"
              "<li>Change data types</li>"
              "<li>Split/merge columns</li>"
              "<li>Pivot/unpivot</li>"
              "<li>Merge/append queries</li>"
              "<li>Add custom columns (M expressions)</li></ul>"
              "<h3>M Language</h3><p>The formula language behind Power Query. Each query is a <code>let ... in</code> expression.</p>",
              "// M Language — Power Query formula\nlet\n    // 1. Load source\n    Source = Excel.Workbook(File.Contents(\"C:\\Data\\Sales.xlsx\"), null, true),\n    Sheet  = Source{[Item=\"Sheet1\",Kind=\"Sheet\"]}[Data],\n\n    // 2. Promote headers from first row\n    #\"Promoted Headers\" = Table.PromoteHeaders(Sheet, [PromoteAllScalars=true]),\n\n    // 3. Change types\n    #\"Changed Types\" = Table.TransformColumnTypes(\n        #\"Promoted Headers\",\n        {{\"Date\", type date}, {\"Revenue\", type number}, {\"Region\", type text}}\n    ),\n\n    // 4. Filter out blank rows\n    #\"Filtered Rows\" = Table.SelectRows(\n        #\"Changed Types\",\n        each [Revenue] <> null and [Revenue] > 0\n    ),\n\n    // 5. Add custom column — Profit Margin\n    #\"Added Column\" = Table.AddColumn(\n        #\"Filtered Rows\",\n        \"Profit Margin %\",\n        each if [Revenue] > 0 then [Profit] / [Revenue] * 100 else 0,\n        type number\n    )\nin\n    #\"Added Column\"",
              "Add a step to unpivot 'Jan', 'Feb', 'Mar' columns into 'Month' and 'Revenue' columns."),
        ]
    },
]

# ───────────────────────────────────────────────────────────────
# ASSEMBLE ALL DOMAINS
# ───────────────────────────────────────────────────────────────
SEED_DATA = [
    {"domain": "Data Analytics",          "topics": DA_TOPICS},
    {"domain": "Web Development",         "topics": WD_TOPICS},
    {"domain": "Machine Learning",        "topics": ML_TOPICS},
    {"domain": "Data Science",            "topics": DS_TOPICS},
    {"domain": "Artificial Intelligence", "topics": AI_TOPICS},
    {"domain": "Power BI developer",      "topics": PBI_TOPICS},
]


class Command(BaseCommand):
    help = "Seeds expanded W3Schools-style learning content for all 6 internship domains."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true",
            help="Delete all existing content before seeding.")

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing content..."))
            LearningLesson.objects.all().delete()
            LearningTopic.objects.all().delete()
            self.stdout.write("Cleared.")

        tc = tu = lc = lu = 0

        for domain_data in SEED_DATA:
            domain = domain_data["domain"]
            for td in domain_data["topics"]:
                topic, created = LearningTopic.objects.update_or_create(
                    domain=domain,
                    title=td["title"],
                    defaults={
                        "icon":        td.get("icon",        "bi-book-fill"),
                        "description": td.get("description", ""),
                        "order":       td.get("order",       0),
                        "is_active":   True,
                    },
                )
                if created:
                    tc += 1
                else:
                    tu += 1

                for ld in td["lessons"]:
                    _lesson, lesson_created = LearningLesson.objects.update_or_create(
                        topic=topic,
                        title=ld["title"],
                        defaults={
                            "content":      ld.get("content",      "").strip(),
                            "code_example": ld.get("code_example", "").strip(),
                            "code_language":ld.get("code_language","python"),
                            "try_it_note":  ld.get("try_it_note",  ""),
                            "order":        ld.get("order",        0),
                            "is_active":    True,
                        },
                    )
                    if lesson_created:
                        lc += 1
                    else:
                        lu += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone!\n"
                f"   Topics  : {tc} created / {tu} updated\n"
                f"   Lessons : {lc} created / {lu} updated\n\n"
                f"Run with --clear to reset and re-seed."
            )
        )

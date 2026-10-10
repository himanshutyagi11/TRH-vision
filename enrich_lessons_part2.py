"""
enrich_lessons_part2.py
Run: python enrich_lessons_part2.py
Updates remaining lessons not covered in enrich_lessons.py
"""
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TRH.settings')
django.setup()

from vision.models import LearningLesson


def h2(t): return f'<h2>{t}</h2>'
def h3(t): return f'<h3>{t}</h3>'
def p(t):  return f'<p>{t}</p>'
def c(t):  return f'<code>{t}</code>'
def b(t):  return f'<strong>{t}</strong>'
def bq(t): return f'<blockquote>{t}</blockquote>'
def tip(t): return f'<div class="tip"><strong>Tip:</strong> {t}</div>'
def note(t): return f'<div class="note"><strong>Note:</strong> {t}</div>'
def warn(t): return f'<div class="warning"><strong>Warning:</strong> {t}</div>'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

def tbl(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    bd = ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{bd}</tbody></table>'


RICH = {}

# ─── AI: What is a Neural Network? ─────────────────────────────────────────
RICH['What is a Neural Network?'] = dict(
    content=(
        h2("What is a Neural Network?")
        + p("A <b>Neural Network</b> is a computational model loosely inspired by the human brain. It consists of layers of interconnected <b>neurons</b>. Each neuron receives inputs, multiplies them by learned weights, adds a bias, applies an activation function, and passes the output to the next layer.")
        + p("Neural networks power modern AI: image recognition, voice assistants, recommendation engines, ChatGPT, and autonomous vehicles.")
        + h2("Architecture: Layers")
        + tbl(
            ["Layer", "Role", "Size Rule"],
            [
                [b("Input Layer"), "Receives raw features. One neuron per input feature.", "= number of features"],
                [b("Hidden Layers"), "Learn abstract patterns and representations.", "You choose (hyperparameter)"],
                [b("Output Layer"), "Produces final prediction.", "1 for regression; N for N-class"],
            ]
        )
        + h2("How a Single Neuron Computes")
        + ol(
            "Weighted sum: " + c("z = w1*x1 + w2*x2 + ... + wn*xn + b"),
            "Apply activation: " + c("a = activation(z)"),
            "Pass output " + c("a") + " to the next layer",
        )
        + h2("The Training Process: Backpropagation")
        + ol(
            b("Forward Pass") + " - compute predictions layer by layer",
            b("Compute Loss") + " - measure prediction error (MSE, Cross-Entropy, etc.)",
            b("Backward Pass") + " - compute gradients using chain rule",
            b("Weight Update") + " - subtract gradient * learning_rate from each weight",
            b("Repeat") + " for many epochs until loss converges",
        )
        + h2("Key Terminology")
        + tbl(
            ["Term", "Definition"],
            [
                [b("Epoch"), "One complete pass through the entire training dataset"],
                [b("Batch Size"), "Number of samples processed before one weight update"],
                [b("Learning Rate"), "Step size for gradient descent (typical: 0.001)"],
                [b("Loss Function"), "Measures prediction error - MSE for regression, Cross-Entropy for classification"],
                [b("Optimizer"), "Algorithm to update weights - SGD, Adam, RMSprop"],
                [b("Overfitting"), "Model memorizes training data, fails on new data"],
                [b("Dropout"), "Randomly disable neurons during training to prevent overfitting"],
            ]
        )
        + tip("Start with a small network (1-2 hidden layers, 32-128 neurons). Only increase complexity if the model is underfitting.")
        + warn("Without activation functions, stacking layers is mathematically equivalent to ONE linear transformation. The network cannot learn non-linear patterns.")
        + bq('"A neural network is a universal function approximator. Given enough neurons and data, it can approximate any continuous function." - Universal Approximation Theorem')
    ),
    code_example=(
        'import numpy as np\n'
        '\n'
        '# ── Implement a simple neural network from scratch ──\n'
        '\n'
        'def sigmoid(z):         return 1 / (1 + np.exp(-z))\n'
        'def sigmoid_deriv(z):   return sigmoid(z) * (1 - sigmoid(z))\n'
        'def relu(z):            return np.maximum(0, z)\n'
        '\n'
        'class SimpleNeuralNet:\n'
        '    def __init__(self, layers):\n'
        '        """layers = [input_size, hidden1, hidden2, output_size]"""\n'
        '        self.weights = []\n'
        '        self.biases  = []\n'
        '        for i in range(len(layers)-1):\n'
        '            # Xavier initialization for better training\n'
        '            w = np.random.randn(layers[i], layers[i+1]) * np.sqrt(2/layers[i])\n'
        '            b = np.zeros((1, layers[i+1]))\n'
        '            self.weights.append(w)\n'
        '            self.biases.append(b)\n'
        '\n'
        '    def forward(self, X):\n'
        '        """Forward pass through all layers."""\n'
        '        self.activations = [X]\n'
        '        for i, (w, b) in enumerate(zip(self.weights, self.biases)):\n'
        '            z = self.activations[-1] @ w + b\n'
        '            # Use ReLU for hidden, sigmoid for output\n'
        '            a = relu(z) if i < len(self.weights)-1 else sigmoid(z)\n'
        '            self.activations.append(a)\n'
        '        return self.activations[-1]\n'
        '\n'
        '# ── Build and run a 3-layer network ──\n'
        'net = SimpleNeuralNet([4, 8, 4, 1])  # 4 inputs, 2 hidden layers, 1 output\n'
        '\n'
        '# Sample input: 3 students, each with 4 features\n'
        'X = np.array([\n'
        '    [0.8, 0.6, 1.0, 0.9],  # Student 1\n'
        '    [0.3, 0.4, 0.2, 0.5],  # Student 2\n'
        '    [0.7, 0.8, 0.6, 0.7],  # Student 3\n'
        '])\n'
        '\n'
        'output = net.forward(X)\n'
        '\n'
        'print("Network Architecture: [4 inputs] -> [8] -> [4] -> [1 output]")\n'
        'print(f"Input shape:  {X.shape}")\n'
        'print(f"Output shape: {output.shape}")\n'
        'print(f"Predictions (pass probability):")\n'
        'for i, prob in enumerate(output.flatten()):\n'
        '    print(f"  Student {i+1}: {prob:.4f} -> {\"PASS\" if prob > 0.5 else \"FAIL\"}")\n'
        '\n'
        '# Count total parameters\n'
        'total_params = sum(w.size + b.size for w, b in zip(net.weights, net.biases))\n'
        'print(f"\\nTotal learnable parameters: {total_params}")'
    ),
    try_it_note="Change the architecture to [4, 16, 8, 1]. Does the number of parameters increase? Run it and see the predictions change."
)

# ─── AI: Activation Functions ───────────────────────────────────────────────
RICH['Activation Functions'] = dict(
    content=(
        h2("Why Do We Need Activation Functions?")
        + p("Without activation functions, a neural network - no matter how many layers deep - computes only a <b>linear transformation</b>. Stacking linear layers is mathematically equivalent to a single linear layer.")
        + p("Activation functions introduce <b>non-linearity</b>, enabling neural networks to learn complex decision boundaries and approximate any function.")
        + h2("The Most Important Activation Functions")
        + tbl(
            ["Function", "Formula", "Output Range", "Best Used In"],
            [
                [b("ReLU"), "max(0, x)", "0 to infinity", "Hidden layers - fast, sparse, default choice"],
                [b("Leaky ReLU"), "x if x > 0 else 0.01x", "(-inf, inf)", "When dying ReLU is a problem"],
                [b("Sigmoid"), "1 / (1 + e^-x)", "0 to 1", "Binary classification output layer"],
                [b("Softmax"), "e^xi / sum(e^xj)", "0 to 1 (sum = 1)", "Multi-class output layer"],
                [b("Tanh"), "tanh(x)", "-1 to 1", "RNNs, hidden layers needing negative outputs"],
                [b("GELU"), "x * Phi(x)", "Smooth", "Transformers (BERT, GPT)"],
            ]
        )
        + h2("ReLU - The Default Choice")
        + p("ReLU (Rectified Linear Unit) is the most popular activation for hidden layers. Computationally simple, solves vanishing gradient better than sigmoid/tanh, and creates sparse activations.")
        + warn("The <b>Dying ReLU Problem</b>: If a neuron always outputs 0, its gradient is always 0 - it never updates again. Use Leaky ReLU or ELU if you see many dead neurons (check activation histograms).")
        + h2("Sigmoid vs Softmax")
        + tbl(
            ["Property", "Sigmoid", "Softmax"],
            [
                ["Output", "Independent probabilities per class", "Probabilities that sum to 1"],
                ["Use Case", "Binary classification (yes/no)", "Multi-class classification"],
                ["Layer", "Output layer only", "Output layer only"],
                ["Formula", "1 / (1 + e^-z)", "e^zi / sum(e^zj)"],
            ]
        )
        + tip("Use ReLU for hidden layers. Only use sigmoid/softmax in the output layer. Never use sigmoid in hidden layers of deep networks - it causes vanishing gradients.")
        + h2("The Vanishing Gradient Problem")
        + p("Sigmoid and tanh output values in a small range (0-1 or -1 to 1). When multiplied across many layers during backpropagation, gradients shrink exponentially. Early layers learn almost nothing.")
        + p("ReLU solves this: its gradient is either 0 or 1 (for x > 0), so it doesn't vanish. Modern networks use ReLU or its variants for all hidden layers.")
        + note("Modern architectures (ResNet, Transformers) also use techniques like batch normalization, residual connections, and careful weight initialization to fight vanishing gradients in very deep networks.")
    ),
    code_example=(
        'import numpy as np\n'
        '\n'
        '# ── Activation functions from scratch ──\n'
        '\n'
        'def relu(x):           return np.maximum(0, x)\n'
        'def leaky_relu(x):     return np.where(x > 0, x, 0.01 * x)\n'
        'def sigmoid(x):        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))\n'
        'def tanh_fn(x):        return np.tanh(x)\n'
        '\n'
        'def softmax(logits):\n'
        '    """Numerically stable softmax."""\n'
        '    e = np.exp(logits - np.max(logits))\n'
        '    return e / e.sum()\n'
        '\n'
        '# ── Compare at sample points ──\n'
        'test_points = [-3.0, -1.0, 0.0, 1.0, 3.0]\n'
        '\n'
        'print("x       ReLU    Leaky   Sigmoid  Tanh")\n'
        'print("-" * 50)\n'
        'for x in test_points:\n'
        '    print(f"{x:7.1f} {relu(x):7.4f} {leaky_relu(x):7.4f}"\n'
        '          f" {sigmoid(x):8.4f} {tanh_fn(x):7.4f}")\n'
        '\n'
        '# ── Softmax: multi-class probabilities ──\n'
        'logits = np.array([2.5, 1.0, 0.3, -0.8, 4.1])\n'
        'classes = ["Cat", "Dog", "Bird", "Fish", "Tiger"]\n'
        'probs = softmax(logits)\n'
        '\n'
        'print("\\n=== Softmax Output ===")\n'
        'for cls, prob in sorted(zip(classes, probs), key=lambda x: x[1], reverse=True):\n'
        '    bar = "#" * int(prob * 40)\n'
        '    print(f"{cls:8}: {prob:.4f}  {bar}")\n'
        'print(f"Sum = {probs.sum():.6f}")  # always 1.0\n'
        '\n'
        '# ── Dying ReLU demo ──\n'
        'print("\\n=== Dying ReLU Demo ===")\n'
        'dead_weights = np.array([-5.0, -3.0, -0.5, 0.1, 2.0])\n'
        'outputs = relu(dead_weights)\n'
        'gradients = (dead_weights > 0).astype(float)\n'
        'print("Weights:   ", dead_weights)\n'
        'print("ReLU out:  ", outputs)\n'
        'print("Gradient:  ", gradients)\n'
        'dead_count = (gradients == 0).sum()\n'
        'print(f"Dead neurons: {dead_count}/5 ({dead_count/5:.0%})")'
    ),
    try_it_note="Implement Leaky ReLU with alpha=0.2 instead of 0.01. Compare the gradients at x=-3, -1. How does a larger alpha help fight dying neurons?"
)

# ─── DATA ANALYTICS: Filtering & Selection ──────────────────────────────────
RICH['Filtering & Selection'] = dict(
    content=(
        h2("Filtering Rows in Pandas")
        + p("Filtering is the process of selecting only the rows that meet certain conditions - just like SQL WHERE clause. Pandas uses <b>boolean indexing</b>: you create a True/False Series based on a condition, then use it to select matching rows.")
        + h2("Boolean Indexing - The Core Concept")
        + p("A condition like " + c("df['score'] > 75") + " returns a Series of True/False values. When you pass this to " + c("df[...]") + ", Pandas returns only the rows where the value is True.")
        + bq(c("mask = df['score'] > 75  # Series of True/False") + "<br>" + c("df_filtered = df[mask]   # keep only True rows"))
        + h2("Combining Multiple Conditions")
        + tbl(
            ["Operator", "Meaning", "Example"],
            [
                [c("&"), "AND - both conditions must be True", c("df[(df['score'] > 60) & (df['city'] == 'Mumbai')]")],
                [c("|"), "OR - at least one condition must be True", c("df[(df['city'] == 'Delhi') | (df['city'] == 'Pune')]")],
                [c("~"), "NOT - invert condition", c("df[~df['is_paid']]  # unpaid students")],
            ]
        )
        + warn("Always wrap each condition in parentheses when combining with & or |. Without parentheses, operator precedence causes bugs: " + c("df[df.a > 1 & df.b < 5]") + " will raise an error!")
        + h2("The .loc and .iloc Accessors")
        + tbl(
            ["Accessor", "Selects by", "Syntax", "Example"],
            [
                [c(".loc"), "Label-based (index names, column names)", c("df.loc[row_label, col_label]"), c("df.loc[0:5, 'name':'score']")],
                [c(".iloc"), "Integer position (0-based)", c("df.iloc[row_int, col_int]"), c("df.iloc[0:5, 0:3]")],
            ]
        )
        + h2("Useful Filtering Methods")
        + tbl(
            ["Method", "What it Does", "Example"],
            [
                [c(".isin([...])"), "Match any value in a list", c("df[df['city'].isin(['Mumbai','Pune','Delhi'])]")],
                [c(".between(a, b)"), "Value in range [a, b]", c("df[df['score'].between(70, 90)]")],
                [c(".str.contains('pat')"), "String contains pattern (regex)", c("df[df['name'].str.contains('Kumar')]")],
                [c(".str.startswith('A')"), "String starts with", c("df[df['name'].str.startswith('A')]")],
                [c(".notna()"), "Non-null values", c("df[df['phone'].notna()]")],
                [c(".query('expr')"), "Filter using string expression", c("df.query('score > 75 and city == \"Mumbai\"')")],
            ]
        )
        + h2("Selecting Specific Columns")
        + ul(
            b("Single column: ") + c("df['score']") + " returns a Series",
            b("Multiple columns: ") + c("df[['name', 'score', 'city']]") + " returns a DataFrame",
            b("By position: ") + c("df.iloc[:, 0:3]") + " first 3 columns",
            b("By type: ") + c("df.select_dtypes(include='number')") + " only numeric columns",
            b("Exclude columns: ") + c("df.drop(columns=['id', 'timestamp'])"),
        )
        + tip("Use " + c(".query()") + " for readable multi-condition filters: " + c("df.query('score > 75 and is_paid == True and city != \"Delhi\"')") + " is much cleaner than chained boolean operators.")
    ),
    code_example=(
        'import pandas as pd\n'
        'import numpy as np\n'
        '\n'
        '# ── Sample student dataset ──\n'
        'data = {\n'
        '    "name":   ["Priya","Raj","Neha","Arjun","Meera","Dev","Sanya","Kabir","Nita","Rohan"],\n'
        '    "score":  [92, 78, None, 91, 63, 85, 55, 74, 88, 42],\n'
        '    "city":   ["Mumbai","Delhi","Mumbai","Chennai","Delhi","Pune","Mumbai","Delhi","Pune","Mumbai"],\n'
        '    "domain": ["DA","ML","DA","WebDev","ML","DA","WebDev","ML","DA","WebDev"],\n'
        '    "is_paid":[True, True, False, True, False, True, False, True, True, False],\n'
        '}\n'
        'df = pd.DataFrame(data)\n'
        '\n'
        '# ── Basic boolean filter ──\n'
        'high_scorers = df[df["score"] > 85]\n'
        'print("High scorers (score > 85):")\n'
        'print(high_scorers[["name","score","domain"]].to_string(index=False))\n'
        '\n'
        '# ── Combined conditions ──\n'
        'paid_mumbai = df[(df["city"] == "Mumbai") & (df["is_paid"] == True)]\n'
        'print("\\nPaid students in Mumbai:")\n'
        'print(paid_mumbai[["name","score"]].to_string(index=False))\n'
        '\n'
        '# ── Invert with ~ ──\n'
        'unpaid = df[~df["is_paid"]]\n'
        'print(f"\\nUnpaid students: {unpaid[\'name\'].tolist()}")\n'
        '\n'
        '# ── .isin() ──\n'
        'metro = df[df["city"].isin(["Mumbai", "Delhi"])]\n'
        'print(f"\\nMetro city students: {len(metro)}")\n'
        '\n'
        '# ── .between() ──\n'
        'mid_range = df[df["score"].between(70, 85)]\n'
        'print("\\nMid-range scores (70-85):")\n'
        'print(mid_range[["name","score"]].to_string(index=False))\n'
        '\n'
        '# ── .query() method ──\n'
        'result = df.query("score > 75 and is_paid == True")\n'
        'print(f"\\nPaid + score>75: {result[\'name\'].tolist()}")\n'
        '\n'
        '# ── Handle missing before filtering ──\n'
        'print("\\nRows with missing scores:")\n'
        'print(df[df["score"].isna()][["name","city"]].to_string(index=False))\n'
        'df_clean = df.dropna(subset=["score"])\n'
        '\n'
        '# ── .loc for label-based selection ──\n'
        'subset = df_clean.loc[df_clean["domain"] == "DA", ["name","score","city"]]\n'
        'print("\\nData Analytics students (loc):")\n'
        'print(subset.to_string(index=False))'
    ),
    try_it_note="Filter students whose names start with a vowel (A, E, I, O, U) using str.startswith(). How many are there? HINT: Use | to combine multiple startswith conditions."
)

# ─── DATA ANALYTICS: GroupBy & Aggregation ──────────────────────────────────
RICH['GroupBy & Aggregation'] = dict(
    content=(
        h2("GroupBy: Split - Apply - Combine")
        + p("Pandas GroupBy follows a <b>Split - Apply - Combine</b> strategy:")
        + ol(
            b("Split") + " - divide the DataFrame into groups based on one or more columns",
            b("Apply") + " - apply an aggregation function to each group",
            b("Combine") + " - combine the results into a new DataFrame",
        )
        + p("This is equivalent to SQL's GROUP BY + aggregate functions, and Excel pivot tables.")
        + h2("Basic GroupBy Syntax")
        + bq(c("df.groupby('column')['value_col'].agg_function()"))
        + h2("Aggregation Functions")
        + tbl(
            ["Function", "What it Computes", "Method"],
            [
                ["Sum", "Total of values", c(".sum()")],
                ["Mean", "Average of values", c(".mean()")],
                ["Count", "Count of non-null values", c(".count()")],
                ["Count unique", "Number of distinct values", c(".nunique()")],
                ["Min / Max", "Smallest / largest value", c(".min()") + " / " + c(".max()")],
                ["Std deviation", "Spread of values", c(".std()")],
                ["Median", "Middle value", c(".median()")],
                ["First / Last", "First or last value in group", c(".first()") + " / " + c(".last()")],
            ]
        )
        + h2("Multiple Aggregations with .agg()")
        + p("You can apply multiple functions at once, or different functions to different columns:")
        + bq(c("df.groupby('domain').agg(") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;avg_score=('score', 'mean'),") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;total=('name', 'count'),") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;max_score=('score', 'max')") + "<br>"
             + c(")"))
        + h2("Grouping by Multiple Columns")
        + p("Group by two or more columns to create hierarchical groups:")
        + bq(c("df.groupby(['city', 'domain'])['score'].mean()"))
        + h2("Transform vs Agg vs Filter")
        + tbl(
            ["Operation", "Returns", "Use Case"],
            [
                [c(".agg()"), "One row per group (summary)", "Domain averages, counts"],
                [c(".transform(fn)"), "Same shape as original DataFrame", "Add group mean as new column"],
                [c(".filter(fn)"), "Subset of original rows", "Keep only groups with count > 5"],
                [c(".apply(fn)"), "Flexible - any custom function", "Complex group operations"],
            ]
        )
        + tip("Use " + c(".reset_index()") + " after groupby to convert the result from MultiIndex to a flat DataFrame - much easier to work with downstream.")
        + h2("Pivot Tables")
        + p("Pivot tables reshape grouped data into a 2D matrix - rows, columns, and values:")
        + bq(c("pd.pivot_table(df, values='score', index='city', columns='domain', aggfunc='mean')"))
    ),
    code_example=(
        'import pandas as pd\n'
        'import numpy as np\n'
        '\n'
        'df = pd.DataFrame({\n'
        '    "name":   ["Priya","Raj","Neha","Arjun","Meera","Dev","Sanya","Kabir","Nita","Rohan"],\n'
        '    "score":  [92, 78, 65, 91, 63, 85, 55, 74, 88, 72],\n'
        '    "city":   ["Mumbai","Delhi","Mumbai","Chennai","Delhi","Pune","Mumbai","Delhi","Pune","Mumbai"],\n'
        '    "domain": ["DA","ML","DA","WebDev","ML","DA","WebDev","ML","DA","WebDev"],\n'
        '    "salary": [55000,62000,48000,70000,58000,60000,45000,63000,52000,49000],\n'
        '})\n'
        '\n'
        '# ── Basic groupby ──\n'
        'domain_stats = df.groupby("domain")["score"].agg(["mean","min","max","count"])\n'
        'domain_stats.columns = ["avg_score","min_score","max_score","students"]\n'
        'domain_stats = domain_stats.round(1).reset_index()\n'
        'print("=== Domain Statistics ===")\n'
        'print(domain_stats.to_string(index=False))\n'
        '\n'
        '# ── Multiple aggregations with named columns ──\n'
        'summary = df.groupby("domain").agg(\n'
        '    students  = ("name", "count"),\n'
        '    avg_score = ("score", "mean"),\n'
        '    avg_salary= ("salary", "mean"),\n'
        '    top_score = ("score", "max"),\n'
        ').round(0).reset_index()\n'
        'print("\\n=== Multi-Column Aggregation ===")\n'
        'print(summary.to_string(index=False))\n'
        '\n'
        '# ── Group by 2 columns ──\n'
        'city_domain = df.groupby(["city","domain"])["score"].mean().round(1).reset_index()\n'
        'print("\\n=== City x Domain Average Score ===")\n'
        'print(city_domain.to_string(index=False))\n'
        '\n'
        '# ── Transform: add group mean as new column ──\n'
        'df["domain_avg"] = df.groupby("domain")["score"].transform("mean").round(1)\n'
        'df["above_avg"]  = df["score"] > df["domain_avg"]\n'
        'print("\\n=== Students Above Their Domain Average ===")\n'
        'print(df[df["above_avg"]][["name","domain","score","domain_avg"]].to_string(index=False))\n'
        '\n'
        '# ── Filter: keep only domains with avg score > 70 ──\n'
        'strong_domains = df.groupby("domain").filter(lambda g: g["score"].mean() > 70)\n'
        'print(f"\\nDomains with avg > 70: {strong_domains[\'domain\'].unique().tolist()}")\n'
        '\n'
        '# ── Pivot table ──\n'
        'pivot = pd.pivot_table(df, values="score", index="city", columns="domain",\n'
        '                       aggfunc="mean", fill_value=0).round(1)\n'
        'print("\\n=== Pivot Table: Score by City x Domain ===")\n'
        'print(pivot)'
    ),
    try_it_note="Add a 'month' column with values 'Jan','Feb','Mar' cycling. Group by domain AND month. Which domain+month combination has the highest average score?"
)

# ─── SQL: JOINs ─────────────────────────────────────────────────────────────
RICH['JOINs - Combining Tables'] = dict(
    content=(
        h2("Why JOINs?")
        + p("In real databases, data is split across multiple tables to avoid redundancy (normalization). A student table won't store the full course details - it just stores a course_id. You need JOINs to combine related data from multiple tables.")
        + p("JOINs are one of the most important and frequently used SQL operations. Every real analytics query uses at least one JOIN.")
        + h2("Types of JOINs")
        + tbl(
            ["Join Type", "What it Returns", "Rows from Left?", "Rows from Right?"],
            [
                [b("INNER JOIN"), "Only rows where the condition matches in BOTH tables", "Only matched", "Only matched"],
                [b("LEFT JOIN"), "All left rows + matched right rows (NULL if no match)", "All", "Only matched"],
                [b("RIGHT JOIN"), "All right rows + matched left rows (NULL if no match)", "Only matched", "All"],
                [b("FULL OUTER JOIN"), "All rows from both tables (NULL where no match)", "All", "All"],
                [b("CROSS JOIN"), "Every combination of left and right rows (Cartesian product)", "All", "All"],
                [b("SELF JOIN"), "A table joined to itself (using aliases)", "All", "All"],
            ]
        )
        + h2("INNER JOIN - The Most Common")
        + p("Returns only rows where the join condition matches in both tables. Missing matches are excluded.")
        + bq(c("SELECT s.name, e.course_name, e.score") + "<br>"
             + c("FROM students s") + "<br>"
             + c("INNER JOIN enrollments e ON s.id = e.student_id;"))
        + h2("LEFT JOIN - Keep All Left Table Rows")
        + p("Returns all rows from the left table. For right table, fills NULL where there is no match. Use LEFT JOIN when you want to see all records from one table, even if they have no related records in the other.")
        + bq(c("SELECT s.name, e.course_name") + "<br>"
             + c("FROM students s") + "<br>"
             + c("LEFT JOIN enrollments e ON s.id = e.student_id;") + "<br><br>"
             + "<em>-- Students with no enrollments appear with NULL in course_name</em>")
        + h2("Finding Unmatched Records (Anti-Join)")
        + p("A common pattern: find rows in the LEFT table with NO match in the RIGHT table:")
        + bq(c("SELECT s.name FROM students s") + "<br>"
             + c("LEFT JOIN enrollments e ON s.id = e.student_id") + "<br>"
             + c("WHERE e.student_id IS NULL;") + "<br><br>"
             + "<em>-- Students who are not enrolled in any course</em>")
        + h2("JOIN Best Practices")
        + ul(
            "Always use <b>table aliases</b> (e.g., " + c("students s") + ") - queries become much more readable",
            "Use <b>INNER JOIN</b> when you only care about matching records",
            "Use <b>LEFT JOIN</b> when you need all records from the primary table",
            "Filter on the <b>joined table in the ON clause</b>, not in WHERE, to maintain LEFT JOIN semantics",
            "Avoid CROSS JOINs on large tables - N x M rows can crash your database",
        )
        + tip("After any JOIN, check for unexpected row multiplication. If your result has more rows than expected, you likely have a many-to-many relationship. Add DISTINCT or GROUP BY to deduplicate.")
        + warn("Never join on unindexed columns in production. JOINs on columns without indexes will cause full table scans - extremely slow on large tables. Always index your foreign key columns.")
    ),
    code_example=(
        '-- ============================================\n'
        '-- SQL JOINs: Combining Tables\n'
        '-- ============================================\n'
        '\n'
        '-- Create sample tables\n'
        'CREATE TABLE students (\n'
        '    id      INTEGER PRIMARY KEY,\n'
        '    name    TEXT,\n'
        '    city    TEXT,\n'
        '    is_paid INTEGER\n'
        ');\n'
        '\n'
        'CREATE TABLE courses (\n'
        '    id    INTEGER PRIMARY KEY,\n'
        '    name  TEXT,\n'
        '    price REAL\n'
        ');\n'
        '\n'
        'CREATE TABLE enrollments (\n'
        '    student_id INTEGER REFERENCES students(id),\n'
        '    course_id  INTEGER REFERENCES courses(id),\n'
        '    score      REAL,\n'
        '    joined_on  TEXT\n'
        ');\n'
        '\n'
        "INSERT INTO students VALUES (1,'Priya','Mumbai',1),(2,'Raj','Delhi',1),\n"
        "  (3,'Neha','Mumbai',0),(4,'Arjun','Chennai',1),(5,'Meera','Delhi',0);\n"
        "\n"
        "INSERT INTO courses VALUES (1,'Data Analytics',15000),(2,'Machine Learning',20000),\n"
        "  (3,'Web Development',12000);\n"
        "\n"
        "INSERT INTO enrollments VALUES\n"
        "  (1,1,92,'2024-01-10'),(1,2,78,'2024-01-10'),\n"
        "  (2,2,85,'2024-02-01'),(3,1,65,'2024-02-15'),\n"
        "  (4,3,91,'2024-03-01');\n"
        "-- Meera (id=5) has NO enrollments\n"
        '\n'
        '-- 1. INNER JOIN: only enrolled students with their course\n'
        'SELECT s.name, c.name AS course, e.score\n'
        'FROM students s\n'
        'INNER JOIN enrollments e ON s.id = e.student_id\n'
        'INNER JOIN courses c ON e.course_id = c.id\n'
        'ORDER BY s.name, e.score DESC;\n'
        '\n'
        '-- 2. LEFT JOIN: all students, even unenrolled (Meera shows up)\n'
        'SELECT s.name, c.name AS course, e.score\n'
        'FROM students s\n'
        'LEFT JOIN enrollments e ON s.id = e.student_id\n'
        'LEFT JOIN courses c ON e.course_id = c.id\n'
        'ORDER BY s.name;\n'
        '\n'
        '-- 3. Anti-join: students with no enrollments\n'
        'SELECT s.name, s.city\n'
        'FROM students s\n'
        'LEFT JOIN enrollments e ON s.id = e.student_id\n'
        'WHERE e.student_id IS NULL;\n'
        '\n'
        '-- 4. Aggregated JOIN: avg score per student\n'
        'SELECT\n'
        '    s.name,\n'
        '    COUNT(e.course_id) AS courses_enrolled,\n'
        '    ROUND(AVG(e.score), 1) AS avg_score,\n'
        '    SUM(c.price) AS total_spent\n'
        'FROM students s\n'
        'LEFT JOIN enrollments e ON s.id = e.student_id\n'
        'LEFT JOIN courses c ON e.course_id = c.id\n'
        'GROUP BY s.id, s.name\n'
        'ORDER BY avg_score DESC;'
    ),
    try_it_note="Write a query to find courses that have ZERO enrollments. Use a LEFT JOIN from courses to enrollments and filter WHERE enrollment is NULL."
)

# ─── SQL: Subqueries & CTEs ─────────────────────────────────────────────────
RICH['Subqueries & CTEs'] = dict(
    content=(
        h2("What are Subqueries?")
        + p("A <b>subquery</b> (also called an inner query or nested query) is a query inside another query. Subqueries allow you to use the result of one query as input to another.")
        + p("They are one of the most powerful SQL tools - enabling complex filtering, computation, and transformation that would be impossible with simple SELECT statements.")
        + h2("Types of Subqueries")
        + tbl(
            ["Type", "Location", "Returns", "Example Use"],
            [
                [b("Scalar"), "SELECT or WHERE", "Single value", "Find students with score above overall average"],
                [b("Row"), "WHERE with comparison", "Single row", "Find the student with exactly the top score"],
                [b("Table"), "FROM clause", "Virtual table", "Pre-aggregate, then join or filter"],
                [b("Correlated"), "WHERE, referencing outer query", "Depends on outer row", "Find each student's rank within their domain"],
            ]
        )
        + h2("Scalar Subquery in WHERE")
        + p("The most common pattern - filter rows based on an aggregate result:")
        + bq(c("SELECT name, score") + "<br>"
             + c("FROM students") + "<br>"
             + c("WHERE score > (SELECT AVG(score) FROM students);"))
        + h2("Subquery in FROM (Derived Table)")
        + p("Create a temporary virtual table from a subquery and then query it:")
        + bq(c("SELECT domain, avg_score") + "<br>"
             + c("FROM (") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;SELECT domain, AVG(score) AS avg_score") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;FROM students GROUP BY domain") + "<br>"
             + c(") AS domain_stats") + "<br>"
             + c("WHERE avg_score > 80;"))
        + h2("CTEs: Common Table Expressions (WITH clause)")
        + p("A <b>CTE</b> is a named temporary result set, defined with the WITH keyword. CTEs make complex queries readable by breaking them into logical, named steps - like variables in programming.")
        + bq(c("WITH domain_stats AS (") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;SELECT domain, AVG(score) AS avg_score, COUNT(*) AS n") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;FROM students GROUP BY domain") + "<br>"
             + c("),") + "<br>"
             + c("top_students AS (") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;SELECT * FROM students WHERE score >= 85") + "<br>"
             + c(")") + "<br>"
             + c("SELECT t.name, t.score, d.avg_score") + "<br>"
             + c("FROM top_students t") + "<br>"
             + c("JOIN domain_stats d ON t.domain = d.domain;"))
        + h2("CTE vs Subquery - When to Use Which")
        + tbl(
            ["Feature", "Subquery", "CTE"],
            [
                ["Readability", "Can get deeply nested and unreadable", "Named steps - much more readable"],
                ["Reuse", "Cannot reuse the same result in same query", "Can reference the same CTE multiple times"],
                ["Debugging", "Hard to debug step-by-step", "Each CTE can be tested independently"],
                ["Recursion", "Not possible", "CTEs support recursive queries"],
                ["Performance", "Same as CTE in most databases", "Same in most cases"],
            ]
        )
        + tip("CTEs are your best tool for writing readable, maintainable SQL. Think of each CTE as a step in an algorithm - give it a descriptive name and make each step do one logical thing.")
        + note("Some databases (PostgreSQL, SQL Server) can use CTEs as optimization fences that affect query planning. In most cases, the optimizer treats CTEs and subqueries equivalently.")
    ),
    code_example=(
        '-- ============================================\n'
        '-- Subqueries and CTEs\n'
        '-- ============================================\n'
        '\n'
        '-- 1. Scalar subquery: above-average scorers\n'
        'SELECT name, domain, score\n'
        'FROM students\n'
        'WHERE score > (SELECT AVG(score) FROM students WHERE score IS NOT NULL)\n'
        'ORDER BY score DESC;\n'
        '\n'
        '-- 2. Subquery with IN: students in domains with avg > 80\n'
        'SELECT name, domain, score\n'
        'FROM students\n'
        'WHERE domain IN (\n'
        '    SELECT domain\n'
        '    FROM students\n'
        '    GROUP BY domain\n'
        '    HAVING AVG(score) > 80\n'
        ')\n'
        'ORDER BY domain, score DESC;\n'
        '\n'
        '-- 3. Subquery in FROM: derived table\n'
        'SELECT s.name, s.score, stats.avg_score,\n'
        '       ROUND(s.score - stats.avg_score, 1) AS vs_domain_avg\n'
        'FROM students s\n'
        'JOIN (\n'
        '    SELECT domain, AVG(score) AS avg_score\n'
        '    FROM students\n'
        '    GROUP BY domain\n'
        ') stats ON s.domain = stats.domain\n'
        'WHERE s.score IS NOT NULL\n'
        'ORDER BY s.domain, vs_domain_avg DESC;\n'
        '\n'
        '-- 4. CTE: readable multi-step analysis\n'
        'WITH\n'
        'domain_stats AS (\n'
        '    SELECT\n'
        '        domain,\n'
        '        COUNT(*) AS n,\n'
        '        ROUND(AVG(score), 1) AS avg_score,\n'
        '        MAX(score) AS top_score\n'
        '    FROM students\n'
        '    WHERE score IS NOT NULL\n'
        '    GROUP BY domain\n'
        '),\n'
        'ranked_students AS (\n'
        '    SELECT s.*, ds.avg_score AS domain_avg,\n'
        '           CASE WHEN s.score >= ds.top_score THEN "Top Performer"\n'
        '                WHEN s.score >= ds.avg_score THEN "Above Average"\n'
        '                ELSE "Below Average"\n'
        '           END AS tier\n'
        '    FROM students s\n'
        '    JOIN domain_stats ds ON s.domain = ds.domain\n'
        '    WHERE s.score IS NOT NULL\n'
        ')\n'
        'SELECT name, domain, score, domain_avg, tier\n'
        'FROM ranked_students\n'
        'ORDER BY domain, score DESC;'
    ),
    try_it_note="Write a CTE to find: (1) the highest score per city, (2) then join back to students to get the name of the top scorer in each city."
)

# ─── MACHINE LEARNING: Linear Regression ────────────────────────────────────
RICH['Linear Regression'] = dict(
    content=(
        h2("Linear Regression: The Foundation of Machine Learning")
        + p("<b>Linear Regression</b> is the most fundamental supervised learning algorithm. It models the relationship between one or more input features and a continuous output by fitting a <b>straight line</b> (or hyperplane) through the data.")
        + p("Despite its simplicity, linear regression is still widely used in finance, economics, healthcare, and many other fields because it is interpretable, fast, and works well when the relationship between variables is approximately linear.")
        + h2("The Linear Regression Equation")
        + bq(c("y = beta_0 + beta_1*x1 + beta_2*x2 + ... + beta_n*xn + epsilon") + "<br><br>"
             + b("y") + " = target variable (what we want to predict)<br>"
             + b("beta_0") + " = intercept (y-value when all x = 0)<br>"
             + b("beta_1...n") + " = coefficients (weights) - learned during training<br>"
             + b("x1...n") + " = input features<br>"
             + b("epsilon") + " = error term (noise)")
        + h2("Simple vs Multiple Linear Regression")
        + tbl(
            ["Type", "Features", "Equation", "Example"],
            [
                [b("Simple"), "1 feature", "y = b0 + b1*x", "Sales = a + b * Advertising_spend"],
                [b("Multiple"), "2+ features", "y = b0 + b1*x1 + ... + bn*xn", "House price = f(area, rooms, location...)"],
            ]
        )
        + h2("How the Model Learns: OLS")
        + p("Linear regression uses <b>Ordinary Least Squares (OLS)</b> to find the best coefficients. It minimizes the sum of squared errors (SSE):")
        + bq(c("SSE = sum((y_true - y_pred)^2)") + "<br>The optimal coefficients have a closed-form solution: " + c("beta = (X^T X)^-1 X^T y"))
        + h2("Evaluation Metrics for Regression")
        + tbl(
            ["Metric", "Formula", "Interpretation", "Good Value"],
            [
                [b("MAE"), "mean(|y_true - y_pred|)", "Average absolute error in output units", "As low as possible"],
                [b("MSE"), "mean((y_true - y_pred)^2)", "Penalizes large errors more heavily", "As low as possible"],
                [b("RMSE"), "sqrt(MSE)", "Same units as output - most interpretable", "As low as possible"],
                [b("R-squared"), "1 - SSE/SST", "Proportion of variance explained by model", "0 to 1; higher is better"],
                [b("Adjusted R2"), "Penalizes for extra features", "Better for comparing models with different number of features", "Close to R2 or higher"],
            ]
        )
        + h2("Key Assumptions")
        + ul(
            b("Linearity") + " - the relationship between X and y is linear",
            b("Independence") + " - observations are independent of each other",
            b("Homoscedasticity") + " - constant variance in residuals across all predictions",
            b("Normality") + " - residuals are approximately normally distributed",
            b("No multicollinearity") + " - features should not be highly correlated with each other",
        )
        + tip("Feature scaling (standardization) is not required for linear regression (unlike SVM or KNN), but it makes coefficient interpretation easier and helps gradient-based optimization converge faster.")
        + warn("A high R-squared does NOT mean the model is a good fit. Always plot residuals. Patterns in residuals (curves, funnels) indicate assumption violations that invalidate your model.")
    ),
    code_example=(
        'import numpy as np\n'
        'from sklearn.linear_model import LinearRegression\n'
        'from sklearn.model_selection import train_test_split, cross_val_score\n'
        'from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n'
        'from sklearn.preprocessing import StandardScaler\n'
        '\n'
        '# ── Generate realistic student performance data ──\n'
        'np.random.seed(42)\n'
        'n = 200\n'
        'study_hours   = np.random.uniform(1, 10, n)\n'
        'prev_score    = np.random.uniform(40, 95, n)\n'
        'attendance    = np.random.uniform(0.5, 1.0, n)\n'
        'assignments   = np.random.randint(5, 15, n)\n'
        '\n'
        '# True relationship + noise\n'
        'score = (5.2 * study_hours + 0.4 * prev_score\n'
        '         + 12 * attendance + 1.1 * assignments + np.random.normal(0, 5, n))\n'
        'score = np.clip(score, 0, 100)\n'
        '\n'
        'X = np.column_stack([study_hours, prev_score, attendance, assignments])\n'
        'feature_names = ["study_hours", "prev_score", "attendance", "assignments"]\n'
        '\n'
        '# ── Train/Test split ──\n'
        'X_train, X_test, y_train, y_test = train_test_split(\n'
        '    X, score, test_size=0.2, random_state=42\n'
        ')\n'
        '\n'
        '# ── Train Linear Regression ──\n'
        'model = LinearRegression()\n'
        'model.fit(X_train, y_train)\n'
        '\n'
        '# ── Evaluate ──\n'
        'y_pred = model.predict(X_test)\n'
        'mae  = mean_absolute_error(y_test, y_pred)\n'
        'rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n'
        'r2   = r2_score(y_test, y_pred)\n'
        '\n'
        'print("=== Model Performance ===")\n'
        'print(f"  MAE  : {mae:.2f} points")\n'
        'print(f"  RMSE : {rmse:.2f} points")\n'
        'print(f"  R2   : {r2:.4f} ({r2:.1%} variance explained)")\n'
        '\n'
        '# ── Interpret coefficients ──\n'
        'print("\\n=== Feature Importance (Coefficients) ===")\n'
        'print(f"  Intercept: {model.intercept_:.2f}")\n'
        'for name, coef in zip(feature_names, model.coef_):\n'
        '    print(f"  {name:15}: {coef:+.3f}")\n'
        '\n'
        '# ── Cross-validation for robust estimate ──\n'
        'cv_scores = cross_val_score(model, X, score, cv=5, scoring="r2")\n'
        'print(f"\\n5-Fold CV R2: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")\n'
        '\n'
        '# ── Predict for a new student ──\n'
        'new_student = np.array([[8.0, 75.0, 0.9, 12]])\n'
        'predicted_score = model.predict(new_student)[0]\n'
        'print(f"\\nNew student prediction: {predicted_score:.1f}/100")'
    ),
    try_it_note="Add a 'sleep_hours' feature with values between 5-9. Does including it improve the R2? Look at its coefficient - does more sleep correlate with better scores?"
)

# ─── WEB DEV: CSS Flexbox ───────────────────────────────────────────────────
RICH['Flexbox Layout'] = dict(
    content=(
        h2("CSS Flexbox: The Modern Layout System")
        + p("<b>Flexbox (Flexible Box Layout)</b> is a CSS layout model that makes it easy to arrange items in rows or columns, distribute space between them, and align them. Before Flexbox, centering things vertically in CSS was notoriously difficult. Flexbox solved that.")
        + p("Flexbox is <b>one-dimensional</b> - it works in one direction at a time (either row or column). For two-dimensional layouts, use CSS Grid.")
        + h2("Enabling Flexbox")
        + bq(c(".container { display: flex; }") + "<br>That's it. All direct children become flex items automatically.")
        + h2("The Two Axes")
        + ul(
            b("Main axis") + " - the direction flex items flow (set by " + c("flex-direction") + "). Default: horizontal (left to right)",
            b("Cross axis") + " - perpendicular to the main axis. Default: vertical (top to bottom)",
        )
        + h2("Container Properties (Parent)")
        + tbl(
            ["Property", "Values", "What it Controls"],
            [
                [c("display"), c("flex | inline-flex"), "Enable flexbox on the container"],
                [c("flex-direction"), c("row | column | row-reverse | column-reverse"), "Direction items flow (main axis)"],
                [c("justify-content"), c("flex-start | center | flex-end | space-between | space-around | space-evenly"), "Alignment along MAIN axis"],
                [c("align-items"), c("stretch | center | flex-start | flex-end | baseline"), "Alignment along CROSS axis"],
                [c("flex-wrap"), c("nowrap | wrap | wrap-reverse"), "Whether items wrap to next line"],
                [c("gap"), c("16px | 1rem | 0"), "Space between flex items (modern, clean)"],
                [c("align-content"), c("flex-start | center | space-between | stretch"), "Multi-line cross-axis alignment"],
            ]
        )
        + h2("Item Properties (Children)")
        + tbl(
            ["Property", "Values", "What it Controls"],
            [
                [c("flex-grow"), "0 (default) | 1 | 2...", "How much space this item takes if extra space available"],
                [c("flex-shrink"), "1 (default) | 0...", "Whether this item shrinks if not enough space"],
                [c("flex-basis"), c("auto | 200px | 30%"), "Initial size of the item before growing/shrinking"],
                [c("flex"), c("flex: 1 1 auto"), "Shorthand for flex-grow, flex-shrink, flex-basis"],
                [c("align-self"), c("auto | center | flex-start | flex-end"), "Override align-items for single item"],
                [c("order"), "0 (default) | 1 | -1...", "Visual order (does not change DOM order)"],
            ]
        )
        + h2("The Most Useful Flexbox Patterns")
        + tbl(
            ["Goal", "CSS"],
            [
                ["Center a div horizontally AND vertically", c("display:flex; justify-content:center; align-items:center;")],
                ["Space items apart with margins between them", c("display:flex; justify-content:space-between;")],
                ["Sticky footer (content fills all remaining height)", c("display:flex; flex-direction:column; min-height:100vh; .main{flex:1}")],
                ["Equal-width columns", c("display:flex; gap:1rem; .col{flex:1}")],
                ["Navigation with logo left, links right", c("display:flex; justify-content:space-between; align-items:center;")],
            ]
        )
        + tip("Remember: " + c("justify-content") + " controls the <b>main axis</b>, " + c("align-items") + " controls the <b>cross axis</b>. This is the most common source of confusion with Flexbox. The axes flip when you change " + c("flex-direction") + "!")
        + note("Use " + c("gap") + " for spacing between flex items instead of margins. It only adds space BETWEEN items, not at the edges, so you don't need to remove margin from first/last items.")
    ),
    code_example=(
        '/* ============================================\n'
        '   Flexbox Layout Examples\n'
        '   ============================================ */\n'
        '\n'
        '/* 1. Classic navigation bar */\n'
        '.navbar {\n'
        '  display: flex;\n'
        '  justify-content: space-between;  /* logo left, links right */\n'
        '  align-items: center;             /* vertically center */\n'
        '  padding: 0 2rem;\n'
        '  height: 64px;\n'
        '  background: #0f172a;\n'
        '  color: white;\n'
        '}\n'
        '.navbar .links {\n'
        '  display: flex;\n'
        '  gap: 1.5rem;         /* clean spacing between links */\n'
        '  list-style: none;\n'
        '}\n'
        '\n'
        '/* 2. Centered hero section */\n'
        '.hero {\n'
        '  display: flex;\n'
        '  flex-direction: column;    /* stack title + button vertically */\n'
        '  justify-content: center;   /* center on main axis (now vertical) */\n'
        '  align-items: center;       /* center on cross axis (now horizontal) */\n'
        '  min-height: 60vh;\n'
        '  text-align: center;\n'
        '  gap: 1.5rem;\n'
        '}\n'
        '\n'
        '/* 3. Card grid that wraps */\n'
        '.card-grid {\n'
        '  display: flex;\n'
        '  flex-wrap: wrap;           /* cards wrap to next line */\n'
        '  gap: 1.5rem;\n'
        '  padding: 1.5rem;\n'
        '}\n'
        '.card-grid .card {\n'
        '  flex: 1 1 280px;           /* grow, shrink, minimum 280px wide */\n'
        '  background: white;\n'
        '  border-radius: 12px;\n'
        '  padding: 1.5rem;\n'
        '  box-shadow: 0 2px 12px rgba(0,0,0,.08);\n'
        '}\n'
        '\n'
        '/* 4. Full-page sticky footer layout */\n'
        'body {\n'
        '  display: flex;\n'
        '  flex-direction: column;\n'
        '  min-height: 100vh;\n'
        '}\n'
        'main { flex: 1; }           /* main fills remaining height */\n'
        'footer { background: #0f172a; color: white; padding: 2rem; }\n'
        '\n'
        '/* 5. Profile card: avatar left, info right */\n'
        '.profile-card {\n'
        '  display: flex;\n'
        '  align-items: center;\n'
        '  gap: 1rem;\n'
        '  padding: 1.5rem;\n'
        '  background: white;\n'
        '  border-radius: 12px;\n'
        '}\n'
        '.profile-card .avatar {\n'
        '  width: 64px;\n'
        '  height: 64px;\n'
        '  border-radius: 50%;\n'
        '  object-fit: cover;\n'
        '  flex-shrink: 0;            /* never shrink the avatar */\n'
        '}\n'
        '.profile-card .info {\n'
        '  flex: 1;                   /* info takes remaining space */\n'
        '}\n'
        '.profile-card .badge {\n'
        '  align-self: flex-start;    /* pin badge to top */\n'
        '  background: #10b981;\n'
        '  color: white;\n'
        '  padding: 2px 10px;\n'
        '  border-radius: 999px;\n'
        '  font-size: .75rem;\n'
        '  font-weight: 700;\n'
        '}'
    ),
    try_it_note="Create a responsive 3-column feature section. On mobile (max-width: 600px), use flex-direction: column so cards stack vertically. Use a media query."
)

# ─── DJANGO: Models & ORM ───────────────────────────────────────────────────
RICH['Models & ORM Queries'] = dict(
    content=(
        h2("Django Models: Your Database in Python")
        + p("A <b>Django Model</b> is a Python class that defines a database table. Each attribute becomes a column, and each model instance is a row. Django's ORM (Object-Relational Mapper) translates Python code into SQL automatically.")
        + p("You never need to write SQL for standard operations. Django handles CREATE TABLE, SELECT, INSERT, UPDATE, and DELETE through Python methods.")
        + h2("Creating a Model")
        + bq(c("class Student(models.Model):") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;name  = models.CharField(max_length=100)") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;score = models.FloatField(default=0)") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;class Meta:") + "<br>"
             + c("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ordering = ['-score']"))
        + h2("Common Field Types")
        + tbl(
            ["Field", "SQL Type", "Use For"],
            [
                [c("CharField(max_length=n)"), "VARCHAR(n)", "Short text: name, city, title"],
                [c("TextField()"), "TEXT", "Long text: description, bio, content"],
                [c("IntegerField()"), "INTEGER", "Whole numbers: count, rank, age"],
                [c("FloatField()"), "REAL", "Decimals: score, percentage"],
                [c("DecimalField(max_digits, decimal_places)"), "DECIMAL", "Money: salary, price (exact precision)"],
                [c("BooleanField()"), "BOOLEAN", "True/False: is_paid, is_active"],
                [c("DateTimeField()"), "DATETIME", "Timestamp: created_at, updated_at"],
                [c("DateField()"), "DATE", "Date only: birthday, deadline"],
                [c("EmailField()"), "VARCHAR(254)", "Email address with validation"],
                [c("ImageField(upload_to='...')"), "VARCHAR", "Image file path"],
                [c("ForeignKey(Model, on_delete=...)"), "INTEGER (FK)", "Many-to-one relationship"],
                [c("OneToOneField(Model, ...)"), "INTEGER (unique FK)", "One-to-one relationship"],
                [c("ManyToManyField(Model)"), "Junction table", "Many-to-many relationship"],
            ]
        )
        + h2("The Django ORM - Common Queries")
        + tbl(
            ["Operation", "ORM Code", "SQL Equivalent"],
            [
                ["Get all records", c("Student.objects.all()"), c("SELECT * FROM students")],
                ["Get by primary key", c("Student.objects.get(pk=1)"), c("SELECT * FROM students WHERE id=1")],
                ["Filter rows", c("Student.objects.filter(score__gte=75)"), c("SELECT * FROM students WHERE score >= 75")],
                ["Exclude rows", c("Student.objects.exclude(city='Delhi')"), c("SELECT * FROM students WHERE city != 'Delhi'")],
                ["Order results", c("Student.objects.order_by('-score')"), c("ORDER BY score DESC")],
                ["Count", c("Student.objects.filter(is_paid=True).count()"), c("SELECT COUNT(*) FROM students WHERE is_paid=1")],
                ["First / Last", c("Student.objects.order_by('-score').first()"), c("LIMIT 1")],
                ["Create", c("Student.objects.create(name='Priya', score=92)"), c("INSERT INTO students ...")],
                ["Update", c("Student.objects.filter(pk=1).update(score=95)"), c("UPDATE students SET score=95 WHERE id=1")],
                ["Delete", c("Student.objects.filter(is_paid=False).delete()"), c("DELETE FROM students WHERE is_paid=0")],
            ]
        )
        + h2("Lookups (Field Lookups)")
        + tbl(
            ["Lookup", "Example", "SQL"],
            [
                [c("__exact"), c(".filter(city__exact='Mumbai')"), c("WHERE city = 'Mumbai'")],
                [c("__icontains"), c(".filter(name__icontains='kumar')"), c("WHERE LOWER(name) LIKE '%kumar%'")],
                [c("__gte"), c(".filter(score__gte=75)"), c("WHERE score >= 75")],
                [c("__in"), c(".filter(city__in=['Mumbai','Delhi'])"), c("WHERE city IN ('Mumbai','Delhi')")],
                [c("__isnull"), c(".filter(phone__isnull=True)"), c("WHERE phone IS NULL")],
                [c("__startswith"), c(".filter(name__startswith='A')"), c("WHERE name LIKE 'A%'")],
            ]
        )
        + tip("Use " + c("select_related('fk_field')") + " when you need to access ForeignKey fields. It does a SQL JOIN in one query instead of N+1 queries. Use " + c("prefetch_related('m2m_field')") + " for ManyToMany fields.")
        + warn("Avoid calling " + c(".all()") + " and then filtering in Python. Always filter at the ORM level. " + c("Student.objects.filter(score__gte=75)") + " is one SQL query; " + c("[s for s in Student.objects.all() if s.score >= 75]") + " loads ALL students into memory first!")
    ),
    code_example=(
        '# ── models.py ──\n'
        'from django.db import models\n'
        'from django.contrib.auth.models import User\n'
        '\n'
        'class Student(models.Model):\n'
        '    DOMAIN_CHOICES = [\n'
        '        ("DA", "Data Analytics"),\n'
        '        ("ML", "Machine Learning"),\n'
        '        ("WD", "Web Development"),\n'
        '        ("DS", "Data Science"),\n'
        '    ]\n'
        '    user        = models.OneToOneField(User, on_delete=models.CASCADE,\n'
        '                                       related_name="student")\n'
        '    student_id  = models.CharField(max_length=20, unique=True)\n'
        '    domain      = models.CharField(max_length=2, choices=DOMAIN_CHOICES)\n'
        '    score       = models.FloatField(default=0, help_text="Score out of 100")\n'
        '    city        = models.CharField(max_length=100, blank=True)\n'
        '    is_paid     = models.BooleanField(default=False)\n'
        '    enrolled_at = models.DateTimeField(auto_now_add=True)\n'
        '    updated_at  = models.DateTimeField(auto_now=True)\n'
        '\n'
        '    class Meta:\n'
        '        ordering = ["-score"]\n'
        '        verbose_name = "Student"\n'
        '        verbose_name_plural = "Students"\n'
        '        indexes = [\n'
        '            models.Index(fields=["domain", "score"]),\n'
        '            models.Index(fields=["city"]),\n'
        '        ]\n'
        '\n'
        '    def __str__(self):\n'
        '        return f"{self.student_id} - {self.user.get_full_name()}"\n'
        '\n'
        '    @property\n'
        '    def grade(self):\n'
        '        if self.score >= 90: return "A"\n'
        '        if self.score >= 75: return "B"\n'
        '        if self.score >= 60: return "C"\n'
        '        return "F"\n'
        '\n'
        '    @property\n'
        '    def is_top_performer(self):\n'
        '        return self.score >= 90\n'
        '\n'
        '\n'
        '# ── ORM Query Examples (in views.py or shell) ──\n'
        '\n'
        '# Get all Data Analytics students ordered by score desc\n'
        'da_students = Student.objects.filter(domain="DA").order_by("-score")\n'
        '\n'
        '# Count paid students\n'
        'paid_count = Student.objects.filter(is_paid=True).count()\n'
        '\n'
        '# Students with score above 80 in Mumbai\n'
        'top_mumbai = Student.objects.filter(\n'
        '    city__icontains="mumbai",\n'
        '    score__gte=80,\n'
        ').select_related("user")  # efficient FK join\n'
        '\n'
        '# Aggregate: average score per domain\n'
        'from django.db.models import Avg, Max, Count\n'
        'domain_stats = Student.objects.values("domain").annotate(\n'
        '    avg_score = Avg("score"),\n'
        '    top_score = Max("score"),\n'
        '    total     = Count("id"),\n'
        ').order_by("-avg_score")\n'
        '\n'
        '# Bulk update: give everyone a 5-point bonus (cap at 100)\n'
        'from django.db.models import F, ExpressionWrapper, FloatField\n'
        'Student.objects.update(score=ExpressionWrapper(\n'
        '    F("score") + 5, output_field=FloatField()\n'
        '))\n'
        '\n'
        '# Get or create a student record\n'
        'student, created = Student.objects.get_or_create(\n'
        '    student_id="TRH2024001",\n'
        '    defaults={"domain": "DA", "is_paid": False},\n'
        ')'
    ),
    try_it_note="Add a 'mentor' ForeignKey field on Student pointing to another Student (self-referential). How would you query 'all students assigned to mentor with id=1'?"
)

# ─── Apply all rich content to DB ───────────────────────────────────────────

updated = 0
skipped = 0

print("\nEnriching lessons in database...")
print("=" * 60)

for lesson in LearningLesson.objects.all().select_related('topic'):
    title = lesson.title
    if title in RICH:
        data = RICH[title]
        lesson.content      = data.get('content', lesson.content)
        lesson.code_example = data.get('code_example', lesson.code_example)
        lesson.try_it_note  = data.get('try_it_note', lesson.try_it_note)
        lesson.save(update_fields=['content', 'code_example', 'try_it_note'])
        print(f"[OK] {title[:65]}")
        updated += 1
    else:
        skipped += 1

print("=" * 60)
print(f"\nDone! Updated {updated} lessons, skipped {skipped}.")
print(f"Hint: Add more entries to RICH dict to enrich remaining lessons.")

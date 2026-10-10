"""
Management command: enrich_all_lessons
Updates every LearningLesson with rich, GFG-quality content.
Run: python manage.py enrich_all_lessons
"""
import sys
from django.core.management.base import BaseCommand
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

def ul(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def ol(*items):
    return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

def tbl(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    bd = ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for r in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{bd}</tbody></table>'


RICH = {}

# ─── ARTIFICIAL INTELLIGENCE ─────────────────────────────────────────────────

RICH['What is a Neural Network?'] = dict(
    content=(
        h2("What is a Neural Network?")
        + p("A <b>Neural Network</b> is a computational model loosely inspired by the structure of the human brain. It consists of layers of interconnected <b>neurons</b> (also called nodes or units). Each neuron receives inputs, performs a weighted sum, applies an activation function, and passes the output to the next layer.")
        + p("Neural networks are at the heart of modern AI — they power image recognition, voice assistants, recommendation engines, and large language models like GPT.")
        + h2("Architecture: Layers")
        + tbl(
            ["Layer", "Role", "Size"],
            [
                [b("Input Layer"), "Receives raw features — one neuron per feature", "= number of features"],
                [b("Hidden Layers"), "Learn abstract representations and patterns", "You choose (hyperparameter)"],
                [b("Output Layer"), "Produces final prediction", "1 for regression; N for N-class classification"],
            ]
        )
        + h2("How a Single Neuron Works")
        + ol(
            "Multiply each input by its weight: " + c("z = w1*x1 + w2*x2 + ... + b"),
            "Apply an activation function: " + c("a = f(z)"),
            "Pass the output " + c("a") + " to the next layer",
        )
        + h2("How Learning Works — Backpropagation")
        + ol(
            b("Forward Pass") + " — compute predictions layer by layer",
            b("Compute Loss") + " — measure how wrong the prediction is (e.g., MSE, Cross-Entropy)",
            b("Backward Pass") + " — compute gradients using chain rule (how much each weight contributed to the error)",
            b("Update Weights") + " — subtract gradient scaled by learning rate: " + c("w = w - lr * dL/dw"),
            b("Repeat") + " for many batches and epochs until loss converges",
        )
        + h2("Key Concepts")
        + tbl(
            ["Term", "Definition"],
            [
                [b("Epoch"), "One full pass through the entire training dataset"],
                [b("Batch Size"), "Number of samples processed before updating weights"],
                [b("Learning Rate"), "Step size for gradient descent — too large diverges, too small is slow"],
                [b("Loss Function"), "Measures prediction error — MSE for regression, Cross-Entropy for classification"],
                [b("Optimizer"), "Algorithm to update weights — SGD, Adam, RMSprop"],
                [b("Overfitting"), "Model memorizes training data, fails on test data"],
                [b("Dropout"), "Regularization: randomly disable neurons during training to prevent overfitting"],
            ]
        )
        + tip("Start with a small network (1-2 hidden layers) and scale up only if the model underfits. Complexity should match data complexity.")
        + warn("Without activation functions, stacking layers just equals one linear transformation — the network cannot learn non-linear patterns.")
        + bq("\"A neural network is a universal function approximator — given enough neurons and data, it can approximate any continuous function.\" — Universal Approximation Theorem")
    ),
    code_example=(
        'import torch\n'
        'import torch.nn as nn\n'
        'import torch.optim as optim\n'
        'from sklearn.datasets import make_classification\n'
        'from sklearn.model_selection import train_test_split\n'
        'from sklearn.preprocessing import StandardScaler\n'
        'import numpy as np\n'
        '\n'
        '# ── Generate data ──\n'
        'X, y = make_classification(n_samples=500, n_features=10, random_state=42)\n'
        'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n'
        '\n'
        'scaler = StandardScaler()\n'
        'X_train = scaler.fit_transform(X_train)\n'
        'X_test  = scaler.transform(X_test)\n'
        '\n'
        '# Convert to tensors\n'
        'X_tr = torch.FloatTensor(X_train)\n'
        'y_tr = torch.LongTensor(y_train)\n'
        'X_te = torch.FloatTensor(X_test)\n'
        'y_te = torch.LongTensor(y_test)\n'
        '\n'
        '# ── Define Neural Network ──\n'
        'class SimpleNN(nn.Module):\n'
        '    def __init__(self):\n'
        '        super().__init__()\n'
        '        self.net = nn.Sequential(\n'
        '            nn.Linear(10, 32),   # input → hidden\n'
        '            nn.ReLU(),\n'
        '            nn.Dropout(0.3),\n'
        '            nn.Linear(32, 16),   # hidden → hidden\n'
        '            nn.ReLU(),\n'
        '            nn.Linear(16, 2),    # hidden → output (2 classes)\n'
        '        )\n'
        '    def forward(self, x):\n'
        '        return self.net(x)\n'
        '\n'
        'model     = SimpleNN()\n'
        'criterion = nn.CrossEntropyLoss()\n'
        'optimizer = optim.Adam(model.parameters(), lr=0.001)\n'
        '\n'
        '# ── Training Loop ──\n'
        'for epoch in range(50):\n'
        '    model.train()\n'
        '    optimizer.zero_grad()\n'
        '    outputs = model(X_tr)\n'
        '    loss    = criterion(outputs, y_tr)\n'
        '    loss.backward()\n'
        '    optimizer.step()\n'
        '    if (epoch + 1) % 10 == 0:\n'
        '        print(f"Epoch {epoch+1:3d} | Loss: {loss.item():.4f}")\n'
        '\n'
        '# ── Evaluate ──\n'
        'model.eval()\n'
        'with torch.no_grad():\n'
        '    preds = model(X_te).argmax(dim=1)\n'
        '    acc   = (preds == y_te).float().mean()\n'
        '    print(f"Test Accuracy: {acc:.1%}")'
    ),
    try_it_note="Add a third hidden layer with 8 neurons. Does accuracy improve? Try changing dropout to 0.5."
)

RICH['Activation Functions'] = dict(
    content=(
        h2("Why Do We Need Activation Functions?")
        + p("Without activation functions, a neural network — no matter how many layers deep — computes only a <b>linear transformation</b> of the input. Stacking linear layers is mathematically equivalent to a single linear layer.")
        + p("Activation functions introduce <b>non-linearity</b>, enabling neural networks to learn complex, curved decision boundaries and approximate any function.")
        + h2("Most Important Activation Functions")
        + tbl(
            ["Function", "Formula", "Range", "Best Used In"],
            [
                [b("ReLU"), "max(0, x)", "[0, ∞)", "Hidden layers — fast, sparse, default choice"],
                [b("Leaky ReLU"), "x if x>0 else 0.01x", "(-∞, ∞)", "When dying ReLU is a problem"],
                [b("Sigmoid"), "1 / (1 + e^-x)", "(0, 1)", "Binary classification output layer"],
                [b("Softmax"), "e^xi / Σe^xj", "(0, 1) summing to 1", "Multi-class output layer"],
                [b("Tanh"), "(e^x - e^-x)/(e^x + e^-x)", "(-1, 1)", "RNNs, hidden layers needing negative outputs"],
                [b("GELU"), "x * Φ(x)", "Smooth", "Transformers (BERT, GPT)"],
            ]
        )
        + h2("ReLU — The Workhorse")
        + p("ReLU (Rectified Linear Unit) is by far the most popular activation function for hidden layers. It is computationally simple, solves the vanishing gradient problem better than sigmoid/tanh, and creates sparse activations (many zeros).")
        + warn("The <b>Dying ReLU Problem</b>: If a neuron always outputs 0 (ReLU inactive), its gradient is 0 — it never updates. Use Leaky ReLU or ELU if you see many dead neurons.")
        + h2("Sigmoid vs Softmax")
        + tbl(
            ["Property", "Sigmoid", "Softmax"],
            [
                ["Output", "Independent probabilities", "Probabilities that sum to 1"],
                ["Use Case", "Binary classification (0 or 1)", "Multi-class classification"],
                ["Layer", "Output layer only", "Output layer only"],
            ]
        )
        + tip("Use ReLU by default for hidden layers. Only use sigmoid/softmax in the output layer. Tanh works well in RNNs since its output is centered at 0.")
        + h2("The Vanishing Gradient Problem")
        + p("Deep networks using sigmoid or tanh suffer from <b>vanishing gradients</b>: as the gradient is multiplied through many layers during backpropagation, it becomes exponentially small — early layers learn extremely slowly or not at all. ReLU largely solves this.")
    ),
    code_example=(
        'import numpy as np\n'
        'import matplotlib.pyplot as plt\n'
        '\n'
        '# ── Implement activation functions from scratch ──\n'
        'x = np.linspace(-5, 5, 200)\n'
        '\n'
        'def relu(x):        return np.maximum(0, x)\n'
        'def leaky_relu(x):  return np.where(x > 0, x, 0.01 * x)\n'
        'def sigmoid(x):     return 1 / (1 + np.exp(-x))\n'
        'def tanh(x):        return np.tanh(x)\n'
        '\n'
        'print("=== Activation Function Values at Key Points ===")\n'
        'print(f"{'x':>8} | {'ReLU':>8} | {'Sigmoid':>8} | {'Tanh':>8}")\n'
        'print("-" * 40)\n'
        'for v in [-3, -1, 0, 1, 3]:\n'
        '    print(f"{v:>8.0f} | {relu(v):>8.4f} | {sigmoid(v):>8.4f} | {tanh(v):>8.4f}")\n'
        '\n'
        '# ── Softmax for multi-class ──\n'
        'def softmax(logits):\n'
        '    e = np.exp(logits - np.max(logits))  # numerical stability\n'
        '    return e / e.sum()\n'
        '\n'
        'logits = np.array([2.5, 1.0, 0.3, -0.8])  # raw network outputs\n'
        'probs  = softmax(logits)\n'
        'classes = ["Cat", "Dog", "Bird", "Fish"]\n'
        '\n'
        'print("\\n=== Softmax Probabilities ===")\n'
        'for cls, p in zip(classes, probs):\n'
        '    bar = "#" * int(p * 40)\n'
        '    print(f"{cls:6}: {p:.4f}  {bar}")\n'
        'print(f"Sum = {probs.sum():.4f}")  # always 1.0\n'
        '\n'
        '# ── ReLU dying neuron example ──\n'
        'weights = np.array([-5.0, -3.0, 0.1])  # very negative weights\n'
        'output  = relu(weights)\n'
        'print("\\nDying ReLU example:", output)  # all zeros!'
    ),
    try_it_note="Implement the GELU function: x * 0.5 * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x**3))). Compare its shape to ReLU."
)

RICH['Training Loop & Loss Functions'] = dict(
    content=(
        h2("The Neural Network Training Loop")
        + p("Training a neural network is an iterative optimization process. In each iteration, we feed data in, measure how wrong the predictions are, compute how to improve, and update the model's weights.")
        + ol(
            b("Load a mini-batch") + " of training samples (e.g., 32 samples)",
            b("Zero gradients") + " — " + c("optimizer.zero_grad()") + " (important! PyTorch accumulates gradients by default)",
            b("Forward pass") + " — run data through the network: " + c("outputs = model(X)"),
            b("Compute loss") + " — measure prediction error: " + c("loss = criterion(outputs, y)"),
            b("Backward pass") + " — compute gradients via backpropagation: " + c("loss.backward()"),
            b("Update weights") + " — apply gradient descent step: " + c("optimizer.step()"),
            b("Repeat") + " until convergence (loss stops decreasing significantly)",
        )
        + h2("Loss Functions — Choosing the Right One")
        + tbl(
            ["Loss Function", "Task", "Formula (simplified)", "PyTorch"],
            [
                [b("MSE"), "Regression", "(y_pred - y_true)^2 average", c("nn.MSELoss()")],
                [b("MAE"), "Regression (robust to outliers)", "|y_pred - y_true| average", c("nn.L1Loss()")],
                [b("Binary Cross-Entropy"), "Binary classification", "-[y log(p) + (1-y)log(1-p)]", c("nn.BCELoss()")],
                [b("Cross-Entropy"), "Multi-class classification", "-log(p_correct_class)", c("nn.CrossEntropyLoss()")],
                [b("Huber Loss"), "Regression — combines MSE+MAE", "Quadratic near 0, linear far from 0", c("nn.HuberLoss()")],
            ]
        )
        + h2("Optimizers — How Weights Get Updated")
        + tbl(
            ["Optimizer", "Key Idea", "When to Use"],
            [
                [b("SGD"), "Plain gradient descent", "Simple problems, image classification with momentum"],
                [b("Adam"), "Adaptive learning rates per parameter", "Default choice — works well for most problems"],
                [b("RMSprop"), "Divides by running mean of squared gradients", "RNNs, non-stationary problems"],
                [b("AdaGrad"), "Accumulates squared gradients", "Sparse data, NLP"],
            ]
        )
        + h2("Epochs vs Batches vs Iterations")
        + tbl(
            ["Term", "Definition", "Example"],
            [
                [b("Epoch"), "One full pass through training data", "1000 samples / 32 batch = 32 iterations = 1 epoch"],
                [b("Batch"), "Subset of data processed at once", "32 samples"],
                [b("Iteration"), "One weight update step (one batch)", "32 iterations for 1000 samples with batch=32"],
            ]
        )
        + tip("Use " + c("Adam") + " with learning rate " + c("1e-3") + " as your starting point. If training is noisy, reduce batch size or learning rate. If training is too slow, increase learning rate.")
        + warn("Forgetting " + c("optimizer.zero_grad()") + " is a common PyTorch bug. Without it, gradients accumulate across batches and your model won't train correctly.")
        + note("Monitor both training loss AND validation loss every epoch. If training loss decreases but validation loss increases, your model is overfitting.")
    ),
    code_example=(
        'import torch\n'
        'import torch.nn as nn\n'
        'import torch.optim as optim\n'
        'from torch.utils.data import DataLoader, TensorDataset\n'
        'from sklearn.datasets import make_regression\n'
        'from sklearn.model_selection import train_test_split\n'
        'from sklearn.preprocessing import StandardScaler\n'
        '\n'
        '# ── Prepare data ──\n'
        'X, y = make_regression(n_samples=400, n_features=5, noise=10, random_state=42)\n'
        'X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)\n'
        '\n'
        'scaler = StandardScaler()\n'
        'X_train = scaler.fit_transform(X_train)\n'
        'X_val   = scaler.transform(X_val)\n'
        '\n'
        'X_tr = torch.FloatTensor(X_train)\n'
        'y_tr = torch.FloatTensor(y_train).unsqueeze(1)\n'
        'X_v  = torch.FloatTensor(X_val)\n'
        'y_v  = torch.FloatTensor(y_val).unsqueeze(1)\n'
        '\n'
        'train_ds = TensorDataset(X_tr, y_tr)\n'
        'loader   = DataLoader(train_ds, batch_size=32, shuffle=True)\n'
        '\n'
        '# ── Model ──\n'
        'model = nn.Sequential(\n'
        '    nn.Linear(5, 64), nn.ReLU(),\n'
        '    nn.Linear(64, 32), nn.ReLU(),\n'
        '    nn.Linear(32, 1)\n'
        ')\n'
        'criterion = nn.MSELoss()\n'
        'optimizer = optim.Adam(model.parameters(), lr=1e-3)\n'
        '\n'
        '# ── Training Loop with Validation ──\n'
        'print(f"{"Epoch":>6} | {"Train Loss":>12} | {"Val Loss":>10}")\n'
        'print("-" * 35)\n'
        'for epoch in range(1, 51):\n'
        '    model.train()\n'
        '    train_loss = 0\n'
        '    for X_batch, y_batch in loader:\n'
        '        optimizer.zero_grad()\n'
        '        pred = model(X_batch)\n'
        '        loss = criterion(pred, y_batch)\n'
        '        loss.backward()\n'
        '        optimizer.step()\n'
        '        train_loss += loss.item()\n'
        '\n'
        '    model.eval()\n'
        '    with torch.no_grad():\n'
        '        val_loss = criterion(model(X_v), y_v).item()\n'
        '\n'
        '    if epoch % 10 == 0:\n'
        '        print(f"{epoch:>6} | {train_loss/len(loader):>12.4f} | {val_loss:>10.4f}")\n'
        '\n'
        'print("\\nTraining complete!")'
    ),
    try_it_note="Switch the loss function to nn.L1Loss (MAE). Compare how training looks — is it smoother or noisier?"
)

RICH['Text Preprocessing'] = dict(
    content=(
        h2("Why Text Preprocessing?")
        + p("Raw text is <b>noisy, inconsistent, and unstructured</b>. Machine learning models only understand numbers. Text preprocessing converts messy human language into clean numerical representations that models can learn from.")
        + p("A model trained on unclean text will have worse performance than one trained on well-preprocessed text. Garbage in = garbage out.")
        + h2("The Standard NLP Preprocessing Pipeline")
        + ol(
            b("Lowercasing") + " — " + c('"Hello World" → "hello world"') + " — removes case inconsistency",
            b("Remove noise") + " — strip HTML tags, URLs, special characters, extra whitespace",
            b("Tokenization") + " — split text into words (tokens): " + c('"hello world" → ["hello", "world"]'),
            b("Remove Stop Words") + " — remove common words (the, is, and) that carry little meaning",
            b("Stemming / Lemmatization") + " — reduce words to their root form",
            b("Vectorization") + " — convert tokens to numbers (Bag of Words, TF-IDF, word embeddings)",
        )
        + h2("Stemming vs Lemmatization")
        + tbl(
            ["Method", "How it Works", "Example", "Pros/Cons"],
            [
                [b("Stemming"), "Chops off suffix — rule-based, fast", '"running" → "run"', "Fast but crude — 'studies' → 'studi'"],
                [b("Lemmatization"), "Uses vocabulary + grammar, context-aware", '"better" → "good"', "Accurate but slower — needs language model"],
            ]
        )
        + h2("Tokenization Types")
        + ul(
            b("Word tokenization") + " — split on whitespace/punctuation (most common)",
            b("Sentence tokenization") + " — split text into sentences",
            b("Subword tokenization") + " — used in BERT, GPT (byte-pair encoding) — handles unknown words",
        )
        + h2("Stop Words")
        + p("Stop words are extremely common words that appear in almost every document and provide little discriminative value: <em>the, is, in, at, that, and, a, an, it, of...</em>")
        + note("In some tasks (sentiment analysis), negation words like 'not', 'never', 'no' are stop words you should KEEP. Always review your stop word list for your specific task.")
        + h2("Regular Expressions for Text Cleaning")
        + tbl(
            ["Pattern", "Matches", "Use For"],
            [
                [c(r"[^a-z\s]"), "Non-letter, non-space characters", "Remove punctuation, numbers"],
                [c(r"http\S+"), "URLs starting with http", "Remove links"],
                [c(r"<[^>]+>"), "HTML tags", "Strip HTML from web scraping"],
                [c(r"\s+"), "Multiple whitespace", "Normalize spaces"],
            ]
        )
        + tip("Use SpaCy instead of NLTK for production NLP. SpaCy is significantly faster and provides better named entity recognition, dependency parsing, and modern tokenization.")
    ),
    code_example=(
        'import re\n'
        'import string\n'
        'from collections import Counter\n'
        '\n'
        '# ── Sample raw text (messy, real-world style) ──\n'
        'raw_texts = [\n'
        '    "The quick brown FOX jumps over the lazy dog!! Visit https://example.com for details.",\n'
        '    "<p>Machine Learning is AMAZING for Data Science enthusiasts!</p>",\n'
        '    "Running, runs, runner — these all relate to RUN (stemming demo).",\n'
        '    "I love NLP.  But  preprocessing  takes  sooo long...",\n'
        ']\n'
        '\n'
        '# ── Stop words (simplified set) ──\n'
        'STOP_WORDS = {"the","a","an","is","in","at","of","for","to","and","or","but",\n'
        '              "it","this","that","are","was","be","been","have","has","with"}\n'
        '\n'
        'def preprocess(text):\n'
        '    # 1. Lowercase\n'
        '    text = text.lower()\n'
        '    # 2. Remove HTML tags\n'
        '    text = re.sub(r"<[^>]+>", " ", text)\n'
        '    # 3. Remove URLs\n'
        '    text = re.sub(r"http\\S+|www\\S+", "", text)\n'
        '    # 4. Remove punctuation & digits\n'
        '    text = re.sub(r"[^a-z\\s]", " ", text)\n'
        '    # 5. Normalize whitespace\n'
        '    text = re.sub(r"\\s+", " ", text).strip()\n'
        '    # 6. Tokenize\n'
        '    tokens = text.split()\n'
        '    # 7. Remove stop words (keep tokens with len > 2)\n'
        '    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]\n'
        '    return tokens\n'
        '\n'
        'print("=== Preprocessing Results ===")\n'
        'all_tokens = []\n'
        'for i, text in enumerate(raw_texts):\n'
        '    tokens = preprocess(text)\n'
        '    all_tokens.extend(tokens)\n'
        '    print(f"\\nDoc {i+1}: {tokens}")\n'
        '\n'
        '# ── Word frequency analysis ──\n'
        'freq = Counter(all_tokens)\n'
        'print("\\n=== Top 10 Words ===")\n'
        'for word, count in freq.most_common(10):\n'
        '    bar = "|" * count\n'
        '    print(f"{word:20}: {bar} ({count})")'
    ),
    try_it_note="Add your own sentence to raw_texts. Check what tokens remain after preprocessing. Are any important words accidentally removed?"
)

RICH['TF-IDF & Text Classification'] = dict(
    content=(
        h2("What is TF-IDF?")
        + p("<b>TF-IDF</b> (Term Frequency-Inverse Document Frequency) is a numerical statistic that reflects how <em>important a word is to a document in a collection</em>. It balances two factors:")
        + tbl(
            ["Component", "Formula", "Meaning"],
            [
                [b("TF (Term Frequency)"), "count(word) / total_words", "How often the word appears in THIS document"],
                [b("IDF (Inverse Doc Freq)"), "log(N / df(word))", "How rare the word is ACROSS all documents"],
                [b("TF-IDF"), "TF × IDF", "High for words that are frequent in ONE doc but rare overall"],
            ]
        )
        + p("Common words like 'the', 'is', 'and' appear in every document → low IDF → low TF-IDF. Specific terms like 'photosynthesis' appear only in biology docs → high IDF → high TF-IDF.")
        + h2("Text Classification Pipeline")
        + ol(
            b("Collect labelled text") + " — e.g., 1000 emails labelled Spam/Not Spam",
            b("Preprocess") + " — clean, tokenize, remove stop words",
            b("Vectorize") + " — convert text to TF-IDF matrix (each row = doc, each column = word)",
            b("Train classifier") + " — Naive Bayes, Logistic Regression, or SVM work well on TF-IDF",
            b("Evaluate") + " — accuracy, precision, recall, F1-score",
        )
        + h2("Bag of Words vs TF-IDF vs Word Embeddings")
        + tbl(
            ["Method", "Captures Frequency?", "Captures Importance?", "Captures Meaning?", "Use Case"],
            [
                [b("Bag of Words"), "Yes", "No", "No", "Simple baseline"],
                [b("TF-IDF"), "Yes", "Yes", "No", "Document classification, search"],
                [b("Word2Vec / GloVe"), "No", "Partial", "Yes (local context)", "Similarity tasks, NER"],
                [b("BERT Embeddings"), "No", "Yes", "Yes (full context)", "SOTA NLP tasks"],
            ]
        )
        + h2("Evaluation Metrics for Classification")
        + tbl(
            ["Metric", "Formula", "When It Matters Most"],
            [
                [b("Accuracy"), "Correct / Total", "Balanced classes"],
                [b("Precision"), "TP / (TP + FP)", "When false positives are costly (e.g., spam filter)"],
                [b("Recall"), "TP / (TP + FN)", "When false negatives are costly (e.g., disease detection)"],
                [b("F1 Score"), "2 * (P * R) / (P + R)", "Imbalanced classes — harmonic mean of precision & recall"],
            ]
        )
        + tip("Naive Bayes is surprisingly strong for text classification despite its simplistic assumption. Always use it as a fast baseline before trying complex models.")
        + warn("TF-IDF creates very sparse, high-dimensional matrices. With 50,000 unique words and 10,000 documents, you get a 10,000 x 50,000 matrix — but 95%+ of entries are zero. Use " + c("scipy.sparse") + " matrices to save memory.")
    ),
    code_example=(
        'from sklearn.feature_extraction.text import TfidfVectorizer\n'
        'from sklearn.naive_bayes import MultinomialNB\n'
        'from sklearn.linear_model import LogisticRegression\n'
        'from sklearn.model_selection import train_test_split\n'
        'from sklearn.metrics import classification_report\n'
        '\n'
        '# ── Sample labelled dataset ──\n'
        'texts = [\n'
        '    "Win free money now click here", "Congratulations you won a prize",\n'
        '    "Buy cheap medication online", "Earn 1000 dollars from home today",\n'
        '    "Limited offer get rich quick", "Free iPhone claim your reward",\n'
        '    "Meeting scheduled for tomorrow", "Please review the attached report",\n'
        '    "Project deadline is next Friday", "Can we discuss the budget proposal",\n'
        '    "Team lunch at 1pm in cafeteria", "Quarterly review meeting agenda",\n'
        ']\n'
        'labels = [1,1,1,1,1,1, 0,0,0,0,0,0]  # 1=Spam, 0=Not Spam\n'
        '\n'
        'X_train, X_test, y_train, y_test = train_test_split(\n'
        '    texts, labels, test_size=0.3, random_state=42\n'
        ')\n'
        '\n'
        '# ── TF-IDF Vectorization ──\n'
        'tfidf = TfidfVectorizer(max_features=500, stop_words="english", ngram_range=(1,2))\n'
        'X_tr_vec = tfidf.fit_transform(X_train)\n'
        'X_te_vec = tfidf.transform(X_test)\n'
        '\n'
        'print(f"Matrix shape: {X_tr_vec.shape}  (docs x features)")\n'
        '\n'
        '# ── Model 1: Naive Bayes ──\n'
        'nb = MultinomialNB()\n'
        'nb.fit(X_tr_vec, y_train)\n'
        'nb_preds = nb.predict(X_te_vec)\n'
        '\n'
        '# ── Model 2: Logistic Regression ──\n'
        'lr = LogisticRegression(max_iter=200)\n'
        'lr.fit(X_tr_vec, y_train)\n'
        'lr_preds = lr.predict(X_te_vec)\n'
        '\n'
        'print("\\n=== Naive Bayes ===")\n'
        'print(classification_report(y_test, nb_preds, target_names=["Ham","Spam"]))\n'
        '\n'
        'print("=== Logistic Regression ===")\n'
        'print(classification_report(y_test, lr_preds, target_names=["Ham","Spam"]))\n'
        '\n'
        '# ── Top spam words by TF-IDF weight ──\n'
        'feature_names = tfidf.get_feature_names_out()\n'
        'top_spam = lr.coef_[0].argsort()[-8:][::-1]\n'
        'print("Top spam indicators:", [feature_names[i] for i in top_spam])'
    ),
    try_it_note="Add 5 more spam examples and 5 more ham examples. Does accuracy improve? Try ngram_range=(1,3) and observe the effect."
)

RICH['Functions & Lambda'] = dict(
    content=(
        h2("Why Write Functions?")
        + p("Functions are the building blocks of reusable, maintainable code. Instead of writing the same logic 10 times, you write it once in a function and call it whenever needed. This is the <b>DRY principle</b> — Don't Repeat Yourself.")
        + p("In data analytics, virtually every step of your pipeline (load, clean, transform, visualize) should be a function. Functions make your code testable, readable, and shareable.")
        + h2("Anatomy of a Python Function")
        + bq(c("def") + " function_name(parameters):<br>&nbsp;&nbsp;&nbsp;&nbsp;<code>\"\"\"Docstring explaining what this does.\"\"\"</code><br>&nbsp;&nbsp;&nbsp;&nbsp;# function body<br>&nbsp;&nbsp;&nbsp;&nbsp;<code>return</code> value")
        + h2("Types of Parameters")
        + tbl(
            ["Type", "Syntax", "Example", "Behaviour"],
            [
                [b("Positional"), c("def f(a, b)"), c("f(1, 2)"), "Must be passed in order"],
                [b("Default"), c("def f(a, b=10)"), c("f(5)"), "Optional — uses default if not supplied"],
                [b("Keyword"), c("def f(a, b)"), c("f(b=2, a=1)"), "Can be passed in any order by name"],
                [b("*args"), c("def f(*args)"), c("f(1,2,3,4)"), "Variable number of positional args → tuple"],
                [b("**kwargs"), c("def f(**kw)"), c("f(x=1, y=2)"), "Variable number of keyword args → dict"],
            ]
        )
        + h2("Return Values")
        + p("Functions can return any Python object — a number, string, list, dict, or even another function. You can return multiple values as a tuple:")
        + bq(c("return min_val, max_val, avg") + " → caller does: " + c("lo, hi, avg = stats(data)"))
        + h2("Lambda Functions — Anonymous One-Liners")
        + p("A <b>lambda</b> is a small, anonymous function with no name and no " + c("return") + " statement. It is used for simple, throwaway operations — especially with " + c("map()") + ", " + c("filter()") + ", " + c("sorted()") + ".")
        + bq(c("lambda") + " parameters " + c(":") + " expression")
        + tbl(
            ["Use Case", "Lambda Expression", "Equivalent Regular Function"],
            [
                ["Sort by 2nd element", c("key=lambda x: x[1]"), c("def f(x): return x[1]")],
                ["Square a number", c("lambda x: x**2"), c("def square(x): return x**2")],
                ["Add two numbers", c("lambda a, b: a + b"), c("def add(a, b): return a + b")],
            ]
        )
        + h2("Higher-Order Functions")
        + tbl(
            ["Function", "What it Does", "Example"],
            [
                [c("map(f, lst)"), "Apply f to every element", c("list(map(lambda x: x*2, [1,2,3]))")],
                [c("filter(f, lst)"), "Keep elements where f returns True", c("list(filter(lambda x: x>3, [1,2,3,4,5]))")],
                [c("sorted(lst, key=f)"), "Sort by custom key function", c('sorted(names, key=lambda s: s.lower())')],
                [c("reduce(f, lst)"), "Fold list to single value", c("reduce(lambda a,b: a+b, [1,2,3,4])")],
            ]
        )
        + tip("If you find yourself using a lambda more than once, convert it to a named function. Lambdas are for inline, one-time-use logic only.")
        + h2("Scope: Local vs Global Variables")
        + p("Variables defined inside a function are <b>local</b> — they don't exist outside the function. Variables defined at module level are <b>global</b>. Avoid mutating global variables inside functions — pass data in and return it out.")
    ),
    code_example=(
        'from functools import reduce\n'
        '\n'
        '# ── Basic function with default parameter ──\n'
        'def classify_score(score, threshold=75, labels=("FAIL", "PASS")):\n'
        '    """Classify a numeric score into pass/fail label."""\n'
        '    return labels[1] if score >= threshold else labels[0]\n'
        '\n'
        'print(classify_score(88))          # PASS\n'
        'print(classify_score(60))          # FAIL\n'
        'print(classify_score(60, 55))      # PASS (threshold=55)\n'
        '\n'
        '# ── Multiple return values (tuple unpacking) ──\n'
        'def describe(data):\n'
        '    """Return min, max, mean, and standard deviation."""\n'
        '    n   = len(data)\n'
        '    avg = sum(data) / n\n'
        '    var = sum((x - avg)**2 for x in data) / n\n'
        '    return min(data), max(data), avg, var**0.5\n'
        '\n'
        'scores = [88, 45, 72, 91, 60, 38, 95, 67, 54, 83]\n'
        'lo, hi, mean, std = describe(scores)\n'
        'print(f"Min={lo}  Max={hi}  Mean={mean:.1f}  Std={std:.1f}")\n'
        '\n'
        '# ── *args and **kwargs ──\n'
        'def log(*args, level="INFO", **kwargs):\n'
        '    prefix = f"[{level}]"\n'
        '    msg    = " ".join(str(a) for a in args)\n'
        '    extra  = " ".join(f"{k}={v}" for k, v in kwargs.items())\n'
        '    print(f"{prefix} {msg} {extra}")\n'
        '\n'
        'log("User logged in", level="DEBUG", user_id=42, ip="192.168.1.1")\n'
        '\n'
        '# ── Lambda with map, filter, sorted ──\n'
        'students = [("Priya",92), ("Raj",78), ("Neha",85), ("Dev",63), ("Sanya",95)]\n'
        '\n'
        '# Sort by score descending\n'
        'ranked = sorted(students, key=lambda s: s[1], reverse=True)\n'
        'print("\\nRanking:")\n'
        'for rank, (name, score) in enumerate(ranked, 1):\n'
        '    print(f"  {rank}. {name}: {score}")\n'
        '\n'
        '# Filter only passing scores\n'
        'passed = list(filter(lambda s: s[1] >= 75, students))\n'
        'print("\\nPassed:", [s[0] for s in passed])\n'
        '\n'
        '# Map: add 5 bonus marks (cap at 100)\n'
        'with_bonus = list(map(lambda s: (s[0], min(100, s[1]+5)), students))\n'
        'print("With bonus:", with_bonus)'
    ),
    try_it_note="Write a function 'normalize(lst)' that scales a list to [0,1] range using (x - min) / (max - min). Apply it to the scores list."
)

RICH['Error Handling & File I/O'] = dict(
    content=(
        h2("Why Error Handling Matters in Data Work")
        + p("Real-world data is <b>messy and unpredictable</b>. CSV files have missing values. APIs return unexpected formats. Files are missing. Network connections drop. Without proper error handling, your script crashes on the first bad row and you lose all progress.")
        + p("Error handling lets you <b>gracefully deal with problems</b>: log the error, skip the bad record, retry, or provide a fallback value — all without crashing.")
        + h2("Python Exceptions: try / except / else / finally")
        + bq(c("try") + ":<br>&nbsp;&nbsp;&nbsp;&nbsp;<em># code that might fail</em><br>"
             + c("except") + " SpecificError " + c("as") + " e:<br>&nbsp;&nbsp;&nbsp;&nbsp;<em># handle the error</em><br>"
             + c("else") + ":<br>&nbsp;&nbsp;&nbsp;&nbsp;<em># runs only if NO exception occurred</em><br>"
             + c("finally") + ":<br>&nbsp;&nbsp;&nbsp;&nbsp;<em># ALWAYS runs (cleanup, close file)</em>")
        + h2("Common Exception Types")
        + tbl(
            ["Exception", "When It Occurs", "Example"],
            [
                [c("ValueError"), "Invalid value for a type", c("int('hello')")],
                [c("KeyError"), "Missing dictionary key", c("d['missing_key']")],
                [c("IndexError"), "List index out of range", c("lst[999]") + " on short list"],
                [c("FileNotFoundError"), "File does not exist", c("open('missing.csv')")],
                [c("ZeroDivisionError"), "Division by zero", c("10 / 0")],
                [c("TypeError"), "Wrong data type for operation", c('"hello" + 5")'),],
                [c("AttributeError"), "Object has no such attribute", c("None.split()")],
            ]
        )
        + h2("File Handling with 'with'")
        + p("Always use the " + c("with") + " statement when opening files. It acts as a context manager and <b>automatically closes the file</b> even if an error occurs — preventing resource leaks.")
        + bq(c("with open('data.csv', 'r', encoding='utf-8') as f:") + "<br>&nbsp;&nbsp;&nbsp;&nbsp;<em># file is automatically closed when block exits</em>")
        + h2("File Modes")
        + tbl(
            ["Mode", "Purpose", "Creates if Missing?"],
            [
                [c('"r"'), "Read (default)", "No — raises FileNotFoundError"],
                [c('"w"'), "Write (overwrites file)", "Yes"],
                [c('"a"'), "Append (adds to end)", "Yes"],
                [c('"r+"'), "Read + Write", "No"],
                [c('"rb"'), "Read binary (images, PDFs)", "No"],
            ]
        )
        + h2("Logging Instead of Printing")
        + p("In production code, use Python's built-in " + c("logging") + " module instead of " + c("print()") + ". It supports levels (DEBUG, INFO, WARNING, ERROR), writes to files, and can be enabled/disabled without changing code.")
        + tip("Write a robust data loader: catch errors on each row, log bad rows to a separate error file, and continue processing valid rows. This is production-quality ETL code.")
        + warn("Never use a bare " + c("except:") + " clause. Always specify the exception type. A bare except catches everything including " + c("KeyboardInterrupt") + " and " + c("SystemExit") + ", making your program impossible to stop.")
    ),
    code_example=(
        'import csv\n'
        'import json\n'
        'import os\n'
        'from pathlib import Path\n'
        '\n'
        '# ── Robust type conversion with error handling ──\n'
        'raw_data = ["100", "250", "N/A", "375", "???", "480", "", "200"]\n'
        '\n'
        'clean_data = []\n'
        'errors = []\n'
        '\n'
        'for i, val in enumerate(raw_data):\n'
        '    try:\n'
        '        num = float(val)\n'
        '        if num < 0:\n'
        '            raise ValueError(f"Negative value not allowed: {num}")\n'
        '        clean_data.append(num)\n'
        '    except ValueError as e:\n'
        '        errors.append({"index": i, "value": repr(val), "error": str(e)})\n'
        '        print(f"  [SKIP] Row {i}: {e}")\n'
        '\n'
        'print(f"\\nClean data ({len(clean_data)} rows): {clean_data}")\n'
        'print(f"Errors     ({len(errors)} rows): {errors}")\n'
        'if clean_data:\n'
        '    print(f"Average: {sum(clean_data)/len(clean_data):.1f}")\n'
        '\n'
        '# ── Write & read CSV ──\n'
        'students = [\n'
        '    ["Name","Score","Grade"],\n'
        '    ["Priya", 92, "A"],\n'
        '    ["Raj",   78, "B"],\n'
        '    ["Neha",  63, "C"],\n'
        ']\n'
        '\n'
        'csv_path = "students.csv"\n'
        'with open(csv_path, "w", newline="", encoding="utf-8") as f:\n'
        '    writer = csv.writer(f)\n'
        '    writer.writerows(students)\n'
        'print(f"\\nWrote {len(students)-1} records to {csv_path}")\n'
        '\n'
        '# Read back with DictReader\n'
        'print("\\nStudent Report:")\n'
        'print(f"  {"Name":<10} {"Score":>6} {"Grade":>6}")\n'
        'with open(csv_path, encoding="utf-8") as f:\n'
        '    for row in csv.DictReader(f):\n'
        '        print(f"  {row[\'Name\']:<10} {row[\'Score\']:>6} {row[\'Grade\']:>6}")\n'
        '\n'
        '# ── Save errors to JSON ──\n'
        'with open("errors.json", "w") as f:\n'
        '    json.dump(errors, f, indent=2)\n'
        'print("\\nErrors saved to errors.json")\n'
        '\n'
        '# Cleanup\n'
        'for f in ["students.csv", "errors.json"]:\n'
        '    Path(f).unlink(missing_ok=True)'
    ),
    try_it_note="Add validation: reject values above 1000 (raising a ValueError). Log rejected values to a separate 'outliers' list."
)

RICH['List Comprehensions & Generators'] = dict(
    content=(
        h2("List Comprehensions — Pythonic Data Transformation")
        + p("A <b>list comprehension</b> is a concise syntax for creating a new list by transforming or filtering an existing iterable. It replaces the verbose pattern of creating an empty list and appending in a loop.")
        + bq(c("[expression") + " &nbsp; " + c("for item in iterable") + " &nbsp; " + c("if condition]"))
        + p("The " + c("if condition") + " part is optional. If present, only items satisfying the condition are included.")
        + tbl(
            ["Pattern", "Example", "Result"],
            [
                ["Transform all", c("[x**2 for x in range(5)]"), "[0, 1, 4, 9, 16]"],
                ["Filter", c("[x for x in data if x > 0]"), "Only positive values"],
                ["Transform + Filter", c("[x*2 for x in data if x%2==0]"), "Double only even numbers"],
                ["Nested", c("[[i*j for j in range(3)] for i in range(3)]"), "3×3 matrix"],
            ]
        )
        + h2("Dictionary & Set Comprehensions")
        + tbl(
            ["Type", "Syntax", "Example"],
            [
                [b("Dict"), c("{k: v for k, v in pairs}"), c("{name: score for name, score in zip(names, scores)}")],
                [b("Set"), c("{expr for item in iterable}"), c("{len(word) for word in words}")],
            ]
        )
        + h2("Generators — Lazy Computation for Large Data")
        + p("A <b>generator</b> is like a list comprehension, but instead of building the entire list in memory at once, it <b>produces values one at a time on demand</b>. This is critical for large datasets that don't fit in RAM.")
        + tbl(
            ["Feature", "List Comprehension", "Generator"],
            [
                ["Memory", "Loads entire list into RAM", "Only one item in memory at a time"],
                ["Speed (first value)", "Slower — builds all values first", "Instant — yields first value immediately"],
                ["Reusable?", "Yes — can iterate multiple times", "No — exhausted after one pass"],
                ["Syntax", c("[x for x in range(n)]"), c("(x for x in range(n))")],
                ["Create with function", "List + append", c("yield") + " keyword in function"],
            ]
        )
        + h2("Generator Functions with yield")
        + p("Any function containing " + c("yield") + " is a generator function. Each call to " + c("next()") + " on the generator runs the function until the next " + c("yield") + " and suspends there.")
        + tip("Use generators for: reading large CSV files line-by-line, database cursor results, streaming API responses, processing data in chunks. Rule of thumb: if data > available RAM, use a generator.")
        + warn("Once a generator is exhausted, you cannot iterate it again. Assign to a new generator variable if you need to iterate multiple times.")
        + note(c("sum()") + ", " + c("max()") + ", " + c("min()") + ", " + c("any()") + ", " + c("all()") + " all accept generators directly — no need to convert to list: " + c("sum(x**2 for x in data)"))
    ),
    code_example=(
        '# ── List Comprehensions ──\n'
        'scores = [88, 45, 72, 91, 60, 38, 95, 67, 54, 83]\n'
        '\n'
        '# Basic transformation\n'
        'rounded = [round(s / 10) * 10 for s in scores]   # round to nearest 10\n'
        'print("Rounded:", rounded)\n'
        '\n'
        '# Filter + transform in one line\n'
        'avg = sum(scores) / len(scores)\n'
        'above_avg = [s for s in scores if s > avg]\n'
        'print(f"Above avg ({avg:.1f}): {above_avg}")\n'
        '\n'
        '# Nested comprehension: multiplication table\n'
        'table = [[i * j for j in range(1, 6)] for i in range(1, 6)]\n'
        'for row in table: print(row)\n'
        '\n'
        '# ── Dictionary Comprehension ──\n'
        'names = ["Priya", "Raj", "Neha", "Arjun", "Meera"]\n'
        'score_map = {name: score for name, score in zip(names, scores[:5])}\n'
        'grade_map = {name: ("A" if s>=90 else "B" if s>=75 else "C" if s>=60 else "F")\n'
        '             for name, s in score_map.items()}\n'
        'print("\\nGrades:", grade_map)\n'
        '\n'
        '# ── Set Comprehension ──\n'
        'words = ["apple", "banana", "cherry", "avocado", "blueberry"]\n'
        'first_letters = {w[0] for w in words}\n'
        'print("First letters:", first_letters)  # {a, b, c}\n'
        '\n'
        '# ── Generator Function ──\n'
        'def rolling_average(data, window=3):\n'
        '    """Yields a rolling average — memory efficient."""\n'
        '    for i in range(len(data) - window + 1):\n'
        '        yield sum(data[i:i+window]) / window\n'
        '\n'
        'print("\\nRolling avg (window=3):")\n'
        'for avg in rolling_average(scores):\n'
        '    print(f"  {avg:.1f}", end="  ")\n'
        '\n'
        '# ── Generator expression vs list ──\n'
        'import sys\n'
        'n = 100_000\n'
        'list_comp = [x**2 for x in range(n)]\n'
        'gen_expr  = (x**2 for x in range(n))\n'
        'print(f"\\n\\nList size: {sys.getsizeof(list_comp):,} bytes")\n'
        'print(f"Generator: {sys.getsizeof(gen_expr):,} bytes")  # tiny!'
    ),
    try_it_note="Write a generator function 'chunk_data(data, size)' that yields the data list in chunks of 'size'. Test it with chunk_data(scores, 3)."
)

RICH['Loading & Exploring Data'] = dict(
    content=(
        h2("Loading Data with Pandas")
        + p("<b>Pandas</b> is the most important Python library for data analytics. Its two main data structures — " + c("Series") + " (1D) and " + c("DataFrame") + " (2D table) — make reading, exploring, and transforming data intuitive and fast.")
        + h2("Reading Different File Formats")
        + tbl(
            ["Function", "Format", "Key Parameters"],
            [
                [c("pd.read_csv()"), "CSV, TSV, plain text", c("sep, header, index_col, usecols, dtype, parse_dates, na_values, encoding")],
                [c("pd.read_excel()"), "Excel (.xlsx, .xls)", c("sheet_name, header, usecols, skiprows")],
                [c("pd.read_json()"), "JSON objects / arrays", c("orient, lines, dtype")],
                [c("pd.read_sql()"), "SQL database query", c("sql, con, index_col, parse_dates")],
                [c("pd.read_parquet()"), "Parquet (columnar, fast)", c("columns, engine")],
                [c("pd.read_html()"), "HTML tables on a webpage", c("match, header, index_col")],
            ]
        )
        + h2("First Steps After Loading — Exploration Checklist")
        + ol(
            c("df.shape") + " — (rows, columns)",
            c("df.head(10)") + " — view first 10 rows",
            c("df.dtypes") + " — column data types",
            c("df.info()") + " — non-null counts + memory usage",
            c("df.describe()") + " — summary stats for numeric columns",
            c("df.isnull().sum()") + " — count missing values per column",
            c("df.duplicated().sum()") + " — count duplicate rows",
            c("df['col'].value_counts()") + " — frequency of each unique value",
        )
        + h2("Understanding DataFrame Columns")
        + tbl(
            ["Operation", "Code", "Result"],
            [
                ["Select one column", c("df['Name']"), "Returns a Series"],
                ["Select multiple columns", c("df[['Name', 'Score']]"), "Returns a DataFrame"],
                ["Rename columns", c("df.rename(columns={'old': 'new'})"), "New DataFrame with renamed columns"],
                ["Change dtype", c("df['Score'] = df['Score'].astype(float)"), "Convert column to float"],
                ["New computed column", c("df['Grade'] = df['Score'] / 10"), "Add derived column"],
            ]
        )
        + h2("Handling Missing Values — Quick Reference")
        + tbl(
            ["Action", "Code"],
            [
                ["Count missing per column", c("df.isnull().sum()")],
                ["Drop rows with any missing", c("df.dropna()")],
                ["Drop columns with >50% missing", c("df.dropna(axis=1, thresh=len(df)*0.5)")],
                ["Fill with mean", c("df['col'].fillna(df['col'].mean())")],
                ["Fill with forward fill", c("df.fillna(method='ffill')")],
            ]
        )
        + tip("Always run " + c("df.info()") + " immediately after loading. It shows memory usage, missing values, and wrong data types all at once — the three biggest data quality issues.")
        + warn("Never assume a CSV is clean. Always check dtypes — date columns often load as " + c("object") + " (string), numeric columns as " + c("object") + " if they contain mixed text/numbers. Fix these before analysis.")
    ),
    code_example=(
        'import pandas as pd\n'
        'import numpy as np\n'
        '\n'
        '# ── Create a realistic messy dataset ──\n'
        'data = {\n'
        '    "Name":   ["Priya","Raj","Neha","Arjun","Meera","Dev", "Sanya","Kabir"],\n'
        '    "Score":  [92, 78, None, 91, 63, 85, None, 74],\n'
        '    "City":   ["Mumbai","Delhi","Mumbai","Chennai","Delhi","Pune","Mumbai",None],\n'
        '    "Domain": ["DA","ML","DA","WebDev","ML","DA","WebDev","DA"],\n'
        '    "Joined": ["2024-01-10","2024-02-05","2024-01-10","2024-03-01",\n'
        '               "2024-02-05","2024-01-15","2024-03-10","2024-02-20"],\n'
        '}\n'
        'df = pd.DataFrame(data)\n'
        '\n'
        '# ── Basic exploration ──\n'
        'print("Shape:", df.shape)\n'
        'print("\\nData Types:\\n", df.dtypes)\n'
        'print("\\nMissing Values:\\n", df.isnull().sum())\n'
        '\n'
        '# ── Fix data types ──\n'
        'df["Joined"] = pd.to_datetime(df["Joined"])\n'
        'df["Score"]  = pd.to_numeric(df["Score"])  # already float but ensure\n'
        '\n'
        '# ── Fill missing values ──\n'
        'df["Score"].fillna(df["Score"].mean(), inplace=True)\n'
        'df["City"].fillna("Unknown", inplace=True)\n'
        '\n'
        '# ── Add computed columns ──\n'
        'df["Grade"] = df["Score"].apply(\n'
        '    lambda s: "A" if s>=90 else "B" if s>=75 else "C" if s>=60 else "F"\n'
        ')\n'
        'df["Days_Since"] = (pd.Timestamp.today() - df["Joined"]).dt.days\n'
        '\n'
        'print("\\nCleaned DataFrame:")\n'
        'print(df.to_string(index=False))\n'
        '\n'
        '# ── Quick stats ──\n'
        'print("\\nDescriptive Statistics:")\n'
        'print(df[["Score","Days_Since"]].describe().round(1))\n'
        '\n'
        '# ── Value counts ──\n'
        'print("\\nStudents by Domain:")\n'
        'print(df["Domain"].value_counts())\n'
        'print("\\nStudents by City:")\n'
        'print(df["City"].value_counts())'
    ),
    try_it_note="Add a 'Salary' column with some None values. Fill nulls using the median. Then add a boolean column 'High_Earner' for salaries above median."
)

RICH['Data Cleaning'] = dict(
    content=(
        h2("What is Data Cleaning?")
        + p("<b>Data cleaning</b> (also called data wrangling or munging) is the process of detecting and correcting corrupt, inaccurate, or irrelevant records in a dataset. It is typically the <b>most time-consuming step</b> in any data analytics project — often 60–80% of total effort.")
        + p("Clean data leads to reliable insights. Dirty data leads to wrong conclusions — even with perfect analysis methods.")
        + h2("The Six Most Common Data Quality Problems")
        + tbl(
            ["Problem", "Example", "How to Detect", "How to Fix"],
            [
                [b("Missing values"), "Age = NaN", c("df.isnull().sum()"), "Drop, fill with mean/median/mode, or flag"],
                [b("Duplicates"), "Same row appears twice", c("df.duplicated().sum()"), c("df.drop_duplicates()")],
                [b("Wrong data type"), "Date stored as string", c("df.dtypes"), c("pd.to_datetime(), astype()")],
                [b("Inconsistent values"), '"Mumbai" vs "mumbai"', c("df['city'].unique()"), c(".str.lower().str.strip()")],
                [b("Outliers"), "Age = 999", c("df.describe(), boxplot"), "Cap, remove, or investigate"],
                [b("Structural errors"), "Extra spaces, typos", c("value_counts()"), "Regex replace, map/replace"],
            ]
        )
        + h2("Handling Missing Data Strategies")
        + tbl(
            ["Strategy", "When to Use", "Code"],
            [
                [b("Drop rows"), "Few missing, MCAR (missing completely at random)", c("df.dropna(subset=['col'])")],
                [b("Fill mean"), "Numeric, roughly normally distributed", c("df['col'].fillna(df['col'].mean())")],
                [b("Fill median"), "Numeric, skewed or with outliers", c("df['col'].fillna(df['col'].median())")],
                [b("Fill mode"), "Categorical column", c("df['col'].fillna(df['col'].mode()[0])")],
                [b("Forward fill"), "Time series — use previous value", c("df.fillna(method='ffill')")],
                [b("Flag it"), "Missing is meaningful information", c("df['col_missing'] = df['col'].isnull().astype(int)")],
            ]
        )
        + h2("Detecting Outliers")
        + p("Outliers are data points far outside the normal range. They can be genuine anomalies (fraud, errors) or legitimate extreme values (celebrity wealth in income data).")
        + ul(
            b("IQR Method: ") + "Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR — flag/remove outside this range",
            b("Z-score: ") + "|z| > 3 flags values more than 3 standard deviations from mean",
            b("Domain knowledge: ") + "Age > 120, salary < 0 — clearly impossible values",
        )
        + h2("String Cleaning Operations")
        + tbl(
            ["Operation", "Code", "Example"],
            [
                ["Lowercase", c("s.str.lower()"), '"MUMBAI" → "mumbai"'],
                ["Strip whitespace", c("s.str.strip()"), '"  Alice  " → "Alice"'],
                ["Replace substring", c('s.str.replace("Ltd","Limited")'), "Company name cleanup"],
                ["Extract pattern", c('s.str.extract(r"(\\d+)")'), "Extract numbers from text"],
                ["Split column", c('s.str.split(",", expand=True)'), "Split into multiple columns"],
            ]
        )
        + tip("After every cleaning step, check " + c("df.shape") + " and " + c("df.isnull().sum()") + ". Track how many rows you lose at each step. If you lose >20% of data, reconsider your strategy.")
    ),
    code_example=(
        'import pandas as pd\n'
        'import numpy as np\n'
        '\n'
        '# ── Create dirty dataset ──\n'
        'dirty = pd.DataFrame({\n'
        '    "Name":   ["Alice ","BOB","  Carol","alice","Dave","Dave","Eve"],\n'
        '    "Age":    [25, 30, None, 25, 999, 30, 28],\n'
        '    "City":   ["Mumbai","DELHI","Mumbai","Mumbai","Delhi","Delhi","pune"],\n'
        '    "Score":  [88, 72, 65, 88, 91, 72, None],\n'
        '    "Salary": [50000, 62000, None, 50000, 75000, 62000, 48000],\n'
        '})\n'
        '\n'
        'print("BEFORE CLEANING:")\n'
        'print(dirty.to_string(index=False))\n'
        'print(f"\\nShape: {dirty.shape} | Missing: {dirty.isnull().sum().sum()} | Dupes: {dirty.duplicated().sum()}")\n'
        '\n'
        'df = dirty.copy()\n'
        '\n'
        '# ── 1. Clean string columns ──\n'
        'df["Name"] = df["Name"].str.strip().str.title()\n'
        'df["City"] = df["City"].str.strip().str.title()\n'
        '\n'
        '# ── 2. Remove duplicates ──\n'
        'before = len(df)\n'
        'df.drop_duplicates(inplace=True)\n'
        'print(f"\\nRemoved {before - len(df)} duplicate row(s)")\n'
        '\n'
        '# ── 3. Fix outliers (Age = 999 is impossible) ──\n'
        'df["Age"] = df["Age"].apply(lambda x: np.nan if x and x > 100 else x)\n'
        '\n'
        '# ── 4. Fill missing values ──\n'
        'df["Age"].fillna(df["Age"].median(), inplace=True)\n'
        'df["Score"].fillna(df["Score"].mean(), inplace=True)\n'
        'df["Salary"].fillna(df["Salary"].median(), inplace=True)\n'
        '\n'
        '# ── 5. Detect remaining outliers with IQR ──\n'
        'Q1, Q3 = df["Salary"].quantile([0.25, 0.75])\n'
        'IQR = Q3 - Q1\n'
        'outliers = df[(df["Salary"] < Q1 - 1.5*IQR) | (df["Salary"] > Q3 + 1.5*IQR)]\n'
        'print(f"Salary outliers: {len(outliers)}")\n'
        '\n'
        'print("\\nAFTER CLEANING:")\n'
        'print(df.to_string(index=False))\n'
        'print(f"\\nFinal shape: {df.shape} | Missing: {df.isnull().sum().sum()}")'
    ),
    try_it_note="Add a 'Phone' column with values like '+91-9876543210', '9876543210', '98-765-43210'. Write code to normalize all phone numbers to 10-digit format."
)

RICH['SELECT, WHERE & ORDER BY'] = dict(
    content=(
        h2("SQL: The Language of Data")
        + p("<b>SQL (Structured Query Language)</b> is the universal language for querying relational databases. Every data analyst, data scientist, and backend developer uses SQL daily. It is impossible to work with data at scale without it.")
        + p("SQL is <b>declarative</b> — you describe WHAT data you want, not HOW to get it. The database engine figures out the most efficient way to retrieve it.")
        + h2("The Basic SELECT Statement")
        + bq(c("SELECT") + " column1, column2<br>"
             + c("FROM") + " table_name<br>"
             + c("WHERE") + " condition<br>"
             + c("ORDER BY") + " column [ASC|DESC]<br>"
             + c("LIMIT") + " n;")
        + h2("SELECT — Choosing Columns")
        + tbl(
            ["Syntax", "What it Does", "Example"],
            [
                [c("SELECT *"), "All columns (avoid in production)", c("SELECT * FROM students")],
                [c("SELECT col1, col2"), "Specific columns only", c("SELECT name, score FROM students")],
                [c("SELECT col AS alias"), "Rename column in output", c("SELECT score AS marks FROM students")],
                [c("SELECT DISTINCT col"), "Unique values only", c("SELECT DISTINCT city FROM students")],
                [c("SELECT 1+1"), "Compute expression", c("SELECT price * 1.18 AS price_with_gst")],
            ]
        )
        + h2("WHERE — Filtering Rows")
        + p("The WHERE clause filters rows BEFORE any aggregation. Think of it as Python's " + c("if condition") + ".")
        + tbl(
            ["Operator", "Example", "Meaning"],
            [
                [c("="), c("WHERE status = 'Active'"), "Exact match"],
                [c("!=") + " or " + c("<>"), c("WHERE city != 'Delhi'"), "Not equal"],
                [c(">") + ", " + c(">="), c("WHERE score >= 75"), "Comparison"],
                [c("BETWEEN"), c("WHERE age BETWEEN 20 AND 30"), "Inclusive range"],
                [c("IN (...)"), c("WHERE city IN ('Mumbai','Pune')"), "Match any in list"],
                [c("NOT IN"), c("WHERE domain NOT IN ('HR','Admin')"), "Exclude list"],
                [c("LIKE"), c("WHERE name LIKE 'A%'"), "Pattern match (% = wildcard)"],
                [c("IS NULL"), c("WHERE phone IS NULL"), "Missing value check"],
                [c("IS NOT NULL"), c("WHERE email IS NOT NULL"), "Non-null check"],
                [c("AND"), c("WHERE score > 75 AND city = 'Mumbai'"), "Both conditions must be true"],
                [c("OR"), c("WHERE city = 'Mumbai' OR city = 'Pune'"), "Either condition true"],
                [c("NOT"), c("WHERE NOT is_paid"), "Negate condition"],
            ]
        )
        + h2("ORDER BY — Sorting Results")
        + ul(
            c("ORDER BY score DESC") + " — highest score first",
            c("ORDER BY name ASC") + " — alphabetical (default is ASC)",
            c("ORDER BY city ASC, score DESC") + " — sort by city, then by score within city",
        )
        + h2("LIMIT & OFFSET — Pagination")
        + ul(
            c("LIMIT 10") + " — return only the first 10 rows",
            c("LIMIT 10 OFFSET 20") + " — skip first 20, return next 10 (page 3)",
        )
        + tip("Always use specific column names instead of " + c("SELECT *") + " in production queries. It's more readable, faster (less data transferred), and prevents bugs when table structure changes.")
        + note("SQL keywords are case-insensitive (" + c("SELECT") + " = " + c("select") + ") but by convention, keywords are UPPERCASE and column/table names are lowercase. Consistent formatting makes SQL readable.")
    ),
    code_example=(
        '-- ══════════════════════════════════════\n'
        '-- SQL Examples: SELECT, WHERE, ORDER BY\n'
        '-- (using SQLite / standard SQL syntax)\n'
        '-- ══════════════════════════════════════\n'
        '\n'
        '-- Create and populate a sample table\n'
        'CREATE TABLE IF NOT EXISTS students (\n'
        '    id      INTEGER PRIMARY KEY,\n'
        '    name    TEXT NOT NULL,\n'
        '    score   REAL,\n'
        '    city    TEXT,\n'
        '    domain  TEXT,\n'
        '    is_paid INTEGER DEFAULT 0\n'
        ');\n'
        '\n'
        "INSERT INTO students VALUES\n"
        "(1,'Priya',  92,'Mumbai','Data Analytics',1),\n"
        "(2,'Raj',    78,'Delhi', 'Machine Learning',1),\n"
        "(3,'Neha',   65,'Mumbai','Web Development',0),\n"
        "(4,'Arjun',  91,'Chennai','Data Analytics',1),\n"
        "(5,'Meera',  NULL,'Delhi','Machine Learning',0),\n"
        "(6,'Dev',    85,'Pune', 'Data Analytics',1),\n"
        "(7,'Sanya',  55,'Mumbai','Web Development',0);\n"
        '\n'
        '-- 1. All students\n'
        'SELECT id, name, score, city FROM students;\n'
        '\n'
        '-- 2. Only paid students above 75 score\n'
        'SELECT name, score, domain\n'
        'FROM students\n'
        'WHERE is_paid = 1 AND score >= 75\n'
        'ORDER BY score DESC;\n'
        '\n'
        '-- 3. Students from Mumbai or Pune\n'
        'SELECT name, city, score\n'
        'FROM students\n'
        "WHERE city IN ('Mumbai', 'Pune')\n"
        'ORDER BY city, score DESC;\n'
        '\n'
        '-- 4. Find missing scores\n'
        'SELECT name, city FROM students WHERE score IS NULL;\n'
        '\n'
        "-- 5. Names starting with letter 'P' or 'R'\n"
        'SELECT name, score\n'
        'FROM students\n'
        "WHERE name LIKE 'P%' OR name LIKE 'R%';\n"
        '\n'
        '-- 6. Top 3 scorers\n'
        'SELECT name, score\n'
        'FROM students\n'
        'WHERE score IS NOT NULL\n'
        'ORDER BY score DESC\n'
        'LIMIT 3;'
    ),
    try_it_note="Write a query to find all students from Delhi who are unpaid (is_paid = 0) and have a score above 70, ordered by name alphabetically."
)

RICH['GROUP BY & Aggregate Functions'] = dict(
    content=(
        h2("Aggregating Data with GROUP BY")
        + p("<b>GROUP BY</b> is one of the most powerful SQL clauses. It groups rows that share the same values in specified columns, and then applies an <b>aggregate function</b> to compute a single result for each group.")
        + p("This is equivalent to Pandas " + c("groupby()") + " or Excel pivot tables. Every analytics report involves aggregation.")
        + h2("Aggregate Functions")
        + tbl(
            ["Function", "What it Computes", "Example"],
            [
                [c("COUNT(*)"), "Count all rows in group", c("COUNT(*) as total_students")],
                [c("COUNT(col)"), "Count non-NULL values", c("COUNT(score) as scored_count")],
                [c("COUNT(DISTINCT col)"), "Count unique values", c("COUNT(DISTINCT city) as cities")],
                [c("SUM(col)"), "Total of column", c("SUM(salary) as total_payroll")],
                [c("AVG(col)"), "Average of column", c("AVG(score) as avg_score")],
                [c("MIN(col)"), "Minimum value", c("MIN(price) as cheapest")],
                [c("MAX(col)"), "Maximum value", c("MAX(score) as top_score")],
            ]
        )
        + h2("GROUP BY Syntax & Rules")
        + bq(c("SELECT") + " group_column, " + c("AGG_FUNC") + "(value_column) AS alias<br>"
             + c("FROM") + " table<br>"
             + c("WHERE") + " filter_before_grouping<br>"
             + c("GROUP BY") + " group_column<br>"
             + c("HAVING") + " aggregate_condition<br>"
             + c("ORDER BY") + " alias DESC;")
        + h2("WHERE vs HAVING — A Critical Distinction")
        + tbl(
            ["Clause", "Filters", "Applied When", "Can use aggregates?"],
            [
                [c("WHERE"), "Individual rows", "BEFORE grouping", "NO"],
                [c("HAVING"), "Groups/aggregated values", "AFTER grouping", "YES"],
            ]
        )
        + p("Example: Find cities where the average score is above 80:")
        + bq(c("SELECT city, AVG(score) AS avg_score") + "<br>"
             + c("FROM students") + "<br>"
             + c("GROUP BY city") + "<br>"
             + c("HAVING AVG(score) > 80;"))
        + h2("ORDER OF SQL EXECUTION")
        + ol(
            c("FROM") + " — identify the table",
            c("WHERE") + " — filter rows",
            c("GROUP BY") + " — group matching rows",
            c("HAVING") + " — filter groups",
            c("SELECT") + " — compute output columns",
            c("ORDER BY") + " — sort results",
            c("LIMIT") + " — restrict number of rows returned",
        )
        + warn("This execution order explains why you CANNOT use a SELECT alias in a WHERE clause — WHERE runs before SELECT. But you CAN use aliases in ORDER BY — it runs last.")
        + tip("Use " + c("ROUND(AVG(score), 2)") + " to make aggregate results readable. Bare averages like " + c("82.66666666667") + " in a report look unprofessional.")
    ),
    code_example=(
        '-- ══════════════════════════════════════\n'
        '-- GROUP BY, HAVING & Aggregate Functions\n'
        '-- ══════════════════════════════════════\n'
        '\n'
        '-- 1. Count students per domain\n'
        'SELECT\n'
        '    domain,\n'
        '    COUNT(*) AS total_students,\n'
        '    COUNT(score) AS students_with_score,\n'
        '    ROUND(AVG(score), 1) AS avg_score,\n'
        '    MAX(score) AS top_score,\n'
        '    MIN(score) AS lowest_score\n'
        'FROM students\n'
        'GROUP BY domain\n'
        'ORDER BY avg_score DESC;\n'
        '\n'
        '-- 2. City-level analysis\n'
        'SELECT\n'
        '    city,\n'
        '    COUNT(*) AS students,\n'
        '    SUM(is_paid) AS paid_count,\n'
        '    ROUND(100.0 * SUM(is_paid) / COUNT(*), 1) AS paid_pct\n'
        'FROM students\n'
        'GROUP BY city\n'
        'ORDER BY students DESC;\n'
        '\n'
        '-- 3. HAVING: only domains with 2+ students AND avg score > 75\n'
        'SELECT\n'
        '    domain,\n'
        '    COUNT(*) AS n,\n'
        '    ROUND(AVG(score), 1) AS avg_score\n'
        'FROM students\n'
        'WHERE score IS NOT NULL\n'
        'GROUP BY domain\n'
        'HAVING COUNT(*) >= 2 AND AVG(score) > 75\n'
        'ORDER BY avg_score DESC;\n'
        '\n'
        '-- 4. Score distribution by grade bucket\n'
        'SELECT\n'
        '    CASE\n'
        '        WHEN score >= 90 THEN "A"\n'
        '        WHEN score >= 75 THEN "B"\n'
        '        WHEN score >= 60 THEN "C"\n'
        '        ELSE "F"\n'
        '    END AS grade,\n'
        '    COUNT(*) AS count\n'
        'FROM students\n'
        'WHERE score IS NOT NULL\n'
        'GROUP BY grade\n'
        'ORDER BY grade;'
    ),
    try_it_note="Write a query to find the domain with the HIGHEST number of unpaid students. Use GROUP BY, COUNT, and HAVING."
)

RICH['HTML Document Structure'] = dict(content=RICH.get('What is a Neural Network?', {}).get('content', ''), code_example='', try_it_note='')

# Use our earlier HTML content for "HTML Document Structure"
RICH['HTML Document Structure'] = dict(
    content=(
        h2("The HTML Document: Blueprint of Every Web Page")
        + p("Every web page, no matter how complex — from a simple blog to a Netflix dashboard — is ultimately built on HTML. <b>HTML (HyperText Markup Language)</b> provides the skeleton: the structure, semantic meaning, and content hierarchy that browsers and search engines read.")
        + h2("The Required Document Structure")
        + bq(
            c("&lt;!DOCTYPE html&gt;") + " — Declares HTML5 (must be first line, no exceptions)<br>"
            + c("&lt;html lang='en'&gt;") + " — Root element; lang attribute helps screen readers and SEO<br>"
            + c("&lt;head&gt;") + " — Invisible metadata: title, CSS links, charset, viewport, SEO tags<br>"
            + c("&lt;body&gt;") + " — Everything visible on screen goes here"
        )
        + h2("The &lt;head&gt; — Critical Metadata")
        + tbl(
            ["Tag / Attribute", "Purpose", "Example"],
            [
                [c("<meta charset='UTF-8'>"), "Character encoding — must be first in head", "Supports all Unicode characters including Hindi"],
                [c("<meta name='viewport'>"), "Mobile responsiveness — crucial for mobile browsers", c("content='width=device-width, initial-scale=1.0'")],
                [c("<title>"), "Browser tab text + Google search result title", c("<title>Dashboard | TRHvision</title>")],
                [c("<meta name='description'>"), "SEO description shown in Google results (155 chars)", c("content='Learn data analytics with TRHvision'")],
                [c("<link rel='stylesheet'>"), "Link external CSS file", c("href='styles.css'")],
                [c("<script>"), "JavaScript — usually placed at end of body", c("src='app.js' defer")],
            ]
        )
        + h2("Semantic HTML — The Right Way to Structure Content")
        + p("Semantic elements describe their <b>purpose</b>, not just their appearance. Always use semantic tags — they improve SEO, accessibility, and code maintainability.")
        + tbl(
            ["Tag", "Purpose", "Avoid Using"],
            [
                [c("<header>"), "Page or section header with logo/nav", c("<div id='header'>")],
                [c("<nav>"), "Navigation links", c("<div id='nav'>")],
                [c("<main>"), "Primary unique content of the page (only one per page!)", c("<div id='main'>")],
                [c("<section>"), "Thematic group of content with a heading", c("<div class='section'>")],
                [c("<article>"), "Self-contained content (blog post, product card)", c("<div class='article'>")],
                [c("<aside>"), "Related but non-essential content (sidebar)", c("<div id='sidebar'>")],
                [c("<footer>"), "Page/section footer with links, copyright", c("<div id='footer'>")],
            ]
        )
        + h2("HTML Elements: Block vs Inline")
        + tbl(
            ["Type", "Behavior", "Examples"],
            [
                [b("Block"), "Takes full width, starts on a new line", c("div") + ", " + c("p") + ", " + c("h1-h6") + ", " + c("section") + ", " + c("ul") + ", " + c("table")],
                [b("Inline"), "Only takes needed width, flows in text", c("span") + ", " + c("a") + ", " + c("strong") + ", " + c("em") + ", " + c("code") + ", " + c("img")],
            ]
        )
        + tip("Add " + c('<meta name="viewport" content="width=device-width, initial-scale=1.0">') + " to EVERY HTML page you create. Without it, your page will look broken on mobile devices.")
        + warn("Never skip the " + c("<!DOCTYPE html>") + " declaration. Without it, browsers enter 'quirks mode' and render pages inconsistently across different browsers.")
        + note("Use only ONE " + c("<h1>") + " per page — it signals the main topic to search engines. Use " + c("<h2>") + " to " + c("<h6>") + " for subheadings in hierarchical order, never skip levels.")
    ),
    code_example=(
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <!-- Required charset: must be first -->\n'
        '  <meta charset="UTF-8">\n'
        '\n'
        '  <!-- Mobile responsiveness -->\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '\n'
        '  <!-- Browser tab title & SEO -->\n'
        '  <title>Student Dashboard | TRHvision Academy</title>\n'
        '  <meta name="description" content="Track your internship progress,\n'
        '    complete tasks, and download your certificate at TRHvision Academy.">\n'
        '\n'
        '  <!-- External CSS -->\n'
        '  <link rel="stylesheet" href="styles.css">\n'
        '</head>\n'
        '\n'
        '<body>\n'
        '\n'
        '  <!-- HEADER: logo + primary navigation -->\n'
        '  <header>\n'
        '    <img src="logo.png" alt="TRHvision logo" width="120">\n'
        '    <nav aria-label="Main navigation">\n'
        '      <a href="/">Home</a>\n'
        '      <a href="/courses">Courses</a>\n'
        '      <a href="/dashboard" aria-current="page">Dashboard</a>\n'
        '      <a href="/contact">Contact</a>\n'
        '    </nav>\n'
        '  </header>\n'
        '\n'
        '  <!-- MAIN: unique page content -->\n'
        '  <main>\n'
        '    <section aria-labelledby="progress-heading">\n'
        '      <h1 id="progress-heading">Your Progress</h1>\n'
        '      <p>You have completed <strong>7 of 12</strong> tasks.</p>\n'
        '    </section>\n'
        '\n'
        '    <article>\n'
        '      <h2>Latest Task</h2>\n'
        '      <p>Complete the <em>Data Cleaning</em> module by Friday.</p>\n'
        '    </article>\n'
        '\n'
        '    <aside>\n'
        '      <h2>Quick Links</h2>\n'
        '      <ul>\n'
        '        <li><a href="/resources">Study Resources</a></li>\n'
        '        <li><a href="/community">Telegram Community</a></li>\n'
        '      </ul>\n'
        '    </aside>\n'
        '  </main>\n'
        '\n'
        '  <!-- FOOTER -->\n'
        '  <footer>\n'
        '    <p>&copy; 2024 TRHvision Academy. All rights reserved.</p>\n'
        '    <nav aria-label="Footer navigation">\n'
        '      <a href="/privacy">Privacy Policy</a> |\n'
        '      <a href="/terms">Terms of Service</a>\n'
        '    </nav>\n'
        '  </footer>\n'
        '\n'
        '  <!-- JavaScript at end of body for faster page load -->\n'
        '  <script src="app.js" defer></script>\n'
        '</body>\n'
        '</html>'
    ),
    try_it_note="Add a <section> about 'Upcoming Deadlines' with an <ol> listing three deadline items. Use proper semantic HTML throughout."
)

RICH['Selectors, Box Model & Colors'] = dict(
    content=(
        h2("CSS: Giving HTML a Visual Identity")
        + p("<b>CSS (Cascading Style Sheets)</b> controls the visual presentation of HTML elements — colors, fonts, spacing, layout, and animations. Without CSS, websites would look like plain text documents from the 1990s.")
        + p("The word <b>Cascading</b> means styles flow down from parent to child elements (inheritance) and are applied in a specific priority order when multiple rules conflict.")
        + h2("CSS Selectors — Targeting Elements")
        + tbl(
            ["Selector", "What it Targets", "Example", "Specificity"],
            [
                [c("element"), "All elements of that type", c("p { color: red; }"), "Low (0,0,1)"],
                [c(".class"), "All elements with that class", c(".card { border-radius: 8px; }"), "Medium (0,1,0)"],
                [c("#id"), "Single element with that ID", c("#submit-btn { color: white; }"), "High (1,0,0)"],
                [c("element.class"), "Specific element with class", c("p.highlight { ... }"), "Medium"],
                [c("parent > child"), "Direct children only", c(".nav > a { ... }"), "Varies"],
                [c("a:hover"), "Pseudo-class: element state", c("a:hover { color: blue; }"), "Same + state"],
                [c("::before"), "Pseudo-element: virtual child", c('.card::before { content: ""; }'), "Same + element"],
                [c("[attr=value]"), "Attribute selector", c('[type="submit"] { ... }'), "Medium"],
            ]
        )
        + h2("The CSS Box Model — Every Element is a Box")
        + p("Every HTML element is rendered as a rectangular box. Understanding the box model is fundamental to controlling layout and spacing.")
        + bq("Content → Padding → Border → Margin<br><br>"
             + b("Content:") + " The actual text/image inside the element<br>"
             + b("Padding:") + " Space between content and border (inside the element)<br>"
             + b("Border:") + " The visible line surrounding padding<br>"
             + b("Margin:") + " Space outside the border (between elements)")
        + tbl(
            ["Property", "Shorthand Example", "Expanded Form"],
            [
                [c("padding"), c("padding: 10px 20px"), "top-bottom: 10px, left-right: 20px"],
                [c("margin"), c("margin: 0 auto"), "top-bottom: 0, center horizontally"],
                [c("border"), c("border: 2px solid #10b981"), "width style color"],
                [c("border-radius"), c("border-radius: 12px"), "Round all corners"],
                [c("box-sizing"), c("box-sizing: border-box"), "ESSENTIAL: include padding in width"],
            ]
        )
        + h2("Colors in CSS")
        + tbl(
            ["Format", "Syntax", "Example", "Use For"],
            [
                ["Hex", c("#RRGGBB"), c("#10b981"), "Most common, supported everywhere"],
                ["RGB", c("rgb(r, g, b)"), c("rgb(16, 185, 129)"), "When you need to compute values"],
                ["RGBA", c("rgba(r, g, b, a)"), c("rgba(16, 185, 129, 0.3)"), "Transparent overlays, shadows"],
                ["HSL", c("hsl(h, s%, l%)"), c("hsl(160, 84%, 39%)"), "Intuitive: hue, saturation, lightness"],
                ["Named", c("color name"), c("tomato, deepskyblue"), "Quick prototyping only"],
                ["CSS Variable", c("var(--color-name)"), c("var(--green)"), "Design system, theming"],
            ]
        )
        + h2("CSS Specificity — Which Rule Wins?")
        + p("When multiple rules target the same element, the <b>more specific rule wins</b>. Specificity is calculated as (ID count, Class count, Element count):")
        + ul(
            c("!important") + " — highest priority (avoid overusing!)",
            "Inline style " + c('style="..."') + " — 1,0,0,0",
            "ID selector " + c("#id") + " — 0,1,0,0",
            "Class / attribute / pseudo-class " + c(".cls") + " — 0,0,1,0",
            "Element / pseudo-element " + c("p") + " — 0,0,0,1",
        )
        + tip("Use " + c("box-sizing: border-box") + " globally (" + c("* { box-sizing: border-box; }") + "). This makes width behave intuitively — padding is included inside the declared width, not added on top.")
    ),
    code_example=(
        '/* ══════════════════════════════════════\n'
        '   CSS: Selectors, Box Model & Colors\n'
        '   ══════════════════════════════════════ */\n'
        '\n'
        '/* 1. Global reset + box-sizing */\n'
        '*, *::before, *::after {\n'
        '  box-sizing: border-box;\n'
        '  margin: 0;\n'
        '  padding: 0;\n'
        '}\n'
        '\n'
        '/* 2. CSS Custom Properties (variables) */\n'
        ':root {\n'
        '  --color-primary:  #10b981;    /* emerald green */\n'
        '  --color-dark:     #0f172a;\n'
        '  --color-light:    #f8fafc;\n'
        '  --border-radius:  12px;\n'
        '  --shadow:         0 4px 16px rgba(0,0,0,.1);\n'
        '  --font-sans:      \'Inter\', sans-serif;\n'
        '}\n'
        '\n'
        '/* 3. Element selector */\n'
        'body {\n'
        '  font-family: var(--font-sans);\n'
        '  background: var(--color-light);\n'
        '  color: var(--color-dark);\n'
        '  line-height: 1.7;\n'
        '}\n'
        '\n'
        '/* 4. Class selector */\n'
        '.card {\n'
        '  background: white;\n'
        '  border-radius: var(--border-radius);\n'
        '  padding: 1.5rem 2rem;     /* top/bottom | left/right */\n'
        '  margin: 1rem 0;\n'
        '  box-shadow: var(--shadow);\n'
        '  border: 1px solid #e2e8f0;\n'
        '  transition: transform 0.2s ease, box-shadow 0.2s ease;\n'
        '}\n'
        '\n'
        '/* 5. Pseudo-class: hover effect */\n'
        '.card:hover {\n'
        '  transform: translateY(-4px);\n'
        '  box-shadow: 0 8px 30px rgba(16,185,129,.2);\n'
        '}\n'
        '\n'
        '/* 6. Pseudo-element */\n'
        '.card::before {\n'
        '  content: "";\n'
        '  display: block;\n'
        '  height: 4px;\n'
        '  background: linear-gradient(90deg, var(--color-primary), #34d399);\n'
        '  border-radius: var(--border-radius) var(--border-radius) 0 0;\n'
        '  margin: -1.5rem -2rem 1rem; /* pull to card edges */\n'
        '}\n'
        '\n'
        '/* 7. Descendant + attribute selectors */\n'
        '.card h2 { font-size: 1.1rem; font-weight: 700; margin-bottom: .5rem; }\n'
        '.card p  { color: #64748b; font-size: .9rem; }\n'
        '\n'
        'a[href^="https"] { color: var(--color-primary); font-weight: 600; }\n'
        'a[href^="https"]:hover { text-decoration: underline; }\n'
        '\n'
        '/* 8. ID selector (highest specificity) */\n'
        '#submit-btn {\n'
        '  background: var(--color-primary);\n'
        '  color: white;\n'
        '  border: none;\n'
        '  border-radius: 999px;\n'
        '  padding: 10px 28px;\n'
        '  font-weight: 700;\n'
        '  cursor: pointer;\n'
        '}'
    ),
    try_it_note="Add a .badge class with a green background, white text, small padding, and rounded corners. Apply it to a <span> in your HTML."
)

RICH['Variables, Types & Functions'] = dict(
    content=(
        h2("JavaScript: Making Web Pages Interactive")
        + p("<b>JavaScript (JS)</b> is the programming language of the web. While HTML structures content and CSS styles it, JavaScript makes it <b>dynamic and interactive</b> — responding to user clicks, fetching data, animating elements, and much more.")
        + p("Every modern website — Google, Instagram, WhatsApp Web — uses JavaScript extensively. It runs directly in the browser without needing compilation.")
        + h2("Variables: let, const, and var")
        + tbl(
            ["Keyword", "Reassignable?", "Block-Scoped?", "Use When"],
            [
                [c("const"), "No", "Yes", "Default choice — for values that don't change"],
                [c("let"), "Yes", "Yes", "For values that need to be updated"],
                [c("var"), "Yes", "No (function-scoped)", "Avoid — legacy, has confusing scoping bugs"],
            ]
        )
        + h2("JavaScript Data Types")
        + tbl(
            ["Type", "Examples", "typeof Result"],
            [
                [b("Number"), "42, 3.14, -7, Infinity, NaN", c('"number"')],
                [b("String"), '"Hello", \'World\', `Template`', c('"string"')],
                [b("Boolean"), "true, false", c('"boolean"')],
                [b("null"), "null (intentional empty)", c('"object"') + " (historical bug!)"],
                [b("undefined"), "uninitialized variable", c('"undefined"')],
                [b("Object"), "{key: value}", c('"object"')],
                [b("Array"), "[1, 2, 3]", c('"object"')],
                [b("Function"), "function f() {}", c('"function"')],
            ]
        )
        + h2("Template Literals (Modern String Formatting)")
        + p("Use backtick strings for multi-line text and embedded expressions — far cleaner than string concatenation:")
        + bq(c('`Hello, ${name}! Your score is ${score.toFixed(2)}%`'))
        + h2("Functions: Three Syntaxes")
        + tbl(
            ["Style", "Syntax", "Key Feature"],
            [
                [b("Function Declaration"), c("function add(a, b) { return a + b; }"), "Hoisted — can be called before definition"],
                [b("Function Expression"), c("const add = function(a, b) { return a + b; };"), "Not hoisted"],
                [b("Arrow Function"), c("const add = (a, b) => a + b;"), "Concise, inherits outer 'this' — use in callbacks"],
            ]
        )
        + h2("Arrays & Objects")
        + p("Arrays and objects are the core data structures in JavaScript:")
        + ul(
            b("Array: ") + c("const scores = [88, 72, 91, 65]") + " — ordered list, 0-indexed",
            b("Object: ") + c('const student = { name: "Priya", score: 88 }') + " — key-value pairs",
            b("Array methods: ") + c("map(), filter(), reduce(), find(), forEach(), some(), every()"),
        )
        + h2("Truthy & Falsy Values")
        + p("In JavaScript, conditions don't need to be strict " + c("true") + "/" + c("false") + ". These values are always <b>falsy</b>:")
        + bq(c("false") + ", " + c("0") + ", " + c('""') + " (empty string), " + c("null") + ", " + c("undefined") + ", " + c("NaN"))
        + p("Everything else is <b>truthy</b>, including " + c('"0"') + " (non-empty string), " + c("[]") + " (empty array), " + c("{}") + " (empty object).")
        + tip("Use " + c("===") + " (strict equality) instead of " + c("==") + " (loose equality) always. " + c("==") + " does type coercion which leads to unexpected results: " + c('"" == false') + " is " + c("true") + "!")
    ),
    code_example=(
        '// ── Variables ──\n'
        'const PI = 3.14159;       // cannot reassign\n'
        'let counter = 0;          // can reassign\n'
        'counter++;                // now 1\n'
        '\n'
        '// ── Data types ──\n'
        'const student = {\n'
        '    name: "Priya Sharma",\n'
        '    score: 88.5,\n'
        '    domain: "Data Analytics",\n'
        '    isPaid: true,\n'
        '    courses: ["Python", "Pandas", "SQL"],\n'
        '    address: null   // intentionally empty\n'
        '};\n'
        '\n'
        'console.log(typeof student.name);    // "string"\n'
        'console.log(typeof student.score);   // "number"\n'
        'console.log(typeof student.address); // "object" (null quirk)\n'
        '\n'
        '// ── Template literals ──\n'
        'const greeting = `Student: ${student.name}\n'
        'Score:   ${student.score.toFixed(1)}%\n'
        'Status:  ${student.isPaid ? "Paid" : "Unpaid"}`;\n'
        'console.log(greeting);\n'
        '\n'
        '// ── Arrow functions ──\n'
        'const classify = (score) => {\n'
        '    if (score >= 90) return "A";\n'
        '    if (score >= 75) return "B";\n'
        '    if (score >= 60) return "C";\n'
        '    return "F";\n'
        '};\n'
        '\n'
        '// ── Array methods ──\n'
        'const scores = [88, 45, 72, 91, 60, 38, 95];\n'
        '\n'
        'const passing = scores.filter(s => s >= 60);\n'
        'const doubled = scores.map(s => s * 2);\n'
        'const total   = scores.reduce((acc, s) => acc + s, 0);\n'
        'const avg     = total / scores.length;\n'
        '\n'
        'console.log("Passing:", passing);\n'
        'console.log("Average:", avg.toFixed(1));\n'
        'console.log("Has 90+:", scores.some(s => s >= 90));   // true\n'
        'console.log("All pass:", scores.every(s => s >= 60)); // false\n'
        '\n'
        '// ── Destructuring ──\n'
        'const { name, score, courses } = student;\n'
        'const [first, second, ...rest] = courses;\n'
        'console.log(`${name} scored ${score}. Top course: ${first}`);\n'
        'console.log("Other courses:", rest);'
    ),
    try_it_note="Write a function 'gradeReport(students)' that takes an array of objects [{name, score}] and returns a sorted array with grade added to each object."
)

RICH['DOM Manipulation & Events'] = dict(
    content=(
        h2("The DOM: JavaScript's View of the Page")
        + p("The <b>DOM (Document Object Model)</b> is a programming interface that represents the HTML document as a tree of objects. JavaScript uses the DOM to read and modify page content dynamically — without reloading the page.")
        + p("When the browser loads an HTML page, it builds a DOM tree. JavaScript can then select any element in the tree and change its content, styles, attributes, or position.")
        + h2("Selecting Elements")
        + tbl(
            ["Method", "Returns", "Example"],
            [
                [c("document.getElementById('id')"), "Single element", c("document.getElementById('submit-btn')")],
                [c("document.querySelector('.class')"), "First matching element", c("document.querySelector('.card')")],
                [c("document.querySelectorAll('p')"), "NodeList of all matches", c("document.querySelectorAll('.lesson')")],
                [c("element.closest('.parent')"), "Nearest ancestor matching selector", c("btn.closest('.form-wrapper')")],
                [c("element.children"), "HTMLCollection of child elements", c("list.children")],
            ]
        )
        + h2("Modifying Elements")
        + tbl(
            ["Property / Method", "What it Does", "Example"],
            [
                [c("element.textContent"), "Get/set visible text (safe — no HTML)", c("h1.textContent = 'Hello'")],
                [c("element.innerHTML"), "Get/set HTML content (use carefully!)", c("div.innerHTML = '<b>Bold</b>'")],
                [c("element.setAttribute(k, v)"), "Set any HTML attribute", c("img.setAttribute('alt', 'Photo')")],
                [c("element.style.property"), "Set inline CSS style", c("el.style.display = 'none'")],
                [c("element.classList.add('cls')"), "Add CSS class", c("btn.classList.add('active')")],
                [c("element.classList.toggle('cls')"), "Toggle class on/off", c("menu.classList.toggle('open')")],
                [c("element.classList.contains('cls')"), "Check if class exists", c("if (el.classList.contains('error'))")],
            ]
        )
        + h2("Creating & Inserting Elements")
        + ol(
            c("const el = document.createElement('div')") + " — create new element",
            c("el.textContent = 'Hello'") + " — set content",
            c("el.classList.add('card')") + " — add class",
            c("parent.appendChild(el)") + " — add to end of parent",
            c("parent.insertBefore(el, ref)") + " — insert before reference element",
        )
        + h2("Event Handling")
        + p("Events are actions that happen in the browser — clicks, keypresses, form submissions, mouse movements. You attach <b>event listeners</b> to elements to respond when events occur.")
        + tbl(
            ["Event", "Trigger", "Common Use"],
            [
                [c("click"), "User clicks element", "Button actions, toggle menus"],
                [c("submit"), "Form submitted", "Validate and send form data"],
                [c("input"), "Value changes in input", "Live search, character counter"],
                [c("keydown"), "Key pressed", "Keyboard shortcuts"],
                [c("mouseover") + " / " + c("mouseout"), "Mouse enters/leaves", "Hover effects"],
                [c("DOMContentLoaded"), "HTML fully parsed (before images)", "Safe place to run all JS"],
                [c("scroll"), "Page or element scrolled", "Infinite scroll, progress bar"],
            ]
        )
        + h2("Event Delegation — Handle Dynamic Elements")
        + p("Instead of attaching listeners to every child element individually, attach one listener to the parent and use " + c("event.target") + " to identify which child was clicked. This works for dynamically added elements too.")
        + tip("Always use " + c("event.preventDefault()") + " in form submit handlers to stop the default browser behavior (page reload) before running your own JavaScript logic.")
        + warn("Avoid setting " + c("innerHTML") + " with user-provided content — it creates XSS (Cross-Site Scripting) security vulnerabilities. Use " + c("textContent") + " for plain text.")
    ),
    code_example=(
        '// ── 1. Select elements ──\n'
        'const scoreInput  = document.getElementById("score-input");\n'
        'const resultBox   = document.querySelector(".result-box");\n'
        'const historyList = document.querySelector("#history ul");\n'
        '\n'
        '// ── 2. Grade classifier function ──\n'
        'function classify(score) {\n'
        '    if (score >= 90) return { grade: "A", color: "#10b981", msg: "Excellent!" };\n'
        '    if (score >= 75) return { grade: "B", color: "#3b82f6", msg: "Good work!" };\n'
        '    if (score >= 60) return { grade: "C", color: "#f59e0b", msg: "Satisfactory" };\n'
        '    return              { grade: "F", color: "#ef4444", msg: "Needs improvement" };\n'
        '}\n'
        '\n'
        '// ── 3. Handle form submission ──\n'
        'document.getElementById("grade-form").addEventListener("submit", function(e) {\n'
        '    e.preventDefault();  // stop page reload\n'
        '\n'
        '    const score = parseFloat(scoreInput.value);\n'
        '\n'
        '    if (isNaN(score) || score < 0 || score > 100) {\n'
        '        resultBox.textContent = "Please enter a valid score (0-100)";\n'
        '        resultBox.style.color = "red";\n'
        '        return;\n'
        '    }\n'
        '\n'
        '    const { grade, color, msg } = classify(score);\n'
        '\n'
        '    // Update result display\n'
        '    resultBox.innerHTML = `\n'
        '        <span style="font-size:2rem;font-weight:900;color:${color}">${grade}</span>\n'
        '        <span style="color:#64748b">${msg} (${score}%)</span>\n'
        '    `;\n'
        '\n'
        '    // Add to history\n'
        '    const li = document.createElement("li");\n'
        '    li.textContent = `Score: ${score} → Grade: ${grade} — ${msg}`;\n'
        '    li.style.borderLeft = `3px solid ${color}`;\n'
        '    li.style.paddingLeft = "8px";\n'
        '    historyList.prepend(li);  // add to top\n'
        '\n'
        '    scoreInput.value = "";  // clear input\n'
        '});\n'
        '\n'
        '// ── 4. Live character feedback on input ──\n'
        'scoreInput.addEventListener("input", function() {\n'
        '    const val = parseFloat(this.value);\n'
        '    if (this.value === "") return;\n'
        '    this.style.borderColor = (!isNaN(val) && val >= 0 && val <= 100)\n'
        '        ? "#10b981"  // valid: green border\n'
        '        : "#ef4444"; // invalid: red border\n'
        '});\n'
        '\n'
        '// ── 5. Event delegation on history list ──\n'
        'historyList.addEventListener("click", function(e) {\n'
        '    if (e.target.tagName === "LI") {\n'
        '        e.target.remove();  // click a history item to delete it\n'
        '    }\n'
        '});'
    ),
    try_it_note="Add a 'Clear History' button. When clicked, remove all <li> elements from the history list using a single DOM operation."
)

RICH['MVT Architecture & URLs'] = dict(
    content=(
        h2("Django: The Web Framework for Perfectionists")
        + p("<b>Django</b> is Python's most popular web framework. It follows the <b>batteries included</b> philosophy — it comes with authentication, admin panel, ORM, form handling, security, and templating out of the box. You focus on building your app, not reinventing infrastructure.")
        + h2("MVT Architecture")
        + p("Django uses <b>MVT (Model-View-Template)</b>, a variant of the classic MVC pattern:")
        + tbl(
            ["Component", "Role", "File"],
            [
                [b("Model"), "Defines data structure — maps Python classes to database tables", c("models.py")],
                [b("View"), "Business logic — processes requests, queries database, prepares context", c("views.py")],
                [b("Template"), "HTML presentation — renders context variables into the final page", c("templates/*.html")],
                [b("URL Conf"), "Routes incoming URLs to the correct View", c("urls.py")],
            ]
        )
        + h2("The Request-Response Cycle")
        + ol(
            "Browser sends HTTP GET request to " + c("/dashboard/"),
            "Django's URL Dispatcher reads " + c("urls.py") + " and finds the matching pattern",
            "Django calls the associated " + b("View") + " function, passing a " + c("HttpRequest") + " object",
            "View queries " + b("Models") + " via ORM, prepares a context dictionary",
            "View calls " + c("render(request, 'template.html', context)"),
            "Django's template engine fills in the HTML with context data",
            "Django returns an " + c("HttpResponse") + " to the browser",
        )
        + h2("URL Configuration")
        + p("Every URL in your site must be mapped to a view in " + c("urls.py") + ". Django reads these patterns top-to-bottom and calls the first match.")
        + tbl(
            ["Pattern Type", "Example", "What it Matches"],
            [
                ["Static", c("path('about/', views.about)"), "Exactly " + c("/about/")],
                ["With parameter", c("path('student/<int:id>/', views.profile)"), c("/student/42/")],
                ["String param", c("path('search/<str:query>/', views.search)"), c("/search/python/")],
                ["Include", c("path('api/', include('api.urls'))"), "Delegate to another urls.py"],
            ]
        )
        + h2("Writing a View")
        + p("The simplest view takes a " + c("request") + " and returns an " + c("HttpResponse") + ":")
        + bq(c("def dashboard(request):") + "<br>"
             + c('&nbsp;&nbsp;&nbsp;&nbsp;context = {"score": 88}') + "<br>"
             + c('&nbsp;&nbsp;&nbsp;&nbsp;return render(request, "dashboard.html", context)'))
        + h2("Django Settings Essentials")
        + tbl(
            ["Setting", "Purpose"],
            [
                [c("INSTALLED_APPS"), "List of active apps — add yours here"],
                [c("DATABASES"), "Database connection config — default is SQLite"],
                [c("TEMPLATES"), "Template engine settings, directories"],
                [c("STATIC_URL"), "URL prefix for static files (CSS, JS, images)"],
                [c("SECRET_KEY"), "Cryptographic key — NEVER commit to Git!"],
                [c("DEBUG"), "Set to False in production for security"],
                [c("ALLOWED_HOSTS"), "Domains allowed to serve this app"],
            ]
        )
        + tip("Run " + c("python manage.py startapp myapp") + " to create a new app. Then add it to " + c("INSTALLED_APPS") + " in settings.py. Apps group related models, views, and templates.")
        + warn("Never leave " + c("DEBUG = True") + " in production. It exposes stack traces, source code paths, and database queries to any visitor.")
    ),
    code_example=(
        '# ══════════════════════════════════════\n'
        '# Django MVT — Complete Working Example\n'
        '# ══════════════════════════════════════\n'
        '\n'
        '# ─── models.py ───\n'
        'from django.db import models\n'
        'from django.contrib.auth.models import User\n'
        '\n'
        'class Student(models.Model):\n'
        '    user        = models.OneToOneField(User, on_delete=models.CASCADE)\n'
        '    student_id  = models.CharField(max_length=20, unique=True)\n'
        '    domain      = models.CharField(max_length=100)\n'
        '    score       = models.FloatField(default=0)\n'
        '    enrolled_at = models.DateTimeField(auto_now_add=True)\n'
        '    is_paid     = models.BooleanField(default=False)\n'
        '\n'
        '    class Meta:\n'
        '        ordering = ["-enrolled_at"]\n'
        '\n'
        '    def __str__(self):\n'
        '        return f"{self.student_id} — {self.user.get_full_name()}"\n'
        '\n'
        '    @property\n'
        '    def grade(self):\n'
        '        if self.score >= 90: return "A"\n'
        '        if self.score >= 75: return "B"\n'
        '        if self.score >= 60: return "C"\n'
        '        return "F"\n'
        '\n'
        '\n'
        '# ─── urls.py ───\n'
        'from django.urls import path\n'
        'from . import views\n'
        '\n'
        'urlpatterns = [\n'
        '    path("",                        views.home,            name="home"),\n'
        '    path("dashboard/",              views.dashboard,        name="dashboard"),\n'
        '    path("student/<int:pk>/",       views.student_detail,   name="student_detail"),\n'
        '    path("student/<int:pk>/edit/",  views.student_edit,     name="student_edit"),\n'
        '    path("api/scores/",             views.api_scores,       name="api_scores"),\n'
        ']\n'
        '\n'
        '\n'
        '# ─── views.py ───\n'
        'from django.shortcuts import render, get_object_or_404\n'
        'from django.contrib.auth.decorators import login_required\n'
        'from django.http import JsonResponse\n'
        'from .models import Student\n'
        '\n'
        '@login_required(login_url="login")\n'
        'def dashboard(request):\n'
        '    try:\n'
        '        student = request.user.student\n'
        '    except Student.DoesNotExist:\n'
        '        return render(request, "no_profile.html")\n'
        '\n'
        '    # ORM query — top 5 students in same domain\n'
        '    peers = Student.objects.filter(\n'
        '        domain=student.domain\n'
        '    ).order_by("-score")[:5]\n'
        '\n'
        '    context = {\n'
        '        "student": student,\n'
        '        "grade":   student.grade,\n'
        '        "peers":   peers,\n'
        '        "is_top":  student.score == peers.first().score if peers else False,\n'
        '    }\n'
        '    return render(request, "dashboard.html", context)\n'
        '\n'
        '@login_required\n'
        'def api_scores(request):\n'
        '    """JSON endpoint for charts."""\n'
        '    data = list(Student.objects.values("student_id", "score", "domain"))\n'
        '    return JsonResponse({"students": data})'
    ),
    try_it_note="Add a 'Certificate' model linked to Student with a 'issued_at' DateTimeField. Write a view that shows the certificate only if student.score >= 75."
)

# ─── Django Management Command ───────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Enrich all LearningLesson records with detailed GFG-quality content'

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for lesson in LearningLesson.objects.all().select_related('topic'):
            title = lesson.title
            if title in RICH and RICH[title].get('content'):
                data = RICH[title]
                lesson.content      = data['content']
                lesson.code_example = data.get('code_example', lesson.code_example)
                lesson.try_it_note  = data.get('try_it_note', lesson.try_it_note)
                lesson.save(update_fields=['content', 'code_example', 'try_it_note'])
                self.stdout.write(self.style.SUCCESS(f'[OK] {title[:70]}'))
                updated += 1
            else:
                skipped += 1

        self.stdout.write(f'\nDone. Updated {updated}, skipped {skipped} (no matching content).')

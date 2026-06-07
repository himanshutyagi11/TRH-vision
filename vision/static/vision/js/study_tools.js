/* study_tools.js - Interaction Engine for TRHvision Study Tools */

// Build ordered list of all panels: overview → materials → assessment
let panelOrder = [];
let currentIdx = 0;

// Flashcard State
let flashcardsData = {};

// SQL Database Initialization state
let sqlDbInitialized = false;

// Audiobook TTS State
let currentUtterance = null;
let isSpeaking = false;
let speechParagraphs = [];
let currentParaIndex = 0;

// Focus Ruler & Highlights state
let rulerEnabled = false;
let currentSelectionRange = null;
let currentSelectionText = '';
let currentMaterialId = '';

function initNav() {
    panelOrder = Array.from(document.querySelectorAll('.material-panel'))
        .map(p => p.id.replace('panel-', ''));
    showPanel('overview', false);  // start at overview
}

function showPanel(id, scroll = true) {
    // Cancel TTS if speaking
    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        document.querySelectorAll('[id^=btn-tts-]').forEach(btn => {
            btn.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-secondary');
        });
        document.querySelectorAll('.content-card *').forEach(el => el.style.backgroundColor = '');
    }

    // Hide all panels & deactivate all sidebar buttons
    document.querySelectorAll('.material-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.material-btn').forEach(b => b.classList.remove('active'));

    // Activate chosen panel & sidebar button
    const panel = document.getElementById('panel-' + id);
    const btn = document.getElementById('btn-' + id);
    if (panel) panel.classList.add('active');
    if (btn) btn.classList.add('active');

    // Track position
    const idx = panelOrder.indexOf(id);
    if (idx !== -1) currentIdx = idx;

    updateSeqNav();
    
    // If switching to a material panel, prepare details
    if (id.startsWith('mat-')) {
        const matId = id.replace('mat-', '');
        // Auto load notes
        loadNotesList(matId);
        // Trigger playground preparation
        prepareCodePlaygrounds(matId);
        // Trigger active recall targets preparation
        prepareActiveRecall();
    }

    if (scroll) window.scrollTo({ top: 0, behavior: 'smooth' });
}

function navigate(dir) {
    const next = currentIdx + dir;
    if (next >= 0 && next < panelOrder.length) {
        showPanel(panelOrder[next]);
    }
}

function updateSeqNav() {
    const prevBtn = document.getElementById('seq-prev');
    const nextBtn = document.getElementById('seq-next');
    const indicator = document.getElementById('seq-indicator');

    prevBtn.disabled = currentIdx === 0;
    nextBtn.disabled = currentIdx === panelOrder.length - 1;

    // Label indicator
    const total = panelOrder.length;
    const label = panelOrder[currentIdx];
    if (label === 'overview') {
        indicator.textContent = `Overview  ·  ${total - 1} lesson${total - 2 !== 1 ? 's' : ''} ahead`;
    } else if (label === 'assessment') {
        indicator.textContent = `Final Assessment  ·  ${currentIdx} of ${total - 1}`;
    } else {
        indicator.textContent = `Lesson ${currentIdx} of ${total - 2}`;
    }
}

function selectOption(el, inputId) {
    const group = el.closest('.mb-5');
    if (group) {
        group.querySelectorAll('.quiz-option').forEach(opt => {
            opt.style.borderColor = '';
            opt.style.background = '';
            opt.classList.remove('correct', 'incorrect');
        });
    }
    el.style.borderColor = '#0ea5e9';
    el.style.background = 'rgba(14,165,233,0.08)';
    document.getElementById(inputId).checked = true;
}

// ── Check Quiz Question Option ──
function checkQuizQuestion(questionId) {
    const block = document.getElementById('q-block-' + questionId);
    if (!block) return;
    
    const correctOpt = block.getAttribute('data-correct');
    const selectedInput = block.querySelector('input[type="radio"]:checked');
    const feedbackText = document.getElementById('feedback-' + questionId);
    
    if (!selectedInput) {
        feedbackText.innerHTML = "<span class='text-warning'><i class='bi bi-exclamation-triangle'></i> Select an option first!</span>";
        return;
    }
    
    const selectedVal = selectedInput.value;
    
    // Clear previous styles
    block.querySelectorAll('.quiz-option').forEach(opt => {
        opt.classList.remove('correct', 'incorrect');
    });
    
    const selectedBlock = selectedInput.closest('.quiz-option');
    
    if (selectedVal === correctOpt) {
        selectedBlock.classList.add('correct');
        feedbackText.innerHTML = "<span class='text-success'><i class='bi bi-check-circle-fill'></i> Correct! Perfect!</span>";
        // Mini success explosion on correct answer!
        confetti({
            particleCount: 50,
            spread: 40,
            origin: { y: 0.8 }
        });
    } else {
        selectedBlock.classList.add('incorrect');
        feedbackText.innerHTML = `<span class='text-danger'><i class='bi bi-x-circle-fill'></i> Incorrect! Try again.</span>`;
        // Also highlight correct answer in green
        const correctBlock = block.querySelector(`.quiz-option-${correctOpt}`);
        if (correctBlock) correctBlock.classList.add('correct');
    }
}

// ── Switch Study Mode ──
function switchStudyMode(materialId, mode) {
    // Hide all views for this material
    document.getElementById('card-content-' + materialId).style.display = 'none';
    document.getElementById('card-flashcards-' + materialId).style.display = 'none';
    document.getElementById('card-sandbox-' + materialId).style.display = 'none';
    document.getElementById('card-notes-' + materialId).style.display = 'none';
    
    // Hide resource bar if not reading mode
    const resBar = document.getElementById('resource-bar-' + materialId);
    if (resBar) {
        resBar.style.display = mode === 'read' || mode === 'recall' ? 'flex' : 'none';
    }

    // Remove active recall classes
    const contentCard = document.getElementById('card-content-' + materialId);
    contentCard.classList.remove('active-recall-enabled');

    // Deactivate active tab buttons
    const tabsContainer = document.getElementById('study-tabs-' + materialId);
    tabsContainer.querySelectorAll('.study-tab-btn').forEach(btn => btn.classList.remove('active'));

    // Activate chosen mode
    if (mode === 'read') {
        contentCard.style.display = 'block';
        document.getElementById('tab-read-' + materialId).classList.add('active');
    } else if (mode === 'recall') {
        contentCard.style.display = 'block';
        contentCard.classList.add('active-recall-enabled');
        document.getElementById('tab-recall-' + materialId).classList.add('active');
        prepareActiveRecall();
    } else if (mode === 'cards') {
        document.getElementById('card-flashcards-' + materialId).style.display = 'block';
        document.getElementById('tab-cards-' + materialId).classList.add('active');
        startFlashcards(materialId);
    } else if (mode === 'sandbox') {
        document.getElementById('card-sandbox-' + materialId).style.display = 'block';
        document.getElementById('tab-sandbox-' + materialId).classList.add('active');
        if (!sqlDbInitialized) {
            initSqlDatabase();
            sqlDbInitialized = true;
        }
    } else if (mode === 'notes') {
        document.getElementById('card-notes-' + materialId).style.display = 'block';
        document.getElementById('tab-notes-' + materialId).classList.add('active');
        loadNotesList(materialId);
    }
}

// ── Active Recall Preparation ──
function prepareActiveRecall() {
    document.querySelectorAll('.content-card').forEach(card => {
        const targets = card.querySelectorAll('strong, b, code:not(pre code)');
        targets.forEach(el => {
            if (el.classList.contains('active-recall-target')) return;
            el.classList.add('active-recall-target');
            el.setAttribute('title', 'Click to reveal');
            el.addEventListener('click', function(e) {
                if (card.classList.contains('active-recall-enabled')) {
                    e.stopPropagation();
                    this.classList.toggle('revealed');
                }
            });
        });
    });
}

// ── Reading Controls ──
let currentFontSize = 100;
function setFontSize(val) {
    currentFontSize = val;
    document.querySelectorAll('.content-card').forEach(card => {
        card.style.fontSize = (val / 100) + 'rem';
    });
    // sync sliders
    document.querySelectorAll('#font-size-slider').forEach(slider => {
        slider.value = val;
    });
    document.querySelectorAll('#font-size-val').forEach(span => {
        span.textContent = val + '%';
    });
}

function setFontFamily(family) {
    document.querySelectorAll('.content-card').forEach(card => {
        card.classList.remove('font-sans', 'font-serif', 'font-dyslexic');
        card.classList.add('font-' + family);
    });
    // Update active state in dropdown
    document.querySelectorAll('.font-switcher').forEach(btn => {
        btn.classList.remove('active');
        if (btn.innerText.toLowerCase() === family) {
            btn.classList.add('active');
        }
    });
}

function setReadingTheme(theme) {
    document.querySelectorAll('.content-card').forEach(card => {
        card.classList.remove('theme-sepia', 'theme-dark');
        if (theme === 'sepia' || theme === 'dark') {
            card.classList.add('theme-' + theme);
        }
    });
}

// ── Focus Ruler ──
function toggleRuler() {
    rulerEnabled = !rulerEnabled;
    const ruler = document.getElementById('focus-ruler');
    ruler.style.display = rulerEnabled ? 'block' : 'none';
    
    document.querySelectorAll('[id^=btn-ruler-]').forEach(btn => {
        if (rulerEnabled) {
            btn.classList.remove('btn-outline-secondary');
            btn.classList.add('btn-warning', 'text-white');
        } else {
            btn.classList.remove('btn-warning', 'text-white');
            btn.classList.add('btn-outline-secondary');
        }
    });
}
document.addEventListener('mousemove', function(e) {
    if (rulerEnabled) {
        const ruler = document.getElementById('focus-ruler');
        ruler.style.top = (e.clientY - 20) + 'px';
    }
});

// ── Audiobook TTS ──
function toggleTTS(materialId) {
    const btn = document.getElementById('btn-tts-' + materialId);
    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        btn.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-outline-secondary');
        clearParagraphHighlights(materialId);
    } else {
        const contentCard = document.getElementById('card-content-' + materialId);
        if (!contentCard) return;
        
        speechParagraphs = Array.from(contentCard.querySelectorAll('p, h2, h3, h4, li')).filter(el => el.innerText.trim().length > 0);
        if (speechParagraphs.length === 0) return;
        
        isSpeaking = true;
        btn.innerHTML = '<i class="bi bi-pause-fill"></i>';
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-danger');
        currentParaIndex = 0;
        speakParagraph(materialId);
    }
}

function speakParagraph(materialId) {
    if (!isSpeaking || currentParaIndex >= speechParagraphs.length) {
        isSpeaking = false;
        const btn = document.getElementById('btn-tts-' + materialId);
        if (btn) {
            btn.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-secondary');
        }
        clearParagraphHighlights(materialId);
        return;
    }
    
    clearParagraphHighlights(materialId);
    const activeEl = speechParagraphs[currentParaIndex];
    activeEl.style.backgroundColor = 'rgba(14, 165, 233, 0.15)';
    activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    currentUtterance = new SpeechSynthesisUtterance(activeEl.innerText);
    currentUtterance.onend = function() {
        currentParaIndex++;
        speakParagraph(materialId);
    };
    currentUtterance.onerror = function() {
        isSpeaking = false;
        const btn = document.getElementById('btn-tts-' + materialId);
        if (btn) {
            btn.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-secondary');
        }
        clearParagraphHighlights(materialId);
    };
    window.speechSynthesis.speak(currentUtterance);
}

function clearParagraphHighlights(materialId) {
    speechParagraphs.forEach(el => {
        el.style.backgroundColor = '';
    });
}

// ── Flashcard Engine ──
function generateFlashcards(materialId) {
    const contentCard = document.getElementById('card-content-' + materialId);
    if (!contentCard) return [];
    
    let cards = [];
    
    // Rules-based parsing
    const elements = Array.from(contentCard.querySelectorAll('h2, h3, h4, p, ul, ol'));
    let currentHeading = null;
    let currentAnswer = [];
    
    elements.forEach(el => {
        if (['H2', 'H3', 'H4'].includes(el.tagName)) {
            if (currentHeading && currentAnswer.length > 0) {
                cards.push({
                    front: currentHeading,
                    back: currentAnswer.join('')
                });
            }
            currentHeading = el.innerText;
            currentAnswer = [];
        } else if (currentHeading) {
            currentAnswer.push(el.outerHTML);
        }
    });
    if (currentHeading && currentAnswer.length > 0) {
        cards.push({
            front: currentHeading,
            back: currentAnswer.join('')
        });
    }
    
    // Sentence-based rules fallback
    if (cards.length < 3) {
        const paragraphs = contentCard.querySelectorAll('p');
        paragraphs.forEach(p => {
            const text = p.innerText;
            const matches = text.match(/([^.]+)(?:is defined as|is a|means|refers to)([^.]+)\./i);
            if (matches && matches.length >= 3) {
                let term = matches[1].trim();
                let definition = matches[2].trim();
                if (term.length < 50 && definition.length > 10 && definition.length < 200) {
                    cards.push({
                        front: `What is "${term}"?`,
                        back: `<p>${term} ${matches[0].includes('is defined as') ? 'is defined as' : matches[0].includes('is a') ? 'is a' : matches[0].includes('means') ? 'means' : 'refers to'} ${definition}.</p>`
                    });
                }
            }
        });
    }
    
    if (cards.length === 0) {
        cards.push({
            front: "Study Tip",
            back: "<p>Read through the lesson text in the first tab, highlight key notes, and use Sandbox to try examples!</p>"
        });
    }
    return cards;
}

function startFlashcards(materialId) {
    if (!flashcardsData[materialId]) {
        flashcardsData[materialId] = {
            cards: generateFlashcards(materialId),
            currentIndex: 0,
            masteredIds: new Set()
        };
    }
    renderFlashcard(materialId);
}

function renderFlashcard(materialId) {
    const data = flashcardsData[materialId];
    const cardEl = document.getElementById('flashcard-element-' + materialId);
    
    cardEl.classList.remove('flipped');
    
    const card = data.cards[data.currentIndex];
    if (!card) return;
    
    cardEl.querySelector('.flashcard-front .flashcard-text').innerHTML = card.front;
    cardEl.querySelector('.flashcard-back .flashcard-text').innerHTML = card.back;
    
    document.getElementById('flashcard-count-' + materialId).textContent = `Card ${data.currentIndex + 1} of ${data.cards.length}`;
    document.getElementById('flashcard-mastered-' + materialId).textContent = `${data.masteredIds.size} Mastered`;
}

function flipFlashcard(materialId) {
    const cardEl = document.getElementById('flashcard-element-' + materialId);
    cardEl.classList.toggle('flipped');
}

function prevFlashcard(materialId) {
    const data = flashcardsData[materialId];
    if (data.currentIndex > 0) {
        data.currentIndex--;
        renderFlashcard(materialId);
    }
}

function nextFlashcard(materialId) {
    const data = flashcardsData[materialId];
    if (data.currentIndex < data.cards.length - 1) {
        data.currentIndex++;
        renderFlashcard(materialId);
    }
}

function markCardMastered(materialId) {
    const data = flashcardsData[materialId];
    data.masteredIds.add(data.currentIndex);
    
    // Pop confetti
    confetti({
        particleCount: 30,
        angle: 60,
        spread: 55,
        origin: { x: 0 }
    });
    confetti({
        particleCount: 30,
        angle: 120,
        spread: 55,
        origin: { x: 1 }
    });
    
    document.getElementById('flashcard-mastered-' + materialId).textContent = `${data.masteredIds.size} Mastered`;
    
    // Auto advance
    if (data.currentIndex < data.cards.length - 1) {
        setTimeout(() => nextFlashcard(materialId), 600);
    }
}

// ── Playgrounds Scanner ──
function prepareCodePlaygrounds(materialId) {
    const contentCard = document.getElementById('card-content-' + materialId);
    if (!contentCard) return;
    
    const preBlocks = contentCard.querySelectorAll('pre');
    if (preBlocks.length > 0) {
        const sandboxTab = document.getElementById('tab-sandbox-' + materialId);
        if (sandboxTab) sandboxTab.classList.remove('d-none');
    }
    
    preBlocks.forEach((pre, index) => {
        const codeEl = pre.querySelector('code');
        if (!codeEl) return;
        
        let lang = 'python';
        const codeClass = codeEl.className.toLowerCase();
        if (codeClass.includes('python')) lang = 'python';
        else if (codeClass.includes('sql')) lang = 'sql';
        else if (codeClass.includes('html') || codeClass.includes('css') || codeClass.includes('javascript')) lang = 'web';
        
        // Add runner trigger bar
        if (pre.previousElementSibling && pre.previousElementSibling.classList.contains('playground-trigger-bar')) return;
        
        const triggerBar = document.createElement('div');
        triggerBar.className = 'playground-trigger-bar d-flex justify-content-between align-items-center bg-dark text-light px-3 py-2 rounded-top-3 border-bottom border-secondary';
        triggerBar.style.fontSize = '0.8rem';
        
        const encoded = encodeURIComponent(codeEl.innerText);
        triggerBar.innerHTML = `
            <span class="fw-bold"><i class="bi bi-terminal me-1"></i> ${lang.toUpperCase()} Code Block</span>
            <button class="btn btn-xs btn-outline-info text-info py-0 px-2 fw-semibold rounded-pill" onclick="openCodeInSandbox('${materialId}', '${encoded}', '${lang}')">
                <i class="bi bi-play-fill"></i> Try in Sandbox
            </button>
        `;
        pre.classList.add('rounded-top-0');
        pre.parentNode.insertBefore(triggerBar, pre);
    });
}

function openCodeInSandbox(materialId, encodedCode, lang) {
    const code = decodeURIComponent(encodedCode);
    switchStudyMode(materialId, 'sandbox');
    
    const editor = document.getElementById('sandbox-editor-' + materialId);
    const selector = document.getElementById('sandbox-lang-' + materialId);
    
    if (editor) editor.value = code;
    if (selector) {
        selector.value = lang;
    }
}

function clearSandboxConsole(materialId) {
    document.getElementById('sandbox-console-' + materialId).innerHTML = 'Console cleared.';
    document.getElementById('web-preview-bar-' + materialId).classList.add('d-none');
}

async function loadPyodideEngine() {
    if (window.loadPyodide) return;
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js";
        script.onload = () => resolve();
        script.onerror = () => reject(new Error("Failed to load Pyodide Python interpreter. Check connection."));
        document.head.appendChild(script);
    });
}

async function executeSandboxCode(materialId) {
    const code = document.getElementById('sandbox-editor-' + materialId).value;
    const lang = document.getElementById('sandbox-lang-' + materialId).value;
    const outputEl = document.getElementById('sandbox-console-' + materialId);
    const previewBar = document.getElementById('web-preview-bar-' + materialId);
    
    previewBar.classList.add('d-none');
    
    if (lang === 'python') {
        outputEl.innerHTML = "Loading Python Engine WASM... (first run takes 2-3 seconds)";
        try {
            await loadPyodideEngine();
            if (!window.pyodide) {
                window.pyodide = await loadPyodide({
                    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
                });
            }
            // Redirect standard outputs
            await window.pyodide.runPythonAsync(`
                import sys, io
                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()
            `);
            
            await window.pyodide.runPythonAsync(code);
            let stdout = await window.pyodide.runPythonAsync("sys.stdout.getvalue()");
            let stderr = await window.pyodide.runPythonAsync("sys.stderr.getvalue()");
            
            let result = stdout || "";
            if (stderr) result += "\nTraceback:\n" + stderr;
            if (!result) result = "Executed successfully with no output.";
            outputEl.innerHTML = "<pre class='text-dark'>" + result + "</pre>";
        } catch (err) {
            outputEl.innerHTML = "<span class='text-danger'>Python Error:\n" + err.message + "</span>";
        }
    } else if (lang === 'sql') {
        outputEl.innerHTML = "Running Query...";
        try {
            let res = alasql(code);
            if (!res || res.length === 0) {
                outputEl.innerHTML = "Query executed successfully. 0 rows returned.";
                return;
            }
            if (!Array.isArray(res)) {
                outputEl.innerHTML = JSON.stringify(res);
                return;
            }
            
            // Render ASCII Table
            let keys = Object.keys(res[0]);
            let table = "| " + keys.join(" | ") + " |\n";
            table += "| " + keys.map(() => "---").join(" | ") + " |\n";
            res.forEach(row => {
                table += "| " + keys.map(k => (row[k] !== undefined && row[k] !== null) ? row[k] : "NULL").join(" | ") + " |\n";
            });
            outputEl.innerHTML = "<pre class='text-dark p-2 rounded bg-light border'>" + table + "</pre>";
        } catch (err) {
            outputEl.innerHTML = "<span class='text-danger'>SQL Query Error:\n" + err.message + "</span>";
        }
    } else if (lang === 'web') {
        outputEl.innerHTML = "Compiling Live Preview...";
        previewBar.classList.remove('d-none');
        
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';
        iframe.style.background = '#ffffff';
        
        outputEl.innerHTML = '';
        outputEl.appendChild(iframe);
        
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.open();
        doc.write(code);
        doc.close();
    }
}

function openFullWebPreview(materialId) {
    const code = document.getElementById('sandbox-editor-' + materialId).value;
    const w = window.open();
    w.document.open();
    w.document.write(code);
    w.document.close();
}

// ── Notes & Highlights System ──
function initHighlighter() {
    document.querySelectorAll('.content-card').forEach(card => {
        card.addEventListener('mouseup', function(e) {
            handleTextSelection(e, card);
        });
    });
    document.addEventListener('mousedown', function(e) {
        const toolbar = document.getElementById('highlight-toolbar');
        if (toolbar && !toolbar.contains(e.target) && !window.getSelection().toString()) {
            hideHighlightToolbar();
        }
    });
}

function handleTextSelection(e, card) {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (text.length > 0) {
        currentSelectionRange = selection.getRangeAt(0).cloneRange();
        currentSelectionText = text;
        const panel = card.closest('.material-panel');
        if (panel) {
            currentMaterialId = panel.id.replace('panel-mat-', '');
        }
        const rect = currentSelectionRange.getBoundingClientRect();
        const toolbar = document.getElementById('highlight-toolbar');
        toolbar.style.display = 'flex';
        toolbar.style.top = `${rect.top + window.scrollY - 40}px`;
        toolbar.style.left = `${rect.left + window.scrollX + (rect.width/2) - (toolbar.offsetWidth/2)}px`;
    } else {
        hideHighlightToolbar();
    }
}

function hideHighlightToolbar() {
    const toolbar = document.getElementById('highlight-toolbar');
    if (toolbar) toolbar.style.display = 'none';
}

function applyHighlight(color) {
    if (!currentSelectionRange) return;
    try {
        const span = document.createElement('span');
        span.className = `study-highlight highlight-${color}`;
        currentSelectionRange.surroundContents(span);
        saveHighlightData(currentMaterialId, currentSelectionText, color);
    } catch (err) {
        saveHighlightData(currentMaterialId, currentSelectionText, color, "Cross-element clip");
    }
    window.getSelection().removeAllRanges();
    hideHighlightToolbar();
    loadNotesList(currentMaterialId);
}

function addHighlightNote() {
    if (!currentSelectionText) return;
    const noteText = prompt("Add a study note for this selection:");
    if (noteText === null) return;
    
    try {
        const span = document.createElement('span');
        span.className = `study-highlight highlight-yellow`;
        currentSelectionRange.surroundContents(span);
        saveHighlightData(currentMaterialId, currentSelectionText, 'yellow', noteText);
    } catch (err) {
        saveHighlightData(currentMaterialId, currentSelectionText, 'yellow', noteText);
    }
    window.getSelection().removeAllRanges();
    hideHighlightToolbar();
    loadNotesList(currentMaterialId);
}

function clearSelectionHighlight() {
    window.getSelection().removeAllRanges();
    hideHighlightToolbar();
}

function saveHighlightData(materialId, text, color, noteText = '') {
    let key = `notes_mat_${materialId}`;
    let data = JSON.parse(localStorage.getItem(key) || '[]');
    data.push({
        id: Date.now(),
        text: text,
        color: color,
        note: noteText,
        timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    });
    localStorage.setItem(key, JSON.stringify(data));
}

function saveGeneralNote(materialId) {
    const textEl = document.getElementById('note-text-' + materialId);
    const text = textEl.value.trim();
    if (!text) return;
    saveHighlightData(materialId, "General Note", "note", text);
    textEl.value = '';
    loadNotesList(materialId);
}

function deleteNoteItem(materialId, noteId) {
    let key = `notes_mat_${materialId}`;
    let data = JSON.parse(localStorage.getItem(key) || '[]');
    data = data.filter(item => item.id !== noteId);
    localStorage.setItem(key, JSON.stringify(data));
    loadNotesList(materialId);
}

function clearAllNotes(materialId) {
    if (confirm("Are you sure you want to clear all notes for this lesson?")) {
        localStorage.removeItem(`notes_mat_${materialId}`);
        loadNotesList(materialId);
    }
}

function loadNotesList(materialId) {
    const container = document.getElementById('notes-list-' + materialId);
    if (!container) return;
    
    let key = `notes_mat_${materialId}`;
    let data = JSON.parse(localStorage.getItem(key) || '[]');
    
    if (data.length === 0) {
        container.innerHTML = `<p class="text-muted small py-4 text-center">No notes or highlights saved yet. Highlight text or write a note to get started!</p>`;
        return;
    }
    
    let html = '';
    data.forEach(item => {
        const colorVal = item.color === 'yellow' ? '#fef08a' : item.color === 'green' ? '#bbf7d0' : item.color === 'pink' ? '#fbcfe8' : '#bfdbfe';
        if (item.color === 'note') {
            html += `
                <div class="note-item border-start border-4 border-info p-3 mb-2 bg-light rounded-end-3 position-relative">
                    <span class="badge bg-info text-dark rounded-pill px-2 py-0.5 small position-absolute" style="top: 8px; right: 12px; font-size: 0.65rem;">Note</span>
                    <p class="mb-1 small fw-semibold text-dark">${item.note}</p>
                    <small class="text-muted" style="font-size:0.7rem;">Saved at ${item.timestamp}</small>
                    <button class="btn btn-xs text-danger border-0 p-0 position-absolute" style="bottom: 8px; right: 12px; font-size: 0.8rem;" onclick="deleteNoteItem('${materialId}', ${item.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `;
        } else {
            html += `
                <div class="note-item border-start border-4 p-3 mb-2 bg-light rounded-end-3 position-relative" style="border-color: ${colorVal} !important;">
                    <span class="badge text-dark rounded-pill px-2 py-0.5 small position-absolute" style="top: 8px; right: 12px; font-size: 0.65rem; background: ${colorVal};">Highlight</span>
                    <p class="mb-1 small italic text-muted">"${item.text}"</p>
                    ${item.note ? `<p class="mb-1 small fw-semibold text-dark"><i class="bi bi-chat-left-text me-1"></i> ${item.note}</p>` : ''}
                    <small class="text-muted" style="font-size:0.7rem;">Saved at ${item.timestamp}</small>
                    <button class="btn btn-xs text-danger border-0 p-0 position-absolute" style="bottom: 8px; right: 12px; font-size: 0.8rem;" onclick="deleteNoteItem('${materialId}', ${item.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `;
        }
    });
    container.innerHTML = html;
}

// ── SQL Mock DB Prepopulation ──
function initSqlDatabase() {
    if (!window.alasql) return;
    try {
        // Core mock data
        alasql("CREATE TABLE IF NOT EXISTS users (id INT, username STRING, email STRING, date_joined STRING)");
        alasql("INSERT INTO users VALUES (1, 'amit_singh', 'amit@trhvision.com', '2026-04-10'), (2, 'neha_patel', 'neha@gmail.com', '2026-05-12'), (3, 'rohan_sharma', 'rohan.s@outlook.com', '2026-05-20')");
        
        alasql("CREATE TABLE IF NOT EXISTS projects (id INT, title STRING, category STRING, price INT)");
        alasql("INSERT INTO projects VALUES (1, 'E-Commerce Site', 'Web Development', 12000), (2, 'Sales Dashboard', 'Data Analytics', 8000), (3, 'Customer Churn Predictor', 'Machine Learning', 15000)");

        alasql("CREATE TABLE IF NOT EXISTS submissions (id INT, user_id INT, project_id INT, score INT, status STRING)");
        alasql("INSERT INTO submissions VALUES (101, 1, 2, 95, 'Approved'), (102, 2, 1, 88, 'Approved'), (103, 3, 3, 45, 'Pending')");

        // Employees & Departments data (matching SQL lesson examples)
        alasql("CREATE TABLE IF NOT EXISTS departments (id INT, name STRING)");
        alasql("INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'Marketing'), (4, 'HR')");

        alasql("CREATE TABLE IF NOT EXISTS employees (id INT, name STRING, department_id INT, salary DECIMAL(10,2), hire_date STRING, email STRING)");
        alasql("INSERT INTO employees VALUES " +
               "(1, 'Rajesh Kumar', 1, 75000.00, '2025-01-15', 'rajesh@trhvision.com'), " +
               "(2, 'Priya Sharma', 1, 82000.00, '2024-06-10', 'priya@trhvision.com'), " +
               "(3, 'Amit Patel', 2, 45000.00, '2025-03-01', 'amit@trhvision.com'), " +
               "(4, 'Ananya Sen', 2, 55000.00, '2024-11-20', 'ananya@trhvision.com'), " +
               "(5, 'Vikram Singh', 3, 62000.00, '2025-02-14', 'vikram@trhvision.com'), " +
               "(6, 'Sneha Rao', 3, 48000.00, '2025-04-18', 'sneha@trhvision.com'), " +
               "(7, 'Rohan Verma', 4, 40000.00, '2025-05-01', 'rohan@trhvision.com'), " +
               "(10, 'John Doe', 1, 30000.00, '2026-01-01', 'john@trhvision.com')");

        // Customers & Orders data (matching SQL Join examples)
        alasql("CREATE TABLE IF NOT EXISTS customers (id INT, name STRING)");
        alasql("INSERT INTO customers VALUES (1, 'Aditya'), (2, 'Bhavna'), (3, 'Chiraag'), (4, 'Divya')");

        alasql("CREATE TABLE IF NOT EXISTS orders (id INT, customer_id INT, amount INT)");
        alasql("INSERT INTO orders VALUES (1001, 1, 250), (1002, 1, 150), (1003, 2, 450), (1004, 4, 300)");

        console.log("Mock SQL DB populated: users, projects, submissions, departments, employees, customers, orders.");
    } catch (err) {
        console.error("SQL initialization error:", err);
    }
}

// Chatbot support removed completely

// ── Form Confetti Interception ──
function initQuizSubmit() {
    const form = document.querySelector('.assessment-card form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Final splash confetti!
            confetti({
                particleCount: 150,
                spread: 80,
                origin: { y: 0.6 }
            });
            
            // Delay submission for 1.5s to display the confetti animation
            setTimeout(() => {
                form.submit();
            }, 1500);
        });
    }
}

// ── Image Lightbox ──
function initImageLightbox() {
    if (!document.getElementById('img-lightbox')) {
        const overlay = document.createElement('div');
        overlay.id = 'img-lightbox';
        overlay.style.cssText = `
            display:none; position:fixed; inset:0; z-index:9999;
            background:rgba(0,0,0,0.88); align-items:center;
            justify-content:center; cursor:zoom-out; padding:20px;
        `;
        overlay.innerHTML = `
            <img id="img-lightbox-img" style="
                max-width:92vw; max-height:92vh; object-fit:contain;
                border-radius:12px; box-shadow:0 8px 48px rgba(0,0,0,0.6);
                image-rendering:-webkit-optimize-contrast;
                image-rendering:crisp-edges;
            ">
            <button style="
                position:absolute; top:18px; right:24px; background:rgba(255,255,255,0.15);
                border:none; color:#fff; font-size:1.5rem; border-radius:50%;
                width:42px; height:42px; cursor:pointer; line-height:1;
            " onclick="closeLightbox(event)">✕</button>
        `;
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) closeLightbox(e);
        });
        document.body.appendChild(overlay);
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeLightbox(e);
        });
    }

    document.querySelectorAll('.content-card img').forEach(img => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', function() {
            const lb = document.getElementById('img-lightbox');
            const lbImg = document.getElementById('img-lightbox-img');
            lbImg.src = img.src;
            lbImg.alt = img.alt || '';
            lb.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });
}

function closeLightbox(e) {
    if (e) e.stopPropagation();
    const lb = document.getElementById('img-lightbox');
    if (lb) lb.style.display = 'none';
    document.body.style.overflow = '';
}

// Boot
document.addEventListener('DOMContentLoaded', function() {
    initNav();
    initImageLightbox();
    initHighlighter();
    initQuizSubmit();
});

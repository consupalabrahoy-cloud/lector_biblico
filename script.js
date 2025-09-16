// URLs de los archivos de datos
const BOOKS_URLS = {
    "Mateo": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Mateo.csv",
    "Marcos": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Marcos.csv",
    "Lucas": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Lucas.csv",
    "Juan": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Juan.csv",
    "Hechos": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Hechos.csv",
    "Romanos": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Romanos.csv",
    "1º a los Corintios": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/PrimeraCorintios.csv",
    "2º a los Corintios": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/SegundaCorintios.csv",
    "Gálatas": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Gálatas.csv",
    "Efesios": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Efesios.csv",
    "Filipenses": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Filipenses.csv",
    "Colosenses": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Colosenses.csv",
    "1º a los Tesalonicenses": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/PrimeraTesalonicenses.csv",
    "2º a los Tesalonicenses": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/SegundaTesalonicenses.csv",
    "1º a Timoteo": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/PrimeraTimoteo.csv",
    "2º a Timoteo": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/SegundaTimoteo.csv",
    "Tito": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Tito.csv",
    "Filemón": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Filemón.csv",
    "Hebreos": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Hebreos.csv",
    "Santiago": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Santiago.csv",
    "1º de Pedro": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/PrimeraPedro.csv",
    "2º de Pedro": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/SegundaPedro.csv",
    "1º de Juan": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/PrimeraJuan.csv",
    "2º de Juan": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/SegundaJuan.csv",
    "3º de Juan": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/TerceraJuan.csv",
    "Judas": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Judas.csv",
    "Apocalipsis": "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/Apocalipsis.csv",
};
const DICTIONARY_URL = "https://raw.githubusercontent.com/consupalabrahoy-cloud/unoaunointerlineal/main/vocabulario_nt.json";

// Variables globales para almacenar los datos
let allBibleData = [];
let dictionaryData = {};
let currentBook = '';
let currentChapter = 0;

// Referencias a elementos del DOM
const bookSelect = document.getElementById('book-select');
const chapterSelect = document.getElementById('chapter-select');
const bibleTextContainer = document.getElementById('bible-text');
const passageTitle = document.getElementById('passage-title');
const searchInput = document.getElementById('search-input');
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
const concordanceContent = document.getElementById('concordance-tab-content');
const dictionaryContent = document.getElementById('dictionary-tab-content');
const fontSizeSelect = document.getElementById('font-size-select');

// --- Funciones de Carga de Datos y Procesamiento ---
async function loadData() {
    try {
        const bookPromises = Object.entries(BOOKS_URLS).map(async ([bookName, url]) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.error(`Error al cargar ${url}: ${response.statusText}`);
                    return null;
                }
                const text = await response.text();
                const lines = text.split('\n').slice(1);
                return lines.map(line => {
                    const match = line.match(/^(\d+),(\d+),([\s\S]*)/);
                    if (!match) return null;
                    const [_, capitulo, versiculo, texto] = match;
                    const [texto_espanol, texto_griego] = splitText(texto);
                    return {
                        Libro: bookName,
                        Capítulo: parseInt(capitulo, 10),
                        Versículo: parseInt(versiculo, 10),
                        Texto_Español: texto_espanol,
                        Texto_Griego: texto_griego,
                        Normalized_Espanol: normalizeText(texto_espanol),
                        Normalized_Griego: normalizeText(texto_griego),
                    };
                }).filter(Boolean);
            } catch (error) {
                console.error(`Error de red al cargar ${url}:`, error);
                return null;
            }
        });
        const allBooks = await Promise.all(bookPromises);
        allBibleData = allBooks.flat().filter(Boolean);

        const dictResponse = await fetch(DICTIONARY_URL);
        if (!dictResponse.ok) {
            console.error(`Error al cargar el diccionario: ${dictResponse.statusText}`);
            return;
        }
        const dictList = await dictResponse.json();
        dictList.forEach(entry => {
            const normalizedWord = normalizeText(entry.palabra);
            dictionaryData[normalizedWord] = entry;
        });

        if (allBibleData.length > 0) {
            initializeUI();
        } else {
            bibleTextContainer.innerHTML = `<p style="color:red;">No se pudieron cargar los datos de la Biblia. Revisa la consola del navegador para más detalles.</p>`;
        }

    } catch (error) {
        console.error("Error inesperado en la carga de datos:", error);
        bibleTextContainer.innerHTML = `<p style="color:red;">Error inesperado en la aplicación. Revisa la consola del navegador para más detalles.</p>`;
    }
}

function splitText(fullText) {
    const match = fullText.match(/\s(?=[α-ωΑ-Ω])/);
    if (match) {
        const splitIndex = match.index;
        const spanishText = fullText.substring(0, splitIndex).trim();
        const greekText = fullText.substring(splitIndex).trim();
        return [spanishText, greekText];
    }
    return [fullText, ""];
}

function normalizeText(word) {
    if (!word) return '';
    const normalized = word.normalize('NFD');
    const stripped = normalized.replace(/[\u0300-\u036f]/g, "");
    return stripped.toLowerCase();
}

// --- Lógica de la interfaz de usuario ---
function initializeUI() {
    const books = [...new Set(allBibleData.map(item => item.Libro))].sort();

    bookSelect.innerHTML = '';
    books.forEach(book => {
        const option = document.createElement('option');
        option.value = book;
        option.textContent = book;
        bookSelect.appendChild(option);
    });

    bookSelect.addEventListener('change', handleBookChange);
    chapterSelect.addEventListener('change', handleChapterChange);
    fontSizeSelect.addEventListener('change', handleFontSizeChange);
    searchInput.addEventListener('input', handleSearch);
    tabButtons.forEach(button => button.addEventListener('click', handleTabClick));

    currentBook = bookSelect.value;
    handleBookChange();
}

function handleBookChange() {
    currentBook = bookSelect.value;
    const chapters = [...new Set(allBibleData
        .filter(item => item.Libro === currentBook)
        .map(item => item.Capítulo))].sort((a, b) => a - b);

    chapterSelect.innerHTML = '';
    chapters.forEach(chapter => {
        const option = document.createElement('option');
        option.value = chapter;
        option.textContent = chapter;
        chapterSelect.appendChild(option);
    });

    currentChapter = chapters[0];
    displayPassage();
}

function handleChapterChange() {
    currentChapter = parseInt(chapterSelect.value, 10);
    displayPassage();
}

function displayPassage() {
    const passages = allBibleData.filter(item => item.Libro === currentBook && item.Capítulo === currentChapter);
    bibleTextContainer.innerHTML = '';
    passageTitle.textContent = `${currentBook} ${currentChapter}`;
    const fontSize = `${fontSizeSelect.value}px`;

    passages.forEach(item => {
        const verseContainer = document.createElement('div');
        verseContainer.classList.add('verse-container');
        const spanishText = document.createElement('p');
        spanishText.classList.add('text-espanol');
        spanishText.style.fontSize = fontSize;
        spanishText.innerHTML = `<span class="verse-number">${item.Versículo}</span> ${item.Texto_Español}`;
        const greekText = document.createElement('p');
        greekText.classList.add('text-griego');
        greekText.style.fontSize = fontSize;
        greekText.textContent = item.Texto_Griego;
        verseContainer.appendChild(spanishText);
        verseContainer.appendChild(greekText);
        bibleTextContainer.appendChild(verseContainer);
    });
}

function handleFontSizeChange() {
    displayPassage();
}

// --- Lógica de búsqueda y pestañas ---
function handleSearch() {
    const searchTerm = searchInput.value.trim();
    if (searchTerm.length === 0) {
        concordanceContent.innerHTML = '';
        dictionaryContent.innerHTML = '';
        return;
    }
    const normalizedSearchTerm = normalizeText(searchTerm);
    searchConcordance(normalizedSearchTerm);
    searchDictionary(normalizedSearchTerm);
}

function searchConcordance(term) {
    const occurrences = allBibleData.filter(item => {
        return item.Normalized_Espanol.includes(term) || item.Normalized_Griego.includes(term);
    });
    concordanceContent.innerHTML = '';
    if (occurrences.length > 0) {
        concordanceContent.innerHTML = `<p class="info-message">Se encontraron ${occurrences.length} ocurrencias en total.</p>`;
        occurrences.forEach(item => {
            const occurrenceDiv = document.createElement('div');
            occurrenceDiv.classList.add('concordance-item');
            occurrenceDiv.innerHTML = `
                <p><strong>${item.Libro} ${item.Capítulo}:${item.Versículo}</strong></p>
                <p class="text-espanol">${item.Texto_Español}</p>
                <p class="text-griego">${item.Texto_Griego}</p>
            `;
            concordanceContent.appendChild(occurrenceDiv);
        });
    } else {
        concordanceContent.innerHTML = '<p class="info-message">No se encontraron ocurrencias.</p>';
    }
}

function searchDictionary(term) {
    const dictEntry = dictionaryData[term];
    dictionaryContent.innerHTML = '';
    if (dictEntry) {
        const entryDiv = document.createElement('div');
        entryDiv.classList.add('dict-item');
        const analisisHtml = Object.entries(dictEntry.analisis_gramatical || {}).map(([key, value]) => {
            return `<p><strong>${key.charAt(0).toUpperCase() + key.slice(1)}:</strong> ${value}</p>`;
        }).join('');
        entryDiv.innerHTML = `
            <h4>${dictEntry.palabra || 'No disponible'}</h4>
            <p><strong>Transliteración:</strong> ${dictEntry.transliteracion || 'No disponible'}</p>
            <p><strong>Traducción literal:</strong> ${dictEntry.traduccion_literal || 'No disponible'}</p>
            <p><strong>Análisis Morfológico:</strong></p>
            ${analisisHtml || '<p>No disponible</p>'}
        `;
        dictionaryContent.appendChild(entryDiv);
    } else {
        dictionaryContent.innerHTML = '<p class="info-message">No se encontró información gramatical para esta palabra.</p>';
    }
}

function handleTabClick(event) {
    tabButtons.forEach(button => button.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    const tab = event.target.dataset.tab;
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    document.getElementById(`${tab}-tab-content`).classList.add('active');
}

document.addEventListener('DOMContentLoaded', loadData);
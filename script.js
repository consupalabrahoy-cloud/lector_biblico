// URLs de los archivos de datos (rutas directas en la carpeta principal)
const BOOKS_URLS = {
    "Mateo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e866f6e1554298f5c96601a500aad1b0/raw/1698e351a24d0ce1731f74eb5ffeede61f8936f1/Mateo.csv",
    "Marcos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/279a23eb035734174d2f1ab934c60a4c/raw/f102760bab3a6c1bc0f5678736977ae1cb39d8b0/Marcos.csv",
    "Lucas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/18caf9a4a6c7fbbb6cb737575226e2b2/raw/2c1f99c882cd48a5bbadc934a1ada265a54d67b2/Lucas.csv",
    "Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/de1be45bd708b8e5a9faa27180928c6d/raw/21c37db0ad85a68c310976cb4da83cf3e37ff421/Juan.csv",
    "Hechos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/57ad8a0d06aff8cc558ab049ecc986f6/raw/dd1cc2af6d04ddfff3738c43be53c638453eedfe/Hechos.csv",
    "Romanos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/9ed5dd10e494b5a2b59fb72a27659494/raw/64a9f092ec80d0b41bddecf8d87e6b0529544209/romanos.csv",
    "1º a los Corintios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/d91777893510b11a73c403472c3fc053/raw/4165385e2f3ea71c4184e2af76e1816890e85143/PrimeraCorintios.csv",
    "2º a los Corintios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/23835350791d75a2fd2b74460c47f313/raw/3f297fca8a20271294ee50be43377abb8d255779/SegundaCorintios.csv",
    "Gálatas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/191befa64bed89146535058beb193d73/raw/4f08d3626fd889b28446fa0736ed7ce1e257b94b/G%25C3%25A1latas.csv",
    "Efesios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e494aa96ec0921af3c26f5cb4e838070/raw/e50b7c28a97e241fca44622a27ac5c4addc0684a/Efesios.csv",
    "Filipenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/1410fab184350abc0456899fa275d922/raw/8122da6a4caafb3c57a4f0ef16c5e077e07d3ac9/Filipenses.csv",
    "Colosenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/513d84d430af573d6758e9111842834f/raw/5cb45edc3c349761add831d7c39799a3c5dd09cd/Colosenses.csv",
    "1º a los Tesalonicenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/5927763cc04e71fc1cb9d8077c71d4dd/raw/8ba01a0c3033439e1e1c645de299b99180687ca1/PrimeraTesalonicenses",
    "2º a los Tesalonicenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/c9eade95386dea0021d373b44ac43f77/raw/03b55d89cf5b0582e5fae419ad362bf746ca64cc/SegundaTesalonicenses.csv",
    "1º a Timoteo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/b5c12c3507bc458ab7fc17f1f7f9b7df/raw/4876881d64d65c799a9731752e59de434f5ff221/PrimeraTimoteo.csv",
    "2º a Timoteo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/28c5875b0f6212a46a42b11f7aa4d91d/raw/ac4181e903c690bd075d1023cc3c36d172f0beb5/SegundaTimoteo.csv",
    "Tito": "https://gist.githubusercontent.com/consupalabrahoy-cloud/ab4fc95416837371385d075957a56efc/raw/39e6dd720a19ce949aac4c54ba9715d02b00908a/Tito.csv",
    "Filemón": "https://gist.githubusercontent.com/consupalabrahoy-cloud/35f2c52e4199e169d375875052d7383c/raw/3efa655484184c07b5e54ab6deae493af20d9734/Filemon.csv",
    "Hebreos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/82df333eb092948670371501c4863b4e/raw/e29329ac705757313e531bf124cea8b6c231ef33/Hebreos.csv",
    "Santiago": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e825c31c8fa88560ec91f37cf52f8442/raw/6288124abc9b3e96c2fd60213703ecc02f112b7c/Santiago.csv",
    "1º de Pedro": "https://gist.githubusercontent.com/consupalabrahoy-cloud/9519dac9507f0518b6ab80208420c62a/raw/93d4fc402d7635bc251f6ed1386d9a9783b79667/PrimeraPedro.csv",
    "2º de Pedro": "https://gist.githubusercontent.com/consupalabrahoy-cloud/13f172ea05f41376ea3cd831c7816fd3/raw/245c8510ce8f750a63eef8f92d8f38435cdc6b07/SegundaPedro.csv",
    "1º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/1666b27d0db16ae636d227cd974c5062/raw/d365df0d1f8c4956142749a55023532a818cf954/PrimeraJuan.csv",
    "2º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/36ce60ee4f590f2e4dc3070dd065b97b/raw/577e514f43b19af0465a96711c9083f16681e1fd/SegundaJuan.csv",
    "3º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e9dbbe82c952fce14bf0e6704df144ab/raw/896226e6f87b9e596f1ddcb91e0ec9d8eb9285e3/TerceraJuan.csv",
    "Judas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/fede1c609f50bd6e8607f2713df0eb8d/raw/7228ff11bc2319f1ef263028b0b5fbf2644f6136/Judas.csv",
    "Apocalipsis": "https://gist.githubusercontent.com/consupalabrahoy-cloud/50089fb1221cb00f8c7f7a2b8fc2c56f/raw/f08b0b312a8f564da935aecd3b6cd48ce5bad033/Apocalipsis.csv",
};
const DICTIONARY_URL = "https://gist.githubusercontent.com/consupalabrahoy-cloud/964829a32e2c35313f44e39983422397/raw/83710666f4db56e60a0eba4ce021fcaed38e9ccb/vocabulario_nt.json";

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
        const bibleData = [];
        for (const [bookName, url] of Object.entries(BOOKS_URLS)) {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.error(`Error al cargar ${url}: ${response.statusText}`);
                    continue;
                }
                const text = await response.text();
                const lines = text.split('\n');
                lines.forEach(line => {
                    if (!line.trim() || line.startsWith('Libro,Capítulo,Versículo,Texto')) {
                        return;
                    }
                    const match = line.match(/^(.*?),(.*?),(.*?),([\s\S]*)/);
                    if (!match) {
                        console.error(`Error de formato en la línea del libro ${bookName}: "${line}"`);
                        return;
                    }
                    const [_, book, capitulo, versiculo, texto] = match;
                    const [texto_espanol, texto_griego] = splitText(texto);
                    bibleData.push({
                        Libro: book,
                        Capítulo: parseInt(capitulo, 10),
                        Versículo: parseInt(versiculo, 10),
                        Texto_Español: texto_espanol,
                        Texto_Griego: texto_griego,
                        Normalized_Espanol: normalizeText(texto_espanol),
                        Normalized_Griego: normalizeText(texto_griego),
                    });
                });
            } catch (error) {
                console.error(`Error de red al cargar ${url}:`, error);
                continue;
            }
        }
        allBibleData = bibleData.filter(Boolean);

        const dictResponse = await fetch(DICTIONARY_URL);
        if (!dictResponse.ok) {
            console.error(`Error al cargar el diccionario: ${dictResponse.statusText}`);
        } else {
            const dictList = await dictResponse.json();
            dictList.forEach(entry => {
                const normalizedWord = normalizeText(entry.palabra);
                dictionaryData[normalizedWord] = entry;
            });
        }
        
        if (allBibleData.length > 0) {
            initializeUI();
        } else {
            bibleTextContainer.innerHTML = `<p style="color:red;">Error fatal: No se pudieron cargar datos válidos. Verifique los archivos CSV.</p>`;
        }
    } catch (error) {
        console.error("Error inesperado en la carga de datos:", error);
        bibleTextContainer.innerHTML = `<p style="color:red;">Error al cargar datos. Mensaje: ${error.message}</p>`;
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










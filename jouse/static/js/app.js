/**
 * Application Web - Prédiction de Qualité Réseau
 * Gère les interactions du formulaire et les appels API
 */

// URL de base de l'API
const API_BASE_URL = '/predict';

// Exemples de données
const EXAMPLES = [
    {
        name: "Excellente Connexion",
        data: {
            "Opérateur": "Orange",
            "Quartier": "Centre",
            "Type réseau": "5G",
            "Download (Mbps)": 200,
            "Upload (Mbps)": 100,
            "Latence (ms)": 5,
            "Jitter (ms)": 1,
            "Loss (%)": 0
        }
    },
    {
        name: "Connexion Moyenne",
        data: {
            "Opérateur": "Maroc Telecom",
            "Quartier": "Tahrir",
            "Type réseau": "4G",
            "Download (Mbps)": 50,
            "Upload (Mbps)": 25,
            "Latence (ms)": 30,
            "Jitter (ms)": 5,
            "Loss (%)": 1
        }
    },
    {
        name: "Mauvaise Connexion",
        data: {
            "Opérateur": "Vodafone",
            "Quartier": "Souissi",
            "Type réseau": "3G",
            "Download (Mbps)": 10,
            "Upload (Mbps)": 5,
            "Latence (ms)": 100,
            "Jitter (ms)": 20,
            "Loss (%)": 5
        }
    }
];

/**
 * Initialiser l'application au chargement de la page
 */
document.addEventListener('DOMContentLoaded', function () {
    // Attacher l'écouteur d'événement sur le formulaire
    document.getElementById('predictionForm').addEventListener('submit', handleFormSubmit);
    
    // Logger que l'app est prête
    console.log('Application Network Quality Prediction chargée');
});

/**
 * Gérer la soumission du formulaire
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Récupérer les données du formulaire
    const formData = new FormData(document.getElementById('predictionForm'));
    const data = Object.fromEntries(formData);
    
    // Convertir les valeurs numériques en nombres
    const numericFields = [
        "Download (Mbps)",
        "Upload (Mbps)",
        "Latence (ms)",
        "Jitter (ms)",
        "Loss (%)"
    ];
    
    numericFields.forEach(field => {
        if (data[field]) {
            data[field] = parseFloat(data[field]);
        }
    });
    
    console.log('Données du formulaire:', data);
    
    // Afficher la zone de chargement
    showLoading(true);
    
    try {
        // Envoyer la requête à l'API
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        // Récupérer les données de réponse
        const responseData = await response.json();
        
        if (response.ok && responseData.success) {
            // Afficher le résultat
            displayResult(responseData.result);
        } else {
            // Afficher l'erreur
            displayError(responseData.error || 'Erreur inconnue', responseData.message);
        }
    } catch (error) {
        console.error('Erreur lors de l\'appel API:', error);
        displayError('Erreur de Connexion', error.message);
    } finally {
        // Masquer la zone de chargement
        showLoading(false);
    }
}

/**
 * Afficher les résultats de la prédiction
 */
function displayResult(result) {
    // Masquer la zone d'erreur
    document.getElementById('errorSection').style.display = 'none';
    
    // Afficher la zone de résultat
    document.getElementById('resultSection').style.display = 'block';
    
    // Prédiction principale
    const predictionValue = document.getElementById('predictionValue');
    predictionValue.textContent = result.prediction;
    
    // Ajouter une classe CSS selon la prédiction
    predictionValue.className = 'prediction-value ' + result.prediction.toLowerCase();
    
    // Confiance
    const confidence = Math.round(result.confidence * 100);
    document.getElementById('confidenceBar').style.width = confidence + '%';
    document.getElementById('confidencePercent').textContent = confidence + '%';
    
    // Probabilités
    displayProbabilities(result.probabilities);
    
    // Données envoyées
    displayInputData(result.input_features);
    
    // Scroller vers le résultat
    scroll_to_result();
}

/**
 * Afficher les probabilités par classe
 */
function displayProbabilities(probabilities) {
    const container = document.getElementById('probabilitiesContainer');
    container.innerHTML = '';
    
    for (const [className, probability] of Object.entries(probabilities)) {
        const percentage = Math.round(probability * 100);
        
        const probItem = document.createElement('div');
        probItem.className = 'prob-item';
        probItem.innerHTML = `
            <div class="prob-class">${className}</div>
            <div class="prob-value">${percentage}%</div>
            <div style="background: #e0e0e0; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;">
                <div style="background: #3498db; height: 100%; width: ${percentage}%"></div>
            </div>
        `;
        
        container.appendChild(probItem);
    }
}

/**
 * Afficher les données envoyées
 */
function displayInputData(inputFeatures) {
    const container = document.getElementById('inputDataContainer');
    container.innerHTML = '';
    
    for (const [field, value] of Object.entries(inputFeatures)) {
        const dataItem = document.createElement('div');
        dataItem.className = 'data-item';
        
        // Formater la valeur
        let displayValue = value;
        if (typeof value === 'number') {
            displayValue = value.toFixed(2);
        }
        
        dataItem.innerHTML = `
            <div class="data-label">${field}</div>
            <div class="data-value">${displayValue}</div>
        `;
        
        container.appendChild(dataItem);
    }
}

/**
 * Afficher une erreur
 */
function displayError(errorTitle, errorMessage) {
    // Masquer la zone de résultat
    document.getElementById('resultSection').style.display = 'none';
    
    // Afficher la zone d'erreur
    const errorSection = document.getElementById('errorSection');
    errorSection.style.display = 'block';
    
    // Remplir le contenu de l'erreur
    const errorContent = document.getElementById('errorContent');
    errorContent.innerHTML = `
        <strong>${errorTitle}</strong>
        <p>${errorMessage}</p>
    `;
    
    // Scroller vers l'erreur
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Afficher/Masquer la zone de chargement
 */
function showLoading(show) {
    document.getElementById('loadingSection').style.display = show ? 'block' : 'none';
}

/**
 * Remplir le formulaire avec un exemple
 */
function fillExample(exampleIndex) {
    if (exampleIndex < 0 || exampleIndex >= EXAMPLES.length) {
        return;
    }
    
    const example = EXAMPLES[exampleIndex];
    const form = document.getElementById('predictionForm');
    
    // Remplir les champs du formulaire
    for (const [field, value] of Object.entries(example.data)) {
        const input = form.elements[field];
        if (input) {
            input.value = value;
        }
    }
    
    // Scroller vers le formulaire
    form.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Scroller vers le résultat
 */
function scroll_to_result() {
    const resultSection = document.getElementById('resultSection');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Mettre à jour le schéma de l'API au chargement
 */
async function loadApiSchema() {
    try {
        const response = await fetch('/predict/schema');
        const data = await response.json();
        console.log('Schéma API:', data.schema);
    } catch (error) {
        console.error('Erreur lors du chargement du schéma:', error);
    }
}

// Charger le schéma au démarrage
loadApiSchema();

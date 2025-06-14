document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');

    // Load stored language
    const storedLanguage = localStorage.getItem('selectedLanguage');
    if (storedLanguage) {
        languageSelector.value = storedLanguage;
        translatePage(storedLanguage);
    }

    languageSelector.addEventListener('change', function() {
        const targetLanguage = languageSelector.value;
        translatePage(targetLanguage);
        // Store selected language
        localStorage.setItem('selectedLanguage', targetLanguage);
    });

    function translatePage(targetLanguage) {
        // Get all translatable elements (e.g., elements with a specific class)
        const translatableElements = document.querySelectorAll('.translatable');

        translatableElements.forEach(element => {
            const textToTranslate = element.textContent;
            console.log('Text to translate:', textToTranslate);

            // Remove the class before translating
            element.classList.remove('translated-text');
            element.classList.remove('translated-button');

            // Use Google Translate API (no API key required for simple requests)
            const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLanguage}&dt=t&q=${encodeURIComponent(textToTranslate)}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log('Translation API response:', data);
                    if (data && data[0] && data[0][0] && data[0][0][0]) {
                        element.textContent = data[0][0][0];
                        if (element.tagName === 'BUTTON' || (element.tagName === 'A' && element.classList.contains('btn'))) {
                            element.classList.add('translated-button');
                        } else {
                            element.classList.add('translated-text');
                        }
                    } else {
                        console.error('Translation failed: Invalid response format', data);
                    }
                })
                .catch(error => {
                    console.error('Translation error:', error);
                });
        });
    }
});

// Add the "translatable" class to all elements that need to be translated.
// For example:
// <h2 class="translatable">Welcome to our website</h2>
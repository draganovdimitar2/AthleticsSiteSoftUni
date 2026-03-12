document.addEventListener('DOMContentLoaded', function() {
    const competitionNameInput = document.getElementById('competition-name-input');
    const yearSelect = document.getElementById('year-select'); // Use ID now
    const wrapperResultsDiv = document.querySelector('.wrapper-results');

    function debounce(func, delay) {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }

    const fetchResults = async () => {
        const resultsForm = document.querySelector('.results');
        if (!resultsForm) return;

        const formData = new FormData(resultsForm);
        const params = new URLSearchParams(formData).toString();
        const url = `${window.location.pathname}?${params}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();

            // Re-render the entire partial content
            if (wrapperResultsDiv) {
                wrapperResultsDiv.innerHTML = html;
                // After re-rendering, we need to re-attach listeners because the elements are new
                attachEventListeners();
            }

        } catch (e) {
            console.error('Error fetching results:', e);
        }
    };

    const debouncedFetchResults = debounce(fetchResults, 400); // Faster response

    function attachEventListeners() {
        const input = document.getElementById('competition-name-input');
        const select = document.getElementById('year-select');

        if (input) {
            input.addEventListener('input', debouncedFetchResults);
            // Put cursor at the end of input if it was active
            input.focus();
            const val = input.value;
            input.value = '';
            input.value = val;
        }

        if (select) {
            select.addEventListener('change', fetchResults); // No debounce for dropdown
        }
    }

    attachEventListeners();
});

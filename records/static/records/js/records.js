document.addEventListener('DOMContentLoaded', function() {
    const competitionNameInput = document.getElementById('competition-name-input');
    const yearSelect = document.querySelector('.year-select');
    const resultsForm = document.querySelector('.results'); // The form element
    const tableWrapper = document.querySelector('.table-wrapper');
    const noResultsFoundDiv = document.querySelector('.no-results-found');
    const wrapperResultsDiv = document.querySelector('.wrapper-results'); // The main wrapper for results and form

    function debounce(func, delay) {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }

    const fetchResults = async () => {
        const formData = new FormData(resultsForm);
        const params = new URLSearchParams(formData).toString();
        const url = `${window.location.pathname}?${params}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Identify as AJAX request
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();

            // Create a temporary div to parse the fetched HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const newTableWrapper = doc.querySelector('.table-wrapper');
            const newNoResultsFoundDiv = doc.querySelector('.no-results-found');

            if (newTableWrapper && tableWrapper) {
                tableWrapper.innerHTML = newTableWrapper.innerHTML;
                // Ensure no-results-found is hidden if results are found
                if (noResultsFoundDiv) {
                    noResultsFoundDiv.style.display = 'none';
                }
                // Also ensure the main wrapper is visible if it was hidden
                if (wrapperResultsDiv) {
                    wrapperResultsDiv.style.display = 'block';
                }
            } else if (newNoResultsFoundDiv && noResultsFoundDiv) {
                // If there are no results, hide the table and show the no results message
                if (tableWrapper) {
                    tableWrapper.innerHTML = ''; // Clear table content
                }
                noResultsFoundDiv.innerHTML = newNoResultsFoundDiv.innerHTML;
                noResultsFoundDiv.style.display = 'block';
                 if (wrapperResultsDiv) {
                    // Adjust visibility of the main wrapper if needed, depending on how you want to handle it
                    // For now, if no results and newNoResultsFoundDiv is within the general flow, keep wrapperResultsDiv block
                    wrapperResultsDiv.style.display = 'none'; // Hide wrapper-results if no results
                }

            } else {
                // Fallback if neither newTableWrapper nor newNoResultsFoundDiv is found,
                // or if the original elements are missing.
                console.error("Could not find expected content in the fetched HTML.");
                if (tableWrapper) tableWrapper.innerHTML = '<p>Error loading results.</p>';
            }

        } catch (e) {
            console.error('Error fetching results:', e);
            if (tableWrapper) tableWrapper.innerHTML = '<p>Error loading results.</p>';
        }
    };

    const debouncedFetchResults = debounce(fetchResults, 800); // 800ms debounce

    if (competitionNameInput) {
        competitionNameInput.addEventListener('input', debouncedFetchResults);
    }

    if (yearSelect) {
        yearSelect.addEventListener('change', debouncedFetchResults);
    }

    // Remove existing inline onchange from yearSelect if it was present
    if (yearSelect && yearSelect.hasAttribute('onchange')) {
        yearSelect.removeAttribute('onchange');
    }
});
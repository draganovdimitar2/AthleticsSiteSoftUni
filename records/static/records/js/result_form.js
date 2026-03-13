document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[data-get-age-category-url]');
    if (!form) return;

    const url = form.getAttribute('data-get-age-category-url');
    const athleteSelect = form.querySelector('select[name="athlete"]');
    const competitionSelect = form.querySelector('select[name="competition"]');
    const ageCategorySelect = form.querySelector('select[name="age_category"]');
    
    async function updateAgeCategory() {
        const competitionId = competitionSelect.value;
        const athleteId = athleteSelect.value;
        
        if (!competitionId) {
            // Keep existing options if any, or just leave it. 
            // Usually, we should clear it if no competition.
            ageCategorySelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        const fetchUrl = `${url}?competition_id=${competitionId}&athlete_id=${athleteId}`;

        try {
            const response = await fetch(fetchUrl);
            const data = await response.json();
            
            if (data.categories) {
                // Store current selection if we want to try and preserve it
                const currentVal = ageCategorySelect.value;
                
                ageCategorySelect.innerHTML = '<option value="">---------</option>';
                data.categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id;
                    option.textContent = cat.name;
                    ageCategorySelect.appendChild(option);
                });
                
                // If the view returned a specific match, use it
                if (data.selected_id) {
                    ageCategorySelect.value = data.selected_id;
                } else if (currentVal) {
                    // Try to restore previous value if it's still in the list
                    ageCategorySelect.value = currentVal;
                }
            }
        } catch (error) {
            console.error('Error fetching age categories:', error);
        }
    }
    
    if (athleteSelect && competitionSelect && ageCategorySelect) {
        athleteSelect.addEventListener('change', updateAgeCategory);
        competitionSelect.addEventListener('change', updateAgeCategory);
        
        // Initial load for update view
        if (competitionSelect.value) {
            updateAgeCategory();
        }
    }
});

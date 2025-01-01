
const items = [
    "i",
    "just",
    "lost",
    "my",
    "dog",
]

// perform fuzzy search

function searchItems() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('results');

    resultsContainer.innerHTML = '';

    const matches = items.filter(item => item.toLowerCase().includes(input));

    matches.forEach(match => {
        const button = document.createElement('button');
        button.className = 'result-button';
        button.textContent = match;

        button.onclick = () => {
            console.log('clicked', match);
        }

        resultsContainer.appendChild(button);
    });
}
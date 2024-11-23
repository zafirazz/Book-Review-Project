document.getElementById('search-button').addEventListener('click', function () {
    const query = document.getElementById('search-input').value;
    const resultsContainer = document.getElementById('search-results');

    // Example search results
    const results = [
        'Book 1: The Great Gatsby',
        'Book 2: To Kill a Mockingbird',
        'Author: J.K. Rowling',
        'Author: George Orwell',
        'Book 3: 1984',
    ];

    resultsContainer.innerHTML = ''; // Clear previous results

    results.forEach((result) => {
        if (result.toLowerCase().includes(query.toLowerCase())) {
            const resultDiv = document.createElement('div');
            resultDiv.textContent = result;
            resultsContainer.appendChild(resultDiv);
        }
    });

    if (resultsContainer.innerHTML === '') {
        resultsContainer.innerHTML = '<div>No results found.</div>';
    }
});

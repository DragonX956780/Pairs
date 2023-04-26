document.addEventListener('DOMContentLoaded', function() {
    fetch('/static/candidates.txt')
        .then(response => response.text())
        .then(text => {
            const stockPairs = text.split('\n').filter(line => line.length > 0).map(pair => pair.trim());
            const stockPairSelect = document.getElementById('stock-pair');
            stockPairs.forEach(pair => {
                const option = document.createElement('option');
                option.value = pair.replace(', ', ','); // Replace ', ' with ','
                option.textContent = pair;
                stockPairSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching stock pairs:', error);
        });
});


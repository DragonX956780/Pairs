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
    const form = document.querySelector("form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        fetch("/", {
        method: "POST",
        body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            const capitalElement = document.getElementById("capital");
            capitalElement.textContent = `Capital: $${data.new_capital.toFixed(2)}`;
            // Reload the images to show the updated charts
            document.querySelectorAll("img").forEach((img) => {
            img.src = img.src.split("?")[0] + "?" + new Date().getTime();
            });
        })
        .catch((error) => {
            console.error("Error updating capital:", error);
        });
    });
});


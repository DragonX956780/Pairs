document.addEventListener('DOMContentLoaded', function () {
  fetch('/static/tickers.txt')
    .then(response => response.text())
    .then(text => {
      const tickers = text.trim().split(" ");

      const tickerSelector = document.getElementById('stock');

      tickers.forEach((ticker) => {
        const option = document.createElement("option");
        option.text = ticker;
        option.value = ticker;
        tickerSelector.add(option);
      });

      document.getElementById('stock-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(event.target);
        const request = new XMLHttpRequest();

        request.onreadystatechange = function () {
          if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
              const response = JSON.parse(request.responseText);
              const chartFilename = response.chart_filename;
              document.getElementById('stock-chart').src = `/stock_chart?${new Date().getTime()}`;

              // Add this line to reload the page after updating the chart image src
              location.reload();
            } else {
              console.error('Error submitting form:', request.status, request.statusText);
            }
          }
        };

        request.open('POST', '/channels', true);
        request.send(formData);
      });

      console.log('Initial ticker:', tickers[0]);
    })
    .catch(error => {
      console.error('Error fetching tickers:', error);
    });
});


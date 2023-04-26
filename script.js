async function generateChart() {
    const stockPair = document.getElementById("stock-pair").value.split(",");
    const stock1 = stockPair[0];
    const stock2 = stockPair[1];

    // Fetch data for the selected stocks
    const stock1Data = await fetchStockData(stock1);
    const stock2Data = await fetchStockData(stock2);

    // Generate chart data
    const trace1 = {
        x: stock1Data.timestamps,
        y: stock1Data.prices,
        mode: "lines",
        name: stock1,
        line: { color: "blue" },
    };

    const trace2 = {
        x: stock2Data.timestamps,
        y: stock2Data.prices,
        mode: "lines",
        name: stock2,
        line: { color: "green" },
    };

    const data = [trace1, trace2];

    // Configure chart layout
    const layout = {
        title: "Stock Prices",
        xaxis: { title: "Time" },
        yaxis: { title: "Price" },
    };

    // Render the chart
    Plotly.newPlot("chart", data, layout);
}

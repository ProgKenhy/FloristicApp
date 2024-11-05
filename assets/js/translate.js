function showResults() {
	// Sample data with culture details
	const results = [
		{ flower: 'Роза', color: 'Красный', culture: 'Западная', meaning: 'Любовь и Страсть', image: '../static/img/rose.png' },
		{ flower: 'Роза', color: 'Красный', culture: 'Восточная', meaning: 'Преданность и Уважение', image: '../static/img/rose.png' },
		{ flower: 'Лилия', color: 'Белый', culture: 'Западная', meaning: 'Чистота и Невинность', image: '../static/img/lily.png' },
		{ flower: 'Лилия', color: 'Белый', culture: 'Японская', meaning: 'Богатство и Процветание', image: '../static/img/lily.png' }
	];

	// Get the selected culture from the dropdown
	const selectedCulture = document.getElementById('cultureSelect').value;

	// Filter results based on selected culture
	const filteredResults = selectedCulture === 'all'
		? results // Show all results if 'All Cultures' is selected
		: results.filter(result => result.culture === selectedCulture);

	// Display the filtered results in a table
	const resultsTable = document.getElementById('resultsTable');
	resultsTable.innerHTML = ''; // Clear previous results
	filteredResults.forEach(result => {
		const row = document.createElement('tr');
		row.innerHTML = `
	<td><img src="${result.image}" alt="${result.flower}" style="width: 30px;"> ${result.flower}</td>
	<td>${result.color}</td>
	<td>${result.culture}</td>
	<td>${result.meaning}</td>
`;
		resultsTable.appendChild(row);
	});

	document.getElementById('resultsSection').style.display = 'block';
}
document.addEventListener('DOMContentLoaded', function () {
    // Proposal Status Chart
    const proposalStatusCtx = document.getElementById('proposalStatusChart').getContext('2d');
    const proposalStatusChart = new Chart(proposalStatusCtx, {
        type: 'pie',
        data: {
            labels: ['Accepted', 'Rejected', 'Under Review', 'Submitted'],
            datasets: [{
                label: 'Proposal Status',
                data: JSON.parse(document.getElementById('proposalStatusData').textContent),
                backgroundColor: ['#28a745', '#dc3545', '#ffc107', '#007bff'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
            },
        },
    });

    // Evaluation Scores Chart
    const evaluationScoresCtx = document.getElementById('evaluationScoresChart').getContext('2d');
    const evaluationScoresChart = new Chart(evaluationScoresCtx, {
        type: 'bar',
        data: {
            labels: ['Average Score'],
            datasets: [{
                label: 'Scores',
                data: JSON.parse(document.getElementById('evaluationScoresData').textContent),
                backgroundColor: ['#17a2b8'],
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
});
/**
 * Logika pembuatan chart untuk halaman dashboard.
 * Data (window.dashboardData) di-set lewat script inline kecil
 * di templates/dashboard.html, karena data itu hasil query
 * database yang perlu Jinja untuk dikirim dari server.
 */

document.addEventListener("DOMContentLoaded", function () {
    const data = window.dashboardData;

    if (!data) {
        return;
    }

    /* =====================================
       ADUAN PER BULAN
    ====================================== */

    new Chart(
        document.getElementById("aduanBulananChart"),
        {
            type: "line",

            data: {
                labels: data.bulanLabels,

                datasets: [{
                    label: "Jumlah Aduan",
                    data: data.bulanData,
                    tension: 0.3,
                    fill: false,
                    borderWidth: 2
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        }
    );

    /* =====================================
       KONDISI PERANGKAT
    ====================================== */

    new Chart(
        document.getElementById("kondisiPerangkatChart"),
        {
            type: "doughnut",

            data: {
                labels: data.kondisiLabels,

                datasets: [{
                    label: "Jumlah Perangkat",
                    data: data.kondisiData,
                    borderWidth: 1
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const total = context.chart.data.datasets[0].data.reduce(
                                    (a, b) => a + b, 0
                                );
                                const value = context.parsed;
                                const percentage = total > 0
                                    ? ((value / total) * 100).toFixed(1)
                                    : 0;
                                return `${context.label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        }
    );

    /* =====================================
       KATEGORI GANGGUAN
    ====================================== */

    new Chart(
        document.getElementById("kategoriGangguanChart"),
        {
            type: "bar",

            data: {
                labels: data.gangguanLabels,

                datasets: [{
                    label: "Jumlah Aduan",
                    data: data.gangguanData,
                    borderWidth: 1
                }]
            },

            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        }
    );
});

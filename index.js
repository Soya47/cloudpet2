const db = firebase.firestore();

db.collection("noise_events").onSnapshot(snapshot => {
    let dailyData = [], weeklyData = [], monthlyData = [], yearlyData = [];

    snapshot.forEach(doc => {
        let data = doc.data();
        dailyData.push({ date: data.date, level: data.level });
        weeklyData.push({ week: data.week, level: data.level });
        monthlyData.push({ month: data.month, level: data.level });
        yearlyData.push({ year: data.year, level: data.level });
    });

    updateCharts(dailyData, weeklyData, monthlyData, yearlyData);
});

function updateCharts(daily, weekly, monthly, yearly) {
    renderChart("dailyChart", daily, "Date", "Noise Level");
    renderChart("weeklyChart", weekly, "Week Number", "Noise Level");
    renderChart("monthlyChart", monthly, "Month", "Noise Level");
    renderChart("yearlyChart", yearly, "Year", "Noise Level");
}

<select id="chartTypeSelect" onchange="updateCharts(daily, weekly, monthly, yearly)">
    <option value="bar">Bar Chart</option>
    <option value="line">Area Chart</option>
</select>

db.collection("noise_events").onSnapshot(snapshot => {
    let gallery = document.getElementById("mediaGallery");
    gallery.innerHTML = ""; // Clear previous images

    snapshot.forEach(doc => {
        let data = doc.data();
        if (data.image_url) {
            let imgContainer = document.createElement("div");
            imgContainer.classList.add("gallery-item");

            let img = document.createElement("img");
            img.src = data.image_url;
            img.onclick = function() { enlargeImage(data.image_url); };

            imgContainer.appendChild(img);
            gallery.appendChild(imgContainer);
        }
    });
});

const API_URL = "https://automated-job-data-collector.onrender.com/api/jobs";


let allJobs = [];
let showFavoritesOnly = false;

// Fetch jobs
async function fetchJobs() {
    try {
        const response = await fetch(API_URL);
        allJobs = await response.json();

        document.getElementById("loading").style.display = "none";
        renderJobs(allJobs);
    } catch {
        document.getElementById("loading").innerText = "Error loading jobs!";
    }
}

// Render UI
function renderJobs(jobList) {
    const grid = document.getElementById("job-grid");
    const empty = document.getElementById("empty");
    grid.innerHTML = "";

    let filtered = jobList;

    if (showFavoritesOnly) {
        const saved = getSavedIds();
        filtered = jobList.filter(j => saved.includes(j.id));
    }

    if (filtered.length === 0) {
        empty.classList.remove("hidden");
        return;
    }

    empty.classList.add("hidden");

    filtered.forEach(job => {
        const saved = isSaved(job.id);
        const logoLetter = job.company ? job.company[0].toUpperCase() : "P";

        const div = document.createElement("div");
        div.className = "job-card";

        div.innerHTML = `
            <div class="logo">${logoLetter}</div>
            <div class="job-title">${job.title}</div>
            <div class="company"><i class="fa-regular fa-building"></i> ${job.company}</div>
            <div class="location"><i class="fa-solid fa-location-dot"></i> ${job.location}</div>

            <div class="tags">
                <span class="tag">Python</span>
                <span class="tag">Remote</span>
            </div>

            <div class="card-footer">
                <button class="save-btn ${saved ? "saved" : ""}" onclick="toggleSave(${job.id})">
                    <i class="${saved ? "fa-solid" : "fa-regular"} fa-heart"></i>
                </button>
                <a href="${job.job_link}" target="_blank" class="apply-btn">Apply</a>
            </div>
        `;

        grid.appendChild(div);
    });
}

// Search filter
document.getElementById("search-input").addEventListener("keyup", () => {
    const q = document.getElementById("search-input").value.toLowerCase();
    const filtered = allJobs.filter(job =>
        job.title.toLowerCase().includes(q) ||
        job.company.toLowerCase().includes(q)
    );
    renderJobs(filtered);
});

// Favorites localStorage
function getSavedIds() {
    return JSON.parse(localStorage.getItem("savedJobs") || "[]");
}
function isSaved(id) {
    return getSavedIds().includes(id);
}
function toggleSave(id) {
    let saved = getSavedIds();
    if (saved.includes(id)) saved = saved.filter(i => i !== id);
    else saved.push(id);
    localStorage.setItem("savedJobs", JSON.stringify(saved));
    renderJobs(allJobs);
}

// Toggle favorites view
function toggleFavorites() {
    showFavoritesOnly = !showFavoritesOnly;
    document.getElementById("fav-btn").innerHTML = 
        showFavoritesOnly 
            ? `<i class="fa-solid fa-heart"></i> Show All`
            : `<i class="fa-regular fa-heart"></i> Saved Jobs`;

    renderJobs(allJobs);
}

fetchJobs();

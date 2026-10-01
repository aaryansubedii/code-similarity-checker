const API = "/compare";

let file1 = null;
let file2 = null;

function setupDropZone(zoneId, inputId, labelId, onFile) {
    const zone = document.getElementById(zoneId);
    const input = document.getElementById(inputId);
    const label = document.getElementById(labelId);

    zone.addEventListener("click", () => input.click());

    input.addEventListener("change", () => {
        if (input.files[0]) {
            onFile(input.files[0]);
            label.textContent = input.files[0].name;
            zone.classList.add("filled");
        }
    });

    zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("dragover"); });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.classList.remove("dragover");
        const f = e.dataTransfer.files[0];
        if (f) {
            input.files = e.dataTransfer.files;
            onFile(f);
            label.textContent = f.name;
            zone.classList.add("filled");
        }
    });
}

setupDropZone("drop1", "file1", "label1", (f) => { file1 = f; checkReady(); });
setupDropZone("drop2", "file2", "label2", (f) => { file2 = f; checkReady(); });

function checkReady() {
    document.getElementById("compare-btn").disabled = !(file1 && file2);
}

document.getElementById("compare-btn").addEventListener("click", async () => {
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const btn = document.getElementById("compare-btn");
    btn.disabled = true;
    btn.textContent = "Comparing...";

    try {
        const res = await fetch(API, { method: "POST", body: formData });
        const data = await res.json();
        renderResult(data);
    } catch (err) {
        alert("Comparison failed. Is the backend running?");
    } finally {
        btn.disabled = false;
        btn.textContent = "Compare";
    }
});

function renderResult(data) {
    document.getElementById("score-panel").classList.remove("hidden");
    document.getElementById("panes").classList.remove("hidden");

    const pct = data.similarity_percent;
    const circumference = 283;
    const offset = circumference - (pct / 100) * circumference;
    const fill = document.getElementById("gauge-fill");
    fill.style.strokeDashoffset = offset;
    fill.style.stroke = pct > 60 ? "#f85149" : pct > 30 ? "#d29922" : "#3fb950";

    document.getElementById("gauge-text").textContent = `${pct}%`;

    document.getElementById("stats").innerHTML = `
        <div><strong>${data.file1_name}</strong> vs <strong>${data.file2_name}</strong></div>
        <div>${data.shared_fingerprints} shared fingerprints</div>
        <div>${data.matched_lines_1.length} matched lines (file 1) · ${data.matched_lines_2.length} matched lines (file 2)</div>
    `;

    renderPane("pane1", data.file1_content, data.matched_lines_1);
    renderPane("pane2", data.file2_content, data.matched_lines_2);
}

function renderPane(paneId, content, matchedLines) {
    const pane = document.getElementById(paneId);
    const matchedSet = new Set(matchedLines);
    const lines = content.split("\n");

    pane.innerHTML = lines.map((line, idx) => {
        const lineNum = idx + 1;
        const cls = matchedSet.has(lineNum) ? "line match" : "line";
        const escaped = line.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return `<span class="${cls}">${escaped || " "}</span>`;
    }).join("\n");
}
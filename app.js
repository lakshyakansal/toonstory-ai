const form = document.querySelector("#story-form");
const topic = document.querySelector("#topic");
const statusBox = document.querySelector("#status");
const results = document.querySelector("#results");
const sceneGrid = document.querySelector("#scene-grid");
const createBtn = document.querySelector("#create-btn");
const videoBtn = document.querySelector("#video-btn");
let currentProject = null;
let currentStory = null;

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  createBtn.disabled = true;
  createBtn.textContent = "✦ Creating your story…";
  statusBox.textContent = "Writing scenes and drawing your cartoon friends. This may take a few seconds.";
  results.classList.add("hidden");
  try {
    const response = await fetch("/api/story", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({topic: topic.value, age: document.querySelector("#age").value, language: document.querySelector("#language").value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not create story.");
    currentProject = data.project_id;
    currentStory = data;
    document.querySelector("#story-title").textContent = data.title;
    document.querySelector("#story-intro").textContent = data.intro + " " + data.note;
    document.querySelector("#script-link").href = data.script_file;
    sceneGrid.innerHTML = data.scenes.map((scene, i) => `
      <article class="scene-card">
        <img src="${escapeHtml(scene.image)}" alt="Cartoon illustration for ${escapeHtml(scene.heading)}" loading="lazy">
        <div class="scene-copy"><span class="scene-number">SCENE ${String(i+1).padStart(2,"0")}</span>
        <h3>${escapeHtml(scene.heading)}</h3><p>${escapeHtml(scene.narration)}</p></div>
      </article>`).join("");
    results.classList.remove("hidden");
    statusBox.textContent = "Your story is ready!";
    document.querySelector("#video-status").textContent = "";
    document.querySelector("#video-wrap").classList.add("hidden");
    results.scrollIntoView({behavior:"smooth", block:"start"});
  } catch (error) {
    statusBox.textContent = error.message || "Something went wrong. Please try again.";
  } finally {
    createBtn.disabled = false;
    createBtn.innerHTML = '<span>✦</span> Generate my story <span class="button-arrow">→</span>';
  }
});

document.querySelector("#read-btn").addEventListener("click", () => {
  if (!currentStory || !("speechSynthesis" in window)) {
    document.querySelector("#video-status").textContent = "Narration is not supported by this browser.";
    return;
  }
  speechSynthesis.cancel();
  const text = currentStory.title + ". " + currentStory.scenes.map(s => s.heading + ". " + s.narration).join(" ");
  const utterance = new SpeechSynthesisUtterance(text);
  const lang = currentStory.language;
  utterance.lang = lang === "Hindi" ? "hi-IN" : "en-US";
  utterance.rate = 0.88;
  speechSynthesis.speak(utterance);
});
document.querySelector("#stop-btn").addEventListener("click", () => {
  if ("speechSynthesis" in window) speechSynthesis.cancel();
});

videoBtn.addEventListener("click", async () => {
  if (!currentProject) return;
  videoBtn.disabled = true;
  videoBtn.textContent = "Building MP4…";
  const videoStatus = document.querySelector("#video-status");
  videoStatus.textContent = "Assembling your cartoon scenes. Please keep this page open.";
  try {
    const response = await fetch("/api/video", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({project_id: currentProject})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Video export failed.");
    const videoUrl = data.video_url + "?v=" + Date.now();
    document.querySelector("#video-player").src = videoUrl;
    document.querySelector("#video-download").href = data.video_url;
    document.querySelector("#video-wrap").classList.remove("hidden");
    videoStatus.textContent = data.message;
    document.querySelector("#video-wrap").scrollIntoView({behavior:"smooth",block:"center"});
  } catch (error) {
    videoStatus.textContent = error.message || "Video export failed. Please try again.";
  } finally {
    videoBtn.disabled = false;
    videoBtn.textContent = "✦ Build MP4 video";
  }
});

const AGENTS = ["researcher", "planner", "executor", "critic"];

const graphEl = document.getElementById("graph");
const logEl = document.getElementById("log");
const nodeEls = {};

for (const agent of AGENTS) {
  const node = document.createElement("div");
  node.className = "node";
  node.innerHTML = `<div class="name">${agent}</div><div class="state"></div>`;
  graphEl.appendChild(node);
  nodeEls[agent] = node;
}

function setActive(agent, state) {
  const node = nodeEls[agent];
  if (!node) return; // "system" events have no node
  node.classList.add("active");
  node.querySelector(".state").textContent = state;
  clearTimeout(node._timer);
  node._timer = setTimeout(() => node.classList.remove("active"), 1200);
}

function appendLog(event) {
  const line = document.createElement("div");
  line.className = "log-line";
  const time = new Date(event.ts * 1000).toLocaleTimeString();
  line.innerHTML =
    `<span class="agent">${event.agent}</span>` +
    `<span class="type">${event.type}</span>` +
    `<span>${event.payload}</span>` +
    `<span style="float:right;color:#4a4f5a">${time}</span>`;
  logEl.appendChild(line);
  logEl.scrollTop = logEl.scrollHeight;
}

const source = new EventSource("/events");

source.onmessage = (e) => {
  const event = JSON.parse(e.data);
  setActive(event.agent, event.type);
  appendLog(event);
  if (event.type === "done") {
    source.close();
  }
};

source.onerror = () => {
  appendLog({ agent: "system", type: "connection", payload: "stream closed", ts: Date.now() / 1000 });
  source.close();
};

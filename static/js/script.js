// Change birth and due date inputs type
const due = document.getElementById("due");
if (due) {
  due.addEventListener("pointerdown", () => {
    if (due.type !== "date") due.type = "date";
  });

  due.addEventListener("blur", () => {
    if (!due.value) due.type = "text";
  });
}

const birth = document.getElementById("birth");
if (birth) {
  birth.addEventListener("pointerdown", () => {
    if (birth.type !== "date") birth.type = "date";
  });

  birth.addEventListener("blur", () => {
    if (!birth.value) birth.type = "text";
  });
}

// Modal (description)
const modal = document.getElementById("descModal");
if (modal) {
  const title = document.getElementById("descTitle");
  const body = document.getElementById("descBody");

  modal.addEventListener("show.bs.modal", async (event) => {
    const btn = event.relatedTarget;
    const id = btn.getAttribute("data-task-id");

    title.textContent = "Loading...";
    body.textContent = "Loading...";

    try {
      const res = await fetch(`/task/${id}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      title.textContent = data.title || "Task";
      body.textContent = data.description || "(no description)";
    } catch (e) {
      title.textContent = "Error";
      body.textContent = "Could not load description.";
      console.error(e);
    }
  });
}

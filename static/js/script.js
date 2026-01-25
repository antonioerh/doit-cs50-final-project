const due = document.getElementById("due");

due.addEventListener("pointerdown", function() {
    if (due.type !== "date") due.type = "date";
});

due.addEventListener("blur", function() {
    if (!due.value) due.type = "text";
});

const birth = document.getElementById("birth");

birth.addEventListener("pointerdown", function() {
    if (birth.type !== "date") birth.type = "date";
});

birth.addEventListener("blur", function() {
    if (!birth.value) birth.type = "text";
});
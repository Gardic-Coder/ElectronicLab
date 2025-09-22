document.addEventListener('DOMContentLoaded', () => {
    const tagDataElement = document.getElementById("tag-list");
    const allowCreate = document.body.dataset.allowTagCreate === "true";
    if (!tagDataElement) return;

    const allTags = JSON.parse(tagDataElement.textContent);

    const input = document.getElementById("tagInput");
    const suggestions = document.getElementById("tagSuggestions");
    const selectedTags = document.getElementById("selectedTags");
    const hiddenTags = document.getElementById("hiddenTags");

    if (!input || !suggestions || !selectedTags || !hiddenTags) return;

    input.addEventListener("input", () => {
        const query = input.value.toLowerCase();
        suggestions.innerHTML = "";
        if (!query) return;

        const matches = allTags.filter(tag => tag.name.toLowerCase().includes(query));
        if (matches.length === 0 && allowCreate) {
            const createBtn = document.createElement("button");
            createBtn.className = "list-group-item list-group-item-action text-success";
            createBtn.textContent = `Crear categoría "${query}"`;
            createBtn.onclick = (e) => {
                e.preventDefault();
                addTag(query);
                input.value = "";
                suggestions.innerHTML = "";
            };
            suggestions.appendChild(createBtn);
        } else {
            matches.forEach(tag => {
                const item = document.createElement("button");
                item.className = "list-group-item list-group-item-action";
                item.textContent = tag.name;
                item.onclick = (e) => {
                    e.preventDefault();
                    addTag(tag.name);
                    input.value = "";
                    suggestions.innerHTML = "";
                };
                suggestions.appendChild(item);
            });
        }
    });

    function addTag(tagName) {
        if (document.querySelector(`input[value="${tagName}"]`)) return;

        const badge = document.createElement("span");
        badge.className = "badge bg-primary me-1";
        badge.innerHTML = `${tagName} <a href="#" class="text-white ms-1 text-decoration-none" onclick="removeTag('${tagName}')">&times;</a>`;
        selectedTags.appendChild(badge);

        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = "tags";
        hiddenInput.value = tagName;
        hiddenTags.appendChild(hiddenInput);
    }

    window.removeTag = function(tagName) {
        document.querySelectorAll(`input[value="${tagName}"]`).forEach(el => el.remove());
        document.querySelectorAll(`#selectedTags span`).forEach(span => {
            if (span.textContent.includes(tagName)) span.remove();
        });
    };
});
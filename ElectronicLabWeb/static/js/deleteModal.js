document.addEventListener('DOMContentLoaded', () => {
  const trigger = document.getElementById('deleteTrigger');
  const modalElement = document.getElementById('confirmDeleteModal');
  if (!trigger || !modalElement) return;

  trigger.addEventListener('click', () => {
    const seleccionados = document.querySelectorAll('input[name="selected"]:checked');
    if (seleccionados.length === 0) {
      alert("No seleccionaste ningún componente.");
      return;
    }

    const form = modalElement.querySelector('form');
    form.querySelectorAll('input[name="selected"]').forEach(e => e.remove());

    seleccionados.forEach(checkbox => {
      const clone = document.createElement("input");
      clone.type = "hidden";
      clone.name = "selected";
      clone.value = checkbox.value;
      form.appendChild(clone);
    });

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  });
});
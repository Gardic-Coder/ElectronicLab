document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('editForm');
  const cancelBtn = document.getElementById('cancelBtn');
  const initialData = new FormData(form);

  cancelBtn.addEventListener('click', (e) => {
    const currentData = new FormData(form);
    let changed = false;

    for (let [key, value] of currentData.entries()) {
      if (initialData.get(key) !== value) {
        changed = true;
        break;
      }
    }

    if (changed) {
      const confirmExit = confirm("Hay cambios sin guardar. ¿Estás seguro de que quieres salir?");
      if (!confirmExit) {
        e.preventDefault();
      }
    }
  });
});
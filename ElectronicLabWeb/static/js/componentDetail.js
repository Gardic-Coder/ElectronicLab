document.addEventListener('DOMContentLoaded', () => {
  window.mostrarDetalleComponente = function(id, event) {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'LABEL') return;

    fetch(`/inventario/detalle/${id}/`)
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById("componentDetailContent");

        const imageUrl = data.preview_url || data.thumbnail_url || "/static/img/no-image.png";

        const editButton = data.can_edit
        ? `<div class="text-end mt-3">
            <a href="${data.edit_url}" class="btn btn-outline-warning">Editar componente</a>
          </div>`
        : "";

        container.innerHTML = `
          <div class="row">
            <div class="col-md-5 text-center">
              <img src="${imageUrl}" class="img-fluid rounded mb-3" alt="${data.code}">
            </div>
            <div class="col-md-7">
              <h5 class="mb-2">${data.code}</h5>
              <p><strong>Descripción:</strong> ${data.description}</p>
              <p><strong>Disponible:</strong> ${data.available}</p>
              ${data.can_edit ? `
                <p><strong>Existencia:</strong> ${data.stock}</p>
                <p><strong>Prestado:</strong> ${data.prestado}</p>
              ` : ''}
              <p><strong>Ubicación:</strong> ${data.location}</p>
              <p><strong>Categorías:</strong> ${data.categories.join(', ') || 'Sin categorías'}</p>
              ${data.datasheet_url ? `<p><strong>Datasheet:</strong> <a href="${data.datasheet_url}" target="_blank">Descargar PDF</a></p>` : ''}
              ${editButton}
            </div>
          </div>
        `;

        const modal = new bootstrap.Modal(document.getElementById('componentDetailModal'));
        modal.show();
      });
  };
});
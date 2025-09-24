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
          ${data.available > 0 ? `
            <div class="mt-4">
              <label><strong>Cantidad a solicitar:</strong></label>
              <div class="input-group" style="max-width: 200px;">
                <button class="btn btn-outline-secondary" type="button" id="btnDecrementar">−</button>
                <input type="number" class="form-control text-center" id="cantidadInput" value="${data.cantidad_carrito || 1}" min="1" max="${data.available}">
                <button class="btn btn-outline-secondary" type="button" id="btnIncrementar">+</button>
              </div>
              <button class="btn btn-primary mt-2" id="btnAgregarCarrito">Agregar a la bolsa</button>
            </div>
          ` : `<p class="text-danger mt-3"><strong>No disponible para préstamo</strong></p>`}
        `;

        const modal = new bootstrap.Modal(document.getElementById('componentDetailModal'));
        modal.show();
        initLoanCartControls(data.id, data.available);
      });
  };
});
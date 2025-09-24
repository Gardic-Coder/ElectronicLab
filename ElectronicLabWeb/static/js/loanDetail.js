window.verDetallePrestamo = function(id) {
  fetch(`/prestamos/prestamo/${id}/`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("loanDetailContent");
      let html = `
        <p><strong>Estado:</strong> ${data.estado}</p>
        <p><strong>Fecha de solicitud:</strong> ${data.fecha_solicitud}</p>
        ${data.fecha_aprobacion ? `<p><strong>Fecha de aprobación:</strong> ${data.fecha_aprobacion}</p>` : ''}
        ${data.fecha_devolucion ? `<p><strong>Fecha de devolución:</strong> ${data.fecha_devolucion}</p>` : ''}
        ${data.observaciones ? `<p><strong>Motivo del rechazo:</strong> ${data.observaciones}</p>` : ''}
        <h6 class="mt-3">Componentes solicitados:</h6>
        <ul class="list-group">
          ${data.componentes.map(c => `
            <li class="list-group-item d-flex justify-content-between">
              <span>${c.code} - ${c.description}</span>
              <span><strong>${c.cantidad}</strong></span>
            </li>
          `).join('')}
        </ul>
      `;
      container.innerHTML = html;
      new bootstrap.Modal(document.getElementById('loanDetailModal')).show();
    });
};
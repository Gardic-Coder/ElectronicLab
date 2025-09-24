window.verPerfilUsuario = function(userId) {
  fetch(`/users/perfil/${userId}/`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("userProfileContent");
      const photo = data.photo || "/static/img/default-user.png";

      container.innerHTML = `
        <div class="text-center mb-3">
          <img src="${photo}" class="rounded-circle img-thumbnail" style="width: 150px;" alt="Foto de perfil">
        </div>
        <ul class="list-group">
          <li class="list-group-item"><strong>Nombre:</strong> ${data.nombre} ${data.apellido}</li>
          <li class="list-group-item"><strong>Cédula:</strong> ${data.cedula}</li>
          <li class="list-group-item"><strong>Correo:</strong> ${data.email}</li>
          <li class="list-group-item"><strong>Teléfono:</strong> ${data.telefono || 'No registrado'}</li>
          <li class="list-group-item"><strong>Rol:</strong> ${data.rol}</li>
          <li class="list-group-item"><strong>Estado:</strong> ${data.estado}</li>
        </ul>
      `;
      new bootstrap.Modal(document.getElementById('userProfileModal')).show();
    });
};

window.verDetalleAdmin = function(loanId) {
  fetch(`/prestamos/prestamo/${loanId}/`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("adminLoanDetailContent");

      let html = `
        <p><strong>Estado:</strong> ${data.estado}</p>
        <p><strong>Fecha de solicitud:</strong> ${data.fecha_solicitud}</p>
        <div class="mb-3">
          <label class="form-label">Fecha de devolución (opcional)</label>
          <input type="date" name="fecha_devolucion" class="form-control">
        </div>
        <div class="mb-3">
          <label class="form-label">Observaciones (opcional)</label>
          <textarea name="observaciones" class="form-control" rows="2"></textarea>
        </div>
        <h6 class="mt-3">Componentes solicitados:</h6>
        <table class="table">
          <thead>
            <tr><th>Código</th><th>Descripción</th><th>Cantidad</th></tr>
          </thead>
          <tbody>
            ${data.componentes.map(c => `
              <tr>
                <td>${c.code}</td>
                <td>${c.description}</td>
                <td>
                  <input type="number" name="cantidad_${c.id}" value="${c.cantidad}" min="1" class="form-control">
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      container.innerHTML = html;

      const form = document.getElementById("procesarPrestamoForm");
      form.setAttribute("data-loan-id", loanId);

      const modal = new bootstrap.Modal(document.getElementById('adminLoanDetailModal'));
      modal.show();

      window.enviarPrestamo = function(estado) {
        const form = document.getElementById("procesarPrestamoForm");
        const loanId = form.getAttribute("data-loan-id");
        const formData = new FormData(form);
        formData.set('estado', estado);

        fetch(`/prestamos/admin/procesar/${loanId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: new URLSearchParams(formData)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Solicitud procesada correctamente.");
                bootstrap.Modal.getInstance(document.getElementById('adminLoanDetailModal')).hide();
                location.reload();
            } else {
                alert(data.error || "Error al procesar.");
            }
        });
     };
    });
};

function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, val] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(val);
  }
  return '';
}
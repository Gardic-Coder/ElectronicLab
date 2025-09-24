function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, val] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(val);
  }
  return '';
}

window.eliminarDelCarrito = function(componentId) {
  fetch('/prestamos/carrito/eliminar/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCSRFToken()
    },
    body: `component_id=${componentId}`
  }).then(() => location.reload());
};

window.actualizarCantidad = function(componentId, cantidad) {
  fetch('/prestamos/carrito/actualizar/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCSRFToken()
    },
    body: `component_id=${componentId}&cantidad=${cantidad}`
  }).then(res => res.json())
    .then(data => {
      if (!data.success) alert(data.error || "Error al actualizar cantidad.");
    });
};
// static/js/loanCart.js

window.initLoanCartControls = function(componentId, available) {
  const input = document.getElementById('cantidadInput');
  const btnAdd = document.getElementById('btnAgregarCarrito');

  document.getElementById('btnIncrementar').onclick = () => {
    let val = parseInt(input.value) || 0;
    if (val < available) input.value = val + 1;
  };

  document.getElementById('btnDecrementar').onclick = () => {
    let val = parseInt(input.value) || 0;
    if (val > 1) input.value = val - 1;
  };

  btnAdd.onclick = () => {
    const cantidad = parseInt(input.value);
    if (!cantidad || cantidad < 1 || cantidad > available) {
      alert("Cantidad inválida o excede disponibilidad.");
      return;
    }

    fetch('/prestamos/agregar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCSRFToken()
      },
      body: `component_id=${componentId}&cantidad=${cantidad}`
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Agregado a la bolsa de préstamo.");
      } else {
        alert(data.error || "Error al agregar.");
      }
    });
  };
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
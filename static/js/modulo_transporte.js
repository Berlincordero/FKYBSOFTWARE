document.addEventListener('DOMContentLoaded', function () {
    const formConductor = document.getElementById('form-conductor');
    const formPlaca = document.getElementById('form-placa');
    const formRuta = document.getElementById('form-ruta');
    const successAlert = document.getElementById('success-alert');
    const tableRoutes = document.getElementById('table-routes').getElementsByTagName('tbody')[0];
    const btnDeleteAll = document.getElementById('btn-delete-all');
    const btnPrint = document.getElementById('btn-print');

    function showAlert(message) {
        successAlert.innerText = message;
        successAlert.style.display = 'block';
        setTimeout(() => {
            successAlert.style.display = 'none';
        }, 3000);
    }

    function addRouteToTable(route) {
        const row = tableRoutes.insertRow();
        row.insertCell().innerText = route.conductor;
        row.insertCell().innerText = route.placa;
        row.insertCell().innerText = route.nombreRuta;
        row.insertCell().innerText = route.numeroFactura;
        row.insertCell().innerText = route.horaSalida;
        const actionsCell = row.insertCell();
        const deleteButton = document.createElement('button');
        deleteButton.innerText = 'Eliminar';
        deleteButton.className = 'btn btn-delete';
        deleteButton.onclick = function () {
            if (confirm('¿Estás seguro de que deseas eliminar esta ruta?')) {
                row.remove();
                showAlert('Ruta eliminada con éxito.');
            }
        };
        actionsCell.appendChild(deleteButton);
    }

    function handleFormSubmit(form, event) {
        event.preventDefault();
        const formData = new FormData(form);
        const route = {
            conductor: formData.get('conductor'),
            placa: formData.get('placa'),
            nombreRuta: formData.get('nombre_ruta'),
            numeroFactura: formData.get('numero_factura'),
            horaSalida: formData.get('hora_salida')
        };
        addRouteToTable(route);
        showAlert('Ruta guardada con éxito.');
    }

    formConductor.addEventListener('submit', function (event) {
        handleFormSubmit(this, event);
    });

    formPlaca.addEventListener('submit', function (event) {
        handleFormSubmit(this, event);
    });

    formRuta.addEventListener('submit', function (event) {
        handleFormSubmit(this, event);
    });

    btnDeleteAll.addEventListener('click', function () {
        if (confirm('¿Estás seguro de que deseas eliminar todas las rutas del día?')) {
            tableRoutes.innerHTML = '';
            showAlert('Todas las rutas del día han sido eliminadas.');
        }
    });

    btnPrint.addEventListener('click', function () {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Configurar la fuente y el estilo
        doc.setFont('Helvetica', 'normal');
        doc.setFontSize(12);
        
        // Agregar título
        doc.setFontSize(16);
        doc.setTextColor(40, 60, 100);
        doc.text('Rutas del Día', 14, 20);
        
        // Agregar encabezados de la tabla
        doc.setFontSize(12);
        doc.setTextColor(100, 100, 100);
        doc.setFillColor(220, 220, 220);
        doc.rect(14, 25, 180, 10, 'F');
        doc.text('Conductor', 16, 30);
        doc.text('Placa', 45, 30);
        doc.text('Ruta', 75, 30);
        doc.text('Número de Factura', 105, 30);
        doc.text('Hora de Salida', 145, 30);
        
        // Dibujar bordes de la tabla
        doc.setDrawColor(200, 200, 200);
        doc.setLineWidth(0.5);
        doc.line(14, 31, 194, 31);  // Línea horizontal superior
        doc.line(14, 25, 14, 35);    // Línea vertical izquierda
        doc.line(194, 25, 194, 35);  // Línea vertical derecha

        // Agregar contenido de la tabla
        let y = 35;
        Array.from(tableRoutes.rows).forEach(row => {
            doc.setTextColor(50, 50, 50);
            doc.text(row.cells[0].innerText, 16, y);
            doc.text(row.cells[1].innerText, 45, y);
            doc.text(row.cells[2].innerText, 75, y);
            doc.text(row.cells[3].innerText, 105, y);
            doc.text(row.cells[4].innerText, 145, y);
            y += 10;
            // Dibujar líneas horizontales
            doc.line(14, y - 5, 194, y - 5);
        });

        // Añadir línea final
        doc.line(14, y - 5, 194, y - 5);

        doc.save('rutas_del_dia.pdf');
    });
});

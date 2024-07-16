document.getElementById('button-search').addEventListener('click', function() {
    // Obtener el valor del input
    const productInput = document.getElementById('product-input').value;

    // Verificar que el input no esté vacío
    if (productInput.trim() === '') {
        alert('Por favor, ingrese un producto.');
        return;
    }

    // Crear una nueva fila
    const tableBody = document.getElementById('product-table-body');
    const newRow = document.createElement('tr');

    newRow.innerHTML = `
        <td><input type="text" class="form-control" placeholder="Código" aria-label="Código" value="${productInput}"></td>
        <td><input type="text" class="form-control" placeholder="Descripción" aria-label="Descripción"></td>
        <td>
            <div class="quantity">
                <input type="number" class="form-control" value="1" min="1" max="100">
            </div>
        </td>
        <td>
            <select class="form-control unidad-select" aria-label="Unidad">
                <option value="kg">kg</option>
                <option value="mts">mts</option>
                <option value="unid">unid</option>
                <option value="litros">litros</option>
                <option value="gal">gal</option>
                <option value="cms">cms</option>
            </select>
        </td>
        <td><input type="text" class="form-control col-2" placeholder="Prec. Unid." aria-label="Prec. Unid."></td>
        <td><input type="text" class="form-control col-1" placeholder="Desc %" aria-label="Desc %"></td>
        <td><input type="text" class="form-control col-2" placeholder="Total" aria-label="Total"></td>
        <td><i class="fa fa-trash delete-icon" aria-hidden="true"></i></td>
    `;

    // Añadir la nueva fila a la tabla
    tableBody.appendChild(newRow);

    // Añadir evento para el icono de borrar
    newRow.querySelector('.delete-icon').addEventListener('click', function() {
        newRow.remove();
    });

    // Limpiar el input
    document.getElementById('product-input').value = '';
});

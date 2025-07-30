import React, { useState, useEffect } from 'react';
import DataTable from 'react-data-table-component';

function App() {
  const [dados, setDados] = useState([]);
  const [erro, setErro] = useState(null);

  const columns = [
    { name: 'Referencia Giant', selector: row => row.ref_giant, sortable: true },
    { name: 'MAWB', selector: row => row.document_info?.mawb, sortable: true },
    { name: 'Status Liberacao', selector: row => row.status_info?.status_liberacao, sortable: true },
    { name: 'Data Liberacao', selector: row => row.date_info?.data_liberacao, sortable: true },
    { name: 'Valor', selector: row => row.valor, sortable: true },
    { name: 'Peso', selector: row => row.peso, sortable: true },
    { name: 'Data Emissao', selector: row => row.delivery_info?.data_emissao, sortable: true },
    { name: 'Data Prevista Entrega', selector: row => row.delivery_info?.data_prevista_entrega, sortable: true },
    { name: 'Dias Atraso', selector: row => row.delay_info?.dias_atraso, sortable: true },
  ];

  useEffect(() => {
    fetch('http://localhost:8000/api/desembaraco/')
      .then(response => {
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
        return response.json();
      })
      .then(data => setDados(data))
      .catch(error => setErro(error.message));
  }, []);

  return (
    <div style={{ padding: '1rem' }}>
      <h1>Grid de Dados</h1>
      {erro ? (
        <p style={{ color: 'red' }}>Erro: {erro}</p>
      ) : (
        <DataTable
          title="Dados Importados"
          columns={columns}
          data={dados}
          pagination
          keyField="ref_giant"
          dense
          highlightOnHover
          striped
        />
      )}
    </div>
  );
}

export default App;

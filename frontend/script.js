document.addEventListener('DOMContentLoaded', () => {
  const API_URL = 'http://localhost:8000/api-backend/dados/';
  const gridElement = document.getElementById('myGrid');
  const searchInput = document.getElementById('search-input');
  const itemsPerPageSelect = document.getElementById('items-per-page');
  const showingFrom = document.getElementById('showing-from');
  const showingTo = document.getElementById('showing-to');
  const totalItems = document.getElementById('total-items');
  const firstPageBtn = document.getElementById('first-page');
  const prevPageBtn = document.getElementById('prev-page');
  const nextPageBtn = document.getElementById('next-page');
  const lastPageBtn = document.getElementById('last-page');

  let currentPage = 1;
  let itemsPerPage = parseInt(itemsPerPageSelect.value, 10);
  let gridApi;
  let totalRecords = 0;

  // Formatter de datas
  function dateFormatter(params) {
    if (!params.value) return '-';
    const date = new Date(params.value);
    return date.toLocaleDateString('pt-BR');
  }

  // Definição completa das colunas
const columnDefs = [
  // 🔒 Colunas não-editáveis
  { headerName: "Ref do Desembaraço", field: "ref_giant", minWidth: 150 },
  { headerName: "Número do Master", field: "mawb", minWidth: 130 },
  { headerName: "Número do House", field: "hawb", minWidth: 130 },
  { headerName: "Ref do cliente (C3)", field: "c3", minWidth: 150 },
  { headerName: "Delivery ID", field: "deliveryid", minWidth: 150 },
  { headerName: "Valor da Mercadoria", field: "cipbrl", minWidth: 150 },
  { headerName: "Número de peças", field: "pc", minWidth: 130 },
  { headerName: "Peso da Mercadoria", field: "peso", minWidth: 150 },
  { headerName: "Peso Cobrável", field: "peso_cobravel", minWidth: 150 },
  { headerName: "Tipo da Mercadoria", field: "tipo", minWidth: 150 },
  { headerName: "Data PUPDT", field: "pupdt", valueFormatter: dateFormatter, minWidth: 150 },
  { headerName: "Data CIOK", field: "ciok", valueFormatter: dateFormatter, minWidth: 150 },
  { headerName: "Data LI Entry", field: "lientrydt", valueFormatter: dateFormatter, minWidth: 180 },
  { headerName: "Data LI OK", field: "liok", valueFormatter: dateFormatter, minWidth: 200 },
  { headerName: "OK to Ship", field: "ok_to_ship", minWidth: 220 },
  { headerName: "Número da LI", field: "li", minWidth: 150 },
  { headerName: "Data HAWB", field: "hawbdt", valueFormatter: dateFormatter, minWidth: 200 },
  { headerName: "Data Estimada Booking", field: "estimatedbookingdt", valueFormatter: dateFormatter, minWidth: 200 },
  { headerName: "Data Chegada Destino", field: "arrivaldestinationdt", valueFormatter: dateFormatter, minWidth: 240 },
  { headerName: "Solicitação de Fundos", field: "solicitacao_fundos", minWidth: 240 },
  { headerName: "Fundos Recebidos", field: "fundos_recebidos", minWidth: 240 },
  { headerName: "Data EAD", field: "eadidt", valueFormatter: dateFormatter, minWidth: 200 },
  { headerName: "Data DI Due", field: "diduedt", valueFormatter: dateFormatter, minWidth: 180 },
  { headerName: "Número da DI", field: "diduenumber", minWidth: 150 },
  { headerName: "Data Pagamento ICMS", field: "icmspago", minWidth: 200 },
  { headerName: "Parametrização (Canal)", field: "canal_cor", minWidth: 280 },
  { headerName: "Data Liberação CCR", field: "data_liberacao_ccr", valueFormatter: dateFormatter, minWidth: 220 },
  { headerName: "Data Estimada Entrega BR1", field: "data_estimada", valueFormatter: dateFormatter, minWidth: 280 },
  { headerName: "Data Real Entrega", field: "real_lead_time", minWidth: 180 },
  { headerName: "Diferença Dias Entrega", field: "ship_failure_days", minWidth: 200 },
  { headerName: "Necessidade Justificativa", field: "tipo_justificativa_atraso", minWidth: 240 },
  { headerName: "Justificativa Atraso", field: "justificativa_atraso", minWidth: 240 },

  // ✏️ Colunas editáveis (com ícone e destaque visual)
  { headerName: "🖉 Ref Quarter", field: "q", editable: true, cellClass: 'editable-cell', cellEditor: 'agSelectCellEditor', cellEditorParams: { values: ['', 'Q1', 'Q2', 'Q3', 'Q4'] }, minWidth: 120 },
  { headerName: "🖉 Status de liberação", field: "sostatus_releasedonholdreturned", editable: true, cellClass: 'editable-cell', cellEditor: 'agSelectCellEditor', cellEditorParams: { values: ['', 'RELEASED', 'ON_HOLD', 'RETURNED'] }, minWidth: 160 },
  { headerName: "🖉 Data da coleta", field: "data_liberacao", editable: true, cellClass: 'editable-cell', cellEditor: 'agDateStringCellEditor', valueFormatter: dateFormatter, minWidth: 150 },
  { headerName: "🖉 Data da Nota Fiscal (Giant)", field: "data_nfe", editable: true, cellClass: 'editable-cell', cellEditor: 'agDateStringCellEditor', valueFormatter: dateFormatter, minWidth: 200 },
  { headerName: "🖉 Número NFE (Giant)", field: "numero_nfe", editable: true, cellClass: 'editable-cell', minWidth: 220 },
  { headerName: "🖉 Data Nota Fiscal (Deloitte)", field: "nftgdt", editable: true, cellClass: 'editable-cell', cellEditor: 'agDateStringCellEditor', valueFormatter: dateFormatter, minWidth: 220 },
  { headerName: "🖉 Número NFE (Deloitte)", field: "nftg", editable: true, cellClass: 'editable-cell', minWidth: 240 },
  { headerName: "🖉 Data Entrega BR1", field: "dlvatdestination", editable: true, cellClass: 'editable-cell', cellEditor: 'agDateStringCellEditor', valueFormatter: dateFormatter, minWidth: 220 },
  { headerName: "🖉 Status Atual Processo", field: "status_impexp", editable: true, cellClass: 'editable-cell', cellEditor: 'agSelectCellEditor', cellEditorParams: { values: ['', 'PENDENTE', 'LIBERADO', 'BLOQUEADO', 'CANCELADO'] }, minWidth: 220 },
  { headerName: "🖉 Eventos Processo", field: "eventos", editable: true, cellClass: 'editable-cell', cellEditor: 'agLargeTextCellEditor', minWidth: 300 }
];


  // Opções do grid atualizadas
  const gridOptions = {
    columnDefs,
    defaultColDef: {
      sortable: true,
      filter: true,
      resizable: true,
      flex: 1,
      minWidth: 120,
      wrapText: true,
      autoHeight: true
    },
    // Removido: enableRangeSelection (para evitar erro sem Enterprise)
    domLayout: 'autoHeight',
    onGridReady: params => {
      gridApi = params.api;
      loadData();
      gridApi.addEventListener('paginationChanged', updatePagination);
    },
    onCellValueChanged: event => {
      if (event.newValue !== event.oldValue) {
        saveField(event.data.ref_giant, event.colDef.field, event.newValue);
      }
    }
  };

  // Criação do grid com o novo método
  gridApi = agGrid.createGrid(gridElement, gridOptions);

  // Atualiza paginação
  function updatePagination() {
    const pageSize = gridApi.paginationGetPageSize();
    const current = gridApi.paginationGetCurrentPage() + 1;
    const start = (current - 1) * pageSize + 1;
    const end = Math.min(current * pageSize, totalRecords);

    showingFrom.textContent = start;
    showingTo.textContent = end;
    totalItems.textContent = totalRecords;

    firstPageBtn.disabled = current === 1;
    prevPageBtn.disabled = current === 1;
    nextPageBtn.disabled = current === gridApi.paginationGetTotalPages();
    lastPageBtn.disabled = current === gridApi.paginationGetTotalPages();
  }

  // Carrega dados do backend
  async function loadData() {
    const params = new URLSearchParams({
      page: currentPage,
      page_size: itemsPerPage,
      search: searchInput.value.trim()
    });
    try {
      const res = await fetch(`${API_URL}?${params}`);
      const data = await res.json();

      // Métodos atualizados:
      gridApi.setGridOption('rowData', data.resultados || []);
      gridApi.setGridOption('paginationPageSize', itemsPerPage);

      totalRecords = data.total || 0;
      updatePagination();
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
    }
  }

  // Salva campo alterado
  async function saveField(ref, field, value) {
    try {
      const res = await fetch(`${API_URL}${ref}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ [field]: value })
      });
      if (!res.ok) throw new Error('Falha ao salvar');
    } catch (err) {
      console.error('Erro ao salvar campo:', err);
      alert('Não foi possível salvar alteração: ' + err.message);
    }
  }

  // Obtém CSRF Token
  function getCSRFToken() {
    return document.cookie.split(';')
      .map(c => c.trim())
      .find(c => c.startsWith('csrftoken='))
      ?.split('=')[1];
  }

  // Listeners de interface
  searchInput.addEventListener('keyup', e => { if (e.key === 'Enter') { currentPage = 1; loadData(); }});
  itemsPerPageSelect.addEventListener('change', () => { 
    itemsPerPage = parseInt(itemsPerPageSelect.value, 10); 
    gridApi.setGridOption('paginationPageSize', itemsPerPage); // Método atualizado
    currentPage = 1; 
    loadData(); 
  });
  firstPageBtn.addEventListener('click', () => { gridApi.paginationGoToFirstPage(); updatePagination(); });
  prevPageBtn.addEventListener('click', () => { gridApi.paginationGoToPreviousPage(); updatePagination(); });
  nextPageBtn.addEventListener('click', () => { gridApi.paginationGoToNextPage(); updatePagination(); });
  lastPageBtn.addEventListener('click', () => { gridApi.paginationGoToLastPage(); updatePagination(); });
});
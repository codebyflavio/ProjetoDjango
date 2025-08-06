import { aplicarPermissoes } from './ui.js';
import { fetchUserInfo } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const usuario = await fetchUserInfo();
    
    if (!usuario || !usuario.is_authenticated) {
      window.location.href = '/login/';
      return;
    }

    aplicarPermissoes(usuario);
    console.log('Usuário logado:', usuario.username);

    // Configurações iniciais
    const API_URL = 'http://localhost:8000/api/dados/';// Adicionei barra no final
    const gridElement = document.getElementById('myGrid');
    
    // Elementos da UI
    const elements = {
      searchInput: document.getElementById('search-input'),
      itemsPerPageSelect: document.getElementById('items-per-page'),
      showingFrom: document.getElementById('showing-from'),
      showingTo: document.getElementById('showing-to'),
      totalItems: document.getElementById('total-items'),
      currentPageEl: document.getElementById('current-page'),
      totalPagesEl: document.getElementById('total-pages'),
      firstPageBtn: document.getElementById('first-page'),
      prevPageBtn: document.getElementById('prev-page'),
      nextPageBtn: document.getElementById('next-page'),
      lastPageBtn: document.getElementById('last-page')
    };

    let currentPage = 1;
    let itemsPerPage = parseInt(elements.itemsPerPageSelect.value, 10);
    let gridApi;
    let totalRecords = 0;

    // Funções auxiliares
    const dateFormatter = (params) => {
      if (!params.value) return '-';
      const date = new Date(params.value);
      return date.toLocaleDateString('pt-BR');
    };

    const getCSRFToken = () => {
      const cookie = document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='));
      return cookie ? cookie.split('=')[1] : '';
    };

    // Definição das colunas
    const columnDefs = [
      // Colunas não editáveis
      { headerName: "Ref do Desembaraço", field: "ref_giant", minWidth: 150 },
      // ... (mantenha as outras colunas como estão)
      
      // Colunas editáveis (exemplo)
      { 
        headerName: "🖉 Status de liberação", 
        field: "sostatus_releasedonholdreturned", 
        editable: usuario.tipo === 'editor', 
        cellClass: usuario.tipo === 'editor' ? 'editable-cell' : '', 
        cellEditor: 'agSelectCellEditor', 
        cellEditorParams: { 
          values: ['', 'RELEASED', 'ON_HOLD', 'RETURNED'] 
        }, 
        minWidth: 160 
      },
      // ... (mantenha as outras colunas editáveis)
    ];

    // Configuração da grid
    const gridOptions = {
      columnDefs,
      defaultColDef: {
        sortable: true,
        filter: true,
        resizable: true,
        flex: 1,
        minWidth: 120,
        wrapText: true,
        autoHeight: true,
      },
      pagination: true,
      paginationPageSize: itemsPerPage,
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

    // Inicializa a grid
    new agGrid.Grid(gridElement, gridOptions);

    // Funções principais
    async function loadData() {
      try {
        const params = new URLSearchParams({
          page: currentPage,
          page_size: itemsPerPage,
          search: elements.searchInput.value.trim()
        });

        const res = await fetch(`${API_URL}?${params.toString()}`, {
          credentials: 'include'
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        totalRecords = data.total || 0;
        gridApi.setRowData(data.resultados || []);
        updatePagination();
      } catch (err) {
        console.error('Erro ao carregar dados:', err);
        alert('Erro ao carregar dados. Tente novamente.');
      }
    }

    function updatePagination() {
      if (!gridApi) return;
      
      const current = gridApi.paginationGetCurrentPage() + 1;
      const pageSize = gridApi.paginationGetPageSize();
      const totalPages = gridApi.paginationGetTotalPages();

      const start = (current - 1) * pageSize + 1;
      const end = Math.min(current * pageSize, totalRecords);

      elements.showingFrom.textContent = start;
      elements.showingTo.textContent = end;
      elements.totalItems.textContent = totalRecords;
      elements.currentPageEl.textContent = current;
      elements.totalPagesEl.textContent = totalPages;

      elements.firstPageBtn.disabled = current === 1;
      elements.prevPageBtn.disabled = current === 1;
      elements.nextPageBtn.disabled = current === totalPages;
      elements.lastPageBtn.disabled = current === totalPages;
    }

    async function saveField(ref, field, value) {
      try {
        const csrfToken = getCSRFToken();
        const res = await fetch(`${API_URL}${ref}/`, {  // Adicionei barra no final
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include',
          body: JSON.stringify({ [field]: value }),
        });

        if (!res.ok) throw new Error('Falha ao salvar');
      } catch (err) {
        console.error('Erro ao salvar campo:', err);
        alert('Não foi possível salvar alteração: ' + err.message);
        // Reverte a mudança na grid
        gridApi.applyTransaction({ update: [event.data] });
      }
    }

    // Event listeners
    elements.searchInput.addEventListener('keyup', e => {
      if (e.key === 'Enter') {
        currentPage = 1;
        loadData();
      }
    });

    elements.itemsPerPageSelect.addEventListener('change', e => {
      itemsPerPage = parseInt(e.target.value, 10);
      gridApi.paginationSetPageSize(itemsPerPage);
      currentPage = 1;
      loadData();
    });

    elements.firstPageBtn.addEventListener('click', () => {
      gridApi.paginationGoToFirstPage();
    });

    elements.prevPageBtn.addEventListener('click', () => {
      gridApi.paginationGoToPreviousPage();
    });

    elements.nextPageBtn.addEventListener('click', () => {
      gridApi.paginationGoToNextPage();
    });

    elements.lastPageBtn.addEventListener('click', () => {
      gridApi.paginationGoToLastPage();
    });

  } catch (error) {
    console.error('Erro na inicialização:', error);
    window.location.href = '/login/';
  }
});
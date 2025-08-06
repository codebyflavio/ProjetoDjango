const API_BASE_URL = "http://localhost:8000/api-backend";

export async function fetchDados(page = 1, pageSize = 10, search = "") {
    const url = `${API_BASE_URL}/dados/?page=${page}&page_size=${pageSize}&search=${search}`;
    const response = await fetch(url, {
        credentials: 'include' // Importante para enviar cookies
    });
    return response.json();
}

export async function updateDado(ref_giant, data) {
    const url = `${API_BASE_URL}/dados/${ref_giant}/`;
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data),
        credentials: 'include'
    });
    return response.json();
}

export async function getUserInfo() {
    const response = await fetch(`${API_BASE_URL}/user-info/`, {
        credentials: 'include'
    });
    return response.json();
}

// Função para obter o token CSRF
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}
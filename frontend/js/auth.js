// js/auth.js
const AUTH_API = 'http://localhost:8000/api/';
let currentUser = null;

export async function fetchUserInfo() {
  try {
    const response = await fetch(`${AUTH_API}user-info/`, {
      credentials: 'include'  // Importante para enviar cookies de sessão
    });
    
    if (!response.ok) {
      throw new Error(`Erro HTTP! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Erro ao buscar informações do usuário:", error);
    return { is_authenticated: false };
  }
}
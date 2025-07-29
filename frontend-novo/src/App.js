import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('Carregando...');

  useEffect(() => {
    fetch('http://localhost:8000/api/exemplo/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`Erro HTTP! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => setMessage(data.mensagem))
      .catch(error => setMessage(`Erro: ${error.message}`));
  }, []);

  return (
    <div>
      <h1>Mensagem do backend:</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;

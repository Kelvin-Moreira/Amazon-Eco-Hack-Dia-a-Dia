let appConfig = null;
let chatHistory = [];

// Carrega as configurações do arquivo config.json
async function initGemmaClient() {
  try {
    const response = await fetch('config.json');
    appConfig = await response.json();
    console.log("✅ Configuração da IA carregada com sucesso.");
  } catch (error) {
    console.error("❌ Erro ao carregar config.json:", error);
  }
}

// Envia a mensagem para o backend do Gemma
async function sendToGemma(userMessage) {
  if (!appConfig) await initGemmaClient();

  // Adiciona a pergunta do usuário ao histórico local
  const glicoseLocal = JSON.parse(localStorage.getItem('ddia_glicose') || '[]');
  const ultimoRegistro = glicoseLocal[glicoseLocal.length - 1] ? `${glicoseLocal[glicoseLocal.length - 1].valor} mg/dL` : 'Não registrada';
  
  const contextoDinamico = `[Contexto atual do Sr. Raimundo - Última glicemia registrada: ${ultimoRegistro}. Remédio de uso contínuo: Metformina].`;

  // Adiciona a pergunta ao histórico local
  chatHistory.push({ role: "user", content: `${contextoDinamico} Pergunta do usuário: ${userMessage}` });

  const payload = {
    system_prompt: appConfig.system_prompt,
    messages: chatHistory.slice(-10)
  };

  try {
    const response = await fetch(appConfig.api_endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`Erro na API: ${response.statusText}`);

    const data = await response.json();
    const botReply = data.response;

    // Salva a resposta no histórico de contexto
    chatHistory.push({ role: "assistant", content: botReply });
    return botReply;

  } catch (error) {
    console.warn("⚠️ Sem resposta do servidor. Acionando modo de contingência local...");
    // Resposta de segurança local caso a conexão com a internet falhe
    return "Não consegui me conectar ao modelo Gemma no momento. Por favor, verifique sua conexão com a internet. Se estiver com sintomas graves, procure uma UPA ou ligue 192.";
  }
}

// Executa a inicialização ao carregar o script
initGemmaClient();
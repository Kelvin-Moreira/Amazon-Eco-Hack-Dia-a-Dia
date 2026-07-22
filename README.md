# Amazon-Eco-Hack-Dia-a-Dia
# Dia a Dia IA — Assistente Inteligente de Autocuidado para Diabetes 🌿🤖

O **Dia a Dia IA** é uma solução de inteligência artificial voltada para o apoio ao autocuidado de pacientes com diabetes, desenvolvida com foco especial na realidade da Região Norte (com ênfase no contexto de Rio Branco, Acre).

---

## 📌 Contexto do Problema

A gestão crônica do diabetes exige monitoramento constante, adesão rigorosa a tratamentos medicamentosos e capacidade de triagem rápida para evitar complicações agudas (como hiperglicemia severa, cetoacidose ou neuropatias). Em regiões distantes dos grandes centros urbanos ou com desafios de conectividade — como o interior e a capital do Acre —, o acesso contínuo a orientações médicas especializadas é limitado. 

Muitos pacientes enfrentam barreiras para interpretar sintomas, calcular riscos glicêmicos ou saber o momento exato de buscar atendimento de urgência em uma Unidade Básica de Saúde (UBS) ou Pronto-Socorro, dependendo de uma rede de saúde pública que muitas vezes carece de suporte digital de proximidade.

---

## 🎯 Escolha Arquitetural: A Interface Focada na Conversa com IA

Para esta versão do projeto, optamos por **simplificar a interface, mantendo apenas a tela de conversa direta com a Assistente de IA**. Essa escolha estratégica fundamenta-se nos seguintes pilares:

1. **Foco na Funcionalidade Principal (Core Value):** O valor real da solução reside na capacidade de processar linguagem natural, cruzar dados com protocolos de triagem do SUS (orientando cuidados caseiros para níveis moderados e urgência para valores $>250\text{ mg/dL}$ ou sintomas graves) e fornecer respostas humanizadas e contextualizadas.
2. **Experiência do Usuário (UX) Acessível:** Pacientes crônicos de faixas etárias mais maduras (como o perfil de atendimento simulado do Sr. Raimundo, 58 anos) beneficiam-se mais de uma interação conversacional simples, natural e por voz do que de dashboards complexos ou múltiplos menus de navegação.
3. **Isolamento e Robustez Técnica:** Reduzir o escopo para um chat centrado na API local do modelo **Gemma 2B** elimina ruídos de interface, garante estabilidade na execução assíncrona e demonstra uma arquitetura limpa de ponta a ponta (Frontend Web + Backend Flask + Inferência Local com PyTorch).

---

## 🧠 Arquitetura e Execução Offline (Local-First)

Este projeto foi construído para rodar **100% localmente**, utilizando o modelo de linguagem leve e aberto **Gemma 2B (`google/gemma-2-2b-it`)** executado diretamente na máquina do usuário via Hugging Face Transformers e PyTorch. Isso significa que, após o primeiro download dos pesos, o sistema opera de forma totalmente independente de conexão com a internet, garantindo privacidade de dados e resiliência operacional.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente na sua máquina:

### 1. Clonar o repositório e preparar o ambiente
```powershell
# Crie e ative um ambiente virtual Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

python app.py

### 🔑 Autenticação na Hugging Face (Obrigatório para o primeiro uso)
Como o modelo Gemma 2B exige a aceitação de termos na plataforma da Hugging Face:
1. Crie uma conta gratuita em [Hugging Face](https://huggingface.co/).
2. Acesse a página oficial do modelo [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it) e clique em aceitar os termos de uso (*Agree and access*).
3. Vá em **Settings ➔ Access Tokens** na sua conta e crie um token do tipo **Read**.
4. No seu terminal, faça o login executando:
   ```powershell
   hf auth login
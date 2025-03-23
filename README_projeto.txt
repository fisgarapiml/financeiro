
📘 RESUMO DO PROJETO: SISTEMA DE GESTÃO DO GRUPO FISGAR

Este projeto é um sistema de gestão completo para controle de estoque, produtos, movimentações e análises, desenvolvido com Python + Streamlit + SQLite.

📁 ESTRUTURA DE PASTAS:
- /src/
    - interface_estoque_dashboard.py      # Painel principal do módulo de estoque
    - teste.py                            # Script auxiliar de testes
- /src/pages/
    - interface_estoque.py                # Tela de controle geral de estoque
    - interface_movimentacoes.py          # Histórico de movimentações
    - interface_listagem_edicao.py        # Edição em massa
    - interface_cadastro.py               # Cadastro de produtos
    - interface_edicao.py                 # Edição individual
    - interface_estoque_entradas.py       # Registro de entradas
    - interface_estoque_saidas.py         # Registro de saídas
- contas_apagar.db                        # Banco de dados SQLite
- .venv/                                  # Ambiente virtual Python

🎨 PALETA DE CORES:
- Azul Turquesa: #40E0D0 → Módulos principais
- Amarelo Alegre: #FFD700 → Vendas
- Rosa Vibrante: #FF69B4 → Brinquedos
- Verde Limão: #32CD32 → Doces
- Laranja Energético: #FFA500 → Botões
- Roxo Criativo: #800080 → Financeiro

✅ FUNCIONALIDADES JÁ IMPLEMENTADAS:
- Painel de estoque com cards e indicadores visuais
- Menu lateral com navegação entre páginas
- Cadastro completo de produtos (simples, kit, variação)
- Edição individual e em massa (com tradução para português)
- Histórico completo de movimentações
- Entradas e saídas separadas
- Gráficos e métricas integradas ao estoque

📌 COMO EXECUTAR O PROJETO:
1. Ative seu ambiente virtual:
   - Windows: .venv\Scripts\activate
2. Execute o comando:
   streamlit run src/interface_estoque_dashboard.py

🔧 PRÓXIMAS ETAPAS:
- Finalizar integração de compras e leitura automática de XML/NFe
- Criar a tela inicial do sistema com KPIs e atalhos
- Implementar relatórios e automações no financeiro
- Aplicar autenticação de usuário (login/senha)
- Acesso web e integração com SEFAZ futuramente

🧭 IMPORTANTE:
- Todos os módulos já foram criados como chats separados e nomeados.
- Este arquivo README garante que você poderá continuar o projeto mesmo em outro computador.


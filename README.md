# Migrado - Sistema de Flashcards

## 🎯 Sobre o Projeto

O **Migrado** é um sistema completo de estudos com flashcards desenvolvido especificamente para estudantes de medicina. O sistema oferece uma interface moderna e intuitiva para criar, organizar e estudar flashcards de forma eficiente.

## 🌐 Acesso ao Sistema

**URL do Site:** http://18.228.44.133

## ✨ Funcionalidades Implementadas

### 🔐 Sistema de Autenticação
- ✅ Cadastro e login de usuários
- ✅ **NOVO**: Interface de login moderna com design glassmorphism
- ✅ **NOVO**: Animações e micro-interações na tela de login
- ✅ **NOVO**: Validação visual de formulários
- ✅ **NOVO**: Toggle de visualização de senha
- ✅ Período de teste gratuito de 24 horas
- ✅ Sistema de níveis de acesso (usuário e administrador)
- ✅ Contador de tempo de teste no topo do site
- ✅ Integração com sistema de pagamento (Mercado Pago)

### 🎨 Interface Moderna
- ✅ **NOVO**: Página inicial redesenhada com design glassmorphism
- ✅ **NOVO**: Elementos flutuantes animados no background
- ✅ **NOVO**: Cards com efeito de vidro fosco (backdrop-filter)
- ✅ **NOVO**: Animações suaves de entrada (slideUp, pulse)
- ✅ **NOVO**: Hover effects e micro-interações
- ✅ **NOVO**: Design responsivo otimizado para mobile

### 📊 Dashboard Moderno
- ✅ Interface moderna baseada no design fornecido
- ✅ Cards de estatísticas coloridos (Cards Estudados, Sequência, Precisão, Meta Diária)
- ✅ Navegação horizontal intuitiva
- ✅ Seção de ações rápidas (Estudar, Criar Novo Card)
- ✅ Atividades recentes
- ✅ Gráfico de progresso semanal
- ✅ Tutorial animado para novos usuários

### 📚 Sistema de Flashcards
- ✅ Criação, edição e exclusão de flashcards
- ✅ Categorias pré-definidas:
  - Medicina Interna
  - Cirurgia
  - Pediatria
  - Gineco e Obstetriz
  - Perguntas do Grado
- ✅ Sistema de estudo com animações
- ✅ Visualização em grade e lista
- ✅ Preview dos cards durante criação

### 💳 Sistema de Pagamento
- ✅ Integração com Mercado Pago
- ✅ Pagamento via PIX e Cartão de Crédito
- ✅ Plano Premium: R$ 49,99 por 6 meses
- ✅ Interface moderna de pagamento

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem principal
- **Flask** - Framework web
- **PostgreSQL** - Banco de dados
- **SQLAlchemy** - ORM
- **Flask-Login** - Autenticação
- **Flask-Mail** - Envio de emails
- **Flask-CORS** - Suporte a CORS

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **Bootstrap 5** - Framework CSS
- **JavaScript** - Interatividade
- **Chart.js** - Gráficos
- **Font Awesome** - Ícones

### Infraestrutura
- **Ubuntu 22.04** - Sistema operacional
- **Nginx** - Servidor web/proxy reverso
- **VPS Amazon EC2** - Hospedagem

## 📁 Estrutura do Projeto

```
flashcards_project/
├── app.py                 # Aplicação principal Flask
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── login.html        # Página de login
│   ├── register.html     # Página de cadastro
│   ├── dashboard.html    # Dashboard principal
│   ├── flashcards.html   # Gerenciamento de cards
│   └── payment.html      # Página de pagamento
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── start_app.sh         # Script de inicialização
├── nginx_config         # Configuração do Nginx
└── app.log             # Logs da aplicação
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- PostgreSQL
- Nginx

### Instalação
1. Clone o projeto
2. Instale as dependências: `pip3 install flask flask-sqlalchemy flask-login flask-mail flask-cors psycopg2-binary`
3. Configure o banco de dados PostgreSQL
4. Execute: `python3 app.py`

### Configuração do Nginx
O Nginx está configurado como proxy reverso na porta 80, redirecionando para a aplicação Flask na porta 5000.

## 🔧 Configurações

### Banco de Dados
- **Nome:** flashcards_db
- **Usuário:** flashcards_user
- **Porta:** 5432 (padrão PostgreSQL)

### Aplicação
- **Porta Flask:** 5000
- **Porta Nginx:** 80
- **Modo:** Produção

### 🔧 Melhorias Técnicas Implementadas
- ✅ **NOVO**: Configuração otimizada do Gunicorn com 3 workers
- ✅ **NOVO**: Proxy reverso Nginx configurado corretamente
- ✅ **NOVO**: Arquivo WSGI otimizado para produção
- ✅ **NOVO**: Inicialização automática do banco de dados
- ✅ **NOVO**: Templates básicos para todas as páginas (study, community, reports)
- ✅ **NOVO**: Sistema de navegação consistente
- ✅ **NOVO**: Arquivo requirements.txt para dependências
- ✅ **NOVO**: Configuração de ambiente (.env.example)
- ✅ **NOVO**: Documentação técnica atualizada

## 📋 Funcionalidades Pendentes

As seguintes funcionalidades estão na estrutura base e podem ser expandidas:

### 🔄 Sistema de Revisão
- Agendamento de revisões em 10, 15 ou 30 dias
- Página dedicada para revisões pendentes
- Algoritmo de repetição espaçada

### 👥 Comunidade Interna
- Sistema de seguidores
- Feed de publicações
- Interações (curtir, comentar, compartilhar)
- Mensagens privadas
- Compartilhamento de flashcards

### 📈 Relatórios Avançados
- Gráficos interativos de progresso
- Análise de rendimento por categoria
- Estatísticas de interações sociais
- Metas personalizadas

### ⚙️ Painel Administrativo
- Gerenciamento de usuários
- Moderação de conteúdo
- Controle de pagamentos
- Estatísticas do sistema

## 🔐 Segurança

- Senhas criptografadas com hash
- Proteção CSRF
- Validação de entrada
- Sessões seguras
- CORS configurado

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, entre em contato através dos canais disponíveis na plataforma.

---

**Desenvolvido com ❤️ para estudantes de medicina**


// frontend/script.js

// URL base da sua API Flask
const API_BASE_URL = 'http://127.0.0.1:5000/api';

let allProducts = []; // Armazenar todos os produtos do backend globalmente
let cart = JSON.parse(localStorage.getItem('futcamisasCart')) || []; // Carregar carrinho do localStorage
let currentUser = JSON.parse(localStorage.getItem('futcamisasUser')) || null; // Carregar usuário logado
// Variáveis para gerenciar dados nas telas de administração (para evitar recarregar tudo sempre)
let currentProductsInAdmin = [];
let currentUsersInAdmin = [];
let currentSalesInAdmin = [];
let currentStockInAdmin = [];

// --- Variáveis de elementos HTML (para melhor organização e acesso) ---
// Seções principais
const loginRegisterPage = document.getElementById('login-register-page');
const homeProductsSection = document.getElementById('home-products-section'); // Contém Hero, Featured, Products
const productDetailPage = document.getElementById('product-detail-page');
const cartPage = document.getElementById('cart-page-section');
const profilePage = document.getElementById('profile-page-section');
const adminDashboardPage = document.getElementById('admin-dashboard-section');
const adminManageUsersPage = document.getElementById('admin-manage-users');
const adminManageProductsPage = document.getElementById('admin-manage-products');
const adminManageSalesPage = document.getElementById('admin-manage-sales');
const adminManageStockPage = document.getElementById('admin-manage-stock');

// Navbar links e elementos de UI
const navHomeLink = document.getElementById('nav-home-link');
const navProductsLink = document.getElementById('nav-products-link');
const navCartLink = document.getElementById('nav-cart-link');
const navProfileLink = document.getElementById('nav-profile-link');
const navAdminLink = document.getElementById('nav-admin-link');
const navLoginLink = document.getElementById('nav-login-link');
const navLogoutLink = document.getElementById('nav-logout-link');
const logoutBtn = document.getElementById('logout-btn');
const cartItemCountSpan = document.getElementById('cart-item-count');

// Modais e seus botões
const registerModal = document.getElementById('register-modal');
const showRegisterModalBtn = document.getElementById('show-register-modal');
const closeRegisterModalBtn = document.getElementById('close-register-modal');
const userFormModal = document.getElementById('user-form-modal');
const closeUserFormModalBtn = document.getElementById('close-user-form-modal');
const productFormModal = document.getElementById('product-form-modal');
const closeProductFormModalBtn = document.getElementById('close-product-form-modal');

// Forms de Login/Cadastro/Perfil/Gerenciamento
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const profileForm = document.getElementById('profile-form');
const userManagementForm = document.getElementById('user-management-form');
const productManagementForm = document.getElementById('product-management-form');

// Campos de mensagem (feedback ao usuário)
const loginMessage = document.getElementById('login-message');
const registerMessage = document.getElementById('register-message');
const profileMessage = document.getElementById('profile-message');
const usersManagementMessage = document.getElementById('users-management-message');
const productsManagementMessage = document.getElementById('products-management-message');
const salesManagementMessage = document.getElementById('sales-management-message');
const stockManagementMessage = document.getElementById('stock-management-message');
const userFormMessage = document.getElementById('user-form-message');
const productFormMessage = document.getElementById('product-form-message');


// --- Funções de Utilidade Geral ---

// Exibe mensagens de feedback (sucesso/erro) em um elemento específico
function showMessage(element, message, type) {
    element.innerText = message;
    element.className = `message-box ${type}`; // Adiciona classe 'success' ou 'error'
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
        element.innerText = ''; // Limpa a mensagem
    }, 5000); // Esconde a mensagem após 5 segundos
}

// Habilita/Desabilita botões e mostra spinner durante requisições assíncronas
function setButtonLoading(button, isLoading, originalText) {
    if (isLoading) {
        button.dataset.originalText = button.innerHTML; // Salva o texto original
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...';
    } else {
        button.disabled = false;
        button.innerHTML = originalText || button.dataset.originalText || 'Salvar'; // Restaura o texto original
    }
}

// --- Funções de Gerenciamento de Seções da Página ---
function hideAllSections() {
    document.querySelectorAll('main section').forEach(section => {
        section.style.display = 'none';
    });
}

// Atualiza a visibilidade dos links da navbar com base no status de login e tipo de usuário
function updateNavbarVisibility() {
    if (currentUser) {
        navLoginLink.style.display = 'none';
        navLogoutLink.style.display = 'block';
        navProfileLink.style.display = 'block';
        if (currentUser.type === 'funcionario') {
            navAdminLink.style.display = 'block';
        } else {
            navAdminLink.style.display = 'none';
        }
    } else {
        navLoginLink.style.display = 'block';
        navLogoutLink.style.display = 'none';
        navProfileLink.style.display = 'none';
        navAdminLink.style.display = 'none';
    }
}

// Mostra a tela de login/cadastro
function showLoginPage() {
    hideAllSections();
    loginRegisterPage.style.display = 'flex';
    registerModal.style.display = 'none'; // Garante que o modal de cadastro esteja oculto
    updateNavbarVisibility();
}

// Mostra a página principal (Home, Destaques, Catálogo de Produtos)
function showHomePage() {
    hideAllSections();
    homeProductsSection.style.display = 'block'; // Contém Hero, Featured, Products (flex)
    // As sub-seções dentro de homeProductsSection já são exibidas pelo CSS/JS
    updateNavbarVisibility();
    fetchProducts(); // Garante que os produtos sejam carregados para o catálogo
}

// Mostra a página de listagem de produtos completa (igual à home no layout atual)
function showProductsListingPage() {
    showHomePage(); // Reutiliza a função que já exibe o catálogo principal
}

// Mostra a página do carrinho
function showCartPage() {
    hideAllSections();
    cartPage.style.display = 'block';
    renderCart(); // Garante que o carrinho esteja atualizado ao entrar
    updateNavbarVisibility();
}

// Mostra a página de perfil do usuário
function showProfilePage() {
    if (!currentUser) { // Redireciona para login se não estiver logado
        showLoginPage();
        return;
    }
    hideAllSections();
    profilePage.style.display = 'flex';
    // Preenche os campos do formulário de perfil
    document.getElementById('profile-name').value = currentUser.name;
    document.getElementById('profile-cpf').value = currentUser.cpf || ''; // CPF pode ser opcionalmente vazio
    document.getElementById('profile-email').value = currentUser.email;
    // Limpa campos de senha ao abrir
    document.getElementById('profile-password').value = '';
    document.getElementById('profile-new-password').value = '';
    document.getElementById('profile-confirm-new-password').value = '';
    updateNavbarVisibility();
}

// Mostra o painel de administração (apenas para funcionários)
function showAdminDashboard() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminDashboardPage.style.display = 'block';
        updateNavbarVisibility();
    } else {
        alert("Acesso negado. Você não tem permissão para acessar o painel de administração.");
        showHomePage(); // Redireciona para a home
    }
}

// Mostra a tela de gerenciamento de usuários (Admin)
function showAdminManageUsers() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageUsersPage.style.display = 'block';
        fetchUsers(); // Carrega usuários para a tabela
    } else {
        alert("Acesso negado.");
        showHomePage();
    }
}

// Mostra a tela de gerenciamento de produtos (Admin)
function showAdminManageProducts() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageProductsPage.style.display = 'block';
        fetchAllProductsForAdmin(); // Carrega todos os produtos para admin
    } else {
        alert("Acesso negado.");
        showHomePage();
    }
}

// Mostra a tela de gerenciamento de vendas (Admin)
function showAdminManageSales() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageSalesPage.style.display = 'block';
        fetchAllSales(); // Carrega todas as vendas
    } else {
        alert("Acesso negado.");
        showHomePage();
    }
}

// Mostra a tela de gerenciamento de estoque (Admin)
function showAdminManageStock() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageStockPage.style.display = 'block';
        fetchAllStock(); // Carrega o estoque detalhado
    } else {
        alert("Acesso negado.");
        showHomePage();
    }
}

// --- Funções de Autenticação (Login/Cadastro) ---

// Lida com o envio do formulário de Login
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Impede o recarregamento da página
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const loginButton = loginForm.querySelector('button[type="submit"]');

    setButtonLoading(loginButton, true, "Entrar"); // Mostra spinner no botão
    loginMessage.style.display = 'none'; // Esconde mensagens anteriores

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, senha: password })
        });

        const data = await response.json(); // Tenta ler a resposta JSON
        if (response.ok) { // Verifica se a resposta HTTP é 2xx (Sucesso)
            showMessage(loginMessage, data.message, 'success');
            // Armazena informações do usuário logado localmente
            currentUser = {
                id: data.user.id,
                name: data.user.name,
                email: data.user.email,
                type: data.user.type || 'cliente' // Assume 'cliente' se o tipo não for especificado
            };
            localStorage.setItem('futcamisasUser', JSON.stringify(currentUser)); // Persiste no localStorage

            updateNavbarVisibility(); // Atualiza a navbar (links de perfil/admin)
            setTimeout(() => {
                showHomePage(); // Redireciona para a home/catálogo após login bem-sucedido
            }, 500); // Pequeno atraso para a mensagem ser lida
        } else {
            // Lida com erros do backend (ex: 401 Unauthorized)
            showMessage(loginMessage, data.message || "Erro desconhecido ao fazer login.", 'error');
        }
    } catch (error) {
        console.error("Erro de conexão ou JSON inválido ao fazer login:", error);
        showMessage(loginMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    } finally {
        setButtonLoading(loginButton, false, "Entrar"); // Restaura o botão
    }
});


// Lida com a exibição do modal de cadastro
showRegisterModalBtn.addEventListener('click', () => {
    registerModal.style.display = 'flex'; // Exibe o modal como flex para centralizar
    registerForm.reset(); // Limpa o formulário ao abrir
    registerMessage.style.display = 'none'; // Esconde mensagens anteriores
});

// Lida com o fechamento do modal de cadastro
closeRegisterModalBtn.addEventListener('click', () => {
    registerModal.style.display = 'none';
    registerForm.reset(); // Limpa o formulário
    registerMessage.style.display = 'none';
});

// Fecha modais clicando fora
window.addEventListener('click', (event) => {
    if (event.target == registerModal) {
        registerModal.style.display = 'none';
        registerForm.reset();
        registerMessage.style.display = 'none';
    }
    if (event.target == userFormModal) {
        userFormModal.style.display = 'none';
        userManagementForm.reset();
        userFormMessage.style.display = 'none';
        // Limpa campo de nova senha (que pode não existir no HTML)
        const newPasswordField = document.getElementById('user-new-password-field');
        if (newPasswordField) newPasswordField.value = '';
        const confirmNewPasswordField = document.getElementById('user-confirm-new-password-field');
        if (confirmNewPasswordField) confirmNewPasswordField.value = '';
    }
    if (event.target == productFormModal) {
        productFormModal.style.display = 'none';
        productManagementForm.reset();
        productFormMessage.style.display = 'none';
        // Limpa campos de tamanho/quantidade gerados dinamicamente
        document.getElementById('sizes-quantities-container').innerHTML = '';
    }
});

// Lida com o envio do formulário de Cadastro
registerForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Impede o recarregamento da página
    const name = document.getElementById('register-name').value;
    const cpf = document.getElementById('register-cpf').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const registerButton = registerForm.querySelector('button[type="submit"]');

    if (password !== confirmPassword) {
        showMessage(registerMessage, "As senhas não coincidem.", 'error');
        return;
    }
    // Validação básica de CPF (apenas números, 11 dígitos)
    if (!/^\d{11}$/.test(cpf)) {
        showMessage(registerMessage, "CPF deve conter 11 dígitos numéricos.", 'error');
        return;
    }

    setButtonLoading(registerButton, true, "Cadastrar"); // Mostra spinner
    registerMessage.style.display = 'none'; // Esconde mensagens anteriores

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/registrar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: name, cpf: cpf, email: email, senha: password, tipo: 'cliente' })
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(registerMessage, data.message, 'success');
            registerForm.reset(); // Limpa o formulário
            // Opcional: Fechar modal e ir para login com email preenchido
            setTimeout(() => {
                registerModal.style.display = 'none';
                document.getElementById('login-email').value = email; // Preenche email para login fácil
                loginMessage.style.display = 'none'; // Limpa a mensagem de login
            }, 2000); // Pequeno atraso para a mensagem ser lida
        } else {
            // Lida com erros do backend (ex: 409 Conflict - email/CPF já existe)
            showMessage(registerMessage, data.message || "Erro desconhecido ao registrar.", 'error');
        }
    } catch (error) {
        console.error("Erro de conexão ou JSON inválido ao registrar:", error);
        showMessage(registerMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    } finally {
        setButtonLoading(registerButton, false, "Cadastrar"); // Restaura o botão
    }
});


// --- Lógica de Logout ---
logoutBtn.addEventListener('click', handleLogout);

function handleLogout() {
    currentUser = null;
    localStorage.removeItem('futcamisasUser'); // Limpa usuário do localStorage
    localStorage.removeItem('futcamisasCart'); // Limpa carrinho também no logout
    cart = []; // Limpa o array do carrinho em memória
    updateCartItemCount(); // Zera o contador do carrinho
    updateNavbarVisibility(); // Atualiza a navbar para mostrar links de login
    showLoginPage(); // Volta para a página de login
    alert("Você foi desconectado(a)."); // Um alert simples para feedback
}

// --- Perfil do Usuário ---
profileForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (!currentUser) {
        showMessage(profileMessage, "Nenhum usuário logado.", 'error');
        return;
    }

    const name = document.getElementById('profile-name').value;
    const email = document.getElementById('profile-email').value;
    const currentPassword = document.getElementById('profile-password').value;
    const newPassword = document.getElementById('profile-new-password').value;
    const confirmNewPassword = document.getElementById('profile-confirm-new-password').value;
    const saveButton = profileForm.querySelector('button[type="submit"]');

    if (newPassword && newPassword !== confirmNewPassword) {
        showMessage(profileMessage, "As novas senhas não coincidem.", 'error');
        return;
    }
    // Validação básica de email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(profileMessage, "Por favor, insira um email válido.", 'error');
        return;
    }

    setButtonLoading(saveButton, true, "Salvar Alterações");
    profileMessage.style.display = 'none';

    const updateData = {
        password: currentPassword, // Senha atual é obrigatória para validação no backend
        new_name: name,
        new_email: email,
        new_password: newPassword || null // Envia null se a nova senha estiver vazia
    };

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/${currentUser.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(profileMessage, data.message, 'success');
            // Atualiza o usuário localmente e no localStorage
            currentUser.name = name;
            currentUser.email = email;
            localStorage.setItem('futcamisasUser', JSON.stringify(currentUser));
            // Limpa campos de senha para segurança
            document.getElementById('profile-password').value = '';
            document.getElementById('profile-new-password').value = '';
            document.getElementById('profile-confirm-new-password').value = '';
            updateNavbarVisibility(); // Atualiza a navbar caso o email mude
        } else {
            showMessage(profileMessage, data.message || "Erro desconhecido ao atualizar perfil.", 'error');
        }
    } catch (error) {
        console.error("Erro de conexão ou JSON inválido ao atualizar perfil:", error);
        showMessage(profileMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    } finally {
        setButtonLoading(saveButton, false, "Salvar Alterações");
    }
});


// --- Funções de Busca e Renderização de Produtos (Catálogo) ---
async function fetchProducts() {
    const allProductsGrid = document.getElementById('all-products-grid');
    const featuredProductsGrid = document.getElementById('featured-products-grid');
    // Mostra spinners enquanto carrega
    if (allProductsGrid) allProductsGrid.innerHTML = '<div class="spinner"></div>';
    if (featuredProductsGrid) featuredProductsGrid.innerHTML = '<div class="spinner"></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const products = await response.json();
        allProducts = products; // Salva todos os produtos globalmente

        console.log("Produtos do backend:", allProducts);

        // Renderiza os produtos nas seções após aplicar filtros (iniciais)
        applyFilters(); // Esta função chamará renderAllProducts
        // Renderiza 4 produtos na seção "Camisas em Destaque"
        renderFeaturedProducts(allProducts.slice(0, 4));

    } catch (error) {
        console.error("Erro ao buscar produtos:", error);
        if (allProductsGrid) allProductsGrid.innerHTML = '<p style="text-align: center; width: 100%;">Erro ao carregar produtos. Tente novamente mais tarde.</p>';
        if (featuredProductsGrid) featuredProductsGrid.innerHTML = '<p style="text-align: center; width: 100%;">Erro ao carregar produtos em destaque.</p>';
    }
}

// Função para renderizar produtos em uma grade específica (reutilizável)
function renderProductGrid(targetGridElement, productsToRender) {
    if (!targetGridElement) return;
    targetGridElement.innerHTML = ''; // Limpa o conteúdo existente

    if (productsToRender.length === 0) {
        targetGridElement.innerHTML = '<p style="text-align: center; width: 100%;">Nenhum produto encontrado.</p>';
        return;
    }

    productsToRender.forEach(product => {
        const imageUrl = `imagens/camisa_${product.id}.png`; // Nome da imagem baseado no ID
        // Tenta extrair o nome do time do nome da camisa (ex: "Camisa Flamengo 2024" -> "Flamengo")
        const teamNameMatch = product.nome.match(/Camisa\s([^\s]+)/i);
        const teamName = teamNameMatch ? teamNameMatch[1] : 'Time';

        // Filtra tamanhos com estoque > 0 para exibir
        const availableSizesText = Object.keys(product.tamanhos).filter(s => product.tamanhos[s] > 0).join(', ') || 'Sem estoque';

        const productCardHTML = `
            <div class="product-card">
                <img src="${imageUrl}" alt="${product.nome}" class="product-card-image"
                    onerror="this.onerror=null;this.src='imagens/placeholder_300x250.png';">
                <h3>${product.nome}</h3>
                <p class="team-name">${teamName}</p>
                <p class="price">R$ ${product.preco.toFixed(2).replace('.', ',')}</p>
                <p class="available-sizes">Disponível: ${availableSizesText}</p>
                <a href="#" class="btn view-details-btn" data-product-id="${product.id}">Detalhes</a>
            </div>
        `;
        targetGridElement.innerHTML += productCardHTML;
    });

    // Adicionar event listeners aos botões de detalhes gerados dinamicamente
    targetGridElement.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o salto da âncora
            const id = parseInt(event.target.dataset.productId);
            showProductDetailPage(id);
        });
    });
}

// Renderiza produtos na seção "Todas as camisetas" (após filtros/ordenação)
function renderAllProducts(products) {
    const allProductsGrid = document.getElementById('all-products-grid');
    renderProductGrid(allProductsGrid, products);
}

// Renderiza produtos na seção "Camisas em Destaque"
function renderFeaturedProducts(products) {
    const featuredProductsGrid = document.getElementById('featured-products-grid');
    renderProductGrid(featuredProductsGrid, products);
}

// --- Lógica dos Filtros e Ordenação ---
const teamFilter = document.getElementById('team-filter');
const searchInput = document.getElementById('search-input');
const priceRangeInput = document.getElementById('price-range');
const priceValueSpan = document.getElementById('price-value');
const popularityFilter = document.getElementById('popularity-filter'); // Para ordenação
const availabilityFilter = document.getElementById('availability-filter');
const clearFiltersBtn = document.getElementById('clear-filters-btn');


// Aplica todos os filtros e ordena os produtos
function applyFilters() {
    let productsToRender = [...allProducts]; // Copia a lista original de produtos

    // 1. Filtrar por Time
    const selectedTeam = teamFilter.value;
    if (selectedTeam) {
        productsToRender = productsToRender.filter(product =>
            product.nome.toLowerCase().includes(selectedTeam.toLowerCase())
        );
    }

    // 2. Filtrar por Busca de Nome
    const searchTerm = searchInput.value.toLowerCase().trim();
    if (searchTerm) {
        productsToRender = productsToRender.filter(product =>
            product.nome.toLowerCase().includes(searchTerm)
        );
    }

    // 3. Filtrar por Preço Máximo
    const maxPrice = parseFloat(priceRangeInput.value);
    productsToRender = productsToRender.filter(product => product.preco <= maxPrice);

    // 4. Filtrar por Disponibilidade
    const selectedAvailability = availabilityFilter.value;
    if (selectedAvailability === 'in-stock') {
        productsToRender = productsToRender.filter(product =>
            Object.values(product.tamanhos).some(qty => qty > 0) // Pelo menos 1 tamanho com estoque
        );
    } else if (selectedAvailability === 'out-of-stock') {
        productsToRender = productsToRender.filter(product =>
            // Todos os tamanhos com estoque zero OU o produto não tem tamanhos registrados
            Object.values(product.tamanhos).every(qty => qty === 0) || Object.keys(product.tamanhos).length === 0
        );
    }

    // 5. Ordenar
    const sortOption = popularityFilter.value;
    if (sortOption === 'low-to-high') {
        productsToRender.sort((a, b) => a.preco - b.preco);
    } else if (sortOption === 'high-to-low') {
        productsToRender.sort((a, b) => b.preco - a.preco);
    }
    // 'default' mantém a ordem da API
    // 'Mais virais' e 'Novidades' exigiriam campos adicionais no backend para ordenar.

    // Renderiza os produtos filtrados e ordenados
    renderAllProducts(productsToRender);
}

// Adiciona event listeners para os elementos de filtro
if (teamFilter) teamFilter.addEventListener('change', applyFilters);
if (searchInput) searchInput.addEventListener('input', applyFilters); // Filtra enquanto digita
if (priceRangeInput) {
    priceRangeInput.addEventListener('input', () => {
        priceValueSpan.textContent = parseFloat(priceRangeInput.value).toFixed(2).replace('.', ',');
    });
    priceRangeInput.addEventListener('change', applyFilters);
}
if (popularityFilter) popularityFilter.addEventListener('change', applyFilters);
if (availabilityFilter) availabilityFilter.addEventListener('change', applyFilters);

// Botão para limpar filtros
if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', () => {
        teamFilter.value = '';
        searchInput.value = '';
        priceRangeInput.value = priceRangeInput.max; // Volta para o máximo
        priceValueSpan.textContent = parseFloat(priceRangeInput.value).toFixed(2).replace('.', ',');
        popularityFilter.value = 'default';
        availabilityFilter.value = 'all';
        applyFilters(); // Aplica todos os filtros limpos
    });
}

// --- Lógica do Carrinho de Compras ---
function saveCart() {
    localStorage.setItem('futcamisasCart', JSON.stringify(cart));
    updateCartItemCount(); // Atualiza o contador no ícone do carrinho
}

function updateCartItemCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartItemCountSpan.innerText = totalItems;
}

function addToCart(product, size, quantity) {
    if (!size) {
        alert("Por favor, selecione um tamanho para adicionar ao carrinho.");
        return;
    }
    if (quantity <= 0) {
        alert("A quantidade deve ser maior que zero.");
        return;
    }
    // Verifica estoque real antes de adicionar
    const productInAllProducts = allProducts.find(p => p.id === product.id);
    if (!productInAllProducts || productInAllProducts.tamanhos[size] < quantity) {
        alert(`Estoque insuficiente para o tamanho ${size}. Disponível: ${productInAllProducts.tamanhos[size] || 0} un.`);
        return;
    }

    const existingItemIndex = cart.findIndex(item => item.id === product.id && item.size === size);

    if (existingItemIndex > -1) {
        // Item já existe no carrinho, atualiza a quantidade
        const newQtyInCart = cart[existingItemIndex].quantity + quantity;
        if (productInAllProducts.tamanhos[size] < newQtyInCart) { // Verifica se a nova quantidade total excede o estoque
            alert(`Não é possível adicionar mais. Limite de estoque para o tamanho ${size}: ${productInAllProducts.tamanhos[size]} un.`);
            return;
        }
        cart[existingItemIndex].quantity = newQtyInCart;

    } else {
        // Adiciona novo item ao carrinho
        cart.push({
            id: product.id,
            name: product.nome,
            price: product.preco,
            size: size,
            quantity: quantity,
            imageUrl: `imagens/camisa_${product.id}.png` // Imagem para o carrinho
        });
    }
    console.log("Carrinho atualizado:", cart);
    alert(`${quantity}x ${product.nome} (Tamanho: ${size}) adicionado ao carrinho!`);
    saveCart(); // Salva no localStorage
    renderCart(); // Renderiza o carrinho para refletir as mudanças
}

function removeFromCart(productId, size) {
    cart = cart.filter(item => !(item.id === productId && item.size === size));
    saveCart();
    renderCart();
    alert("Item removido do carrinho."); // Adiciona feedback visual
}

function updateCartQuantity(productId, size, newQuantity) {
    const item = cart.find(item => item.id === productId && item.size === size);
    if (item) {
        const productInAllProducts = allProducts.find(p => p.id === productId);
        // Valida contra o estoque disponível (o que está no backend)
        if (newQuantity > productInAllProducts.tamanhos[size]) {
            alert(`Quantidade máxima para o tamanho ${size} é ${productInAllProducts.tamanhos[size]} un.`);
            newQuantity = productInAllProducts.tamanhos[size]; // Limita à quantidade máxima
        }
        if (newQuantity <= 0) {
            removeFromCart(productId, size);
        } else {
            item.quantity = newQuantity;
            saveCart();
            renderCart();
        }
    }
}

function renderCart() {
    const cartItemsContainer = document.getElementById('cart-items-container');
    const cartTotalSpan = document.getElementById('cart-total');
    const emptyCartMessage = document.getElementById('empty-cart-message');

    cartItemsContainer.innerHTML = ''; // Limpa conteúdo anterior

    let total = 0;

    if (cart.length === 0) {
        emptyCartMessage.style.display = 'block';
        cartItemsContainer.appendChild(emptyCartMessage);
    } else {
        emptyCartMessage.style.display = 'none';
        cart.forEach(item => {
            total += item.price * item.quantity;
            // O max do input de quantidade no carrinho deve ser a quantidade em estoque global
            const productGlobalStock = allProducts.find(p => p.id === item.id)?.tamanhos[item.size] || 0;
            const maxQtyForCartItem = productGlobalStock;

            const cartItemHTML = `
                <div class="cart-item" data-product-id="${item.id}" data-product-size="${item.size}">
                    <img src="${item.imageUrl}" alt="${item.name}" class="cart-item-image" onerror="this.onerror=null;this.src='imagens/placeholder_100x100.png';">
                    <div class="cart-item-details">
                        <h4>${item.name} (${item.size})</h4>
                        <p class="price">R$ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}</p>
                    </div>
                    <div class="cart-item-quantity">
                        <button class="qty-minus-cart">-</button>
                        <input type="number" value="${item.quantity}" min="1" max="${maxQtyForCartItem}" class="item-quantity-input" data-product-id="${item.id}" data-product-size="${item.size}">
                        <button class="qty-plus-cart">+</button>
                    </div>
                    <button class="remove-item-btn">&times;</button>
                </div>
            `;
            cartItemsContainer.innerHTML += cartItemHTML;
        });
    }

    cartTotalSpan.innerText = total.toFixed(2).replace('.', ',');

    // Adicionar event listeners aos botões de quantidade e remover do carrinho
    document.querySelectorAll('#cart-items-container .qty-minus-cart').forEach(button => {
        button.addEventListener('click', function () {
            const cartItemDiv = this.closest('.cart-item');
            const productId = parseInt(cartItemDiv.dataset.productId);
            const productSize = cartItemDiv.dataset.productSize;
            const input = this.nextElementSibling;
            let newQuantity = parseInt(input.value) - 1;
            updateCartQuantity(productId, productSize, newQuantity);
        });
    });

    document.querySelectorAll('#cart-items-container .qty-plus-cart').forEach(button => {
        button.addEventListener('click', function () {
            const cartItemDiv = this.closest('.cart-item');
            const productId = parseInt(cartItemDiv.dataset.productId);
            const productSize = cartItemDiv.dataset.productSize;
            const input = this.previousElementSibling;
            let newQuantity = parseInt(input.value) + 1;
            updateCartQuantity(productId, productSize, newQuantity);
        });
    });

    document.querySelectorAll('#cart-items-container .item-quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            const cartItemDiv = this.closest('.cart-item');
            const productId = parseInt(cartItemDiv.dataset.productId);
            const productSize = cartItemDiv.dataset.productSize;
            let newQuantity = parseInt(this.value);
            if (isNaN(newQuantity) || newQuantity < 1) newQuantity = 1;
            updateCartQuantity(productId, productSize, newQuantity);
        });
    });

    document.querySelectorAll('#cart-items-container .remove-item-btn').forEach(button => {
        button.addEventListener('click', function () {
            const cartItemDiv = this.closest('.cart-item');
            const productId = parseInt(cartItemDiv.dataset.productId);
            const productSize = cartItemDiv.dataset.productSize; // Corrigido para data-product-size
            removeFromCart(productId, productSize);
        });
    });
}

// --- Finalizar Compra ---
document.querySelector('#cart-page-section .cart-actions .btn:last-child').addEventListener('click', async function () {
    if (cart.length === 0) {
        alert("Seu carrinho está vazio!");
        return;
    }
    if (!currentUser) {
        alert("Você precisa estar logado(a) para finalizar a compra.");
        showLoginPage(); // Redireciona para login
        return;
    }

    const confirmPurchase = confirm("Confirmar a compra dos itens no carrinho?");
    if (!confirmPurchase) {
        return;
    }

    const finalizeButton = this;
    setButtonLoading(finalizeButton, true, "Finalizar compra");

    try {
        // Prepara os itens do carrinho para o backend
        const itemsForSale = cart.map(item => ({
            produto_id: item.id,
            tamanho: item.size,
            quantidade: item.quantity,
            preco_unitario: item.price
        }));

        const response = await fetch(`${API_BASE_URL}/vendas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                usuario_id: currentUser.id,
                carrinho: itemsForSale
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            cart = []; // Limpa o carrinho após a compra
            saveCart(); // Salva o carrinho vazio no localStorage
            renderCart(); // Atualiza a exibição do carrinho
            fetchProducts(); // Recarrega os produtos para atualizar o estoque visível
            showHomePage(); // Volta para a tela principal
        } else {
            alert(`Erro ao finalizar compra: ${data.message || "Erro desconhecido."}`);
        }
    } catch (error) {
        console.error("Erro na comunicação para finalizar compra:", error);
        alert("Erro de conexão ao finalizar compra. Tente novamente.");
    } finally {
        setButtonLoading(finalizeButton, false, "Finalizar compra");
    }
});


// --- Funções de Gerenciamento do Painel Admin ---

// --- Gerenciamento de Usuários ---
async function fetchUsers() {
    usersManagementMessage.style.display = 'none';
    const usersTableBody = document.querySelector('#users-table tbody');
    usersTableBody.innerHTML = '<tr><td colspan="6"><div class="spinner"></div></td></tr>'; // Loading spinner

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentUsersInAdmin = await response.json(); // Guarda para edição
        renderUsersTable(currentUsersInAdmin);
    } catch (error) {
        console.error("Erro ao buscar usuários:", error);
        showMessage(usersManagementMessage, "Erro ao carregar usuários.", 'error');
        usersTableBody.innerHTML = '<tr><td colspan="6">Nenhum usuário encontrado.</td></tr>';
    }
}

function renderUsersTable(users) {
    const usersTableBody = document.querySelector('#users-table tbody');
    usersTableBody.innerHTML = '';
    if (users.length === 0) {
        usersTableBody.innerHTML = '<tr><td colspan="6">Nenhum usuário cadastrado.</td></tr>';
        return;
    }
    users.forEach(user => {
        const row = `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.cpf}</td>
                <td>${user.email}</td>
                <td>${user.type}</td>
                <td class="action-buttons">
                    <button class="edit-user-btn" data-user-id="${user.id}"><i class="fas fa-edit"></i></button>
                    <button class="delete-user-btn" data-user-id="${user.id}"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
        usersTableBody.innerHTML += row;
    });

    // Adicionar event listeners para botões de editar/deletar
    usersTableBody.querySelectorAll('.edit-user-btn').forEach(btn => btn.addEventListener('click', (e) => openUserFormModal(parseInt(e.currentTarget.dataset.userId))));
    usersTableBody.querySelectorAll('.delete-user-btn').forEach(btn => btn.addEventListener('click', (e) => deleteUserConfirmation(parseInt(e.currentTarget.dataset.userId))));
}

// Abrir modal de usuário para adicionar/editar
function openUserFormModal(userId = null) {
    userManagementForm.reset();
    userFormMessage.style.display = 'none';
    document.getElementById('user-id-field').value = ''; // Limpa o ID oculto
    document.getElementById('user-password-field').required = true; // Senha é sempre necessária para cadastro ou confirmação
    // Campos opcionais para nova senha (para edição)
    let newPasswordField = document.getElementById('user-new-password-field'); // Certifique-se que estes campos existam no HTML
    let confirmNewPasswordField = document.getElementById('user-confirm-new-password-field');
    if (newPasswordField) newPasswordField.value = '';
    if (confirmNewPasswordField) confirmNewPasswordField.value = '';


    if (userId) { // Modo edição
        document.getElementById('user-modal-title').innerText = 'Editar Usuário';
        const user = currentUsersInAdmin.find(u => u.id === userId);
        if (user) {
            document.getElementById('user-id-field').value = user.id;
            document.getElementById('user-name-field').value = user.name;
            document.getElementById('user-cpf-field').value = user.cpf;
            document.getElementById('user-email-field').value = user.email;
            document.getElementById('user-type-field').value = user.type;
            document.getElementById('user-password-field').placeholder = 'Confirme a senha atual';
        }
    } else { // Modo adicionar
        document.getElementById('user-modal-title').innerText = 'Adicionar Novo Usuário';
        document.getElementById('user-password-field').placeholder = 'Senha do novo usuário';
    }
    userFormModal.style.display = 'flex'; // Exibe o modal
}

// Lidar com o formulário de adicionar/editar usuário
userManagementForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const userId = document.getElementById('user-id-field').value; // Estará vazio para novo usuário
    const name = document.getElementById('user-name-field').value;
    const cpf = document.getElementById('user-cpf-field').value;
    const email = document.getElementById('user-email-field').value;
    const password = document.getElementById('user-password-field').value; // Senha atual para edição ou senha para novo
    const type = document.getElementById('user-type-field').value;

    const newPasswordField = document.getElementById('user-new-password-field');
    const confirmNewPasswordField = document.getElementById('user-confirm-new-password-field');

    if (newPasswordField && newPasswordField.value && newPasswordField.value !== confirmNewPasswordField.value) {
        showMessage(userFormMessage, "As novas senhas não coincidem.", 'error');
        return;
    }
    if (!userId && !password) { // Para novo usuário, senha é obrigatória
        showMessage(userFormMessage, "A senha é obrigatória para novos usuários.", 'error');
        return;
    }
    if (!/^\d{11}$/.test(cpf)) {
        showMessage(userFormMessage, "CPF deve conter 11 dígitos numéricos.", 'error');
        return;
    }


    const submitButton = userManagementForm.querySelector('button[type="submit"]');
    setButtonLoading(submitButton, true, "Salvar");
    userFormMessage.style.display = 'none';

    let url = `${API_BASE_URL}/usuarios`;
    let method = 'POST';
    let bodyData = {};

    if (userId) { // Modo edição (PUT)
        url = `${API_BASE_URL}/usuarios/${userId}`;
        method = 'PUT';
        bodyData = {
            password: password, // Senha atual para validação no backend
            new_name: name,
            new_email: email,
            new_tipo: type
        };
        if (newPasswordField && newPasswordField.value) { // Se nova senha foi fornecida
            bodyData.new_password = newPasswordField.value;
        }
        // CPF não editável via PUT nesta API (se for, precisaria do campo no bodyData)
    } else { // Modo adicionar (POST)
        bodyData = { nome: name, cpf: cpf, email: email, senha: password, tipo: type };
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(userFormMessage, data.message, 'success');
            userFormModal.style.display = 'none';
            fetchUsers(); // Recarrega a tabela de usuários
        } else {
            showMessage(userFormMessage, data.message || "Erro desconhecido ao salvar usuário.", 'error');
        }
    } catch (error) {
        console.error("Erro ao salvar usuário:", error);
        showMessage(userFormMessage, "Erro de conexão. Tente novamente.", 'error');
    } finally {
        setButtonLoading(submitButton, false, "Salvar");
    }
});

// Excluir Usuário (Confirmação)
async function deleteUserConfirmation(userId) {
    const user = currentUsersInAdmin.find(u => u.id === userId);
    if (!user) {
        showMessage(usersManagementMessage, "Usuário não encontrado.", 'error');
        return;
    }

    if (!confirm(`Tem certeza que deseja excluir o usuário: ${user.name} (ID: ${user.id})?`)) {
        return;
    }

    const passwordConfirmation = prompt("Por favor, digite a senha do usuário logado (Admin) para confirmar a exclusão:"); // Para segurança da operação

    if (!passwordConfirmation) {
        alert("Exclusão cancelada. Senha é obrigatória.");
        return;
    }
    // Em uma aplicação real, a senha confirmada aqui seria comparada com a senha do ADMIN LOGADO,
    // não com a senha do usuário a ser excluído. Ou a API exigiria token de admin.

    usersManagementMessage.style.display = 'none';
    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/${userId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: passwordConfirmation }) // Envia a senha para validação no backend
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(usersManagementMessage, data.message, 'success');
            fetchUsers(); // Recarrega a tabela
        } else {
            showMessage(usersManagementMessage, data.message || "Erro desconhecido ao deletar usuário.", 'error');
        }
    } catch (error) {
        console.error("Erro ao deletar usuário:", error);
        showMessage(usersManagementMessage, "Erro de conexão ao deletar usuário.", 'error');
    }
}


// --- Gerenciamento de Produtos (Admin) ---
async function fetchAllProductsForAdmin() {
    productsManagementMessage.style.display = 'none';
    const productsTableBody = document.querySelector('#products-table tbody');
    productsTableBody.innerHTML = '<tr><td colspan="5"><div class="spinner"></div></td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentProductsInAdmin = await response.json(); // Guarda para edição
        renderProductsTable(currentProductsInAdmin);
    } catch (error) {
        console.error("Erro ao buscar produtos para admin:", error);
        showMessage(productsManagementMessage, "Erro ao carregar produtos.", 'error');
        productsTableBody.innerHTML = '<tr><td colspan="5">Nenhum produto encontrado.</td></tr>';
    }
}

function renderProductsTable(products) {
    const productsTableBody = document.querySelector('#products-table tbody');
    productsTableBody.innerHTML = '';
    if (products.length === 0) {
        productsTableBody.innerHTML = '<tr><td colspan="5">Nenhum produto cadastrado.</td></tr>';
        return;
    }
    products.forEach(product => {
        const availableSizesText = Object.keys(product.tamanhos).filter(s => product.tamanhos[s] > 0).map(s => `${s} (${product.tamanhos[s]})`).join(', ') || 'N/A (Sem estoque)';
        const row = `
            <tr>
                <td>${product.id}</td>
                <td>${product.nome}</td>
                <td>R$ ${product.preco.toFixed(2).replace('.', ',')}</td>
                <td>${availableSizesText}</td>
                <td class="action-buttons">
                    <button class="edit-product-btn" data-product-id="${product.id}"><i class="fas fa-edit"></i></button>
                    <button class="delete-product-btn" data-product-id="${product.id}"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
        productsTableBody.innerHTML += row;
    });

    // Adicionar event listeners para botões de editar/deletar
    productsTableBody.querySelectorAll('.edit-product-btn').forEach(btn => btn.addEventListener('click', (e) => openProductFormModal(parseInt(e.currentTarget.dataset.productId))));
    productsTableBody.querySelectorAll('.delete-product-btn').forEach(btn => btn.addEventListener('click', (e) => deleteProductConfirmation(parseInt(e.currentTarget.dataset.productId))));
}

// Abrir modal de produto para adicionar/editar
function openProductFormModal(productId = null) {
    productManagementForm.reset();
    productFormMessage.style.display = 'none';
    document.getElementById('product-id-field').value = '';
    document.getElementById('sizes-quantities-container').innerHTML = ''; // Limpa campos de tamanho/quantidade existentes

    if (productId) { // Modo edição
        document.getElementById('product-modal-title').innerText = 'Editar Produto';
        const product = currentProductsInAdmin.find(p => p.id === productId);
        if (product) {
            document.getElementById('product-id-field').value = product.id;
            document.getElementById('product-name-field').value = product.nome;
            document.getElementById('product-price-field').value = product.preco;
            // Popula tamanhos e quantidades existentes para edição
            // Converte o objeto de estoque para campos de input
            for (const size in product.tamanhos) {
                addSizeQuantityField(size, product.tamanhos[size]);
            }
        }
    } else { // Modo adicionar
        document.getElementById('product-modal-title').innerText = 'Adicionar Novo Produto';
        addSizeQuantityField(); // Adiciona um campo vazio para começar
    }
    productFormModal.style.display = 'flex'; // Exibe o modal
}

// Adicionar campos de tamanho e quantidade dinamicamente no modal de produto
function addSizeQuantityField(initialSize = '', initialQty = '') {
    const container = document.getElementById('sizes-quantities-container');
    const div = document.createElement('div');
    div.className = 'input-group size-qty-pair';
    div.innerHTML = `
        <label for="size-${Date.now()}" style="display: none;">Tamanho:</label> <!-- Hidden label -->
        <input type="text" class="product-size-field" value="${initialSize}" placeholder="Ex: P, M, G" required style="width: 45%; display: inline-block;">
        <label for="qty-${Date.now()}" style="display: none;">Quantidade:</label> <!-- Hidden label -->
        <input type="number" class="product-qty-field" value="${initialQty}" min="0" required style="width: 45%; display: inline-block; margin-left: 5px;">
        <button type="button" class="btn btn-secondary remove-size-qty-field" style="width: auto; margin-left: 5px; background: none; color: var(--red-alert); border: none;"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(div);

    // Adicionar evento para remover campo
    div.querySelector('.remove-size-qty-field').addEventListener('click', () => div.remove());
}

// Event listener para o botão "Adicionar Tamanho" no modal de produto
document.getElementById('add-size-qty-field').addEventListener('click', () => addSizeQuantityField());

// Lidar com o formulário de adicionar/editar produto
productManagementForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const productId = document.getElementById('product-id-field').value;
    const name = document.getElementById('product-name-field').value;
    const price = parseFloat(document.getElementById('product-price-field').value);

    const sizesQuantities = {};
    let isValidSizes = true;
    document.querySelectorAll('.size-qty-pair').forEach(pair => {
        const sizeInput = pair.querySelector('.product-size-field');
        const qtyInput = pair.querySelector('.product-qty-field');
        const size = sizeInput.value.trim().toUpperCase();
        const qty = parseInt(qtyInput.value);

        if (size && !isNaN(qty)) {
            if (sizesQuantities[size]) { // Evita tamanhos duplicados
                showMessage(productFormMessage, `Tamanho '${size}' duplicado. Por favor, remova ou combine.`, 'error');
                isValidSizes = false;
                return;
            }
            sizesQuantities[size] = qty;
        } else if (!size && !isNaN(qty)) { // Se tem quantidade mas não tamanho
            showMessage(productFormMessage, "Um tamanho não pode ter quantidade sem um nome.", 'error');
            isValidSizes = false;
            return;
        } else if (size && isNaN(qty)) { // Se tem tamanho mas não quantidade
            showMessage(productFormMessage, "Um tamanho precisa de uma quantidade válida.", 'error');
            isValidSizes = false;
            return;
        }
    });

    if (!isValidSizes) {
        setButtonLoading(productManagementForm.querySelector('button[type="submit"]'), false, "Salvar");
        return;
    }
    if (Object.keys(sizesQuantities).length === 0) {
        showMessage(productFormMessage, "Pelo menos um tamanho e quantidade são obrigatórios.", 'error');
        setButtonLoading(productManagementForm.querySelector('button[type="submit"]'), false, "Salvar");
        return;
    }

    const submitButton = productManagementForm.querySelector('button[type="submit"]');
    setButtonLoading(submitButton, true, "Salvar");
    productFormMessage.style.display = 'none';

    let url = `${API_BASE_URL}/produtos`;
    let method = 'POST';
    let bodyData = { nome: name, preco: price, tamanhos: sizesQuantities };

    if (productId) { // Modo edição (PUT)
        url = `${API_BASE_URL}/produtos/${productId}`;
        method = 'PUT';
        bodyData = {
            nome: name,
            preco: price,
            tamanhos: sizesQuantities // Backend deve lidar com atualização/inserção de estoque
        };
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(productFormMessage, data.message, 'success');
            productFormModal.style.display = 'none';
            fetchAllProductsForAdmin(); // Recarrega a tabela de produtos
            fetchProducts(); // Recarrega o catálogo principal também
        } else {
            showMessage(productFormMessage, data.message || "Erro desconhecido ao salvar produto.", 'error');
        }
    } catch (error) {
        console.error("Erro ao salvar produto:", error);
        showMessage(productFormMessage, "Erro de conexão. Tente novamente.", 'error');
    } finally {
        setButtonLoading(submitButton, false, "Salvar");
    }
});

// Excluir Produto (Confirmação)
async function deleteProductConfirmation(productId) {
    const product = currentProductsInAdmin.find(p => p.id === productId);
    if (!product) {
        showMessage(productsManagementMessage, "Produto não encontrado.", 'error');
        return;
    }

    if (!confirm(`Tem certeza que deseja excluir o produto: ${product.nome} (ID: ${product.id})?`)) {
        return;
    }

    productsManagementMessage.style.display = 'none';
    try {
        const response = await fetch(`${API_BASE_URL}/produtos/${productId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' } // Não precisa de body para DELETE simples
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(productsManagementMessage, data.message, 'success');
            fetchAllProductsForAdmin(); // Recarrega a tabela
            fetchProducts(); // Recarrega o catálogo principal
        } else {
            showMessage(productsManagementMessage, data.message || "Erro desconhecido ao deletar produto.", 'error');
        }
    } catch (error) {
        console.error("Erro ao deletar produto:", error);
        showMessage(productsManagementMessage, "Erro de conexão ao deletar produto.", 'error');
    }
}

// --- Gerenciamento de Vendas (Admin) ---
async function fetchAllSales() {
    salesManagementMessage.style.display = 'none';
    const salesTableBody = document.querySelector('#sales-table tbody');
    salesTableBody.innerHTML = '<tr><td colspan="7"><div class="spinner"></div></td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/vendas/todas`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentSalesInAdmin = await response.json();
        renderSalesTable(currentSalesInAdmin);
    } catch (error) {
        console.error("Erro ao buscar vendas:", error);
        showMessage(salesManagementMessage, "Erro ao carregar vendas.", 'error');
        salesTableBody.innerHTML = '<tr><td colspan="7">Nenhuma venda encontrada.</td></tr>';
    }
}

function renderSalesTable(sales) {
    const salesTableBody = document.querySelector('#sales-table tbody');
    salesTableBody.innerHTML = '';
    if (sales.length === 0) {
        salesTableBody.innerHTML = '<tr><td colspan="7">Nenhuma venda registrada.</td></tr>';
        return;
    }
    sales.forEach(sale => {
        // Mapeia os itens da venda para uma lista formatada
        const itemsList = sale.itens.map(item =>
            `${item.quantidade}x ${item.nome} (${item.tamanho}) - R$ ${item.preco_unitario.toFixed(2).replace('.', ',')}`
        ).join('<br>'); // Junta com <br> para quebrar linha no HTML

        const row = `
            <tr>
                <td>${sale.id}</td>
                <td>${new Date(sale.data).toLocaleString()}</td>
                <td>${sale.status}</td>
                <td>R$ ${sale.total.toFixed(2).replace('.', ',')}</td>
                <td>${sale.usuario.nome || 'N/A'}</td> <!-- Pode não ter nome se usuário for deletado -->
                <td>${sale.usuario.email || 'N/A'}</td>
                <td>${itemsList}</td>
            </tr>
        `;
        salesTableBody.innerHTML += row;
    });
}

// --- Gerenciamento de Estoque (Admin) ---
async function fetchAllStock() {
    stockManagementMessage.style.display = 'none';
    const stockTableBody = document.querySelector('#stock-table tbody');
    stockTableBody.innerHTML = '<tr><td colspan="5"><div class="spinner"></div></td></tr>';

    try {
        // Reutiliza a chamada de produtos para obter o estoque atualizado
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const productsWithStock = await response.json();
        currentStockInAdmin = []; // Limpa o array anterior
        productsWithStock.forEach(p => {
            for (const size in p.tamanhos) {
                currentStockInAdmin.push({
                    productId: p.id,
                    productName: p.nome,
                    size: size,
                    quantity: p.tamanhos[size]
                });
            }
        });
        renderStockTable(currentStockInAdmin);
    } catch (error) {
        console.error("Erro ao buscar estoque:", error);
        showMessage(stockManagementMessage, "Erro ao carregar estoque.", 'error');
        stockTableBody.innerHTML = '<tr><td colspan="5">Nenhum item de estoque encontrado.</td></tr>';
    }
}

function renderStockTable(stockItems) {
    const stockTableBody = document.querySelector('#stock-table tbody');
    stockTableBody.innerHTML = '';
    if (stockItems.length === 0) {
        stockTableBody.innerHTML = '<tr><td colspan="5">Nenhum item de estoque cadastrado.</td></tr>';
        return;
    }
    stockItems.forEach(item => {
        const row = `
            <tr>
                <td>${item.productId}</td>
                <td>${item.productName}</td>
                <td>${item.size}</td>
                <td><input type="number" class="stock-qty-input" data-product-id="${item.productId}" data-size="${item.size}" value="${item.quantity}" min="0"></td>
                <td class="action-buttons">
                    <button class="save-stock-qty-btn" data-product-id="${item.productId}" data-size="${item.size}" style="display:none;"><i class="fas fa-save"></i></button>
                </td>
            </tr>
        `;
        stockTableBody.innerHTML += row;
    });

    // Adicionar event listeners para atualizar estoque
    stockTableBody.querySelectorAll('.stock-qty-input').forEach(input => {
        input.addEventListener('input', function () { // Usar 'input' para feedback imediato
            const saveBtn = this.closest('tr').querySelector('.save-stock-qty-btn');
            saveBtn.style.display = 'inline-block'; // Mostra botão Salvar
        });
    });

    stockTableBody.querySelectorAll('.save-stock-qty-btn').forEach(button => {
        button.addEventListener('click', async function () {
            const productId = parseInt(this.dataset.productId);
            const size = this.dataset.size;
            const newQuantity = parseInt(this.closest('tr').querySelector('.stock-qty-input').value);

            // Validação básica
            if (isNaN(newQuantity) || newQuantity < 0) {
                showMessage(stockManagementMessage, "Quantidade inválida. Deve ser um número >= 0.", 'error');
                return;
            }

            // Acha o produto original completo do allProducts (que tem a estrutura de todos os tamanhos)
            const productToUpdate = allProducts.find(p => p.id === productId);
            if (!productToUpdate) {
                showMessage(stockManagementMessage, "Erro: Produto não encontrado para atualização de estoque.", 'error');
                return;
            }
            // Cria uma cópia do dicionário de tamanhos e atualiza apenas o tamanho modificado
            const updatedSizesDict = { ...productToUpdate.tamanhos, [size]: newQuantity };

            // O Flask PUT espera 'nome', 'preco', e o dicionário COMPLETO de 'tamanhos' para o produto
            const updatePayload = {
                nome: productToUpdate.nome,
                preco: productToUpdate.preco,
                tamanhos: updatedSizesDict
            };

            setButtonLoading(this, true, '<i class="fas fa-save"></i>'); // Mostra spinner no botão salvar
            try {
                const response = await fetch(`${API_BASE_URL}/produtos/${productId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatePayload)
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(stockManagementMessage, `Estoque de ${productToUpdate.nome} (Tam: ${size}) atualizado.`, 'success');
                    this.style.display = 'none'; // Esconde botão Salvar após sucesso
                    // Atualiza o allProducts globalmente e a exibição do catálogo
                    fetchProducts();
                    // Opcional: recarregar apenas a linha específica na tabela de estoque ou toda
                    fetchAllStock(); // Recarrega toda a tabela para refletir estado real
                } else {
                    showMessage(stockManagementMessage, data.message || "Erro desconhecido.", 'error');
                }
            } catch (error) {
                console.error("Erro ao atualizar estoque:", error);
                showMessage(stockManagementMessage, "Erro de conexão ao atualizar estoque.", 'error');
            } finally {
                setButtonLoading(this, false, '<i class="fas fa-save"></i>');
            }
        });
    });
}


// --- Event Listeners para Botões do Painel Admin ---
if (document.getElementById('manage-users-btn')) document.getElementById('manage-users-btn').addEventListener('click', showAdminManageUsers);
if (document.getElementById('manage-products-btn')) document.getElementById('manage-products-btn').addEventListener('click', showAdminManageProducts);
if (document.getElementById('manage-sales-btn')) document.getElementById('manage-sales-btn').addEventListener('click', showAdminManageSales);
if (document.getElementById('manage-stock-btn')) document.getElementById('manage-stock-btn').addEventListener('click', showAdminManageStock); // Muda a chamada para a nova função showAdminManageStock

if (document.getElementById('back-to-admin-dashboard-from-users')) document.getElementById('back-to-admin-dashboard-from-users').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-products')) document.getElementById('back-to-admin-dashboard-from-products').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-sales')) document.getElementById('back-to-admin-dashboard-from-sales').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-stock')) document.getElementById('back-to-admin-dashboard-from-stock').addEventListener('click', showAdminDashboard);


// --- Event Listeners para Modais de Gerenciamento ---
// Usuário
if (document.getElementById('add-user-modal-btn')) document.getElementById('add-user-modal-btn').addEventListener('click', () => openUserFormModal(null));
if (document.getElementById('close-user-form-modal')) document.getElementById('close-user-form-modal').addEventListener('click', () => userFormModal.style.display = 'none');
if (document.getElementById('user-form-cancel-btn')) document.getElementById('user-form-cancel-btn').addEventListener('click', () => userFormModal.style.display = 'none');

// Produto
if (document.getElementById('add-product-modal-btn')) document.getElementById('add-product-modal-btn').addEventListener('click', () => openProductFormModal(null));
if (document.getElementById('close-product-form-modal')) document.getElementById('close-product-form-modal').addEventListener('click', () => productFormModal.style.display = 'none');
if (document.getElementById('product-form-cancel-btn')) document.getElementById('product-form-cancel-btn').addEventListener('click', () => productFormModal.style.display = 'none');


// --- Inicialização da Aplicação ---
document.addEventListener('DOMContentLoaded', () => {
    updateNavbarVisibility(); // Define visibilidade da navbar com base no login
    updateCartItemCount(); // Atualiza contador de itens no carrinho

    // Decidir qual página mostrar inicialmente
    if (currentUser) {
        showHomePage(); // Se já logado, vai para o catálogo principal
    } else {
        showLoginPage(); // Se não logado, vai para a página de login
    }
});

const API_BASE_URL = 'http://127.0.0.1:5000/api';


let allProducts = [];
let cart = JSON.parse(localStorage.getItem('futcamisasCart')) || [];
let currentUser = JSON.parse(localStorage.getItem('futcamisasUser')) || null;
let currentProductsInAdmin = [];
let currentUsersInAdmin = [];
let currentSalesInAdmin = [];
let currentStockInAdmin = [];
let currentReports = [];

const loginRegisterPage = document.getElementById('login-register-page');
const homeProductsSection = document.getElementById('home-products-section');
const cartPage = document.getElementById('cart-page-section');
const profilePage = document.getElementById('profile-page-section');
const adminDashboardPage = document.getElementById('admin-dashboard-section');
const adminManageUsersPage = document.getElementById('admin-manage-users');
const adminManageProductsPage = document.getElementById('admin-manage-products');
const adminManageSalesPage = document.getElementById('admin-manage-sales');
const adminManageStockPage = document.getElementById('admin-manage-stock');
const adminViewReportsPage = document.getElementById('admin-view-reports');

const navHomeLink = document.getElementById('nav-home-link');
const navProductsLink = document.getElementById('nav-products-link');
const navCartLink = document.getElementById('nav-cart-link');
const navProfileLink = document.getElementById('nav-profile-link');
const navAdminLink = document.getElementById('nav-admin-link');
const navLoginLink = document.getElementById('nav-login-link');
const navLogoutLink = document.getElementById('nav-logout-link');
const logoutBtn = document.getElementById('logout-btn');
const cartItemCountSpan = document.getElementById('cart-item-count');

const registerModal = document.getElementById('register-modal');
const showRegisterModalBtn = document.getElementById('show-register-modal');
const closeRegisterModalBtn = document.getElementById('close-register-modal');
const userFormModal = document.getElementById('user-form-modal');
const closeUserFormModalBtn = document.getElementById('close-user-form-modal');
const productFormModal = document.getElementById('product-form-modal');
const closeProductFormModalBtn = document.getElementById('close-product-form-modal');
const productDetailModal = document.getElementById('product-detail-modal');
const closeProductDetailModalBtn = document.getElementById('close-product-detail-modal');


const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const profileForm = document.getElementById('profile-form');
const userManagementForm = document.getElementById('user-management-form');
const productManagementForm = document.getElementById('product-management-form');

const loginMessage = document.getElementById('login-message');
const registerMessage = document.getElementById('register-message');
const profileMessage = document.getElementById('profile-message');
const usersManagementMessage = document.getElementById('users-management-message');
const productsManagementMessage = document.getElementById('products-management-message');
const salesManagementMessage = document.getElementById('sales-management-message');
const stockManagementMessage = document.getElementById('stock-management-message');
const userFormMessage = document.getElementById('user-form-message');
const productFormMessage = document.getElementById('product-form-message');
const reportsMessage = document.getElementById('reports-message');


function showMessage(element, message, type) {
    element.innerText = message;
    element.className = `message-box ${type}`;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
        element.innerText = '';
    }, 5000);
}

function setButtonLoading(button, isLoading, originalText) {
    if (isLoading) {
        button.dataset.originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...';
    } else {
        button.disabled = false;
        button.innerHTML = originalText || button.dataset.originalText || 'Salvar';
    }
}

function hideAllSections() {
    document.querySelectorAll('main section').forEach(section => {
        section.style.display = 'none';
    });
}

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

function showLoginPage() {
    hideAllSections();
    loginRegisterPage.style.display = 'flex';
    registerModal.style.display = 'none';
    updateNavbarVisibility();
}

function showHomePage() {
    hideAllSections();
    homeProductsSection.style.display = 'block';
    document.getElementById('home').style.display = 'flex';
    document.getElementById('featured-products').style.display = 'block';
    document.getElementById('products').style.display = 'flex';

    updateNavbarVisibility();
    fetchProducts();
}

function showProductsListingPage() {
    showHomePage();
}

function showCartPage() {
    hideAllSections();
    cartPage.style.display = 'block';
    renderCart();
    updateNavbarVisibility();
}

function showProfilePage() {
    if (!currentUser) {
        showLoginPage();
        return;
    }
    hideAllSections();
    profilePage.style.display = 'flex';
    document.getElementById('profile-name').value = currentUser.name;
    document.getElementById('profile-cpf').value = currentUser.cpf || '';
    document.getElementById('profile-email').value = currentUser.email;
    document.getElementById('profile-password').value = '';
    document.getElementById('profile-new-password').value = '';
    document.getElementById('profile-confirm-new-password').value = '';
    updateNavbarVisibility();
}

function showAdminDashboard() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminDashboardPage.style.display = 'block';
        updateNavbarVisibility();
    } else {
        showMessage(loginMessage, "Acesso negado. Você não tem permissão para acessar o painel de administração.", 'error');
        showHomePage();
    }
}

function showAdminManageUsers() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageUsersPage.style.display = 'block';
        fetchUsers();
    } else {
        showMessage(loginMessage, "Acesso negado.", 'error');
        showHomePage();
    }
}

function showAdminManageProducts() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageProductsPage.style.display = 'block';
        fetchAllProductsForAdmin();
    } else {
        showMessage(loginMessage, "Acesso negado.", 'error');
        showHomePage();
    }
}

function showAdminManageSales() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageSalesPage.style.display = 'block';
        fetchAllSales();
    } else {
        showMessage(loginMessage, "Acesso negado.", 'error');
        showHomePage();
    }
}

function showAdminManageStock() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminManageStockPage.style.display = 'block';
        fetchAllStock();
    } else {
        showMessage(loginMessage, "Acesso negado.", 'error');
        showHomePage();
    }
}

function showAdminViewReports() {
    if (currentUser && currentUser.type === 'funcionario') {
        hideAllSections();
        adminViewReportsPage.style.display = 'block';
        fetchReports();
    } else {
        showMessage(loginMessage, "Acesso negado.", 'error');
        showHomePage();
    }
}

loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();
    const loginButton = loginForm.querySelector('button[type="submit"]');

    if (!email || !password) {
        showMessage(loginMessage, "Email e senha são obrigatórios.", 'error');
        return;
    }

    setButtonLoading(loginButton, true, "Entrar");
    loginMessage.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, senha: password })
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(loginMessage, data.message, 'success');
            currentUser = {
                id: data.user.id,
                name: data.user.name,
                email: data.user.email,
                type: data.user.type || 'cliente',
                cpf: data.user.cpf
            };
            localStorage.setItem('futcamisasUser', JSON.stringify(currentUser));

            updateNavbarVisibility();
            setTimeout(() => {
                if (currentUser.type === 'funcionario') {
                    showAdminDashboard();
                } else {
                    showHomePage();
                }
            }, 500);
        } else {
            showMessage(loginMessage, data.message || "Erro desconhecido ao fazer login.", 'error');
        }
    } catch (error) {
        console.error("Erro de conexão ou JSON inválido ao fazer login:", error);
        showMessage(loginMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    } finally {
        setButtonLoading(loginButton, false, "Entrar");
    }
});


showRegisterModalBtn.addEventListener('click', () => {
    registerModal.style.display = 'flex';
    registerForm.reset();
    registerMessage.style.display = 'none';
});

closeRegisterModalBtn.addEventListener('click', () => {
    registerModal.style.display = 'none';
    registerForm.reset();
    registerMessage.style.display = 'none';
});

closeProductDetailModalBtn.addEventListener('click', () => {
    productDetailModal.style.display = 'none';
    document.getElementById('quantity').value = 1;
});


window.addEventListener('click', (event) => {
    if (event.target === registerModal) {
        registerModal.style.display = 'none';
        registerForm.reset();
        registerMessage.style.display = 'none';
    }
    if (event.target === userFormModal) {
        userFormModal.style.display = 'none';
        userManagementForm.reset();
        userFormMessage.style.display = 'none';
        const newPasswordField = document.getElementById('user-new-password-field');
        if (newPasswordField) newPasswordField.value = '';
        const confirmNewPasswordField = document.getElementById('user-confirm-new-password-field');
        if (confirmNewPasswordField) confirmNewPasswordField.value = '';
    }
    if (event.target === productFormModal) {
        productFormModal.style.display = 'none';
        productManagementForm.reset();
        productFormMessage.style.display = 'none';
        document.getElementById('sizes-quantities-container').innerHTML = '';
    }
    if (event.target === productDetailModal) {
        productDetailModal.style.display = 'none';
        document.getElementById('quantity').value = 1;
    }
});

registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const name = document.getElementById('register-name').value.trim();
    const cpf = document.getElementById('register-cpf').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value.trim();
    const confirmPassword = document.getElementById('register-confirm-password').value.trim();
    const registerButton = registerForm.querySelector('button[type="submit"]');

    if (!name || !cpf || !email || !password || !confirmPassword) {
        showMessage(registerMessage, "Todos os campos são obrigatórios.", 'error');
        return;
    }
    if (password !== confirmPassword) {
        showMessage(registerMessage, "As senhas não coincidem.", 'error');
        return;
    }
    if (password.length < 6) {
        showMessage(registerMessage, "A senha deve ter pelo menos 6 caracteres.", 'error');
        return;
    }
    if (!/^\d{11}$/.test(cpf)) {
        showMessage(registerMessage, "CPF deve conter 11 dígitos numéricos.", 'error');
        return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(registerMessage, "Por favor, insira um email válido.", 'error');
        return;
    }

    setButtonLoading(registerButton, true, "Cadastrar");
    registerMessage.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/registrar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: name, cpf: cpf, email: email, senha: password, tipo: 'cliente' })
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(registerMessage, data.message, 'success');
            registerForm.reset();
            setTimeout(() => {
                registerModal.style.display = 'none';
                document.getElementById('login-email').value = email;
                document.getElementById('login-password').value = password;
                loginMessage.style.display = 'none';
            }, 2000);
        } else {
            showMessage(registerMessage, data.message || "Erro desconhecido ao registrar.", 'error');
        }
    } catch (error) {
        console.error("Erro de conexão ou JSON inválido ao registrar:", error);
        showMessage(registerMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    } finally {
        setButtonLoading(registerButton, false, "Cadastrar");
    }
});


logoutBtn.addEventListener('click', handleLogout);

function handleLogout() {
    currentUser = null;
    localStorage.removeItem('futcamisasUser');
    localStorage.removeItem('futcamisasCart');
    cart = [];
    updateCartItemCount();
    updateNavbarVisibility();
    showLoginPage();
    alert("Você foi desconectado(a).");
}

profileForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (!currentUser) {
        showMessage(profileMessage, "Nenhum usuário logado.", 'error');
        return;
    }

    const name = document.getElementById('profile-name').value.trim();
    const email = document.getElementById('profile-email').value.trim();
    const currentPassword = document.getElementById('profile-password').value.trim();
    const newPassword = document.getElementById('profile-new-password').value.trim();
    const confirmNewPassword = document.getElementById('profile-confirm-new-password').value.trim();
    const saveButton = profileForm.querySelector('button[type="submit"]');

    if (!name || !email || !currentPassword) {
        showMessage(profileMessage, "Nome, email e senha atual são obrigatórios.", 'error');
        return;
    }
    if (newPassword && newPassword !== confirmNewPassword) {
        showMessage(profileMessage, "As novas senhas não coincidem.", 'error');
        return;
    }
    if (newPassword && newPassword.length < 6) {
        showMessage(profileMessage, "A nova senha deve ter pelo menos 6 caracteres.", 'error');
        return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(profileMessage, "Por favor, insira um email válido.", 'error');
        return;
    }

    setButtonLoading(saveButton, true, "Salvar Alterações");
    profileMessage.style.display = 'none';

    const updateData = {
        password: currentPassword,
        new_name: name,
        new_email: email,
        new_password: newPassword || null
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
            currentUser.name = name;
            currentUser.email = email;
            localStorage.setItem('futcamisasUser', JSON.stringify(currentUser));
            document.getElementById('profile-password').value = '';
            document.getElementById('profile-new-password').value = '';
            document.getElementById('profile-confirm-new-password').value = '';
            updateNavbarVisibility();
        } else {
            showMessage(profileMessage, data.message || "Erro desconhecido ao atualizar perfil.", 'error');
        }
    }
    catch (error) {
        console.error("Erro de conexão ou JSON inválido ao atualizar perfil:", error);
        showMessage(profileMessage, "Erro de conexão com o servidor. Tente novamente.", 'error');
    }
    finally {
        setButtonLoading(saveButton, false, "Salvar Alterações");
    }
});


async function fetchProducts() {
    const allProductsGrid = document.getElementById('all-products-grid');
    const featuredProductsGrid = document.getElementById('featured-products-grid');
    if (allProductsGrid) allProductsGrid.innerHTML = '<div class="spinner" aria-label="Carregando produtos"></div>';
    if (featuredProductsGrid) featuredProductsGrid.innerHTML = '<div class="spinner" aria-label="Carregando produtos em destaque"></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const products = await response.json();
        allProducts = products;

        console.log("Produtos do backend:", allProducts);

        populateTeamFilter(allProducts);

        applyFilters();
        renderFeaturedProducts(allProducts.slice(0, 4));

    } catch (error) {
        console.error("Erro ao buscar produtos:", error);
        if (allProductsGrid) allProductsGrid.innerHTML = '<p style="text-align: center; width: 100%;">Erro ao carregar produtos. Tente novamente mais tarde.</p>';
        if (featuredProductsGrid) featuredProductsGrid.innerHTML = '<p style="text-align: center; width: 100%;">Erro ao carregar produtos em destaque.</p>';
    }
}

function populateTeamFilter(products) {
    const teamFilterSelect = document.getElementById('team-filter');
    if (!teamFilterSelect) return;

    while (teamFilterSelect.options.length > 1) {
        teamFilterSelect.remove(1);
    }

    const uniqueTeams = new Set();
    products.forEach(product => {
        const teamNameMatch = product.nome.match(/Camisa\s([^\s]+)/i);
        if (teamNameMatch && teamNameMatch[1]) {
            uniqueTeams.add(teamNameMatch[1]);
        }
    });

    Array.from(uniqueTeams).sort().forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.innerText = team;
        teamFilterSelect.appendChild(option);
    });
}

function renderProductGrid(targetGridElement, productsToRender) {
    if (!targetGridElement) return;
    targetGridElement.innerHTML = '';

    if (productsToRender.length === 0) {
        targetGridElement.innerHTML = '<p style="text-align: center; width: 100%;">Nenhum produto encontrado.</p>';
        return;
    }

    productsToRender.forEach(product => {
        const imageUrl = `imagens/camisa_${product.id}.png`;
        const teamNameMatch = product.nome.match(/Camisa\s([^\s]+)/i);
        const teamName = teamNameMatch ? teamNameMatch[1] : 'Time';

        const availableSizesCount = Object.values(product.tamanhos).filter(qty => qty > 0).length;
        const availableSizesText = availableSizesCount > 0
            ? Object.keys(product.tamanhos).filter(s => product.tamanhos[s] > 0).join(', ')
            : 'Sem estoque';

        const productCardHTML = `
            <div class="product-card" role="gridcell" aria-labelledby="product-${product.id}-name">
                <img src="${imageUrl}" alt="${product.nome}" class="product-card-image"
                    onerror="this.onerror=null;this.src='imagens/placeholder_300x250.png';"
                    aria-label="${product.nome}">
                <h3 id="product-${product.id}-name">${product.nome}</h3>
                <p class="team-name">${teamName}</p>
                <p class="price">R$ ${product.preco.toFixed(2).replace('.', ',')}</p>
                <p class="available-sizes">Disponível: ${availableSizesText}</p>
                <a href="#" class="btn view-details-btn" data-product-id="${product.id}" aria-label="Ver detalhes de ${product.nome}">Detalhes</a>
            </div>
        `;
        targetGridElement.innerHTML += productCardHTML;
    });

    targetGridElement.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', (event) => {
            event.preventDefault();
            const id = parseInt(event.target.dataset.productId);
            showProductDetailPage(id);
        });
    });
}

function renderAllProducts(products) {
    const allProductsGrid = document.getElementById('all-products-grid');
    renderProductGrid(allProductsGrid, products);
}

function renderFeaturedProducts(products) {
    const featuredProductsGrid = document.getElementById('featured-products-grid');
    renderProductGrid(featuredProductsGrid, products);
}

const teamFilter = document.getElementById('team-filter');
const searchInput = document.getElementById('search-input');
const priceRangeInput = document.getElementById('price-range');
const priceValueSpan = document.getElementById('price-value');
const popularityFilter = document.getElementById('popularity-filter');
const availabilityFilter = document.getElementById('availability-filter');
const clearFiltersBtn = document.getElementById('clear-filters-btn');


function applyFilters() {
    let productsToRender = [...allProducts];

    const selectedTeam = teamFilter.value;
    if (selectedTeam) {
        productsToRender = productsToRender.filter(product => {
            const teamNameMatch = product.nome.match(/Camisa\s([^\s]+)/i);
            return teamNameMatch && teamNameMatch[1].toLowerCase() === selectedTeam.toLowerCase();
        });
    }

    const searchTerm = searchInput.value.toLowerCase().trim();
    if (searchTerm) {
        productsToRender = productsToRender.filter(product =>
            product.nome.toLowerCase().includes(searchTerm)
        );
    }

    const maxPrice = parseFloat(priceRangeInput.value);
    productsToRender = productsToRender.filter(product => product.preco <= maxPrice);

    const selectedAvailability = availabilityFilter.value;
    if (selectedAvailability === 'in-stock') {
        productsToRender = productsToRender.filter(product =>
            Object.values(product.tamanhos).some(qty => qty > 0)
        );
    } else if (selectedAvailability === 'out-of-stock') {
        productsToRender = productsToRender.filter(product =>
            Object.values(product.tamanhos).every(qty => qty === 0) || Object.keys(product.tamanhos).length === 0
        );
    }

    const sortOption = popularityFilter.value;
    if (sortOption === 'low-to-high') {
        productsToRender.sort((a, b) => a.preco - b.preco);
    } else if (sortOption === 'high-to-low') {
        productsToRender.sort((a, b) => b.preco - a.preco);
    }

    renderAllProducts(productsToRender);
}

if (teamFilter) teamFilter.addEventListener('change', applyFilters);
if (searchInput) searchInput.addEventListener('input', applyFilters);
if (priceRangeInput) {
    priceRangeInput.addEventListener('input', () => {
        priceValueSpan.textContent = parseFloat(priceRangeInput.value).toFixed(2).replace('.', ',');
    });
    priceRangeInput.addEventListener('change', applyFilters);
}
if (popularityFilter) popularityFilter.addEventListener('change', applyFilters);
if (availabilityFilter) availabilityFilter.addEventListener('change', applyFilters);

if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', () => {
        teamFilter.value = '';
        searchInput.value = '';
        priceRangeInput.value = priceRangeInput.max;
        priceValueSpan.textContent = parseFloat(priceRangeInput.value).toFixed(2).replace('.', ',');
        popularityFilter.value = 'default';
        availabilityFilter.value = 'all';
        applyFilters();
    });
}

function saveCart() {
    localStorage.setItem('futcamisasCart', JSON.stringify(cart));
    updateCartItemCount();
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
    const productInAllProducts = allProducts.find(p => p.id === product.id);
    if (!productInAllProducts || productInAllProducts.tamanhos[size] < quantity) {
        alert(`Estoque insuficiente para o tamanho ${size}. Disponível: ${productInAllProducts.tamanhos[size] || 0} un.`);
        return;
    }

    const existingItemIndex = cart.findIndex(item => item.id === product.id && item.size === size);

    if (existingItemIndex > -1) {
        const newQtyInCart = cart[existingItemIndex].quantity + quantity;
        if (productInAllProducts.tamanhos[size] < newQtyInCart) {
            alert(`Não é possível adicionar mais. Limite de estoque para o tamanho ${size}: ${productInAllProducts.tamanhos[size]} un.`);
            return;
        }
        cart[existingItemIndex].quantity = newQtyInCart;

    } else {
        cart.push({
            id: product.id,
            name: product.nome,
            price: product.preco,
            size: size,
            quantity: quantity,
            imageUrl: `imagens/camisa_${product.id}.png`
        });
    }
    console.log("Carrinho atualizado:", cart);
    alert(`${quantity}x ${product.nome} (Tamanho: ${size}) adicionado ao carrinho!`);
    saveCart();
    renderCart();
}

function removeFromCart(productId, size) {
    cart = cart.filter(item => !(item.id === productId && item.size === size));
    saveCart();
    renderCart();
    alert("Item removido do carrinho.");
}

function updateCartQuantity(productId, size, newQuantity) {
    const item = cart.find(item => item.id === productId && item.size === size);
    if (item) {
        const productInAllProducts = allProducts.find(p => p.id === productId);
        if (newQuantity > productInAllProducts.tamanhos[size]) {
            alert(`Quantidade máxima para o tamanho ${size} é ${productInAllProducts.tamanhos[size]} un.`);
            newQuantity = productInAllProducts.tamanhos[size];
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

    cartItemsContainer.innerHTML = '';

    let total = 0;

    if (cart.length === 0) {
        emptyCartMessage.style.display = 'block';
        cartItemsContainer.appendChild(emptyCartMessage);
    } else {
        emptyCartMessage.style.display = 'none';
        cart.forEach(item => {
            total += item.price * item.quantity;
            const productGlobalStock = allProducts.find(p => p.id === item.id)?.tamanhos[item.size] || 0;
            const maxQtyForCartItem = productGlobalStock;

            const cartItemHTML = `
                <div class="cart-item" data-product-id="${item.id}" data-product-size="${item.size}" aria-label="Item no carrinho: ${item.name} tamanho ${item.size}">
                    <img src="${item.imageUrl}" alt="${item.name}" class="cart-item-image" onerror="this.onerror=null;this.src='imagens/placeholder_100x100.png';">
                    <div class="cart-item-details">
                        <h4>${item.name} (${item.size})</h4>
                        <p class="price">R$ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}</p>
                    </div>
                    <div class="cart-item-quantity">
                        <button class="qty-minus-cart" aria-label="Diminuir quantidade de ${item.name}">-</button>
                        <input type="number" value="${item.quantity}" min="1" max="${maxQtyForCartItem}" class="item-quantity-input" data-product-id="${item.id}" data-product-size="${item.size}" aria-label="Quantidade de ${item.name}">
                        <button class="qty-plus-cart" aria-label="Aumentar quantidade de ${item.name}">+</button>
                    </div>
                    <button class="remove-item-btn" aria-label="Remover ${item.name} do carrinho">&times;</button>
                </div>
            `;
            cartItemsContainer.innerHTML += cartItemHTML;
        });
    }

    cartTotalSpan.innerText = total.toFixed(2).replace('.', ',');

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
            const productSize = cartItemDiv.dataset.productSize;
            removeFromCart(productId, productSize);
        });
    });
}

document.getElementById('checkout-btn').addEventListener('click', async function () {
    if (cart.length === 0) {
        alert("Seu carrinho está vazio!");
        return;
    }
    if (!currentUser) {
        alert("Você precisa estar logado(a) para finalizar a compra.");
        showLoginPage();
        return;
    }

    const confirmPurchase = confirm("Confirmar a compra dos itens no carrinho?");
    if (!confirmPurchase) {
        return;
    }

    const finalizeButton = this;
    setButtonLoading(finalizeButton, true, "Finalizar compra");

    try {
        const itemsForSale = cart.map(item => ({
            produto_id: item.id,
            tamanho: item.size,
            quantidade: item.quantity,
            preco_unitario: item.price,
            name: item.name
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
            cart = [];
            saveCart();
            renderCart();
            fetchProducts();
            showHomePage();
        } else {
            alert(`Erro ao finalizar compra: ${data.message || "Erro desconhecido."}`);
        }
    }
    catch (error) {
        console.error("Erro na comunicação para finalizar compra:", error);
        alert("Erro de conexão ao finalizar compra. Tente novamente.");
    }
    finally {
        setButtonLoading(finalizeButton, false, "Finalizar compra");
    }
});

async function showProductDetailPage(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) {
        console.error("Produto não encontrado no cache local:", productId);
        alert("Detalhes do produto não puderam ser carregados.");
        return;
    }

    const detailProductImage = document.getElementById('detail-product-image');
    const detailProductName = document.getElementById('detail-product-name');
    const detailTeamName = document.getElementById('detail-team-name');
    const detailProductPrice = document.getElementById('detail-product-price');
    const detailProductDescription = document.getElementById('detail-product-description');
    const detailSizeSelector = document.getElementById('detail-size-selector');
    const quantityInput = document.getElementById('quantity');
    const addToCartDetailBtn = document.getElementById('add-to-cart-detail-btn');

    detailProductImage.src = `imagens/camisa_${product.id}.png`;
    detailProductImage.onerror = function () { this.onerror = null; this.src = 'imagens/placeholder_detail.png'; };
    detailProductName.innerText = product.nome;
    const teamNameMatch = product.nome.match(/Camisa\s([^\s]+)/i);
    detailTeamName.innerText = teamNameMatch ? teamNameMatch[1] : 'Time';
    detailProductPrice.innerText = `R$ ${product.preco.toFixed(2).replace('.', ',')}`;
    detailProductDescription.innerText = `Detalhes sobre a ${product.nome}. Qualidade superior e design exclusivo para torcedores apaixonados.`;

    detailSizeSelector.innerHTML = '';
    let selectedSize = null;
    const sortedSizes = Object.keys(product.tamanhos).sort((a, b) => {
        const order = { 'P': 1, 'M': 2, 'G': 3, 'GG': 4 };
        return (order[a] || 99) - (order[b] || 99);
    });

    sortedSizes.forEach(size => {
        const qty = product.tamanhos[size];
        const button = document.createElement('button');
        button.type = 'button';
        button.innerText = size;
        button.dataset.size = size;
        if (qty === 0) {
            button.disabled = true;
            button.title = "Esgotado";
        }
        button.addEventListener('click', () => {
            detailSizeSelector.querySelectorAll('button').forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            selectedSize = size;
            quantityInput.value = 1;
            quantityInput.max = qty;
        });
        detailSizeSelector.appendChild(button);
    });

    quantityInput.value = 1;
    quantityInput.max = 99;

    document.getElementById('qty-minus').onclick = () => {
        let currentQty = parseInt(quantityInput.value);
        if (currentQty > 1) {
            quantityInput.value = currentQty - 1;
        }
    };
    document.getElementById('qty-plus').onclick = () => {
        let currentQty = parseInt(quantityInput.value);
        const maxQty = parseInt(quantityInput.max);
        if (currentQty < maxQty) {
            quantityInput.value = currentQty + 1;
        }
    };

    addToCartDetailBtn.onclick = () => {
        if (!currentUser) {
            alert("Você precisa estar logado(a) para adicionar itens ao carrinho.");
            showLoginPage();
            return;
        }
        if (!selectedSize) {
            alert("Por favor, selecione um tamanho.");
            return;
        }
        const quantityToAdd = parseInt(quantityInput.value);
        addToCart(product, selectedSize, quantityToAdd);
        productDetailModal.style.display = 'none';
        document.getElementById('quantity').value = 1;
    };

    productDetailModal.style.display = 'flex';
}

async function fetchUsers() {
    usersManagementMessage.style.display = 'none';
    const usersTableBody = document.querySelector('#users-table tbody');
    usersTableBody.innerHTML = '<tr><td colspan="6"><div class="spinner" aria-label="Carregando usuários"></div></td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/usuarios`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentUsersInAdmin = await response.json();
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
                    <button class="edit-user-btn" data-user-id="${user.id}" aria-label="Editar usuário ${user.name}"><i class="fas fa-edit"></i></button>
                    <button class="delete-user-btn" data-user-id="${user.id}" aria-label="Excluir usuário ${user.name}"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
        usersTableBody.innerHTML += row;
    });

    usersTableBody.querySelectorAll('.edit-user-btn').forEach(btn => btn.addEventListener('click', (e) => openUserFormModal(parseInt(e.currentTarget.dataset.userId))));
    usersTableBody.querySelectorAll('.delete-user-btn').forEach(btn => btn.addEventListener('click', (e) => deleteUserConfirmation(parseInt(e.currentTarget.dataset.userId))));
}

function openUserFormModal(userId = null) {
    userManagementForm.reset();
    userFormMessage.style.display = 'none';
    document.getElementById('user-id-field').value = '';

    const userNewPasswordGroup = document.getElementById('user-new-password-group');
    const userConfirmNewPasswordGroup = document.getElementById('user-confirm-new-password-group');
    const userPasswordField = document.getElementById('user-password-field');


    if (userId) {
        document.getElementById('user-modal-title').innerText = 'Editar Usuário';
        const user = currentUsersInAdmin.find(u => u.id === userId);
        if (user) {
            document.getElementById('user-id-field').value = user.id;
            document.getElementById('user-name-field').value = user.name;
            document.getElementById('user-cpf-field').value = user.cpf;
            document.getElementById('user-email-field').value = user.email;
            document.getElementById('user-type-field').value = user.type;
            userPasswordField.placeholder = 'Confirme a senha atual';
            userPasswordField.required = true;

            if (userNewPasswordGroup) userNewPasswordGroup.style.display = 'block';
            if (userConfirmNewPasswordGroup) userConfirmNewPasswordGroup.style.display = 'block';
            document.getElementById('user-new-password-field').value = '';
            document.getElementById('user-confirm-new-password-field').value = '';
        }
    } else {
        document.getElementById('user-modal-title').innerText = 'Adicionar Novo Usuário';
        userPasswordField.placeholder = 'Senha do novo usuário';
        userPasswordField.required = true;

        if (userNewPasswordGroup) userNewPasswordGroup.style.display = 'none';
        if (userConfirmNewPasswordGroup) userConfirmNewPasswordGroup.style.display = 'none';
    }
    userFormModal.style.display = 'flex';
}

document.getElementById('add-user-modal-btn').addEventListener('click', () => openUserFormModal());
document.getElementById('close-user-form-modal').addEventListener('click', () => {
    userFormModal.style.display = 'none';
    userManagementForm.reset();
    userFormMessage.style.display = 'none';
});
document.getElementById('user-form-cancel-btn').addEventListener('click', () => {
    userFormModal.style.display = 'none';
    userManagementForm.reset();
    userFormMessage.style.display = 'none';
});


userManagementForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const userId = document.getElementById('user-id-field').value;
    const name = document.getElementById('user-name-field').value.trim();
    const cpf = document.getElementById('user-cpf-field').value.trim();
    const email = document.getElementById('user-email-field').value.trim();
    const password = document.getElementById('user-password-field').value.trim();
    const type = document.getElementById('user-type-field').value;

    const newPasswordField = document.getElementById('user-new-password-field');
    const confirmNewPasswordField = document.getElementById('user-confirm-new-password-field');
    const newPassword = (newPasswordField && newPasswordField.value.trim()) || null;
    const confirmNewPassword = (confirmNewPasswordField && confirmNewPasswordField.value.trim()) || null;


    if (!name || !cpf || !email || !password) {
        showMessage(userFormMessage, "Nome, CPF, email e senha são obrigatórios.", 'error');
        return;
    }
    if (newPassword && newPassword !== confirmNewPassword) {
        showMessage(userFormMessage, "As novas senhas não coincidem.", 'error');
        return;
    }
    if (newPassword && newPassword.length < 6) {
        showMessage(userFormMessage, "A nova senha deve ter pelo menos 6 caracteres.", 'error');
        return;
    }
    if (!userId && password.length < 6) {
        showMessage(userFormMessage, "A senha para novos usuários deve ter pelo menos 6 caracteres.", 'error');
        return;
    }
    if (!/^\d{11}$/.test(cpf)) {
        showMessage(userFormMessage, "CPF deve conter 11 dígitos numéricos.", 'error');
        return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showMessage(userFormMessage, "Por favor, insira um email válido.", 'error');
        return;
    }


    const submitButton = userManagementForm.querySelector('button[type="submit"]');
    setButtonLoading(submitButton, true, "Salvar");
    userFormMessage.style.display = 'none';

    let url = `${API_BASE_URL}/usuarios`;
    let method = 'POST';
    let bodyData = {};

    if (userId) {
        url = `${API_BASE_URL}/usuarios/${userId}`;
        method = 'PUT';
        bodyData = {
            password: password,
            new_name: name,
            new_email: email,
            new_tipo: type
        };
        if (newPassword) {
            bodyData.new_password = newPassword;
        }
    } else {
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
            fetchUsers();
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

async function deleteUserConfirmation(userId) {
    const user = currentUsersInAdmin.find(u => u.id === userId);
    if (!user) {
        showMessage(usersManagementMessage, "Usuário não encontrado.", 'error');
        return;
    }

    if (!confirm(`Tem certeza que deseja excluir o usuário: ${user.name} (ID: ${user.id})? Esta ação é irreversível!`)) {
        return;
    }

    const passwordConfirmation = prompt("Por favor, digite a senha do usuário logado (Admin) para confirmar a exclusão:");

    if (!passwordConfirmation) {
        alert("Exclusão cancelada. Senha é obrigatória.");
        return;
    }

    if (!currentUser || currentUser.type !== 'funcionario') {
        showMessage(usersManagementMessage, "Erro: Você não está logado como funcionário.", 'error');
        return;
    }

    usersManagementMessage.style.display = 'none';
    try {
        const response = await fetch(`${API_BASE_URL}/usuarios/${userId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: passwordConfirmation })
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(usersManagementMessage, data.message, 'success');
            fetchUsers();
        } else {
            showMessage(usersManagementMessage, data.message || "Erro desconhecido ao deletar usuário.", 'error');
        }
    } catch (error) {
        console.error("Erro ao deletar usuário:", error);
        showMessage(usersManagementMessage, "Erro de conexão ao deletar usuário.", 'error');
    }
}


async function fetchAllProductsForAdmin() {
    productsManagementMessage.style.display = 'none';
    const productsTableBody = document.querySelector('#products-table tbody');
    productsTableBody.innerHTML = '<tr><td colspan="5"><div class="spinner" aria-label="Carregando produtos para gerenciamento"></div></td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentProductsInAdmin = await response.json();
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
        const sizesWithQty = Object.keys(product.tamanhos).map(s => `${s} (${product.tamanhos[s]})`).join(', ') || 'N/A (Sem estoque)';
        const row = `
            <tr>
                <td>${product.id}</td>
                <td>${product.nome}</td>
                <td>R$ ${product.preco.toFixed(2).replace('.', ',')}</td>
                <td>${sizesWithQty}</td>
                <td class="action-buttons">
                    <button class="edit-product-btn" data-product-id="${product.id}" aria-label="Editar produto ${product.nome}"><i class="fas fa-edit"></i></button>
                    <button class="delete-product-btn" data-product-id="${product.id}" aria-label="Excluir produto ${product.nome}"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
        productsTableBody.innerHTML += row;
    });

    productsTableBody.querySelectorAll('.edit-product-btn').forEach(btn => btn.addEventListener('click', (e) => openProductFormModal(parseInt(e.currentTarget.dataset.productId))));
    productsTableBody.querySelectorAll('.delete-product-btn').forEach(btn => btn.addEventListener('click', (e) => deleteProductConfirmation(parseInt(e.currentTarget.dataset.productId))));
}

function openProductFormModal(productId = null) {
    productManagementForm.reset();
    productFormMessage.style.display = 'none';
    document.getElementById('product-id-field').value = '';
    document.getElementById('sizes-quantities-container').innerHTML = '';

    if (productId) {
        document.getElementById('product-modal-title').innerText = 'Editar Produto';
        const product = currentProductsInAdmin.find(p => p.id === productId);
        if (product) {
            document.getElementById('product-id-field').value = product.id;
            document.getElementById('product-name-field').value = product.nome;
            document.getElementById('product-price-field').value = product.preco;
            for (const size in product.tamanhos) {
                addSizeQuantityField(size, product.tamanhos[size]);
            }
        }
    } else {
        document.getElementById('product-modal-title').innerText = 'Adicionar Novo Produto';
        addSizeQuantityField();
    }
    productFormModal.style.display = 'flex';
}

document.getElementById('add-product-modal-btn').addEventListener('click', () => openProductFormModal());
document.getElementById('close-product-form-modal').addEventListener('click', () => {
    productFormModal.style.display = 'none';
    productManagementForm.reset();
    productFormMessage.style.display = 'none';
    document.getElementById('sizes-quantities-container').innerHTML = '';
});
document.getElementById('product-form-cancel-btn').addEventListener('click', () => {
    productFormModal.style.display = 'none';
    productManagementForm.reset();
    productFormMessage.style.display = 'none';
    document.getElementById('sizes-quantities-container').innerHTML = '';
});

function addSizeQuantityField(initialSize = '', initialQty = '') {
    const container = document.getElementById('sizes-quantities-container');
    const div = document.createElement('div');
    div.className = 'input-group size-qty-pair';
    div.innerHTML = `
        <label for="size-${Date.now()}" class="sr-only">Tamanho:</label>
        <input type="text" class="product-size-field" value="${initialSize}" placeholder="Ex: P, M, G" required aria-label="Tamanho" style="width: 45%; display: inline-block;">
        <label for="qty-${Date.now()}" class="sr-only">Quantidade:</label>
        <input type="number" class="product-qty-field" value="${initialQty}" min="0" required aria-label="Quantidade" style="width: 45%; display: inline-block; margin-left: 5px;">
        <button type="button" class="btn btn-secondary remove-size-qty-field" aria-label="Remover este tamanho e quantidade" style="width: auto; margin-left: 5px; background: none; color: var(--red-alert); border: none;"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(div);

    div.querySelector('.remove-size-qty-field').addEventListener('click', () => div.remove());
}

document.getElementById('add-size-qty-field').addEventListener('click', () => addSizeQuantityField());

productManagementForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const productId = document.getElementById('product-id-field').value;
    const name = document.getElementById('product-name-field').value.trim();
    const price = parseFloat(document.getElementById('product-price-field').value);

    const sizesQuantities = {};
    let isValidSizes = true;
    document.querySelectorAll('.size-qty-pair').forEach(pair => {
        const sizeInput = pair.querySelector('.product-size-field');
        const qtyInput = pair.querySelector('.product-qty-field');
        const size = sizeInput.value.trim().toUpperCase();
        const qty = parseInt(qtyInput.value);

        if (!size) {
            showMessage(productFormMessage, "O nome do tamanho não pode ser vazio.", 'error');
            isValidSizes = false;
            return;
        }
        if (isNaN(qty) || qty < 0) {
            showMessage(productFormMessage, `Quantidade para o tamanho '${size}' é inválida.`, 'error');
            isValidSizes = false;
            return;
        }
        if (sizesQuantities[size]) {
            showMessage(productFormMessage, `Tamanho '${size}' duplicado. Por favor, remova ou combine.`, 'error');
            isValidSizes = false;
            return;
        }
        sizesQuantities[size] = qty;
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

    if (productId) {
        url = `${API_BASE_URL}/produtos/${productId}`;
        method = 'PUT';
        bodyData = {
            nome: name,
            preco: price,
            tamanhos: sizesQuantities
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
            fetchAllProductsForAdmin();
            fetchProducts();
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

async function deleteProductConfirmation(productId) {
    const product = currentProductsInAdmin.find(p => p.id === productId);
    if (!product) {
        showMessage(productsManagementMessage, "Produto não encontrado.", 'error');
        return;
    }

    if (!confirm(`Tem certeza que deseja excluir o produto: ${product.nome} (ID: ${product.id})? Esta ação é irreversível e removerá o estoque associado!`)) {
        return;
    }

    productsManagementMessage.style.display = 'none';
    try {
        const response = await fetch(`${API_BASE_URL}/produtos/${productId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (response.ok) {
            showMessage(productsManagementMessage, data.message, 'success');
            fetchAllProductsForAdmin();
            fetchProducts();
        } else {
            showMessage(productsManagementMessage, data.message || "Erro desconhecido ao deletar produto.", 'error');
        }
    } catch (error) {
        console.error("Erro ao deletar produto:", error);
        showMessage(productsManagementMessage, "Erro de conexão ao deletar produto.", 'error');
    }
}

async function fetchAllSales() {
    salesManagementMessage.style.display = 'none';
    const salesTableBody = document.querySelector('#sales-table tbody');
    salesTableBody.innerHTML = '<tr><td colspan="7"><div class="spinner" aria-label="Carregando vendas"></div></td></tr>';

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
        const itemsList = sale.itens.map(item =>
            `${item.quantidade}x ${item.nome} (${item.tamanho}) - R$ ${item.preco_unitario.toFixed(2).replace('.', ',')}`
        ).join('<br>');

        const row = `
            <tr>
                <td>${sale.id}</td>
                <td>${new Date(sale.data).toLocaleString('pt-BR')}</td>
                <td>${sale.status}</td>
                <td>R$ ${sale.total.toFixed(2).replace('.', ',')}</td>
                <td>${sale.usuario.nome || 'N/A (Usuário removido)'}</td>
                <td>${sale.usuario.email || 'N/A'}</td>
                <td>${itemsList}</td>
            </tr>
        `;
        salesTableBody.innerHTML += row;
    });
}

async function fetchAllStock() {
    stockManagementMessage.style.display = 'none';
    const stockTableBody = document.querySelector('#stock-table tbody');
    stockTableBody.innerHTML = '<tr><td colspan="5"><div class="spinner" aria-label="Carregando estoque"></div></td></tr>';

    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const productsWithStock = await response.json();
        currentStockInAdmin = [];
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
                <td><input type="number" class="stock-qty-input" data-product-id="${item.productId}" data-size="${item.size}" value="${item.quantity}" min="0" aria-label="Quantidade em estoque para ${item.productName} tamanho ${item.size}"></td>
                <td class="action-buttons">
                    <button class="save-stock-qty-btn" data-product-id="${item.productId}" data-size="${item.size}" style="display:none;" aria-label="Salvar estoque"><i class="fas fa-save"></i></button>
                </td>
            </tr>
        `;
        stockTableBody.innerHTML += row;
    });

    stockTableBody.querySelectorAll('.stock-qty-input').forEach(input => {
        input.addEventListener('input', function () {
            const saveBtn = this.closest('tr').querySelector('.save-stock-qty-btn');
            saveBtn.style.display = 'inline-block';
        });
    });

    stockTableBody.querySelectorAll('.save-stock-qty-btn').forEach(button => {
        button.addEventListener('click', async function () {
            const productId = parseInt(this.dataset.productId);
            const size = this.dataset.size;
            const newQuantity = parseInt(this.closest('tr').querySelector('.stock-qty-input').value);

            if (isNaN(newQuantity) || newQuantity < 0) {
                showMessage(stockManagementMessage, "Quantidade inválida. Deve ser um número >= 0.", 'error');
                return;
            }

            const productToUpdate = allProducts.find(p => p.id === productId);
            if (!productToUpdate) {
                showMessage(stockManagementMessage, "Erro: Produto não encontrado para atualização de estoque.", 'error');
                return;
            }
            const updatedSizesDict = { ...productToUpdate.tamanhos, [size]: newQuantity };

            const updatePayload = {
                nome: productToUpdate.nome,
                preco: productToUpdate.preco,
                tamanhos: updatedSizesDict
            };

            setButtonLoading(this, true, '<i class="fas fa-save"></i>');
            try {
                const response = await fetch(`${API_BASE_URL}/produtos/${productId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatePayload)
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(stockManagementMessage, `Estoque de ${productToUpdate.nome} (Tam: ${size}) atualizado.`, 'success');
                    this.style.display = 'none';
                    fetchProducts();
                    fetchAllStock();
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

async function fetchReports() {
    reportsMessage.style.display = 'none';
    const reportsContentDiv = document.getElementById('reports-content');
    reportsContentDiv.innerHTML = '<div class="spinner" aria-label="Carregando relatórios"></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/relatorios/vendas`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        currentReports = await response.json();
        renderReports(currentReports);
    } catch (error) {
        console.error("Erro ao buscar relatórios:", error);
        showMessage(reportsMessage, "Erro ao carregar relatórios.", 'error');
        reportsContentDiv.innerHTML = '<p id="empty-reports-message" style="text-align: center; color: #666; font-size: 1.2rem;">Erro ao carregar relatórios.</p>';
    }
}

function renderReports(reports) {
    const reportsContentDiv = document.getElementById('reports-content');
    reportsContentDiv.innerHTML = '';

    if (reports.length === 0) {
        reportsContentDiv.innerHTML = '<p id="empty-reports-message" style="text-align: center; color: #666; font-size: 1.2rem;">Nenhum relatório de vendas encontrado.</p>';
        return;
    }

    reports.forEach(report => {
        const productsList = report.produtos.map(p =>
            `- ${p.quantidade}x ${p.nome} (Tam: ${p.tamanho}) - R$ ${p.preco_unitario.toFixed(2).replace('.', ',')}`
        ).join('<br>');

        const reportCardHtml = `
            <div class="report-card" style="background: #f0f0f0; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3>Relatório de Venda ID: ${report.id_venda}</h3>
                <p><strong>Cliente:</strong> ${report.cliente_nome}</p>
                <p><strong>Data/Hora:</strong> ${new Date(report.data_hora).toLocaleString('pt-BR')}</p>
                <p><strong>Total:</strong> R$ ${report.valor_total.toFixed(2).replace('.', ',')}</p>
                <p><strong>Produtos:</strong></p>
                <div style="margin-left: 20px;">${productsList}</div>
            </div>
        `;
        reportsContentDiv.innerHTML += reportCardHtml;
    });
}

document.getElementById('mobile-menu').addEventListener('click', function () {
    const navList = document.getElementById('nav-list');
    navList.classList.toggle('active');
});

window.addEventListener('scroll', function () {
    const header = document.querySelector('.main-header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

document.querySelectorAll('.nav-list a').forEach(link => {
    link.addEventListener('click', function (event) {
        const navList = document.getElementById('nav-list');
        if (navList.classList.contains('active')) {
            navList.classList.remove('active');
        }

        const targetId = this.getAttribute('href').substring(1);
        event.preventDefault();

        if (targetId === 'home' || targetId === 'products') {
            showProductsListingPage();
        } else if (targetId === 'cart') {
            showCartPage();
        } else if (targetId === 'profile') {
            showProfilePage();
        } else if (targetId === 'admin') {
            showAdminDashboard();
        } else if (targetId === 'login') {
            showLoginPage();
        } else if (this.id === 'logout-btn') {
            handleLogout();
        } else if (targetId === 'teams') {
            alert(`Página de ${targetId.toUpperCase()} em desenvolvimento!`);
            hideAllSections();
        } else {
            hideAllSections();
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = 'block';
            }
            window.scrollTo(0, 0);
        }
    });
});

if (document.getElementById('manage-users-btn')) document.getElementById('manage-users-btn').addEventListener('click', showAdminManageUsers);
if (document.getElementById('manage-products-btn')) document.getElementById('manage-products-btn').addEventListener('click', showAdminManageProducts);
if (document.getElementById('manage-sales-btn')) document.getElementById('manage-sales-btn').addEventListener('click', showAdminManageSales);
if (document.getElementById('manage-stock-btn')) document.getElementById('manage-stock-btn').addEventListener('click', showAdminManageStock);
if (document.getElementById('view-reports-btn')) document.getElementById('view-reports-btn').addEventListener('click', showAdminViewReports);

if (document.getElementById('back-to-admin-dashboard-from-users')) document.getElementById('back-to-admin-dashboard-from-users').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-products')) document.getElementById('back-to-admin-dashboard-from-products').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-sales')) document.getElementById('back-to-admin-dashboard-from-sales').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-stock')) document.getElementById('back-to-admin-dashboard-from-stock').addEventListener('click', showAdminDashboard);
if (document.getElementById('back-to-admin-dashboard-from-reports')) document.getElementById('back-to-admin-dashboard-from-reports').addEventListener('click', showAdminDashboard);

document.addEventListener('DOMContentLoaded', () => {
    updateNavbarVisibility();
    updateCartItemCount();

    if (currentUser) {
        showHomePage();
    } else {
        showLoginPage();
    }
});
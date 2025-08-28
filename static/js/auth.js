const API_BASE_URL = "http://localhost:5500";

// 處理登入
async function handleLogin(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || "登入失敗");
        }

        const data = await response.json();
        localStorage.setItem("user", JSON.stringify(data.user));
        return data;
    } catch (error) {
        console.error("Login error:", error);
        throw error;
    }
}

// 處理註冊
async function handleRegister(userName, email, password, userRole) {
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_name: userName,
                email: email,
                password: password,
                user_role: userRole
            })
        });

        const data = await response.json();

        if (!response.ok) {
            // 檢查是否為用戶已存在的錯誤
            if (response.status === 409) {
                throw new Error('此電子郵件已被註冊，請使用其他電子郵件或直接登入');
            }
            throw new Error(data.error?.message || '註冊失敗');
        }

        return data;
    } catch (error) {
        console.error('註冊錯誤:', error);
        throw error;
    }
}

// 根據用戶角色決定跳轉頁面
function redirectBasedOnRole(userRole) {
    switch (userRole) {
        case 'user':
            window.location.href = '/loan';
            break;
        case 'admin':
            window.location.href = '/check';
            break;
        default:
            alert('未知的用戶角色');
            break;
    }
}

// 個人用戶登入表單提交處理
document.getElementById('userLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('userLoginEmail').value;
    const password = document.getElementById('userLoginPassword').value;

    try {
        const result = await handleLogin(email, password);
        alert('登入成功！');
        redirectBasedOnRole(result.user.user_role);
    } catch (error) {
        alert(error.message);
    }
});

// 社團登入表單提交處理
document.getElementById('clubLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('clubLoginEmail').value;
    const password = document.getElementById('clubLoginPassword').value;

    try {
        const result = await handleLogin(email, password);
        alert('社團登入成功！');
        redirectBasedOnRole(result.user.user_role);
    } catch (error) {
        alert(error.message);
    }
});

// 個人用戶註冊表單提交處理
document.getElementById('userRegisterForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userName = document.getElementById('userRegisterName').value;
    const email = document.getElementById('userRegisterEmail').value;
    const password = document.getElementById('userRegisterPassword').value;

    try {
        const result = await handleRegister(userName, email, password, 'user');
        window.location.href = '/registerSuccess';
    } catch (error) {
        alert(error.message);
        // 如果是用戶已存在的錯誤，提供直接跳轉到登入頁面的選項
        if (error.message.includes('已被註冊')) {
            if (confirm('是否要直接前往登入頁面？')) {
                window.location.href = '/userLogin';
            }
        }
    }
});

// 社團註冊表單提交處理
document.getElementById('clubRegisterForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userName = document.getElementById('clubRegisterName').value;
    const email = document.getElementById('clubRegisterEmail').value;
    const password = document.getElementById('clubRegisterPassword').value;

    try {
        const result = await handleRegister(userName, email, password, 'admin');
        window.location.href = '/registerSuccess';
    } catch (error) {
        alert(error.message);
        // 如果是用戶已存在的錯誤，提供直接跳轉到登入頁面的選項
        if (error.message.includes('已被註冊')) {
            if (confirm('是否要直接前往登入頁面？')) {
                window.location.href = '/clubLogin';
            }
        }
    }
});

// 檢查用戶是否已登入
function checkAuth() {
    const user = localStorage.getItem('user');
    
    if (!user) {
        // 如果用戶未登入且不在登入/註冊頁面，重定向到登入頁面
        if (!window.location.pathname.includes('login') && 
            !window.location.pathname.includes('註冊')) {
            window.location.href = '/login';
        }
    }
    return user ? JSON.parse(user) : null;
}

// 登出功能
function logout() {
    localStorage.removeItem('user');
    window.location.href = '/login';
}
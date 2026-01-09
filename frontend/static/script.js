// Простые функции для работы с формами и API

async function deleteItem(url, itemName) {
    if (!confirm(`Вы уверены, что хотите удалить ${itemName}?`)) {
        return;
    }
    
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Ошибка при удалении');
        }
    } catch (error) {
        alert('Ошибка: ' + error.message);
    }
}

async function submitForm(formId, url, method = 'POST') {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            if (key === 'amount' || key === 'target_amount' || key === 'current_amount' || key === 'category_id' || key === 'budget_id' || key === 'goal_id') {
                data[key] = parseFloat(value) || parseInt(value);
            } else if (key === 'is_default' || key === 'is_active' || key === 'is_completed') {
                data[key] = value === 'true' || value === 'on';
            } else if (key === 'date' || key === 'start_date' || key === 'end_date' || key === 'deadline') {
                data[key] = value;
            } else {
                data[key] = value;
            }
        });
        
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                // Если это форма входа или регистрации, перенаправляем на главную
                if (url.includes('/auth/login') || url.includes('/auth/register')) {
                    window.location.href = '/';
                } else {
                    window.location.reload();
                }
            } else {
                const error = await response.json();
                alert('Ошибка: ' + (error.detail || 'Неизвестная ошибка'));
            }
        } catch (error) {
            alert('Ошибка: ' + error.message);
        }
    });
}

// Функция выхода
async function logout() {
    try {
        const response = await fetch('/api/v1/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            window.location.href = '/login';
        } else {
            alert('Ошибка при выходе');
        }
    } catch (error) {
        alert('Ошибка: ' + error.message);
    }
}

// Автоматическая отправка форм при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Находим все формы и добавляем обработчики
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const formId = form.id;
        const action = form.action;
        const method = form.method || 'POST';
        
        if (formId && action) {
            submitForm(formId, action, method);
        }
    });
});


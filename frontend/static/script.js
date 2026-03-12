const NUMERIC_FIELDS = new Set([
    'amount', 'target_amount', 'current_amount',
    'category_id', 'budget_id', 'goal_id',
]);

const BOOLEAN_FIELDS = new Set([
    'is_default', 'is_active', 'is_completed',
]);

function parseFormValue(key, value) {
    if (NUMERIC_FIELDS.has(key)) {
        return parseFloat(value) || parseInt(value);
    }
    if (BOOLEAN_FIELDS.has(key)) {
        return value === 'true' || value === 'on';
    }
    return value;
}

async function deleteItem(url, itemName) {
    if (!confirm(`Вы уверены, что хотите удалить ${itemName}?`)) {
        return;
    }

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            credentials: 'include',
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
            data[key] = parseFormValue(key, value);
        });

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(data),
            });

            if (response.ok) {
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

async function logout() {
    try {
        const response = await fetch('/api/v1/auth/logout', {
            method: 'POST',
            credentials: 'include',
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

document.addEventListener('DOMContentLoaded', () => {
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

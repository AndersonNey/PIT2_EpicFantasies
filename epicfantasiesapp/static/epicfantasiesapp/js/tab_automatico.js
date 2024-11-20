document.addEventListener('DOMContentLoaded', (event) => {
    const codes = document.querySelectorAll('.code-item');
    codes.forEach((code, idx) => {
        code.addEventListener('input', () => {
            if (code.value.length === 1) {
                if (idx < codes.length - 1) {
                    codes[idx + 1].focus();
                }
            }
        });

        code.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && code.value === '' && idx > 0) {
                codes[idx - 1].focus();
            }
        });
    });
});

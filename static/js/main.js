/* StockPredict — interaksi form prediksi (vanilla JS, tanpa library). */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('prediction-form');
  const fileInput = document.getElementById('csv_file');
  const fileHint = document.getElementById('file-hint');
  const csvError = document.getElementById('csv-error');
  const csvField = document.getElementById('csv-field');
  const maxSize = 5 * 1024 * 1024;
  const setInvalid = (invalid) => {
    if (!csvField || !fileInput) return;
    if (invalid) {
      csvField.setAttribute('data-invalid', 'true');
      fileInput.setAttribute('aria-invalid', 'true');
    } else {
      csvField.removeAttribute('data-invalid');
      fileInput.removeAttribute('aria-invalid');
    }
  };
  const showError = (message) => {
    if (!csvError) return;
    csvError.textContent = message;
    csvError.hidden = false;
    setInvalid(true);
  };
  const clearError = () => {
    if (!csvError) return;
    csvError.textContent = '';
    csvError.hidden = true;
    setInvalid(false);
  };
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      if (!file) {
        clearError();
        if (fileHint) fileHint.textContent = '';
        return;
      }
      const extension = file.name.split('.').pop().toLowerCase();
      if (extension !== 'csv') {
        showError('Format file harus CSV.');
        fileInput.value = '';
        if (fileHint) fileHint.textContent = '';
        return;
      }
      if (file.size > maxSize) {
        showError('Ukuran file melebihi 5 MB.');
        fileInput.value = '';
        if (fileHint) fileHint.textContent = '';
        return;
      }
      clearError();
      if (fileHint) {
        fileHint.textContent = `${file.name} · ${Math.round(file.size / 1024)} KB`;
      }
    });
  }
  if (form) {
    form.addEventListener('submit', (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        form.reportValidity();
        return;
      }
      const button = form.querySelector('[type="submit"]');
      if (!button) return;
      const label = button.querySelector('[data-label]');
      const spinner = button.querySelector('[data-spinner]');
      const arrow = button.querySelector('[data-arrow]');
      button.disabled = true;
      if (label) label.textContent = 'Memproses…';
      if (spinner) spinner.hidden = false;
      if (arrow) arrow.hidden = true;
    });
  }
});

/* StockPredict — interaksi form prediksi (vanilla JS, tanpa library). */
document.addEventListener('DOMContentLoaded', () => {
  const form       = document.getElementById('prediction-form');
  const fileInput  = document.getElementById('csv_file');
  const fileHint   = document.getElementById('file-hint');
  const csvError   = document.getElementById('csv-error');
  const csvField   = document.getElementById('csv-field');
  const dialog     = document.getElementById('csv-row-dialog');
  const dialogClose = document.getElementById('dialog-close');
  const rowCountEl = document.getElementById('dialog-row-count');
  const submitBtn  = form ? form.querySelector('[type="submit"]') : null;
  const maxSize    = 5 * 1024 * 1024;

  let csvRowCount = null; // null = belum dicek, angka = jumlah baris data

  /* ------------------------------------------------------------------ */
  /* Helpers: state invalid field                                         */
  /* ------------------------------------------------------------------ */
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

  /* ------------------------------------------------------------------ */
  /* Helpers: validasi field wajib                                        */
  /* ------------------------------------------------------------------ */
  const requiredMessages = {
    stock: 'Silakan pilih kode saham.',
    csv_file: 'Silakan unggah file CSV.',
    horizon: 'Silakan pilih horizon prediksi.',
  };

  const getFieldError = (control) => {
    if (control === fileInput) return csvError;
    const field = control.closest('.field');
    let el = field.querySelector('[data-auto-error]');
    if (!el) {
      el = document.createElement('p');
      el.className = 'field-error';
      el.setAttribute('role', 'alert');
      el.setAttribute('data-auto-error', '');
      el.hidden = true;
      field.appendChild(el);
    }
    return el;
  };

  const setFieldInvalid = (control, message) => {
    const field = control.closest('.field');
    const el = getFieldError(control);
    if (message) {
      field.setAttribute('data-invalid', 'true');
      control.setAttribute('aria-invalid', 'true');
      el.textContent = message;
      el.hidden = false;
    } else {
      field.removeAttribute('data-invalid');
      control.removeAttribute('aria-invalid');
      el.textContent = '';
      el.hidden = true;
    }
  };

  const isEmpty = (control) =>
    control.type === 'file' ? control.files.length === 0 : !control.value;

  const validateRequired = () => {
    let firstInvalid = null;
    form.querySelectorAll('[required]').forEach((control) => {
      if (isEmpty(control)) {
        setFieldInvalid(control, requiredMessages[control.id] || 'Field ini wajib diisi.');
        if (!firstInvalid) firstInvalid = control;
      } else if (control !== fileInput) {
        setFieldInvalid(control, null);
      }
    });
    return firstInvalid;
  };

  if (form) {
    form.querySelectorAll('select[required]').forEach((select) => {
      select.addEventListener('change', () => setFieldInvalid(select, null));
    });
  }

  /* ------------------------------------------------------------------ */
  /* Helpers: state tombol submit                                         */
  /* ------------------------------------------------------------------ */
  const setButtonState = (state) => {
    if (!submitBtn) return;
    const label   = submitBtn.querySelector('[data-label]');
    const spinner = submitBtn.querySelector('[data-spinner]');
    const arrow   = submitBtn.querySelector('[data-arrow]');

    if (state === 'loading-file') {
      submitBtn.disabled = true;
      if (label)   label.textContent = 'Memeriksa file…';
      if (spinner) spinner.hidden = false;
      if (arrow)   arrow.hidden   = true;
    } else if (state === 'loading-predict') {
      submitBtn.disabled = true;
      if (label)   label.textContent = 'Memproses…';
      if (spinner) spinner.hidden = false;
      if (arrow)   arrow.hidden   = true;
    } else {
      submitBtn.disabled = false;
      if (label)   label.textContent = 'Mulai Prediksi';
      if (spinner) spinner.hidden = true;
      if (arrow)   arrow.hidden   = false;
    }
  };

  /* ------------------------------------------------------------------ */
  /* Helpers: hitung baris data dalam CSV                                */
  /* ------------------------------------------------------------------ */
  const countCsvDataRows = (text) => {
    const lines = text.split(/\r?\n/).filter((l) => l.trim() !== '');
    let skip = 0;
    if (lines.length > 0 && lines[0].trim().toLowerCase().startsWith('sep=')) skip++;
    skip++; // lewati header
    return Math.max(0, lines.length - skip);
  };

  /* ------------------------------------------------------------------ */
  /* File input: validasi & baca row count                               */
  /* ------------------------------------------------------------------ */
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      csvRowCount = null;

      if (!file) {
        clearError();
        if (fileHint) fileHint.textContent = '';
        return;
      }

      const ext = file.name.split('.').pop().toLowerCase();
      if (ext !== 'csv') {
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

      // Baca isi file untuk hitung baris data
      setButtonState('loading-file');
      const reader = new FileReader();

      reader.onload = (e) => {
        csvRowCount = countCsvDataRows(e.target.result);
        clearError();
        if (fileHint) {
          fileHint.textContent = `${file.name} · ${Math.round(file.size / 1024)} KB`;
        }
        setButtonState('idle');
      };

      reader.onerror = () => {
        showError('File tidak dapat dibaca.');
        csvRowCount = null;
        setButtonState('idle');
      };

      reader.readAsText(file);
    });
  }

  /* ------------------------------------------------------------------ */
  /* Dialog: tutup dengan tombol atau klik backdrop                      */
  /* ------------------------------------------------------------------ */
  if (dialogClose && dialog) {
    dialogClose.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => {
      if (e.target === dialog) dialog.close();
    });
  }

  /* ------------------------------------------------------------------ */
  /* Form submit: cek row count, lalu kirim atau tampilkan popup         */
  /* ------------------------------------------------------------------ */
  if (form) {
    form.addEventListener('submit', (event) => {
      if (submitBtn && submitBtn.disabled) {
        event.preventDefault();
        return;
      }

      const firstInvalid = validateRequired();
      if (firstInvalid) {
        event.preventDefault();
        firstInvalid.focus();
        return;
      }

      // Blok submit jika data kurang dari 30 baris
      if (csvRowCount !== null && csvRowCount < 30) {
        event.preventDefault();
        if (dialog && rowCountEl) {
          rowCountEl.textContent = csvRowCount;
          dialog.showModal();
        }
        return;
      }

      setButtonState('loading-predict');
    });
  }
});

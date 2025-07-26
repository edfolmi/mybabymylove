function showAlert(message, type = 'info', duration = 6000) {
  const container = document.getElementById('alert-container');

  const alert = document.createElement('div');
  alert.className = `alert ${type}`;

  alert.innerHTML = `
    <span>${message}</span>
    <button class="close-btn" onclick="closeAlert(this.parentElement)">&times;</button>
  `;

  container.appendChild(alert);

  // Auto-dismiss
  const timeoutId = setTimeout(() => {
    closeAlert(alert);
  }, duration);

  // Store timeout ID
  alert.dataset.timeoutId = timeoutId;
}

function closeAlert(alertEl) {
  clearTimeout(alertEl.dataset.timeoutId);
  alertEl.style.animation = 'fadeOut 0.5s ease forwards';
  setTimeout(() => {
    alertEl.remove();
  }, 500);
}

document.addEventListener('DOMContentLoaded', function () {
  const pingBtn = document.getElementById('pingBtn');
  const result = document.getElementById('result');
  pingBtn.addEventListener('click', async () => {
    result.textContent = 'Calling /api/ping...';
    try {
      const res = await fetch('/api/ping');
      const data = await res.json();
      result.textContent = JSON.stringify(data);
    } catch (err) {
      result.textContent = 'Error: ' + err.message;
    }
  });

  const form = document.getElementById('demoForm');
  const formResult = document.getElementById('formResult');
  form.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const name = document.getElementById('name').value || 'anonymous';
    formResult.textContent = `Hello, ${name}! (this is client-side)`;
  });
});

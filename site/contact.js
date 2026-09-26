(() => {
  const status = document.querySelector('[aria-live]');
  let clearStatus;

  const fallbackCopy = (text) => {
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.appendChild(field);
    field.select();
    const copied = document.execCommand('copy');
    field.remove();
    return copied;
  };

  const copyText = async (text) => {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    return fallbackCopy(text);
  };

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const value = document.getElementById(button.dataset.copyTarget)?.textContent.trim();
      if (!value) return;
      let copied = false;
      try {
        copied = await copyText(value);
      } catch {
        copied = fallbackCopy(value);
      }
      window.clearTimeout(clearStatus);
      document.querySelectorAll('[data-copy-target]').forEach((copyButton) => copyButton.classList.remove('is-copied'));
      if (copied) button.classList.add('is-copied');
      status.textContent = copied ? 'Copied' : 'Select the text to copy';
      clearStatus = window.setTimeout(() => {
        button.classList.remove('is-copied');
        status.textContent = '';
      }, 1800);
    });
  });
})();

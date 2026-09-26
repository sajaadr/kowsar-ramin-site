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
      const originalLabel = button.dataset.defaultLabel || button.textContent;
      button.dataset.defaultLabel = originalLabel;
      if (copied) button.textContent = 'Copied';
      status.textContent = copied ? 'Copied' : 'Select the text to copy';
      clearStatus = window.setTimeout(() => {
        button.textContent = originalLabel;
        status.textContent = '';
      }, 1800);
    });
  });
})();

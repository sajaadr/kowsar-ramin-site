(() => {
  const status = document.querySelector('[aria-live]');
  const canonicalUrl = 'https://kowsar-ramin.pages.dev/';
  const shareTitle = 'Meet Kowsar & Ramin — Work & Collaboration';
  const shareText = 'Kowsar & Ramin work across hospitality, wellbeing, craftsmanship, music and creative projects, and welcome bookings, commissions, collaborations and selected volunteer opportunities.';
  let clearStatus;

  const announce = (message) => {
    if (!status) return;
    window.clearTimeout(clearStatus);
    status.textContent = message;
    clearStatus = window.setTimeout(() => {
      status.textContent = '';
    }, 1800);
  };

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

      document.querySelectorAll('[data-copy-target]').forEach((copyButton) => {
        copyButton.classList.remove('is-copied');
      });

      if (copied) {
        button.classList.add('is-copied');
        announce('Copied');
        window.setTimeout(() => button.classList.remove('is-copied'), 1800);
      } else {
        announce('Select the text to copy');
      }
    });
  });

  const shareButton = document.getElementById('share-page');
  shareButton?.addEventListener('click', async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: shareTitle,
          text: shareText,
          url: canonicalUrl,
        });
        return;
      } catch (error) {
        if (error?.name === 'AbortError') return;
      }
    }

    let copied = false;
    try {
      copied = await copyText(canonicalUrl);
    } catch {
      copied = fallbackCopy(canonicalUrl);
    }
    announce(copied ? 'Link copied' : 'Copy this link: ' + canonicalUrl);
  });
})();

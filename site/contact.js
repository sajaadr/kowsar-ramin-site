(() => {
  const status = document.querySelector('[aria-live]');
  const page = document.body?.dataset || {};
  const canonicalUrl = 'https://kowsar-ramin.pages.dev/';
  const pageCanonicalUrl = page.canonicalUrl || canonicalUrl;
  const shareUrl = pageCanonicalUrl + '?utm_source=share&utm_medium=referral&utm_campaign=kowsar_ramin';
  const shareTitle = 'Meet Kowsar & Ramin — Work & Collaboration';
  const shareText = 'Kowsar & Ramin work across hospitality, wellbeing, craftsmanship, music and creative projects, and welcome bookings, commissions, collaborations and selected volunteer opportunities.';
  const localizedShareTitle = page.shareTitle || shareTitle;
  const localizedShareText = page.shareText || shareText;
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
        window.krAnalytics?.capture('contact_action', { method: button.dataset.copyTarget === 'contact-email' ? 'copy_email' : 'copy_phone' });
        button.classList.add('is-copied');
        announce(page.statusCopied || 'Copied');
        window.setTimeout(() => button.classList.remove('is-copied'), 1800);
      } else {
        announce(page.statusSelectText || 'Select the text to copy');
      }
    });
  });

  const shareButton = document.getElementById('share-page');
  shareButton?.addEventListener('click', async () => {
    window.krAnalytics?.capture('share_action', { method: 'requested' });
    if (navigator.share) {
      try {
        await navigator.share({
          title: localizedShareTitle,
          text: localizedShareText,
          url: shareUrl,
        });
        window.krAnalytics?.capture('share_action', { method: 'native_completed' });
        return;
      } catch (error) {
        if (error?.name === 'AbortError') return;
      }
    }

    let copied = false;
    try {
      copied = await copyText(shareUrl);
    } catch {
      copied = fallbackCopy(shareUrl);
    }
    if (copied) window.krAnalytics?.capture('share_action', { method: 'fallback_copied' });
    announce(copied ? (page.statusLinkCopied || 'Link copied') : (page.statusCopyLink || 'Copy this link:') + ' ' + shareUrl);
  });
})();

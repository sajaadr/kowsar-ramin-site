(() => {
  'use strict';

  const TOKEN = 'phc_oNXdsncGbLiW7BUgjdj3CY4Uc3pyck6xV9zyvV3xjLMi';
  const API_HOST = 'https://eu.i.posthog.com';
  const allowed = Object.freeze({
    cta_clicked: { target: ['portfolio', 'whatsapp'] },
    instagram_clicked: { profile: ['kowsar', 'together', 'ramin'] },
    contact_action: { method: ['email', 'phone', 'copy_email', 'copy_phone', 'save_contact'] },
    share_action: { method: ['requested', 'native_completed', 'fallback_copied'] },
    section_viewed: { section: ['contact'] },
  });

  const sanitizeUrl = (value) => {
    try {
      const url = new URL(value, window.location.origin);
      const keep = new URLSearchParams();
      ['utm_source', 'utm_medium', 'utm_campaign'].forEach((key) => {
        const v = url.searchParams.get(key);
        if (v) keep.set(key, v.slice(0, 80));
      });
      url.search = keep.toString();
      url.hash = '';
      return url.toString();
    } catch {
      return undefined;
    }
  };
  const safeEvent = (eventName, properties = {}) => {
    const spec = allowed[eventName];
    if (!spec) return null;
    const clean = {};
    for (const [key, allowedValues] of Object.entries(spec)) {
      if (allowedValues.includes(properties[key])) clean[key] = properties[key];
    }
    return clean;
  };

  const capture = (eventName, properties = {}) => {
    const clean = safeEvent(eventName, properties);
    if (!clean || !window.posthog?.capture) return false;
    window.posthog.capture(eventName, clean);
    return true;
  };

  window.krAnalytics = Object.freeze({ capture });

  if (!window.posthog?.init) return;

  window.posthog.init(TOKEN, {
    api_host: API_HOST,
    ui_host: 'https://eu.posthog.com',
    persistence: 'memory',
    cookieless_mode: 'always',
    person_profiles: 'identified_only',
    autocapture: false,
    capture_pageview: true,
    capture_pageleave: false,
    capture_exceptions: false,
    disable_session_recording: true,
    advanced_disable_flags: true,
    respect_dnt: true,
    before_send: (event) => {
      if (!event) return null;
      if (event.properties) {
        const current = sanitizeUrl(event.properties.$current_url);
        if (current) event.properties.$current_url = current;
        else delete event.properties.$current_url;

        if (event.properties.$referrer) {
          try {
            const ref = new URL(event.properties.$referrer);
            ref.search = '';
            ref.hash = '';
            event.properties.$referrer = ref.toString();
          } catch {
            delete event.properties.$referrer;
          }
        }
      }
      return event;
    },
  });

  document.querySelectorAll('[data-analytics]').forEach((element) => {
    element.addEventListener('click', () => {
      const kind = element.dataset.analytics;
      if (kind === 'cta') capture('cta_clicked', { target: element.dataset.target });
      if (kind === 'instagram') capture('instagram_clicked', { profile: element.dataset.profile });
      if (kind === 'contact') capture('contact_action', { method: element.dataset.method });
    });
  });

  const contact = document.querySelector('.contact-card');
  if (contact && 'IntersectionObserver' in window) {
    let sent = false;
    const observer = new IntersectionObserver((entries) => {
      if (!sent && entries.some((entry) => entry.isIntersecting && entry.intersectionRatio >= 0.35)) {
        sent = true;
        capture('section_viewed', { section: 'contact' });
        observer.disconnect();
      }
    }, { threshold: [0.35] });
    observer.observe(contact);
  }
})();

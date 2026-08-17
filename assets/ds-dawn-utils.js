// Polyfill for Dawn utilities missing in Horizon
if (typeof debounce === 'undefined') {
  function debounce(fn, wait) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), wait);
    };
  }
}

if (typeof trapFocus === 'undefined') {
  function trapFocus(handlers, elementToFocus = null) {
    if (elementToFocus) elementToFocus.focus();
  }
}

if (typeof removeTrapFocus === 'undefined') {
  function removeTrapFocus(elementToFocus = null) {
    if (elementToFocus) elementToFocus.focus();
  }
}

if (typeof pauseAllMedia === 'undefined') {
  function pauseAllMedia() {
    document.querySelectorAll('.js-youtube').forEach((video) => {
      video.contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*');
    });
    document.querySelectorAll('.js-vimeo').forEach((video) => {
      video.contentWindow.postMessage('{"method":"pause"}', '*');
    });
    document.querySelectorAll('video').forEach((video) => video.pause());
    document.querySelectorAll('product-model').forEach((model) => {
      if (model.modelViewerUI) model.modelViewerUI.pause();
    });
  }
}

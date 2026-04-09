(function () {
  function setupDropInput(input) {
    if (!input || input.dataset.dropzoneReady === 'true') return;

    const wrapper = document.createElement('div');
    wrapper.className = 'cattleya-drop-wrapper';

    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const hint = document.createElement('div');
    hint.className = 'cattleya-drop-hint';
    hint.textContent = input.getAttribute('data-dropzone-label') || 'Suelta aquí tu archivo JSON o haz clic para seleccionarlo';
    wrapper.appendChild(hint);

    ['dragenter', 'dragover'].forEach((eventName) => {
      wrapper.addEventListener(eventName, function (event) {
        event.preventDefault();
        wrapper.classList.add('is-dragover');
      });
    });

    ['dragleave', 'dragend', 'drop'].forEach((eventName) => {
      wrapper.addEventListener(eventName, function (event) {
        event.preventDefault();
        wrapper.classList.remove('is-dragover');
      });
    });

    wrapper.addEventListener('drop', function (event) {
      const files = event.dataTransfer && event.dataTransfer.files;
      if (!files || !files.length) return;

      input.files = files;
      const changeEvent = new Event('change', { bubbles: true });
      input.dispatchEvent(changeEvent);
    });

    input.addEventListener('change', function () {
      const fileName = input.files && input.files[0] ? input.files[0].name : 'Suelta aquí tu archivo JSON o haz clic para seleccionarlo';
      hint.textContent = fileName;
    });

    input.dataset.dropzoneReady = 'true';
  }

  function init() {
    document.querySelectorAll('input.cattleya-drop-input[type="file"]').forEach(setupDropInput);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

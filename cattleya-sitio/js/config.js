(function () {
  const existingConfig = window.CATTLEYA_CONFIG || {};
  const hostname = window.location.hostname;
  const isLocalhost =
    hostname === '127.0.0.1' ||
    hostname === 'localhost' ||
    window.location.protocol === 'file:';

  const localBackendUrl = 'http://127.0.0.1:8000';
  const productionBackendUrl = 'https://cattleya-backend.onrender.com';

  const defaultApiBaseUrl = isLocalhost ? localBackendUrl : productionBackendUrl;

  window.CATTLEYA_CONFIG = Object.assign(
    {
      API_BASE_URL: defaultApiBaseUrl,
      CHATBOT_API_BASE_URL: defaultApiBaseUrl,
    },
    existingConfig
  );
})();

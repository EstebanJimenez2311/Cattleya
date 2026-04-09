/**
 * <cat-chatbot-btn>
 *
 * Botón flotante que abre un panel de chat para conversar con
 * el asistente de orientación de Cattleya.
 */
if (!customElements.get('cat-chatbot-btn')) {
class CatChatbotBtn extends HTMLElement {
  connectedCallback() {
    if (this.dataset.rendered === 'true') return;

    this.dataset.rendered = 'true';
    this._conversation = [
      {
        role: 'assistant',
        content: 'Hola, soy el asistente de Cattleya. Puedo orientarte sobre violencia basada en género, rutas de ayuda y señales de riesgo.'
      }
    ];
    this._isSending = false;
    this._maxContextMessages = 4;
    this._maxMessageChars = 420;
    this._maxAttempts = 5;
    this._attemptsStorageKey = 'cattleya_chatbot_attempts_used';
    this._attemptsUsed = this._readAttemptsUsed();

    this.innerHTML = `
      <style>
        :host {
          --cat-chatbot-plum: #8d2b61;
          --cat-chatbot-plum-soft: #c18bd4;
          --cat-chatbot-plum-deep: #4d1a43;
          --cat-chatbot-lavender: #f6effd;
          --cat-chatbot-lavender-strong: #ebdef8;
          --cat-chatbot-cream: #fffaf8;
          --cat-chatbot-gold: #e67e22;
          --cat-chatbot-gold-soft: #fff0df;
          --cat-chatbot-gold-deep: #9c4f13;
          --cat-chatbot-ink: #381a3f;
          --cat-chatbot-muted: #735f78;
          --cat-chatbot-success: #6abf8c;
          --cat-chatbot-border: rgba(240, 216, 255, 0.75);
          --cat-chatbot-shell: rgba(255, 255, 255, 0.78);
          --cat-chatbot-shadow: 0 28px 80px rgba(153, 96, 171, 0.28);
        }
        .cat-chatbot {
          position: fixed;
          right: 28px;
          bottom: 28px;
          z-index: 10000;
          font-family: 'DM Sans', sans-serif;
        }
        .cat-chatbot.has-help-btn {
          bottom: 98px;
        }
        .cat-chatbot__toggle {
          display: inline-flex;
          align-items: center;
          gap: 10px;
          background:
            radial-gradient(circle at top left, rgba(255, 224, 185, 0.52), transparent 42%),
            linear-gradient(135deg, #f0953b, #d86f18);
          color: #ffffff;
          border: 1px solid rgba(255, 240, 225, 0.42);
          border-radius: 999px;
          padding: 14px 20px;
          font-size: 0.93rem;
          font-weight: 700;
          cursor: pointer;
          box-shadow:
            0 16px 34px rgba(230, 126, 34, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.26);
          transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
          white-space: nowrap;
          backdrop-filter: blur(10px);
        }
        .cat-chatbot__toggle:hover {
          transform: translateY(-3px);
          box-shadow:
            0 18px 40px rgba(181, 83, 21, 0.42),
            inset 0 1px 0 rgba(255, 255, 255, 0.26);
          filter: saturate(1.05);
        }
        .cat-chatbot__icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.22);
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.24);
        }
        .cat-chatbot__panel {
          width: min(380px, calc(100vw - 32px));
          height: min(620px, calc(100vh - 120px));
          background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(251, 243, 255, 0.62) 52%, rgba(255, 248, 252, 0.7));
          border: 1px solid var(--cat-chatbot-border);
          border-radius: 30px;
          box-shadow: var(--cat-chatbot-shadow);
          overflow: hidden;
          display: none;
          flex-direction: column;
          margin-bottom: 16px;
          backdrop-filter: blur(12px);
        }
        .cat-chatbot__panel::before {
          content: '';
          position: absolute;
          inset: 0;
          background:
            radial-gradient(circle at 16% 18%, rgba(229, 184, 245, 0.42), transparent 18%),
            radial-gradient(circle at 80% 34%, rgba(255, 224, 178, 0.24), transparent 16%),
            radial-gradient(circle at 72% 72%, rgba(195, 228, 177, 0.22), transparent 16%),
            radial-gradient(circle at 28% 80%, rgba(255, 203, 219, 0.22), transparent 18%);
          pointer-events: none;
          opacity: 0.9;
        }
        .cat-chatbot__panel::after {
          content: '';
          position: absolute;
          inset: 6px;
          border-radius: 24px;
          border: 1px solid rgba(210, 160, 237, 0.4);
          pointer-events: none;
          box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.45);
        }
        .cat-chatbot.is-open .cat-chatbot__panel {
          display: flex;
          animation: catChatbotPop 0.22s ease-out;
        }
        @keyframes catChatbotPop {
          from {
            opacity: 0;
            transform: translateY(18px) scale(0.97);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        .cat-chatbot__header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
          padding: 18px 18px 16px;
          background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.46), rgba(255, 255, 255, 0.2));
          color: var(--cat-chatbot-ink);
          position: relative;
          z-index: 1;
        }
        .cat-chatbot__header::after {
          content: '';
          position: absolute;
          inset: auto 0 0;
          height: 1px;
          background: rgba(125, 83, 144, 0.12);
        }
        .cat-chatbot__header-main {
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 0;
        }
        .cat-chatbot__avatar {
          width: 42px;
          height: 42px;
          flex-shrink: 0;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          background:
            radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.98), rgba(249, 232, 244, 0.96) 56%, rgba(232, 206, 246, 0.98));
          border: 1px solid rgba(222, 189, 238, 0.72);
          box-shadow: 0 8px 20px rgba(170, 118, 191, 0.16);
          overflow: hidden;
        }
        .cat-chatbot__avatar img,
        .cat-chatbot__message-avatar img {
          display: block;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        .cat-chatbot__header-copy {
          min-width: 0;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        .cat-chatbot__eyebrow {
          display: none;
        }
        .cat-chatbot__title {
          font-size: 1rem;
          font-weight: 700;
          margin: 0;
        }
        .cat-chatbot__subtitle {
          display: none;
        }
        .cat-chatbot__presence {
          display: inline-flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 7px;
          margin-top: 2px;
          font-size: 0.78rem;
          color: rgba(56, 26, 63, 0.7);
        }
        .cat-chatbot__presence-meta {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          flex-wrap: wrap;
        }
        .cat-chatbot__status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--cat-chatbot-success);
          box-shadow: 0 0 0 4px rgba(106, 191, 140, 0.14);
        }
        .cat-chatbot__close {
          background: rgba(255, 255, 255, 0.36);
          color: var(--cat-chatbot-ink);
          border: 1px solid rgba(141, 43, 97, 0.08);
          width: 34px;
          height: 34px;
          border-radius: 50%;
          cursor: pointer;
          font-size: 1rem;
          flex-shrink: 0;
        }
        .cat-chatbot__messages {
          flex: 1;
          min-height: 0;
          overflow-y: auto;
          padding: 16px 18px 16px;
          background:
            linear-gradient(180deg, rgba(255, 248, 255, 0.16), rgba(255, 255, 255, 0.06));
          display: flex;
          flex-direction: column;
          gap: 12px;
          position: relative;
          z-index: 1;
        }
        .cat-chatbot__messages::before {
          content: '';
          position: sticky;
          top: -18px;
          display: block;
          height: 18px;
          margin-bottom: -2px;
          background: linear-gradient(180deg, rgba(255, 250, 252, 0.95), rgba(255, 250, 252, 0));
          z-index: 1;
          pointer-events: none;
        }
        .cat-chatbot__message {
          display: flex;
          align-items: flex-end;
          gap: 10px;
        }
        .cat-chatbot__message--user {
          justify-content: flex-end;
        }
        .cat-chatbot__message--status {
          justify-content: center;
        }
        .cat-chatbot__message--emergency {
          justify-content: center;
        }
        .cat-chatbot__message-avatar {
          width: 32px;
          height: 32px;
          flex-shrink: 0;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          background: radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.96), rgba(247, 230, 242, 0.92) 58%, rgba(230, 202, 244, 0.95));
          border: 1px solid rgba(222, 189, 238, 0.72);
          color: #d98cab;
          box-shadow: 0 6px 16px rgba(170, 118, 191, 0.14);
          overflow: hidden;
        }
        .cat-chatbot__bubble {
          max-width: calc(100% - 42px);
          padding: 12px 14px;
          border-radius: 20px;
          font-size: 0.88rem;
          line-height: 1.55;
          white-space: pre-wrap;
          word-break: break-word;
          overflow-wrap: anywhere;
          box-shadow: 0 8px 22px rgba(124, 85, 145, 0.1);
          position: relative;
        }
        .cat-chatbot__bubble--assistant {
          background: linear-gradient(180deg, rgba(245, 239, 252, 0.96), rgba(239, 232, 249, 0.95));
          color: var(--cat-chatbot-ink);
          border: 1px solid rgba(186, 157, 210, 0.38);
          border-bottom-left-radius: 12px;
        }
        .cat-chatbot__bubble--user {
          background: linear-gradient(135deg, rgba(171, 119, 214, 0.96), rgba(132, 79, 176, 0.98));
          color: #ffffff;
          border: 1px solid rgba(107, 59, 146, 0.18);
          border-bottom-right-radius: 12px;
        }
        .cat-chatbot__bubble--status {
          background: rgba(245, 239, 252, 0.72);
          color: #6b1a47;
          font-size: 0.8rem;
          border: 1px solid rgba(186, 157, 210, 0.25);
          box-shadow: none;
        }
        .cat-chatbot__bubble--emergency {
          max-width: 100%;
          background: linear-gradient(180deg, rgba(255, 228, 196, 0.98), rgba(255, 221, 181, 0.98));
          color: #3f2610;
          border: 1px solid rgba(230, 126, 34, 0.34);
          padding: 14px 16px 14px 42px;
          font-weight: 800;
          letter-spacing: 0.01em;
          box-shadow: 0 8px 24px rgba(230, 126, 34, 0.22);
        }
        .cat-chatbot__bubble--emergency::before {
          content: '⚠';
          position: absolute;
          top: 14px;
          left: 14px;
          width: 20px;
          height: 20px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          background: transparent;
          color: #c86910;
          font-size: 0.92rem;
          font-weight: 900;
        }
        .cat-chatbot__composer {
          padding: 8px 18px 16px;
          border-top: none;
          background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.22));
          position: relative;
          z-index: 1;
          flex-shrink: 0;
        }
        .cat-chatbot__safety {
          display: flex;
          align-items: center;
          gap: 0;
          margin: 0 0 10px;
          padding: 0;
          border-radius: 0;
          background: transparent;
          color: var(--cat-chatbot-gold-deep);
          font-size: 0.77rem;
          font-weight: 700;
          line-height: 1.45;
          border: none;
        }
        .cat-chatbot__attempts {
          margin: 0;
          font-size: 0.72rem;
          font-weight: 700;
          color: rgba(97, 44, 106, 0.76);
          white-space: nowrap;
        }
        .cat-chatbot__attempt-actions {
          display: none;
        }
        .cat-chatbot__hint {
          display: none;
        }
        .cat-chatbot__quick-replies {
          display: flex;
          gap: 8px;
          overflow-x: auto;
          padding-bottom: 6px;
          margin: 0 0 10px;
          scrollbar-width: none;
        }
        .cat-chatbot__quick-replies::-webkit-scrollbar {
          display: none;
        }
        .cat-chatbot__quick-reply {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          border: 1px solid rgba(210, 193, 222, 0.9);
          background: rgba(255, 255, 255, 0.9);
          color: #4e3b56;
          border-radius: 999px;
          padding: 10px 14px;
          font: inherit;
          font-size: 0.72rem;
          font-weight: 700;
          white-space: nowrap;
          cursor: pointer;
          box-shadow: 0 4px 12px rgba(133, 93, 152, 0.1);
          transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
        }
        .cat-chatbot__quick-reply:hover {
          transform: translateY(-1px);
          background: rgba(255, 255, 255, 0.98);
          border-color: rgba(200, 172, 220, 0.96);
        }
        .cat-chatbot__quick-icon {
          width: 16px;
          height: 16px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          border-radius: 50%;
          font-size: 0.7rem;
          line-height: 1;
          background: rgba(230, 126, 34, 0.12);
        }
        .cat-chatbot__quick-reply:disabled {
          opacity: 0.55;
          cursor: not-allowed;
          transform: none;
        }
        .cat-chatbot__form {
          display: block;
        }
        .cat-chatbot__input-shell {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 8px 8px 8px 18px;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.9);
          border: 1px solid rgba(220, 205, 232, 0.92);
          backdrop-filter: blur(12px);
          box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.5),
            0 8px 24px rgba(141, 110, 160, 0.08);
        }
        .cat-chatbot__input {
          resize: none;
          min-height: 48px;
          max-height: 132px;
          border: none;
          border-radius: 0;
          padding: 13px 0 11px;
          font: inherit;
          font-size: 0.95rem;
          color: var(--cat-chatbot-ink);
          outline: none;
          background: transparent;
          flex: 1;
          line-height: 1.4;
          box-sizing: border-box;
          display: block;
          margin: 0;
          overflow-y: auto;
        }
        .cat-chatbot__input:focus {
          box-shadow: none;
        }
        .cat-chatbot__send {
          border: none;
          border-radius: 50%;
          background: linear-gradient(135deg, #f0953b, #d86f18);
          color: #ffffff;
          font: inherit;
          font-weight: 700;
          width: 46px;
          height: 46px;
          cursor: pointer;
          min-height: 46px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 12px 24px rgba(230, 126, 34, 0.24);
        }
        .cat-chatbot__send:disabled {
          opacity: 0.6;
          cursor: wait;
          box-shadow: none;
        }
        .cat-chatbot__typing {
          display: inline-flex;
          align-items: center;
          gap: 5px;
          min-width: 44px;
          min-height: 12px;
        }
        .cat-chatbot__typing-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: rgba(107, 59, 146, 0.5);
          animation: catChatbotTyping 1s infinite ease-in-out;
        }
        .cat-chatbot__typing-dot:nth-child(2) {
          animation-delay: 0.18s;
        }
        .cat-chatbot__typing-dot:nth-child(3) {
          animation-delay: 0.36s;
        }
        @keyframes catChatbotTyping {
          0%, 80%, 100% {
            transform: translateY(0);
            opacity: 0.45;
          }
          40% {
            transform: translateY(-3px);
            opacity: 1;
          }
        }
        @media (max-width: 640px) {
          .cat-chatbot,
          .cat-chatbot.has-help-btn {
            right: 16px;
            left: 16px;
            bottom: 16px;
          }
          .cat-chatbot__toggle {
            width: 100%;
            justify-content: center;
          }
          .cat-chatbot__panel {
            width: 100%;
            height: min(74vh, 560px);
            border-radius: 24px;
          }
          .cat-chatbot__header {
            padding: 16px;
          }
          .cat-chatbot__presence {
            gap: 6px;
          }
          .cat-chatbot__subtitle {
            max-width: none;
          }
          .cat-chatbot__input-shell {
            padding-left: 14px;
          }
          .cat-chatbot__bubble {
            max-width: calc(100% - 38px);
          }
        }
      </style>
      <div class="cat-chatbot" id="catChatbotRoot">
        <div class="cat-chatbot__panel" id="catChatbotPanel" aria-live="polite">
          <div class="cat-chatbot__header">
            <div class="cat-chatbot__header-main">
              <div class="cat-chatbot__avatar" aria-hidden="true">
                <img src="assets/logo-claro.png" alt="" />
              </div>
              <div class="cat-chatbot__header-copy">
                <p class="cat-chatbot__eyebrow">Apoyo inmediato</p>
                <p class="cat-chatbot__title">Asistente Cattleya</p>
                <p class="cat-chatbot__subtitle">Orientación sobre VBG, rutas de ayuda y evaluación inicial de riesgo.</p>
                <div class="cat-chatbot__presence">
                  <span class="cat-chatbot__status-dot" aria-hidden="true"></span>
                  <span>En línea</span>
                  <span class="cat-chatbot__presence-meta">
                    <span>•</span>
                    <span class="cat-chatbot__attempts" id="catChatbotAttempts"></span>
                  </span>
                </div>
              </div>
            </div>
            <button class="cat-chatbot__close" type="button" aria-label="Cerrar chat">&times;</button>
          </div>
          <div class="cat-chatbot__messages" id="catChatbotMessages"></div>
          <div class="cat-chatbot__composer">
            <p class="cat-chatbot__safety">Si estás en peligro inmediato, llama a la Línea 155 o al 123.</p>
            <p class="cat-chatbot__hint">Si hay riesgo inmediato, llama a la Línea 155 o al 123.</p>
            <div class="cat-chatbot__quick-replies" aria-label="Sugerencias rápidas">
              <button class="cat-chatbot__quick-reply" type="button" data-prompt="¿Cuáles son las rutas de ayuda disponibles en Colombia?"><span class="cat-chatbot__quick-icon">🚨</span><span>Rutas de Ayuda</span></button>
              <button class="cat-chatbot__quick-reply" type="button" data-prompt="¿Cuáles son las principales señales de riesgo en un caso de violencia?"><span class="cat-chatbot__quick-icon">🛑</span><span>Señales de Riesgo</span></button>
              <button class="cat-chatbot__quick-reply" type="button" data-prompt="Necesito hablar con una persona o recibir orientación humana. ¿Qué opciones tengo?"><span class="cat-chatbot__quick-icon">📞</span><span>Hablar con Humano</span></button>
            </div>
            <form class="cat-chatbot__form" id="catChatbotForm">
              <div class="cat-chatbot__input-shell">
                <textarea
                  class="cat-chatbot__input"
                  id="catChatbotInput"
                  rows="1"
                  placeholder="Escribe una pregunta clara y breve..."
                ></textarea>
                <button class="cat-chatbot__send" id="catChatbotSend" type="submit" aria-label="Enviar mensaje">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M4 12L20 4L13 20L11 13L4 12Z" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>
        <button class="cat-chatbot__toggle" id="catChatbotToggle" type="button" aria-label="Abrir chatbot">
          <span class="cat-chatbot__icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 10H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M8 14H13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M12 3C6.477 3 2 6.91 2 11.733C2 14.53 3.504 17.017 5.84 18.64V22L9.49 19.992C10.291 20.145 11.133 20.233 12 20.233C17.523 20.233 22 16.323 22 11.5C22 6.677 17.523 3 12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            </svg>
          </span>
          Abrir chatbot
        </button>
      </div>
    `;

    this._root = this.querySelector('#catChatbotRoot');
    this._panel = this.querySelector('#catChatbotPanel');
    this._toggle = this.querySelector('#catChatbotToggle');
    this._close = this.querySelector('.cat-chatbot__close');
    this._messages = this.querySelector('#catChatbotMessages');
    this._form = this.querySelector('#catChatbotForm');
    this._input = this.querySelector('#catChatbotInput');
    this._send = this.querySelector('#catChatbotSend');
    this._attemptsLabel = this.querySelector('#catChatbotAttempts');
    this._quickReplyButtons = this.querySelectorAll('.cat-chatbot__quick-reply');

    this._setPlacement();
    this._updateAttemptUI();
    this._renderMessages();
    this._resizeInput();
    this._bindEvents();
  }

  _setPlacement() {
    const hasHelpBtn = Boolean(document.querySelector('cat-help-btn') || document.querySelector('.cat-help-fab'));
    this._root.classList.toggle('has-help-btn', hasHelpBtn);
  }

  _bindEvents() {
    this._toggle.addEventListener('click', () => this._openPanel());
    this._close.addEventListener('click', () => this._closePanel());
    this._form.addEventListener('submit', (event) => this._handleSubmit(event));
    this._quickReplyButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (this._isSending || this._getRemainingAttempts() <= 0) return;
        this._input.value = button.dataset.prompt || '';
        this._resizeInput();
        this._form.requestSubmit();
      });
    });
    this._input.addEventListener('input', () => this._resizeInput());
    this._input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this._form.requestSubmit();
      }
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && this._root.classList.contains('is-open')) {
        this._closePanel();
      }
    });
  }

  _openPanel() {
    this._root.classList.add('is-open');
    window.setTimeout(() => this._input.focus(), 50);
  }

  _closePanel() {
    this._root.classList.remove('is-open');
  }

  _renderMessages() {
    this._messages.innerHTML = this._conversation.map((message) => {
      const isUser = message.role === 'user';
      const isEmergency = !isUser && this._isEmergencyMessage(message.content);
      const wrapperClasses = ['cat-chatbot__message'];
      const bubbleClasses = ['cat-chatbot__bubble'];

      if (isUser) {
        wrapperClasses.push('cat-chatbot__message--user');
        bubbleClasses.push('cat-chatbot__bubble--user');
      } else if (isEmergency) {
        wrapperClasses.push('cat-chatbot__message--emergency');
        bubbleClasses.push('cat-chatbot__bubble--assistant', 'cat-chatbot__bubble--emergency');
      } else {
        bubbleClasses.push('cat-chatbot__bubble--assistant');
      }

      const avatar = !isUser && !isEmergency
        ? `
          <span class="cat-chatbot__message-avatar" aria-hidden="true">
            <img src="assets/logo-claro.png" alt="" />
          </span>
        `
        : '';

      if (isUser) {
        return `<div class="${wrapperClasses.join(' ')}"><div class="${bubbleClasses.join(' ')}">${this._escapeHtml(message.content)}</div></div>`;
      }

      return `<div class="${wrapperClasses.join(' ')}">${avatar}<div class="${bubbleClasses.join(' ')}">${this._escapeHtml(message.content)}</div></div>`;
    }).join('');

    this._messages.scrollTop = this._messages.scrollHeight;
  }

  _readAttemptsUsed() {
    try {
      const rawValue = window.sessionStorage.getItem(this._attemptsStorageKey);
      const parsed = Number.parseInt(rawValue || '0', 10);
      return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
    } catch (error) {
      return 0;
    }
  }

  _writeAttemptsUsed() {
    try {
      window.sessionStorage.setItem(this._attemptsStorageKey, String(this._attemptsUsed));
    } catch (error) {
      // Ignore storage failures; the limit still works in-memory for this page.
    }
  }

  _getRemainingAttempts() {
    return Math.max(0, this._maxAttempts - this._attemptsUsed);
  }

  _updateAttemptUI() {
    const remaining = this._getRemainingAttempts();
    if (this._attemptsLabel) {
      this._attemptsLabel.textContent = `${remaining}/${this._maxAttempts} intentos`;
    }

    const isLocked = remaining <= 0;
    if (this._input) {
      this._input.disabled = isLocked;
    }
    if (this._send) {
      this._send.disabled = isLocked || this._isSending;
    }
    this._quickReplyButtons.forEach((button) => {
      button.disabled = isLocked || this._isSending;
    });

    if (this._input) {
      this._input.placeholder = isLocked
        ? 'Ya usaste tus intentos en esta sesión.'
        : 'Escribe una pregunta clara y breve...';
    }
  }

  _appendStatus(text) {
    const status = document.createElement('div');
    status.className = 'cat-chatbot__message cat-chatbot__message--status';
    status.setAttribute('aria-label', text);
    status.innerHTML = `
      <div class="cat-chatbot__bubble cat-chatbot__bubble--status">
        <span class="cat-chatbot__typing" aria-hidden="true">
          <span class="cat-chatbot__typing-dot"></span>
          <span class="cat-chatbot__typing-dot"></span>
          <span class="cat-chatbot__typing-dot"></span>
        </span>
      </div>
    `;
    this._messages.appendChild(status);
    this._messages.scrollTop = this._messages.scrollHeight;
    return status;
  }

  _resizeInput() {
    if (!this._input) return;
    this._input.style.height = 'auto';
    const nextHeight = Math.min(this._input.scrollHeight, 132);
    this._input.style.height = `${Math.max(48, nextHeight)}px`;
  }

  async _handleSubmit(event) {
    event.preventDefault();

    if (this._getRemainingAttempts() <= 0) {
      this._conversation.push({
        role: 'assistant',
        content: `Ya alcanzaste los ${this._maxAttempts} intentos de esta sesión. Recarga la página si necesitas volver a intentar.`
      });
      this._renderMessages();
      this._updateAttemptUI();
      return;
    }

    const text = this._input.value.trim().slice(0, this._maxMessageChars);
    if (!text || this._isSending) return;

    this._conversation.push({ role: 'user', content: text });
    this._renderMessages();
    this._input.value = '';
    this._resizeInput();

    this._isSending = true;
    this._updateAttemptUI();
    const statusEl = this._appendStatus('Pensando...');

    try {
      const reply = await this._fetchReply();
      statusEl.remove();
      this._attemptsUsed += 1;
      this._writeAttemptsUsed();
      this._conversation.push({ role: 'assistant', content: reply });
      this._renderMessages();
    } catch (error) {
      statusEl.remove();
      this._conversation.push({
        role: 'assistant',
        content: String(error && error.message).trim()
          || 'No pude conectarme con el chatbot en este momento. Verifica que el servicio del chat este activo y vuelve a intentarlo.'
      });
      this._renderMessages();
    } finally {
      this._isSending = false;
      this._updateAttemptUI();
      this._input.focus();
    }
  }

  async _fetchReply() {
    const endpoint = this._resolveChatEndpoint();
    const payload = {
      messages: this._buildPayloadMessages().map((message) => ({
        role: message.role,
        content: message.content
      }))
    };

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    return String(data.reply || '').trim() || 'No recibí una respuesta del asistente.';
  }

  _buildPayloadMessages() {
    const messages = [];

    for (let index = this._conversation.length - 1; index >= 0; index -= 1) {
      const message = this._conversation[index];
      const normalized = {
        role: message.role,
        content: String(message.content || '').trim().slice(0, this._maxMessageChars)
      };

      if (!normalized.content || (normalized.role !== 'user' && normalized.role !== 'assistant')) {
        continue;
      }

      if (normalized.role === 'assistant' && messages.some((item) => item.role === 'assistant')) {
        continue;
      }

      messages.push(normalized);

      if (messages.length >= this._maxContextMessages) {
        break;
      }
    }

    messages.reverse();

    while (messages.length && messages[0].role !== 'user') {
      messages.shift();
    }

    return messages;
  }

  _resolveChatEndpoint() {
    const runtimeConfig = window.CATTLEYA_CONFIG || {};
    const configuredChatBase = String(runtimeConfig.CHATBOT_API_BASE_URL || '').trim().replace(/\/+$/, '');
    if (configuredChatBase) {
      return `${configuredChatBase}/api/chat`;
    }

    const configuredApiBase = String(runtimeConfig.API_BASE_URL || '').trim().replace(/\/+$/, '');
    if (configuredApiBase) {
      return `${configuredApiBase}/api/chat`;
    }

    const hostname = window.location.hostname;
    if (hostname === '127.0.0.1' || hostname === 'localhost') {
      return 'http://127.0.0.1:8000/api/chat';
    }

    if (window.location.protocol === 'file:') {
      return 'http://127.0.0.1:8000/api/chat';
    }

    return '/api/chat';
  }

  _escapeHtml(text) {
    return String(text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  _isEmergencyMessage(text) {
    const normalized = String(text || '').toLowerCase();
    return normalized.includes('155')
      || normalized.includes('123')
      || normalized.includes('peligro inmediato')
      || normalized.includes('línea 155')
      || normalized.includes('linea 155');
  }
}

customElements.define('cat-chatbot-btn', CatChatbotBtn);
}

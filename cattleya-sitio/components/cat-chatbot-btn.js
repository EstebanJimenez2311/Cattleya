/**
 * <cat-chatbot-btn>
 *
 * Boton flotante que abre un panel de chat para conversar con
 * el asistente de orientacion de Cattleya.
 */
class CatChatbotBtn extends HTMLElement {
  connectedCallback() {
    if (this.dataset.rendered === 'true') return;

    this.dataset.rendered = 'true';
    this._conversation = [
      {
        role: 'assistant',
        content: 'Hola, soy el asistente de Cattleya. Puedo orientarte sobre violencia basada en genero, rutas de ayuda y senales de riesgo.'
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
          --cat-chatbot-plum-deep: #5f173d;
          --cat-chatbot-rose: #f6d8e6;
          --cat-chatbot-cream: #fff8ef;
          --cat-chatbot-gold: #c86c16;
          --cat-chatbot-gold-deep: #8f4710;
          --cat-chatbot-ink: #2f1730;
          --cat-chatbot-muted: #78626f;
          --cat-chatbot-border: rgba(141, 43, 97, 0.14);
          --cat-chatbot-shadow: 0 30px 90px rgba(63, 20, 43, 0.26);
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
            radial-gradient(circle at top left, rgba(255, 208, 131, 0.42), transparent 42%),
            linear-gradient(135deg, #d97a17, #b55315);
          color: #ffffff;
          border: 1px solid rgba(255, 232, 204, 0.25);
          border-radius: 999px;
          padding: 14px 22px;
          font-size: 0.93rem;
          font-weight: 700;
          cursor: pointer;
          box-shadow:
            0 14px 34px rgba(181, 83, 21, 0.34),
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
          background: rgba(255, 255, 255, 0.16);
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.24);
        }
        .cat-chatbot__panel {
          width: min(380px, calc(100vw - 32px));
          height: min(620px, calc(100vh - 120px));
          background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 250, 244, 0.98));
          border: 1px solid var(--cat-chatbot-border);
          border-radius: 28px;
          box-shadow: var(--cat-chatbot-shadow);
          overflow: hidden;
          display: none;
          flex-direction: column;
          margin-bottom: 16px;
          backdrop-filter: blur(16px);
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
          align-items: flex-start;
          justify-content: space-between;
          gap: 16px;
          padding: 18px 18px 14px;
          background:
            radial-gradient(circle at top left, rgba(255, 210, 150, 0.24), transparent 34%),
            linear-gradient(135deg, var(--cat-chatbot-plum), var(--cat-chatbot-plum-deep));
          color: #ffffff;
          position: relative;
        }
        .cat-chatbot__header::after {
          content: '';
          position: absolute;
          inset: auto 0 0;
          height: 1px;
          background: rgba(255, 255, 255, 0.16);
        }
        .cat-chatbot__eyebrow {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          margin: 0 0 10px;
          padding: 5px 9px;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.14);
          font-size: 0.68rem;
          font-weight: 700;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .cat-chatbot__title {
          font-size: 1.08rem;
          font-weight: 700;
          margin: 0;
        }
        .cat-chatbot__subtitle {
          margin: 6px 0 0;
          max-width: 260px;
          font-size: 0.8rem;
          line-height: 1.5;
          color: rgba(255, 243, 249, 0.9);
        }
        .cat-chatbot__close {
          background: rgba(255, 255, 255, 0.12);
          color: #ffffff;
          border: 1px solid rgba(255, 255, 255, 0.12);
          width: 38px;
          height: 38px;
          border-radius: 14px;
          cursor: pointer;
          font-size: 1rem;
          flex-shrink: 0;
        }
        .cat-chatbot__messages {
          flex: 1;
          overflow-y: auto;
          padding: 18px 18px 14px;
          background:
            radial-gradient(circle at top, rgba(255, 215, 228, 0.22), transparent 24%),
            linear-gradient(180deg, #fffafc, #fff6ef 54%, #fffdfb 100%);
          display: flex;
          flex-direction: column;
          gap: 10px;
          position: relative;
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
        .cat-chatbot__bubble {
          max-width: 88%;
          padding: 12px 14px;
          border-radius: 20px;
          font-size: 0.92rem;
          line-height: 1.6;
          white-space: pre-wrap;
          box-shadow: 0 10px 26px rgba(68, 24, 43, 0.08);
          position: relative;
        }
        .cat-chatbot__bubble--assistant {
          align-self: flex-start;
          background: linear-gradient(180deg, #ffffff, #fdeff5);
          color: #4c1734;
          border: 1px solid rgba(157, 45, 106, 0.08);
          border-bottom-left-radius: 8px;
        }
        .cat-chatbot__bubble--user {
          align-self: flex-end;
          background: linear-gradient(135deg, #d97a17, #bf5915);
          color: #ffffff;
          border: 1px solid rgba(147, 69, 16, 0.16);
          border-bottom-right-radius: 8px;
        }
        .cat-chatbot__bubble--status {
          align-self: center;
          background: rgba(141, 43, 97, 0.09);
          color: #6b1a47;
          font-size: 0.8rem;
          border: 1px solid rgba(141, 43, 97, 0.08);
          box-shadow: none;
        }
        .cat-chatbot__composer {
          padding: 16px;
          border-top: 1px solid rgba(157, 45, 106, 0.12);
          background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(255, 247, 241, 0.98));
        }
        .cat-chatbot__safety {
          display: flex;
          align-items: center;
          gap: 8px;
          margin: 0 0 12px;
          padding: 10px 12px;
          border-radius: 16px;
          background: linear-gradient(135deg, #fff4df, #ffecd0);
          color: var(--cat-chatbot-gold-deep);
          font-size: 0.76rem;
          font-weight: 700;
          line-height: 1.45;
          border: 1px solid rgba(200, 108, 22, 0.14);
        }
        .cat-chatbot__notice {
          margin: 0 0 10px;
          padding: 10px 12px;
          border-radius: 16px;
          background: #fffaf2;
          color: #7a3d00;
          font-size: 0.76rem;
          line-height: 1.45;
          border: 1px solid rgba(200, 108, 22, 0.12);
        }
        .cat-chatbot__attempts {
          margin: 0 0 10px;
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--cat-chatbot-plum);
        }
        .cat-chatbot__attempt-actions {
          display: flex;
          justify-content: flex-end;
          margin: -4px 0 10px;
        }
        .cat-chatbot__reset {
          border: none;
          background: transparent;
          color: var(--cat-chatbot-plum);
          font: inherit;
          font-size: 0.74rem;
          font-weight: 700;
          cursor: pointer;
          padding: 0;
        }
        .cat-chatbot__hint {
          font-size: 0.75rem;
          color: #7b6b75;
          margin: 0 0 10px;
        }
        .cat-chatbot__form {
          display: grid;
          grid-template-columns: 1fr auto;
          gap: 10px;
          align-items: end;
        }
        .cat-chatbot__input {
          resize: none;
          min-height: 52px;
          max-height: 132px;
          border: 1px solid rgba(157, 45, 106, 0.18);
          border-radius: 18px;
          padding: 14px 15px;
          font: inherit;
          color: #333333;
          outline: none;
          background: rgba(255, 255, 255, 0.92);
        }
        .cat-chatbot__input:focus {
          border-color: var(--cat-chatbot-plum);
          box-shadow: 0 0 0 4px rgba(157, 45, 106, 0.12);
        }
        .cat-chatbot__send {
          border: none;
          border-radius: 18px;
          background: linear-gradient(135deg, var(--cat-chatbot-plum), #741f4d);
          color: #ffffff;
          font: inherit;
          font-weight: 700;
          padding: 12px 18px;
          cursor: pointer;
          min-height: 52px;
          box-shadow: 0 12px 24px rgba(141, 43, 97, 0.18);
        }
        .cat-chatbot__send:disabled {
          opacity: 0.6;
          cursor: wait;
          box-shadow: none;
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
          .cat-chatbot__form {
            grid-template-columns: 1fr;
          }
          .cat-chatbot__send {
            width: 100%;
          }
        }
      </style>
      <div class="cat-chatbot" id="catChatbotRoot">
        <div class="cat-chatbot__panel" id="catChatbotPanel" aria-live="polite">
          <div class="cat-chatbot__header">
            <div>
              <p class="cat-chatbot__eyebrow">Apoyo inmediato</p>
              <p class="cat-chatbot__title">Asistente Cattleya</p>
              <p class="cat-chatbot__subtitle">Orientacion sobre VBG, rutas de ayuda y evaluacion inicial de riesgo.</p>
            </div>
            <button class="cat-chatbot__close" type="button" aria-label="Cerrar chat">x</button>
          </div>
          <div class="cat-chatbot__messages" id="catChatbotMessages"></div>
          <div class="cat-chatbot__composer">
            <p class="cat-chatbot__safety">Si estas en peligro inmediato, llama a la Linea 155 o al 123.</p>
            <p class="cat-chatbot__notice">Se clara y concreta. Describe tu situacion o pregunta en un solo mensaje breve.</p>
            <p class="cat-chatbot__attempts" id="catChatbotAttempts"></p>
            <div class="cat-chatbot__attempt-actions">
              <button class="cat-chatbot__reset" id="catChatbotReset" type="button">Reiniciar intentos</button>
            </div>
            <p class="cat-chatbot__hint">Si hay riesgo inmediato, llama a la Linea 155 o al 123.</p>
            <form class="cat-chatbot__form" id="catChatbotForm">
              <textarea
                class="cat-chatbot__input"
                id="catChatbotInput"
                rows="1"
                placeholder="Escribe una pregunta clara y breve..."
              ></textarea>
              <button class="cat-chatbot__send" id="catChatbotSend" type="submit">Enviar</button>
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
    this._resetAttemptsBtn = this.querySelector('#catChatbotReset');

    this._setPlacement();
    this._updateAttemptUI();
    this._renderMessages();
    this._bindEvents();
  }

  _setPlacement() {
    const hasHelpBtn = Boolean(document.querySelector('cat-help-btn') || document.querySelector('.cat-help-fab'));
    this._root.classList.toggle('has-help-btn', hasHelpBtn);
  }

  _bindEvents() {
    this._toggle.addEventListener('click', () => this._openPanel());
    this._close.addEventListener('click', () => this._closePanel());
    this._resetAttemptsBtn.addEventListener('click', () => this._resetAttempts());
    this._form.addEventListener('submit', (event) => this._handleSubmit(event));
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
      const roleClass = message.role === 'user'
        ? 'cat-chatbot__bubble--user'
        : 'cat-chatbot__bubble--assistant';

      return `<div class="cat-chatbot__bubble ${roleClass}">${this._escapeHtml(message.content)}</div>`;
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

  _resetAttempts() {
    this._attemptsUsed = 0;
    this._writeAttemptsUsed();
    this._updateAttemptUI();
    this._conversation.push({
      role: 'assistant',
      content: 'Reinicie el contador de intentos de esta sesion para seguir probando.'
    });
    this._renderMessages();
  }

  _updateAttemptUI() {
    const remaining = this._getRemainingAttempts();
    if (this._attemptsLabel) {
      this._attemptsLabel.textContent = `Intentos disponibles en esta sesion: ${remaining} de ${this._maxAttempts}.`;
    }

    const isLocked = remaining <= 0;
    if (this._input) {
      this._input.disabled = isLocked;
    }
    if (this._send) {
      this._send.disabled = isLocked || this._isSending;
    }

    if (this._input) {
      this._input.placeholder = isLocked
        ? 'Ya usaste tus intentos en esta sesion.'
        : 'Escribe una pregunta clara y breve...';
    }
  }

  _appendStatus(text) {
    const status = document.createElement('div');
    status.className = 'cat-chatbot__bubble cat-chatbot__bubble--status';
    status.textContent = text;
    this._messages.appendChild(status);
    this._messages.scrollTop = this._messages.scrollHeight;
    return status;
  }

  async _handleSubmit(event) {
    event.preventDefault();

    if (this._getRemainingAttempts() <= 0) {
      this._conversation.push({
        role: 'assistant',
        content: `Ya alcanzaste los ${this._maxAttempts} intentos de esta sesion. Recarga la pagina si necesitas volver a intentar.`
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

    return String(data.reply || '').trim() || 'No recibi una respuesta del asistente.';
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
    const configuredBase = String(runtimeConfig.CHATBOT_API_BASE_URL || '').trim().replace(/\/+$/, '');
    if (configuredBase) {
      return `${configuredBase}/api/chat`;
    }

    const hostname = window.location.hostname;
    if (hostname === '127.0.0.1' || hostname === 'localhost') {
      return 'http://127.0.0.1:5000/api/chat';
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
}

customElements.define('cat-chatbot-btn', CatChatbotBtn);

import { APIService } from './service/apiService.js';
import { UIManager } from './js/uiManager.js';
import { FormButtons } from './js/formButtons.js';

document.addEventListener('DOMContentLoaded', () => {
    try {
        const uiManager = new UIManager();
        const apiService = new APIService();
        const app = new FormButtons(uiManager, apiService);
        app.initialize();
    } catch (error) {
        console.error("Falha ao inicializar a aplicação:", error);
        alert("Ocorreu um erro crítico ao carregar a página. Por favor, recarregue.");
    }
});
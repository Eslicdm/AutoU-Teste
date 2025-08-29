import { APIService } from './apiService.js';
import { UIManager } from './uiManager.js';
import { App } from './app.js';

document.addEventListener('DOMContentLoaded', () => {
    try {
        const uiManager = new UIManager();
        const apiService = new APIService();
        const app = new App(uiManager, apiService);
        app.initialize();
    } catch (error) {
        console.error("Falha ao inicializar a aplicação:", error);
        alert("Ocorreu um erro crítico ao carregar a página. Por favor, recarregue.");
    }
});
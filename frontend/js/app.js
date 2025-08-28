export class App {
    constructor(uiManager, apiService) {
        this.ui = uiManager;
        this.api = apiService;
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        const formData = this.ui.getFormData();
        if (!formData) {
            this.ui.displayError('Por favor, insira o texto de um email ou selecione um arquivo.');
            return;
        }
        this.ui.setLoading(true);
        try {
            const result = await this.api.processEmail(formData);
            this.ui.displayResults(result);
        } catch (error) {
            this.ui.displayError(error.message);
        } finally {
            this.ui.setLoading(false);
        }
    }

    handleClearClick() {
        this.ui.clearAll();
    }

    initialize() {
        this.ui.listenForFileChanges();
        this.ui.emailTextInput.addEventListener('input', () => this.ui.updateSubmitButtonState());
        this.ui.form.addEventListener('submit', (event) => this.handleFormSubmit(event));
        this.ui.clearButton.addEventListener('click', () => this.handleClearClick());
    }
}
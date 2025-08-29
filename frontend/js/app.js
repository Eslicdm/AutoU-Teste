export class App {
    constructor(uiManager, apiService) {
        this.ui = uiManager;
        this.api = apiService;
    }

    async handleFormSubmit(event) {
        event.preventDefault();

        const hasText = this.ui.emailTextInput.value.trim() !== '';
        const hasFile = this.ui.emailFileInput.files.length > 0;

        if (hasText && hasFile) {
            this.ui.displayError('Por favor, envie apenas texto ou um arquivo, não ambos.');
            return;
        }

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
        this.ui.form.addEventListener('submit', (event) => this.handleFormSubmit(event));
        this.ui.clearButton.addEventListener('click', () => this.handleClearClick());
    }
}
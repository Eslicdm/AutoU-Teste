export class UIManager {
    constructor() {
        this.form = document.getElementById('email-form');
        this.emailTextInput = document.getElementById('email-text');
        this.emailFileInput = document.getElementById('email-file');
        this.fileNameDisplay = document.getElementById('file-name');
        this.resultsDiv = document.getElementById('results');
        this.classificationDescription = document.getElementById('classification-description');
        this.classificationResultSpan = document.getElementById('classification-result');
        this.suggestedResponseDiv = document.getElementById('suggested-response-text');
        this.submitButton = document.getElementById('submit-button');
        this.spinner = this.submitButton.querySelector('.spinner-border');
        this.clearButton = document.getElementById('clear-button');
    }

    setLoading(isLoading) {
        this.submitButton.disabled = isLoading;
        this.spinner.classList.toggle('d-none', !isLoading);
        if (isLoading) {
            this.resultsDiv.classList.add('d-none');
        }
    }

    displayResults(data) {
        this.classificationResultSpan.textContent = data.classification;
        this.classificationResultSpan.className = 'badge fs-6'; // Reseta as classes
        if (data.classification === 'Produtivo') {
            this.classificationResultSpan.classList.add('bg-success');
        } else {
            this.classificationResultSpan.classList.add('bg-warning', 'text-dark');
        }
        this.suggestedResponseDiv.textContent = data.response;
        this.classificationDescription.textContent = data.description;
        this.resultsDiv.classList.remove('d-none');
        requestAnimationFrame(() => {
            this.resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    displayError(message) {
        alert(message);
    }

    getFormData() {
        const formData = new FormData();
        if (this.emailTextInput.value.trim()) {
            formData.append('email_text', this.emailTextInput.value.trim());
        } else if (this.emailFileInput.files.length > 0) {
            formData.append('email_file', this.emailFileInput.files[0]);
        } else {
            return null;
        }
        return formData;
    }

    clearAll() {
        this.emailTextInput.value = '';
        this.emailFileInput.value = null;
        this.fileNameDisplay.textContent = '';
        this.resultsDiv.classList.add('d-none');
        this.submitButton.disabled = false;
        this.emailTextInput.focus();
    }

    listenForFileChanges() {
        this.emailFileInput.addEventListener('change', () => {
            this.fileNameDisplay.textContent =
                this.emailFileInput.files.length > 0 ?
                    `Arquivo: ${this.emailFileInput.files[0].name}` : '';
        });
    }
}
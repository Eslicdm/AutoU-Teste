export class APIService {
    async processEmail(formData) {
        try {
            const response = await fetch('/process-email/', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Ocorreu um erro no servidor.');
            }
            return data;
        } catch (error) {
            throw new Error(`Erro na comunicação com o servidor: ${error.message}`);
        }
    }
}
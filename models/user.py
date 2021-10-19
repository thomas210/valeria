from error import errorCode
from email.utils import parseaddr
import streamlit as st
import requests

class User:

    def __init__(self) -> None:
        
        self.errorCode = errorCode.getErrors()

    def validate(self):
        """Realiza a validação dos campos de contato do usuário para analisar se é possível enviar as informações.
        
        Valições:
            Campos Vazios: É analisado se todos os campos possuem algo preenchido.
            E-mail: É analisado se o texto preenchido no cmpo condiz com um email válido.

        Returns:
            Enum.ErrorCode: Código de erro caso a validação não seja aprovada. Caso não ocorra erro nenum com a validação o codigo SUCCESS é enviado.
        """
        inputs_validate = [self.name, self.email, self.message]

        for input in inputs_validate:
            if not input :
                return self.errorCode.ERROR_MISSING.name, self.errorCode.ERROR_MISSING.value
        
        self.email = parseaddr(self.email)[1]
        if ("mail.com" not in self.email) or ("@" not in self.email):
            return self.errorCode.ERROR_MAIL.name, self.errorCode.ERROR_MAIL.value

        return self.errorCode.SUCCESS.name, self.errorCode.SUCCESS.value

    def sendEmail(self):
        """Envia a mensagem para a equipe contato o nome do usuário, a mensagem enviada e um e-mail para contato.
            
            Devido ao fato de tecnologia atual, a mensagem é enviada pelo bot VALERIA para o nosso grupo no telegram.
        """

        initial_message = "Olá pessoal, temos um usuário que deseja ajuda no nosso sistema e infelizmente não fui capaz de ajudar. Por favor, resposndam ele o quanot antes!"
        message = f"👨‍💻👩‍💻 Autor: {self.name} \n ✉️ E-mail para contato: {self.email} \n 📄 Mesagem: {self.message}"
        bot_token = st.secrets["telegram_token"]
        bot_chatID = st.secrets["chat_id"]
        send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={initial_message}"
        requests.get(send_text)

        send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={message}"
        requests.get(send_text)
        
    # Setters.

    def setName(self, value):
        self.name = value

    def setEmail(self, value):
        self.email = value

    def setMessage(self, value):
        self.message = value
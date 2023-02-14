"""
AQUI VA EL CODIGO DEL TOKEN DE CONFIRMACION DE CUENTA

"""
# importamos la clase PasswordResetTokenGenerator esta clase 
# nos permite generar un token para confirmar la cuenta
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
import six 

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Esta clase nos permite generar un token para confirmar la cuenta
    para que el usuario pueda activar su cuenta.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()
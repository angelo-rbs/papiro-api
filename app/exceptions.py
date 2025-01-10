


class PapiroApiException(Exception):
    """Classe base de exceções"""

    def __init__(self, message: str = 'Serviço indisponível', name: str = 'Papiro'):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class NotFoundException(PapiroApiException):
    """Entidade não encontrada na base de dados"""
    def __init__(self, message: str = 'Entidade não encontrada', name: str = 'Papiro'):
        super().__init__(message, name)


class UnauthorizedException(PapiroApiException):
    """Autorização negada"""
    def __init__(self, message: str = 'Autorização negada', name: str = 'Papiro'):
        super().__init__(message, name)


class AlreadyExistsException(PapiroApiException):
    """Conflito: Entidade já existente"""
    def __init__(self, message: str = 'Entidade já existente', name: str = 'Papiro'):
        super().__init__(message, name)


class InvalidOperationException(PapiroApiException):
    """Operação inválida"""
    def __init__(self, message: str = 'Operação inválida', name: str = 'Papiro'):
        super().__init__(message, name)


class InvalidTokenException(PapiroApiException):
    """Token inválido"""
    def __init__(self, message: str = 'Token inválido', name: str = 'Papiro'):
        super().__init__(message, name)

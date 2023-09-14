from rolepermissions.roles import AbstractUserRole

class Prex(AbstractUserRole):
    available_permissions = {'criar_editais': True, 'avalia_projetos': True}
    
class Aluno(AbstractUserRole):
    available_permissions = {'ver_editais': True, 'insc_editais': True}
    
class Professor(AbstractUserRole):
    available_permissions = {'cria_projetos': True}
    
class Admin(AbstractUserRole):
    available_permissions = {'cadastrar_prex': True}
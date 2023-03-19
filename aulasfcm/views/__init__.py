from .indexView import index
from .aulasView import AulasList, AulasUpdate, AulasCreate, AulasDelete, AulasDetail
from .edificiosView import EdificiosList, EdificiosUpdate, EdificiosCreate, EdificiosDelete, EdificiosDetail, destroy_gestor_edificio, create_gestor_edificio
from .entidadesView import EntidadesList, EntidadesUpdate, EntidadesCreate, EntidadesDelete, EntidadesDetail
from .usuariosView import PasswordChangeView, CustomPasswordChangeView, UsuariosUpdate, CustomUsuariosUpdate, UsuariosList
from .gestoresView import GestoresList
from .calendarView import CalendarView
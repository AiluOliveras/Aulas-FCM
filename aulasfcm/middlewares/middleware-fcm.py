from ..models import Operaciones
from datetime import datetime

def simple_middleware(get_response):

    def middleware(request):
        # logs para admin
        
        if request.user.is_authenticated:

            # get de los params
            params=None
            parametros= request.GET
            if parametros:
                params='?'
                for p,c in parametros.lists():
                    params= params+(p+'='+c[0])+'&'
                params=params[:-1]

                #almaceno params en el log
                log = Operaciones(operacion=str(request.method), endpoint=(str(request.path)+params), fecha=datetime.now(),usuario_id=request.user.id)
            else:
                log = Operaciones(operacion=str(request.method), endpoint=str(request.path), fecha=datetime.now(),usuario_id=request.user.id)
                
            log.save()

        response = get_response(request)

        return response

    return middleware
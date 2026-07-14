import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Simpamos la obtención de un token de seguridad (JWT) guardado, por ejemplo, en la sesión
  const tokenSimulado = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.VerssaXTokenSecret2026';

  console.log(`🛡️ [Interceptor] Interceptada petición saliente hacia: ${req.url}`);

  // En Angular las peticiones son inmutables. Para modificarlas debemos clonarlas
  const reqClonada = req.clone({
    setHeaders: {
      Authorization: `Bearer ${tokenSimulado}`,
      'X-Client-Platform': 'Angular-Enterprise',
      'X-Requested-With': 'XMLHttpRequest'
    }
  });

  // Pasamos la petición clonada al siguiente paso en la tubería del cliente HTTP
  return next(reqClonada);
};
import { useEffect } from 'react';
import { useLocation } from 'wouter';

export default function NotFound() {
  const [, setLocation] = useLocation();

  useEffect(() => {
    const timer = setTimeout(() => {
      setLocation('/');
    }, 3000);

    return () => clearTimeout(timer);
  }, [setLocation]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="max-w-md w-full bg-card rounded-lg shadow-lg p-8 text-center">
        <h1 className="text-4xl font-bold text-primary mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-card-foreground mb-2">Página no encontrada</h2>
        <p className="text-muted-foreground mb-6">
          La página que estás buscando no existe o ha sido movida.
        </p>
        <p className="text-muted-foreground">
          Serás redirigido a la página principal en unos segundos...
        </p>
        <button
          onClick={() => setLocation('/')}
          className="mt-6 inline-flex items-center justify-center bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium transition-colors"
        >
          Volver al inicio
        </button>
      </div>
    </div>
  );
}
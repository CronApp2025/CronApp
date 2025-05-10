import { QueryClient, QueryFunction } from "@tanstack/react-query";
import { API_URL } from './constants';

// Base URL para la API de Flask
// Utilizamos la URL configurada en constants.ts que apunta al puerto correcto del servidor Flask (5002)
// en lugar de basarnos en el origen de la ventana actual
const API_BASE_URL = API_URL;

async function throwIfResNotOk(res: Response) {
  if (!res.ok) {
    let errorMessage: string;
    try {
      // La API Flask normalmente devuelve errores en formato JSON con message
      const errorData = await res.json();
      errorMessage = errorData.message || errorData.msg || res.statusText;
    } catch (e) {
      // Si no es JSON, usar el texto directamente
      errorMessage = await res.text() || res.statusText;
    }
    throw new Error(`${res.status}: ${errorMessage}`);
  }
}

export async function apiRequest(
  method: string,
  url: string,
  data?: unknown | undefined,
  options?: {
    headers?: Record<string, string>;
  }
): Promise<Response> {
  // Añadir el token a los headers si existe
  const token = localStorage.getItem("token");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers || {})
  };
  
  if (token && !headers["Authorization"]) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  
  // Asegurarse de que url comienza con /api
  const fullUrl = url.startsWith("/api") 
    ? `${API_BASE_URL}${url}` 
    : `${API_BASE_URL}/api${url.startsWith("/") ? url : `/${url}`}`;

  console.log(`Haciendo petición ${method} a ${fullUrl}`);
  
  const res = await fetch(fullUrl, {
    method,
    headers,
    body: data ? JSON.stringify(data) : undefined,
    credentials: "include",
  });

  await throwIfResNotOk(res);
  return res;
}

type UnauthorizedBehavior = "returnNull" | "throw";
export const getQueryFn: <T>(options: {
  on401: UnauthorizedBehavior;
}) => QueryFunction<T> =
  ({ on401: unauthorizedBehavior }) =>
  async ({ queryKey }) => {
    const url = queryKey[0] as string;
    // Construir la URL completa para la API de Flask
    const fullUrl = url.startsWith("/api") 
      ? `${API_BASE_URL}${url}` 
      : `${API_BASE_URL}/api${url.startsWith("/") ? url : `/${url}`}`;
    
    // Añadir el token a los headers si existe
    const token = localStorage.getItem("token");
    const headers: Record<string, string> = {};
    
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    
    console.log(`Haciendo petición GET a ${fullUrl}`);

    const res = await fetch(fullUrl, {
      credentials: "include",
      headers,
    });

    if (unauthorizedBehavior === "returnNull" && res.status === 401) {
      return null;
    }

    await throwIfResNotOk(res);
    try {
      const data = await res.json();
      // La API devuelve data dentro de un objeto con success y message
      return data.data || data;
    } catch (error) {
      console.error("Error parsing JSON:", error);
      throw new Error("Error parsing server response");
    }
  };

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: getQueryFn({ on401: "throw" }),
      refetchInterval: false,
      refetchOnWindowFocus: true,
      staleTime: 1000 * 60 * 5, // 5 minutos
      retry: 1,
    },
    mutations: {
      retry: 1,
    },
  },
});

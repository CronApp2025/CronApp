// Tipos de usuario
export interface User {
  id: number | string;
  nombre: string;
  apellido?: string;
  email: string;
  rol?: string;
  especialidad?: string;
  created_at?: string;
  updated_at?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface GoogleLoginData {
  token: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  password: string;
  confirmPassword: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

// Tipos para pacientes
export interface Patient {
  id: number;
  fullName: string;
  age: number;
  gender: string;
  status: string;
  fecha_nacimiento?: string;
  conditions: PatientCondition[];
}

export interface PatientCondition {
  id: number;
  name: string;
  icon?: string;
  lastUpdated: string;
}

// Tipos para condiciones médicas
export interface Condition {
  id: number;
  name: string;
  category: string;
  icon: string;
  description?: string;
  severity: number;
  status: string;
  lastUpdated: string;
  patientId?: number;
}

// Tipos para alertas
export interface Alert {
  id: number;
  patientId: number;
  title: string;
  description: string;
  timestamp: string;
  riskLevel: number;
  isRead?: boolean;
  category?: string;
}

// Tipos para recursos educativos
export interface EducationalResource {
  id: number;
  title: string;
  description: string;
  category: string;
  url?: string;
  publishedAt: string;
  readTime: number;
  isRecommended?: boolean;
}

// Tipos para configuraciones
export interface UserSettings {
  notificaciones: boolean;
  idioma: string;
  temaOscuro: boolean;
}

// Tipos de respuesta API
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combina clases de Tailwind y resuelve conflictos
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formatea una fecha de string a formato legible
 * @param dateString Fecha en formato ISO o string
 * @returns Fecha formateada (ej. "20 Abr 2023, 15:30")
 */
export function formatDateString(dateString: string | Date): string {
  if (!dateString) return "";
  
  const date = new Date(dateString);
  
  // Si la fecha es inválida
  if (isNaN(date.getTime())) return dateString.toString();
  
  // Nombres de meses abreviados
  const months = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun", 
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
  ];
  
  const day = date.getDate();
  const month = months[date.getMonth()];
  const year = date.getFullYear();
  const hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, "0");
  
  return `${day} ${month} ${year}, ${hours}:${minutes}`;
}

/**
 * Calcula la edad a partir de una fecha de nacimiento
 * @param birthDate Fecha de nacimiento
 * @returns Edad en años
 */
export function calculateAge(birthDate: string | Date): number {
  if (!birthDate) return 0;
  
  const today = new Date();
  const birth = new Date(birthDate);
  
  // Si la fecha es inválida
  if (isNaN(birth.getTime())) return 0;
  
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  
  // Si aún no ha cumplido años este año
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
}

/**
 * Formatea nombre y apellido en un nombre completo
 * @param firstName Nombre
 * @param lastName Apellido
 * @returns Nombre completo
 */
export function formatFullName(firstName: string, lastName?: string): string {
  if (!firstName) return "";
  return lastName ? `${firstName} ${lastName}` : firstName;
}

/**
 * Obtiene las iniciales de un nombre
 * @param name Nombre completo
 * @returns Iniciales (máximo 2 caracteres)
 */
export function getInitials(name: string): string {
  if (!name) return "";
  
  const parts = name.trim().split(/\s+/);
  
  if (parts.length === 1) {
    return parts[0].charAt(0).toUpperCase();
  }
  
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

/**
 * Trunca un texto si excede la longitud máxima
 * @param text Texto a truncar
 * @param maxLength Longitud máxima
 * @returns Texto truncado con elipsis si es necesario
 */
export function truncateText(text: string, maxLength: number): string {
  if (!text || text.length <= maxLength) return text || "";
  return `${text.substring(0, maxLength)}...`;
}

/**
 * Comprueba si un valor es null o undefined
 */
export function isNullOrUndefined(value: any): boolean {
  return value === null || value === undefined;
}

/**
 * Genera un identificador único
 * @returns String UUID
 */
export function generateUUID(): string {
  return crypto.randomUUID ? crypto.randomUUID() : 
    'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0, 
        v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}

/**
 * Convierte bytes en un formato legible
 * @param bytes Tamaño en bytes
 * @returns Tamaño formateado (ej. "1.5 MB")
 */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Suaviza una transición de scroll
 * @param elementId ID del elemento al que hacer scroll
 */
export function scrollToElement(elementId: string): void {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

/**
 * Formatea un número como porcentaje
 * @param value Valor numérico
 * @param decimalPlaces Lugares decimales
 * @returns Porcentaje formateado (ej. "42.5%")
 */
export function formatPercentage(value: number, decimalPlaces: number = 1): string {
  if (isNaN(value)) return "0%";
  return `${value.toFixed(decimalPlaces)}%`;
}

/**
 * Genera un color basado en un texto
 * @param text Texto de entrada
 * @returns Color en hexadecimal
 */
export function stringToColor(text: string): string {
  if (!text) return "#6941C6"; // Color predeterminado
  
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = text.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  let color = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xFF;
    color += ('00' + value.toString(16)).substr(-2);
  }
  
  return color;
}
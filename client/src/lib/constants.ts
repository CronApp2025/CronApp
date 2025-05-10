// Constantes de la aplicación

// Configuración para la API - usando el mismo dominio/puerto que el frontend
export const API_URL = import.meta.env.VITE_API_URL || window.location.origin;

// Roles de usuario
export const USER_ROLES = {
  ADMIN: 'admin',
  DOCTOR: 'doctor',
  NURSE: 'enfermero'
};

// Mensajes de error
export const ERROR_MESSAGES = {
  LOGIN_FAILED: 'Credenciales incorrectas. Por favor, inténtalo de nuevo.',
  NETWORK_ERROR: 'Error de conexión. Por favor, verifica tu conexión a internet.',
  UNKNOWN_ERROR: 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo.',
  SESSION_EXPIRED: 'Tu sesión ha expirado. Por favor, inicia sesión de nuevo.',
  INVALID_FORM: 'Por favor, completa correctamente todos los campos requeridos.',
  FORBIDDEN: 'No tienes permiso para realizar esta acción.',
  NOT_FOUND: 'El recurso solicitado no ha sido encontrado.'
};

// Tiempos de expiración
export const TOKEN_EXPIRATION = 15 * 60 * 1000; // 15 minutos en milisegundos
export const REFRESH_TOKEN_EXPIRATION = 7 * 24 * 60 * 60 * 1000; // 7 días en milisegundos

// Datos de ejemplo para la interfaz de usuario
export const MOCK_PATIENTS = [
  {
    id: 1,
    fullName: "María González",
    age: 68,
    gender: "Femenino",
    status: "Estable",
    fecha_nacimiento: "1956-03-15",
    conditions: [
      { id: 1, name: "Diabetes Tipo 2", icon: "🩸", lastUpdated: "2023-12-10T14:30:00" },
      { id: 2, name: "Hipertensión", icon: "❤️", lastUpdated: "2023-12-12T10:15:00" },
      { id: 3, name: "Artritis", icon: "🦴", lastUpdated: "2023-11-30T09:45:00" }
    ]
  },
  {
    id: 2,
    fullName: "Carlos Martínez",
    age: 72,
    gender: "Masculino",
    status: "En tratamiento",
    fecha_nacimiento: "1952-07-22",
    conditions: [
      { id: 4, name: "EPOC", icon: "🫁", lastUpdated: "2023-12-08T11:00:00" },
      { id: 5, name: "Insuficiencia Cardíaca", icon: "❤️", lastUpdated: "2023-12-05T16:30:00" }
    ]
  },
  {
    id: 3,
    fullName: "Ana Rodríguez",
    age: 65,
    gender: "Femenino",
    status: "Mejorando",
    fecha_nacimiento: "1959-11-08",
    conditions: [
      { id: 6, name: "Osteoporosis", icon: "🦴", lastUpdated: "2023-12-01T13:45:00" },
      { id: 7, name: "Hipotiroidismo", icon: "🦋", lastUpdated: "2023-11-28T10:30:00" }
    ]
  }
];

export const CONDITIONS = [
  {
    id: 1,
    name: "Diabetes Tipo 2",
    category: "Endocrina",
    icon: "🩸",
    description: "Niveles elevados de glucosa en sangre con resistencia a la insulina.",
    severity: 7,
    status: "Activo",
    lastUpdated: "2023-12-10T14:30:00",
    patientId: 1
  },
  {
    id: 2,
    name: "Hipertensión",
    category: "Cardiovascular",
    icon: "❤️",
    description: "Presión arterial elevada de forma crónica.",
    severity: 6,
    status: "En tratamiento",
    lastUpdated: "2023-12-12T10:15:00",
    patientId: 1
  },
  {
    id: 3,
    name: "Artritis",
    category: "Reumatológica",
    icon: "🦴",
    description: "Inflamación de las articulaciones con dolor y rigidez.",
    severity: 5,
    status: "Crónico",
    lastUpdated: "2023-11-30T09:45:00",
    patientId: 1
  },
  {
    id: 4,
    name: "EPOC",
    category: "Respiratoria",
    icon: "🫁",
    description: "Enfermedad pulmonar obstructiva crónica con dificultad respiratoria.",
    severity: 8,
    status: "Activo",
    lastUpdated: "2023-12-08T11:00:00",
    patientId: 2
  },
  {
    id: 5,
    name: "Insuficiencia Cardíaca",
    category: "Cardiovascular",
    icon: "❤️",
    description: "Capacidad reducida del corazón para bombear sangre.",
    severity: 9,
    status: "En tratamiento",
    lastUpdated: "2023-12-05T16:30:00",
    patientId: 2
  },
  {
    id: 6,
    name: "Osteoporosis",
    category: "Ósea",
    icon: "🦴",
    description: "Pérdida de densidad ósea con riesgo de fracturas.",
    severity: 4,
    status: "En seguimiento",
    lastUpdated: "2023-12-01T13:45:00",
    patientId: 3
  },
  {
    id: 7,
    name: "Hipotiroidismo",
    category: "Endocrina",
    icon: "🦋",
    description: "Producción insuficiente de hormonas tiroideas.",
    severity: 3,
    status: "Controlado",
    lastUpdated: "2023-11-28T10:30:00",
    patientId: 3
  }
];

export const RISK_ALERTS = [
  {
    id: 1,
    patientId: 1,
    title: "Glucosa elevada",
    description: "Niveles de glucosa consistentemente por encima de 200 mg/dL en las últimas lecturas",
    timestamp: "2023-12-14T08:30:00",
    riskLevel: 85,
    isRead: false,
    category: "Glucemia"
  },
  {
    id: 2,
    patientId: 1,
    title: "Presión arterial elevada",
    description: "Presión arterial promedio de 160/95 mmHg en las últimas 3 mediciones",
    timestamp: "2023-12-13T16:45:00",
    riskLevel: 70,
    isRead: true,
    category: "Presión arterial"
  },
  {
    id: 3,
    patientId: 1,
    title: "Riesgo de interacción medicamentosa",
    description: "La combinación de medicamentos actuales puede aumentar el riesgo de efectos adversos",
    timestamp: "2023-12-12T11:20:00",
    riskLevel: 60,
    isRead: false,
    category: "Medicación"
  },
  {
    id: 4,
    patientId: 1,
    title: "Baja adherencia al tratamiento",
    description: "La paciente ha reportado olvidar tomar sus medicamentos en el último mes",
    timestamp: "2023-12-10T09:15:00",
    riskLevel: 50,
    isRead: true,
    category: "Adherencia"
  },
  {
    id: 5,
    patientId: 2,
    title: "Saturación de oxígeno reducida",
    description: "Saturación de oxígeno por debajo del 90% en las últimas mediciones",
    timestamp: "2023-12-14T10:00:00",
    riskLevel: 90,
    isRead: false,
    category: "Respiratorio"
  },
  {
    id: 6,
    patientId: 2,
    title: "Aumento de edema periférico",
    description: "Incremento significativo del edema en extremidades inferiores",
    timestamp: "2023-12-13T14:30:00",
    riskLevel: 75,
    isRead: false,
    category: "Cardiovascular"
  },
  {
    id: 7,
    patientId: 3,
    title: "Riesgo de caída elevado",
    description: "La evaluación de riesgo de caídas muestra un puntaje de 14/20",
    timestamp: "2023-12-14T09:45:00",
    riskLevel: 65,
    isRead: true,
    category: "Movilidad"
  }
];

export const EDUCATIONAL_RESOURCES = [
  {
    id: 1,
    title: "Manejo Diario de la Diabetes Tipo 2",
    description: "Guía completa para el control de la glucosa, alimentación adecuada y actividad física recomendada para pacientes con diabetes tipo 2.",
    category: "Diabetes",
    url: "/resources/diabetes-management.pdf",
    publishedAt: "2023-11-05T00:00:00",
    readTime: 15,
    isRecommended: true
  },
  {
    id: 2,
    title: "Monitoreo de la Presión Arterial en Casa",
    description: "Instrucciones detalladas sobre cómo medir correctamente la presión arterial en el hogar y llevar un registro para compartir con su médico.",
    category: "Hipertensión",
    url: "/resources/blood-pressure-monitoring.pdf",
    publishedAt: "2023-10-20T00:00:00",
    readTime: 10,
    isRecommended: true
  },
  {
    id: 3,
    title: "Ejercicios Seguros para Personas con Artritis",
    description: "Rutinas de ejercicios de bajo impacto diseñadas específicamente para personas con artritis, que ayudan a mantener la movilidad sin aumentar el dolor.",
    category: "Artritis",
    url: "/resources/arthritis-exercises.pdf",
    publishedAt: "2023-09-15T00:00:00",
    readTime: 20,
    isRecommended: false
  },
  {
    id: 4,
    title: "Plan Alimenticio para Pacientes con Hipertensión",
    description: "Dieta DASH y recomendaciones nutricionales para reducir la presión arterial naturalmente a través de una alimentación balanceada y baja en sodio.",
    category: "Hipertensión",
    url: "/resources/dash-diet.pdf",
    publishedAt: "2023-11-10T00:00:00",
    readTime: 25,
    isRecommended: false
  },
  {
    id: 5,
    title: "Control de Glucosa Post-Prandial",
    description: "Estrategias para gestionar los niveles de glucosa después de las comidas, incluyendo selección de alimentos y tiempo de medicación.",
    category: "Diabetes",
    url: "/resources/post-meal-glucose.pdf",
    publishedAt: "2023-11-28T00:00:00",
    readTime: 12,
    isRecommended: true
  },
  {
    id: 6,
    title: "Nutrición Adecuada para la Salud Ósea",
    description: "Alimentos ricos en calcio, vitamina D y otros nutrientes esenciales para fortalecer los huesos y prevenir fracturas en pacientes con osteoporosis.",
    category: "Osteoporosis",
    url: "/resources/bone-health-nutrition.pdf",
    publishedAt: "2023-10-05T00:00:00",
    readTime: 18,
    isRecommended: false
  },
  {
    id: 7,
    title: "Viviendo con EPOC: Guía para Pacientes",
    description: "Información completa sobre cómo manejar los síntomas de la EPOC, técnicas de respiración y consejos para adaptarse a las actividades diarias.",
    category: "Respiratoria",
    url: "/resources/living-with-copd.pdf",
    publishedAt: "2023-09-28T00:00:00",
    readTime: 30,
    isRecommended: true
  }
];
import { useState } from 'react';
import { Activity, AlertTriangle, Calendar, Clock, Heart, PanelRight, User } from 'lucide-react';
import { MOCK_PATIENTS, RISK_ALERTS, CONDITIONS } from '@/lib/constants';
import { Button } from '@/components/ui/button';
import { formatDateString } from '@/lib/utils';
import { Alert, Condition } from '@/lib/types';

export function PatientProfile() {
  const [activePatient] = useState(MOCK_PATIENTS[0]);
  
  // Simulamos una alerta crítica (riskLevel > 80)
  const alerts = RISK_ALERTS.filter(alert => alert.patientId === activePatient.id);
  const criticalAlert = alerts.find((a: Alert) => (a.riskLevel || 0) > 80);
  
  // Filtramos condiciones por paciente
  const conditions = CONDITIONS.filter(condition => 
    activePatient.conditions.some(c => c.id === condition.id)
  );

  return (
    <div className="bg-white rounded-lg shadow-sm">
      {/* Header con detalle del paciente */}
      <div className="p-6 border-b border-neutral-100">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="bg-neutral-100 rounded-full w-12 h-12 flex items-center justify-center text-neutral-600">
              <User className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-neutral-800">{activePatient.fullName}</h2>
              <div className="flex flex-wrap items-center gap-x-4 text-sm text-neutral-500">
                <span className="flex items-center">
                  <Calendar className="mr-1 h-4 w-4" />
                  {activePatient.age} años
                </span>
                <span className="flex items-center">
                  <Activity className="mr-1 h-4 w-4" />
                  {activePatient.status}
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" size="sm" className="text-neutral-600">
              <PanelRight className="mr-1 h-4 w-4" />
              Historial Completo
            </Button>
            <Button variant="outline" size="sm" className="text-neutral-600">
              <Clock className="mr-1 h-4 w-4" />
              Agendar Cita
            </Button>
          </div>
        </div>
      </div>
      
      {/* Alerta crítica si existe */}
      {criticalAlert && (
        <div className="mx-6 my-4 bg-red-50 border border-red-100 text-red-700 px-4 py-3 rounded-md flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-medium">Alerta crítica: {criticalAlert.title}</p>
            <p className="text-sm mt-1">{criticalAlert.description}</p>
            <div className="mt-2 flex gap-2">
              <Button size="sm" className="h-8 bg-red-600 hover:bg-red-700">Ver detalles</Button>
              <Button size="sm" variant="outline" className="h-8 text-red-700 border-red-200 hover:bg-red-50">
                Marcar como revisada
              </Button>
            </div>
          </div>
        </div>
      )}
      
      {/* Grid con condiciones y alertas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        {/* Condiciones médicas */}
        <div>
          <h3 className="font-medium text-neutral-800 mb-4 flex items-center">
            <Heart className="mr-2 h-5 w-5 text-primary" />
            Condiciones Médicas
          </h3>
          <div className="space-y-3">
            {conditions.length === 0 ? (
              <p className="text-neutral-500 text-sm">No hay condiciones registradas</p>
            ) : (
              conditions.map((condition: Condition) => (
                <div key={condition.id} className="bg-neutral-50 rounded-md p-4">
                  <div className="flex justify-between">
                    <div className="flex items-center">
                      <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-50 flex items-center justify-center mr-3">
                        <span className="text-primary text-lg">{condition.icon}</span>
                      </span>
                      <div>
                        <h4 className="font-medium text-neutral-800">{condition.name}</h4>
                        <p className="text-xs text-neutral-500">
                          Actualizado: {formatDateString(condition.lastUpdated)}
                        </p>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm" className="h-8 text-neutral-600">
                      Ver
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        {/* Alertas recientes */}
        <div>
          <h3 className="font-medium text-neutral-800 mb-4 flex items-center">
            <AlertTriangle className="mr-2 h-5 w-5 text-secondary" />
            Alertas Recientes
          </h3>
          <div className="space-y-3">
            {alerts.length === 0 ? (
              <p className="text-neutral-500 text-sm">No hay alertas recientes</p>
            ) : (
              alerts.map((alert: Alert) => (
                <div 
                  key={alert.id} 
                  className={`rounded-md p-4 ${
                    (alert.riskLevel || 0) > 80 ? 'bg-red-50 border border-red-100' : 
                    (alert.riskLevel || 0) > 50 ? 'bg-amber-50 border border-amber-100' : 
                    'bg-neutral-50'
                  }`}
                >
                  <div className="flex justify-between">
                    <div>
                      <div className="flex items-center">
                        <span 
                          className={`w-2 h-2 rounded-full mr-2 ${
                            (alert.riskLevel || 0) > 80 ? 'bg-red-500' : 
                            (alert.riskLevel || 0) > 50 ? 'bg-amber-500' : 
                            'bg-emerald-500'
                          }`}
                        />
                        <h4 className="font-medium text-neutral-800">{alert.title}</h4>
                      </div>
                      <p className="text-sm text-neutral-600 mt-1">{alert.description}</p>
                      <p className="text-xs text-neutral-500 mt-1">
                        {formatDateString(alert.timestamp)}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
import { useState } from 'react';
import { ChevronDown, AlertTriangle, BarChart, Activity } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { formatDateString } from '@/lib/utils';
import { RISK_ALERTS, MOCK_PATIENTS } from '@/lib/constants';
import { Alert } from '@/lib/types';

export function RiskMonitoring() {
  const [showAll, setShowAll] = useState(false);
  const activePatient = MOCK_PATIENTS[0];
  
  // Filtramos alertas para el paciente actual
  const patientAlerts = RISK_ALERTS.filter(
    alert => alert.patientId === activePatient.id
  ).sort((a, b) => (b.riskLevel || 0) - (a.riskLevel || 0));
  
  // Mostramos solo las 3 primeras alertas si showAll es false
  const displayedAlerts = showAll ? patientAlerts : patientAlerts.slice(0, 3);
  
  // Calculamos el riesgo promedio
  const averageRisk = patientAlerts.length > 0 
    ? Math.round(patientAlerts.reduce((sum, alert) => sum + (alert.riskLevel || 0), 0) / patientAlerts.length) 
    : 0;
  
  // Determinamos el color del indicador de riesgo según nivel
  const riskColor = averageRisk > 80 ? 'bg-red-500' : 
                   averageRisk > 50 ? 'bg-amber-500' : 
                   'bg-emerald-500';
  
  // Determinar el nivel de riesgo textual
  const riskText = averageRisk > 80 ? 'Alto' : 
                  averageRisk > 50 ? 'Moderado' : 
                  'Bajo';
  
  // Determinar el color de fondo según nivel
  const riskBgColor = averageRisk > 80 ? 'bg-red-50 text-red-700' : 
                     averageRisk > 50 ? 'bg-amber-50 text-amber-700' : 
                     'bg-emerald-50 text-emerald-700';

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-neutral-800 flex items-center">
          <AlertTriangle className="mr-2 h-5 w-5 text-secondary" />
          Monitoreo de Riesgos
        </h2>
        <div className="mt-2 md:mt-0 flex items-center gap-2 text-sm">
          <span className="text-neutral-500">Nivel de Riesgo:</span>
          <span className={`font-medium px-2 py-1 rounded ${riskBgColor}`}>
            {riskText} ({averageRisk}%)
          </span>
        </div>
      </div>
      
      {/* Gráfico de riesgo simplificado */}
      <div className="mb-6">
        <div className="h-4 bg-neutral-100 rounded-full overflow-hidden">
          <div 
            className={`h-full ${
              averageRisk > 80 ? 'bg-red-500' : 
              averageRisk > 50 ? 'bg-amber-500' : 
              'bg-emerald-500'
            }`} 
            style={{ width: `${averageRisk}%` }}
          ></div>
        </div>
        <div className="flex justify-between mt-1 text-xs text-neutral-500">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>
      
      {/* Indicadores de riesgo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-neutral-50 rounded-md p-4">
          <div className="flex items-center mb-1">
            <Activity className="h-4 w-4 text-neutral-500 mr-1" />
            <h4 className="font-medium text-neutral-700">Principales Factores</h4>
          </div>
          <div className="text-neutral-800 text-2xl font-semibold">
            {patientAlerts.length > 0 ? patientAlerts[0].title : 'Ninguno'}
          </div>
          <p className="text-xs text-neutral-500">Factor de mayor influencia</p>
        </div>
        
        <div className="bg-neutral-50 rounded-md p-4">
          <div className="flex items-center mb-1">
            <BarChart className="h-4 w-4 text-neutral-500 mr-1" />
            <h4 className="font-medium text-neutral-700">Tendencia</h4>
          </div>
          <div className="text-neutral-800 text-2xl font-semibold flex items-center">
            <span className={`w-3 h-3 rounded-full ${riskColor} mr-2`}></span>
            {averageRisk > 60 ? 'Ascendente' : 'Estable'}
          </div>
          <p className="text-xs text-neutral-500">Basado en últimas 24 horas</p>
        </div>
        
        <div className="bg-neutral-50 rounded-md p-4">
          <div className="flex items-center mb-1">
            <AlertTriangle className="h-4 w-4 text-neutral-500 mr-1" />
            <h4 className="font-medium text-neutral-700">Alertas Activas</h4>
          </div>
          <div className="text-neutral-800 text-2xl font-semibold">
            {patientAlerts.length}
          </div>
          <p className="text-xs text-neutral-500">Total de riesgos identificados</p>
        </div>
      </div>
      
      {/* Lista de alertas */}
      <div>
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-medium text-neutral-800">Alertas Recientes</h3>
          <Button 
            variant="ghost" 
            size="sm" 
            className="h-8 text-neutral-600 flex items-center"
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? 'Mostrar menos' : 'Ver todas'}
            <ChevronDown className={`ml-1 h-4 w-4 transition-transform ${showAll ? 'rotate-180' : ''}`} />
          </Button>
        </div>
        
        <div className="space-y-3">
          {displayedAlerts.length === 0 ? (
            <p className="text-neutral-500 text-sm">No hay alertas recientes</p>
          ) : (
            displayedAlerts.map((alert: Alert) => (
              <div 
                key={alert.id} 
                className={`rounded-md p-4 ${
                  (alert.riskLevel || 0) > 80 ? 'bg-red-50 border border-red-100' : 
                  (alert.riskLevel || 0) > 50 ? 'bg-amber-50 border border-amber-100' : 
                  'bg-neutral-50'
                }`}
              >
                <div className="flex justify-between items-start">
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
                  <div className={`px-2 py-1 rounded text-xs font-medium ${
                    (alert.riskLevel || 0) > 80 ? 'bg-red-100 text-red-700' : 
                    (alert.riskLevel || 0) > 50 ? 'bg-amber-100 text-amber-700' : 
                    'bg-emerald-100 text-emerald-700'
                  }`}>
                    {alert.riskLevel}%
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
        
        {!showAll && patientAlerts.length > 3 && (
          <Button 
            variant="ghost" 
            className="w-full mt-3 text-primary" 
            onClick={() => setShowAll(true)}
          >
            Ver todas las alertas ({patientAlerts.length})
          </Button>
        )}
      </div>
    </div>
  );
}
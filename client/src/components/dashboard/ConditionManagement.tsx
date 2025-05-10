import { useState } from 'react';
import { Activity, Calendar, MoreHorizontal, Plus, Search, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { CONDITIONS, MOCK_PATIENTS } from '@/lib/constants';
import { formatDateString } from '@/lib/utils';
import { Condition } from '@/lib/types';

export function ConditionManagement() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState<string | null>(null);
  const activePatient = MOCK_PATIENTS[0];
  
  // Filtramos condiciones por búsqueda y categoría
  const filteredConditions = CONDITIONS.filter(condition => {
    const matchesSearch = searchTerm.trim() === '' || 
      condition.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === null || condition.category === filter;
    // Solo mostrar condiciones del paciente activo
    const belongsToPatient = activePatient.conditions.some(c => c.id === condition.id);
    
    return matchesSearch && matchesFilter && belongsToPatient;
  });
  
  // Extraemos categorías únicas
  const categories = Array.from(new Set(CONDITIONS.map(c => c.category)));
  
  // Función para obtener color de severidad
  const getSeverityColor = (severity: number) => {
    if (severity >= 8) return 'bg-red-500';
    if (severity >= 5) return 'bg-amber-500';
    return 'bg-emerald-500';
  };
  
  // Función para obtener texto de severidad
  const getSeverityText = (severity: number) => {
    if (severity >= 8) return 'Alta';
    if (severity >= 5) return 'Media';
    return 'Baja';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-neutral-800">Gestión de Condiciones</h2>
        <div className="mt-3 md:mt-0">
          <Button className="bg-primary hover:bg-primary-600 text-white">
            <Plus className="mr-2 h-4 w-4" />
            Nueva Condición
          </Button>
        </div>
      </div>
      
      {/* Barra de búsqueda y filtros */}
      <div className="mb-6">
        <div className="relative mb-4">
          <Input 
            type="text" 
            placeholder="Buscar condiciones..." 
            className="pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <Search className="absolute left-3 top-2.5 h-5 w-5 text-neutral-400" />
          {searchTerm && (
            <button 
              className="absolute right-3 top-2.5 text-neutral-400 hover:text-neutral-600"
              onClick={() => setSearchTerm('')}
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
        
        {/* Filtros de categoría */}
        <div className="flex flex-wrap gap-2">
          <Button
            size="sm"
            variant={filter === null ? "default" : "outline"}
            className={`h-8 ${filter === null ? 'bg-primary text-white' : 'text-neutral-600'}`}
            onClick={() => setFilter(null)}
          >
            Todas
          </Button>
          
          {categories.map(category => (
            <Button
              key={category}
              size="sm"
              variant={filter === category ? "default" : "outline"}
              className={`h-8 ${filter === category ? 'bg-primary text-white' : 'text-neutral-600'}`}
              onClick={() => setFilter(category)}
            >
              {category}
            </Button>
          ))}
        </div>
      </div>
      
      {/* Lista de condiciones */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="text-left border-b border-neutral-200">
              <th className="pb-2 text-sm font-medium text-neutral-500">Condición</th>
              <th className="pb-2 text-sm font-medium text-neutral-500">Categoría</th>
              <th className="pb-2 text-sm font-medium text-neutral-500">Severidad</th>
              <th className="pb-2 text-sm font-medium text-neutral-500">Actualizado</th>
              <th className="pb-2 text-sm font-medium text-neutral-500">Estado</th>
              <th className="pb-2 text-sm font-medium text-neutral-500"></th>
            </tr>
          </thead>
          <tbody>
            {filteredConditions.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-4 text-center text-neutral-500">
                  No se encontraron condiciones que coincidan con la búsqueda
                </td>
              </tr>
            ) : (
              filteredConditions.map((condition: Condition) => (
                <tr key={condition.id} className="border-b border-neutral-100 hover:bg-neutral-50">
                  <td className="py-4">
                    <div className="flex items-center">
                      <span className="w-8 h-8 rounded-full bg-neutral-100 text-primary flex items-center justify-center mr-3 text-lg">
                        {condition.icon}
                      </span>
                      <span className="font-medium text-neutral-800">{condition.name}</span>
                    </div>
                  </td>
                  <td className="py-4">
                    <span className="text-sm text-neutral-600">{condition.category}</span>
                  </td>
                  <td className="py-4">
                    <div className="flex items-center">
                      <span 
                        className={`w-2 h-2 rounded-full mr-2 ${getSeverityColor(condition.severity)}`}
                      />
                      <span className="text-sm text-neutral-600">
                        {getSeverityText(condition.severity)}
                      </span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="flex items-center text-sm text-neutral-500">
                      <Calendar className="h-3 w-3 mr-1" />
                      {formatDateString(condition.lastUpdated)}
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="flex items-center">
                      <span 
                        className={`px-2 py-1 rounded text-xs font-medium ${
                          condition.status === 'Activo' ? 'bg-emerald-100 text-emerald-700' : 
                          condition.status === 'En tratamiento' ? 'bg-blue-100 text-blue-700' : 
                          'bg-neutral-100 text-neutral-700'
                        }`}
                      >
                        {condition.status}
                      </span>
                    </div>
                  </td>
                  <td className="py-4 text-right">
                    <Button variant="ghost" size="sm" className="h-8 p-0">
                      <MoreHorizontal className="h-4 w-4 text-neutral-500" />
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      
      {/* Información de tratamiento */}
      <div className="mt-6 pt-4 border-t border-neutral-100">
        <div className="flex flex-col md:flex-row md:items-center justify-between">
          <h3 className="font-medium text-neutral-800">Plan de Tratamiento Global</h3>
          <div className="flex items-center text-sm text-neutral-500 mt-2 md:mt-0">
            <Activity className="h-4 w-4 mr-1" />
            Adherencia al tratamiento: <span className="font-medium text-emerald-600 ml-1">87%</span>
          </div>
        </div>
        <p className="text-sm text-neutral-600 mt-2">
          El paciente presenta múltiples condiciones que requieren un enfoque coordinado. 
          Se recomienda seguimiento semanal para ajustar medicación y verificar progreso.
        </p>
      </div>
    </div>
  );
}
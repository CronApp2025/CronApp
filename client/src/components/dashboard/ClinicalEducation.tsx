import { Book, Bookmark, BookOpen, ChevronRight, ExternalLink } from 'lucide-react';
import { EDUCATIONAL_RESOURCES } from '@/lib/constants';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { formatDateString } from '@/lib/utils';
import { EducationalResource } from '@/lib/types';

export function ClinicalEducation() {
  const [filter, setFilter] = useState<string | null>(null);
  
  // Recursos filtrados por categoría si hay filtro, o todos si no hay
  const filteredResources = filter 
    ? EDUCATIONAL_RESOURCES.filter(resource => resource.category === filter)
    : EDUCATIONAL_RESOURCES;
  
  // Extraemos categorías únicas para los filtros
  const categories = Array.from(new Set(EDUCATIONAL_RESOURCES.map(r => r.category)));
  
  // Función para renderizar el ícono según categoría
  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'diabetes':
        return <Book className="h-4 w-4 text-red-500" />;
      case 'hipertensión':
        return <Book className="h-4 w-4 text-blue-500" />;
      case 'nutrición':
        return <Book className="h-4 w-4 text-green-500" />;
      default:
        return <Book className="h-4 w-4 text-neutral-500" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-neutral-800 flex items-center">
          <BookOpen className="mr-2 h-5 w-5 text-accent" />
          Educación Clínica
        </h2>
        <div className="mt-3 md:mt-0">
          <Button variant="outline" size="sm" className="text-neutral-600">
            Recomendar Material
          </Button>
        </div>
      </div>
      
      {/* Filtros de categoría */}
      <div className="flex flex-wrap gap-2 mb-4">
        <Button
          size="sm"
          variant={filter === null ? "default" : "outline"}
          className={`h-8 ${filter === null ? 'bg-primary text-white' : 'text-neutral-600'}`}
          onClick={() => setFilter(null)}
        >
          Todos
        </Button>
        
        {categories.map(category => (
          <Button
            key={category}
            size="sm"
            variant={filter === category ? "default" : "outline"}
            className={`h-8 ${filter === category ? 'bg-primary text-white' : 'text-neutral-600'}`}
            onClick={() => setFilter(category)}
          >
            {getCategoryIcon(category)}
            <span className="ml-1">{category}</span>
          </Button>
        ))}
      </div>
      
      {/* Lista de recursos */}
      <div className="space-y-4">
        {filteredResources.length === 0 ? (
          <p className="text-neutral-500 text-sm">No hay recursos disponibles para la categoría seleccionada</p>
        ) : (
          filteredResources.map((resource: EducationalResource) => (
            <div key={resource.id} className="border border-neutral-100 rounded-md p-4 hover:bg-neutral-50 transition-colors">
              <div className="flex justify-between">
                <div>
                  <div className="flex items-center">
                    {getCategoryIcon(resource.category)}
                    <span className="text-xs text-neutral-500 ml-1">{resource.category}</span>
                  </div>
                  <h3 className="font-medium text-neutral-800 mt-1">{resource.title}</h3>
                  <p className="text-sm text-neutral-600 mt-1 line-clamp-2">{resource.description}</p>
                  <div className="flex items-center mt-2 text-xs text-neutral-500">
                    <span>Publicado: {formatDateString(resource.publishedAt)}</span>
                    <span className="mx-2">•</span>
                    <span>{resource.readTime} min de lectura</span>
                  </div>
                </div>
                <div className="flex flex-col items-end justify-between">
                  <Button variant="ghost" size="sm" className="h-8 text-neutral-600 p-0 hover:bg-transparent">
                    <Bookmark className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="h-8 text-primary">
                    <span>Ver</span>
                    <ChevronRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      
      {/* Enlaces de formación adicional */}
      <div className="mt-6 pt-4 border-t border-neutral-100">
        <h3 className="font-medium text-neutral-800 mb-2">Recursos Adicionales</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <a href="#" className="text-sm text-primary flex items-center hover:underline">
            <ExternalLink className="h-3 w-3 mr-1" />
            Portal de Formación Médica Continua
          </a>
          <a href="#" className="text-sm text-primary flex items-center hover:underline">
            <ExternalLink className="h-3 w-3 mr-1" />
            Biblioteca Digital de Investigación Clínica
          </a>
          <a href="#" className="text-sm text-primary flex items-center hover:underline">
            <ExternalLink className="h-3 w-3 mr-1" />
            Directrices Actualizadas de Tratamiento
          </a>
          <a href="#" className="text-sm text-primary flex items-center hover:underline">
            <ExternalLink className="h-3 w-3 mr-1" />
            Webinarios y Formación en Línea
          </a>
        </div>
      </div>
    </div>
  );
}
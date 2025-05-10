import { useState } from "react";
import { Save, User, Bell, Globe, Lock, Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/hooks/use-auth";
import { useSettings } from "@/hooks/use-settings";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { getInitials } from "@/lib/utils";

export function SettingsFormNew() {
  const { user, updateUserInfo } = useAuth();
  const { settings, updateSettings, isLoading } = useSettings();
  
  const [formData, setFormData] = useState({
    nombre: user?.nombre || "",
    email: user?.email || "",
    especialidad: user?.especialidad || "",
    notificaciones: settings?.notificaciones || true,
    idioma: settings?.idioma || "es",
    temaOscuro: settings?.temaOscuro || false
  });
  
  const [saving, setSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    // Manejo especial para checkboxes
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMessage("");
    
    try {
      // Separamos datos del usuario y configuraciones
      const userData = {
        nombre: formData.nombre,
        email: formData.email,
        especialidad: formData.especialidad
      };
      
      const settingsData = {
        notificaciones: formData.notificaciones,
        idioma: formData.idioma,
        temaOscuro: formData.temaOscuro
      };
      
      // Simulamos un retardo para mostrar el estado de guardado
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Actualizamos los datos del usuario
      updateUserInfo(userData);
      
      // Actualizamos las configuraciones
      if (updateSettings) {
        updateSettings(settingsData);
      }
      
      setSuccessMessage("Configuración guardada correctamente");
    } catch (error) {
      console.error("Error al guardar configuración:", error);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold text-neutral-800 mb-6">Configuración de la Cuenta</h2>
      
      <form onSubmit={handleSubmit}>
        {/* Perfil */}
        <div className="mb-8">
          <h3 className="text-md font-medium text-neutral-800 mb-4 flex items-center">
            <User className="mr-2 h-5 w-5 text-neutral-500" />
            Perfil Personal
          </h3>
          
          <div className="flex flex-col md:flex-row gap-6 items-start">
            <div className="flex-shrink-0">
              <Avatar className="w-24 h-24 bg-primary text-white text-xl">
                <AvatarFallback>
                  {getInitials(formData.nombre)}
                </AvatarFallback>
              </Avatar>
            </div>
            
            <div className="grid gap-4 flex-1">
              <div className="grid gap-2">
                <label htmlFor="nombre" className="text-sm font-medium text-neutral-700">
                  Nombre completo
                </label>
                <Input
                  id="nombre"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>
              
              <div className="grid gap-2">
                <label htmlFor="email" className="text-sm font-medium text-neutral-700">
                  Correo electrónico
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>
              
              <div className="grid gap-2">
                <label htmlFor="especialidad" className="text-sm font-medium text-neutral-700">
                  Especialidad
                </label>
                <Input
                  id="especialidad"
                  name="especialidad"
                  value={formData.especialidad}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>
            </div>
          </div>
        </div>
        
        {/* Notificaciones */}
        <div className="mb-8 border-t border-neutral-100 pt-6">
          <h3 className="text-md font-medium text-neutral-800 mb-4 flex items-center">
            <Bell className="mr-2 h-5 w-5 text-neutral-500" />
            Notificaciones
          </h3>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-neutral-800">Notificaciones por correo</p>
              <p className="text-sm text-neutral-500">Recibir notificaciones sobre actualizaciones y alertas de pacientes</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer" 
                name="notificaciones"
                checked={formData.notificaciones}
                onChange={handleChange}
              />
              <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
            </label>
          </div>
        </div>
        
        {/* Idioma */}
        <div className="mb-8 border-t border-neutral-100 pt-6">
          <h3 className="text-md font-medium text-neutral-800 mb-4 flex items-center">
            <Globe className="mr-2 h-5 w-5 text-neutral-500" />
            Idioma y Apariencia
          </h3>
          
          <div className="grid gap-4">
            <div className="grid gap-2">
              <label htmlFor="idioma" className="text-sm font-medium text-neutral-700">
                Idioma de la interfaz
              </label>
              <select
                id="idioma"
                name="idioma"
                value={formData.idioma}
                onChange={handleChange}
                className="rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="es">Español</option>
                <option value="en">Inglés</option>
              </select>
            </div>
            
            <div className="flex items-center justify-between mt-2">
              <div>
                <p className="font-medium text-neutral-800">Tema oscuro</p>
                <p className="text-sm text-neutral-500">Cambiar a tema oscuro para reducir el brillo</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  className="sr-only peer" 
                  name="temaOscuro"
                  checked={formData.temaOscuro}
                  onChange={handleChange}
                />
                <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          </div>
        </div>
        
        {/* Seguridad */}
        <div className="mb-8 border-t border-neutral-100 pt-6">
          <h3 className="text-md font-medium text-neutral-800 mb-4 flex items-center">
            <Lock className="mr-2 h-5 w-5 text-neutral-500" />
            Seguridad
          </h3>
          
          <div className="flex flex-col md:flex-row md:items-center justify-between">
            <div>
              <p className="font-medium text-neutral-800">Cambiar contraseña</p>
              <p className="text-sm text-neutral-500">Actualiza tu contraseña regularmente para mayor seguridad</p>
            </div>
            <Button 
              type="button" 
              variant="outline" 
              className="mt-2 md:mt-0"
              onClick={() => window.location.href = '/forgot-password'}
            >
              Cambiar contraseña
            </Button>
          </div>
        </div>
        
        {/* Botones de acción */}
        <div className="border-t border-neutral-100 pt-6 flex flex-col md:flex-row md:items-center justify-between">
          {successMessage && (
            <div className="bg-emerald-50 text-emerald-700 px-4 py-2 rounded-md mb-4 md:mb-0">
              {successMessage}
            </div>
          )}
          
          <div className="flex space-x-2 ml-auto">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => window.location.reload()}
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              disabled={saving || isLoading}
            >
              {saving ? 'Guardando...' : 'Guardar cambios'}
              {!saving && <Save className="ml-2 h-4 w-4" />}
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'waterVolume', // Este será el nombre que usaremos en el HTML
  standalone: true     // Lo hacemos autónomo para importarlo quirúrgicamente
})
export class WaterVolumePipe implements PipeTransform {
  
  // El método transform es el "Execute" del Pipe. 
  // Toma el valor de entrada y retorna el string formateado.
  transform(value: number | null | undefined): string {
    if (value === null || value === undefined) {
      return '0 ml';
    }

    if (value < 20) {
      return `${value} ml`;
    }

    // Convertimos a Litros si supera o iguala los 1000 ml
    const litros = value / 1000;
    // Formateamos a máximo 2 decimales, removiendo ceros sobrantes
    return `${parseFloat(litros.toFixed(2))} L`;
  }
}
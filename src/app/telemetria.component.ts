import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { WaterVolumePipe } from './pipes/water-volume.pipe';

@Component({
  selector: 'app-telemetria',
  standalone: true,
  imports: [WaterVolumePipe],
  template: `
    <div
      style="background-color: #2b579a; color: white; padding: 15px; border-radius: 6px; margin-bottom: 20px;"
    >
      <h4 style="margin: 0 0 5px 0;">📡 Telemetría de Sensores en Vivo (Componente Hijo)</h4>
      <p style="margin: 0; font-size: 18px;">
        Flujo de Agua Dispensa: <strong>{{ flujoAguaActual() | waterVolume }} /s</strong>
      </p>
    </div>
  `,
})
export class TelemetriaComponent implements OnInit, OnDestroy {
  private telemetriaIntervalId: any;
  public flujoAguaActual = signal<number>(0);

  ngOnInit(): void {
    console.log('👶 [Hijo] TelemetriaComponent Inicializado (ngOnInit)');

    this.telemetriaIntervalId = setInterval(() => {
      const nuevoFlujo = Math.floor(Math.random() * 100);
      this.flujoAguaActual.set(nuevoFlujo);
      console.log(`📡 [Hijo] Ejecutando intervalo... Flujo: ${nuevoFlujo} ml/s`);
    }, 1000);
  }

  ngOnDestroy(): void {
    console.log('💥 [Hijo] Componente TelemetriaComponent DESTRUIDO. Ejecutando Dispose...');

    if (this.telemetriaIntervalId) {
      clearInterval(this.telemetriaIntervalId);
      console.log(
        '🛑 [Hijo] Intervalo de telemetría detenido con éxito. ¡Fuga de memoria evitada!',
      );
    }
  }
}

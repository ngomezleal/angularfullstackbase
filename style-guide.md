# Guía de Estilos del Proyecto (Reglas para el Agente)

## Ecosistema y Dependencias
1. **Framework de Estilos Obligatorio:** Todo el diseño de la aplicación debe estar basado en **Bootstrap 5**.
2. **Verificación de Dependencias:** El agente debe asegurarse de que `bootstrap` esté instalado en el `package.json` y configurado correctamente en los estilos globales del proyecto (`angular.json` o `styles.css`) antes de proponer cambios visuales.

## Reglas de Codificación
1. **Prohibición de Estilos en Línea:** Queda terminantemente prohibido el uso del atributo `style="..."` en las etiquetas HTML.
2. **Diseño Responsivo:** Se deben priorizar las clases utilitarias de Bootstrap para garantizar que la interfaz sea adaptable (responsive).
3. **Preservación de Lógica:** No se debe alterar ninguna propiedad, binding de Angular (`[]`, `()`, `*ngIf`, `*ngFor`) ni la lógica en los archivos TypeScript (`.ts`).
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Product, ProductService } from './services/product-service';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { TelemetriaComponent } from './telemetria.component';
import { DemoEstilos } from './componentes/demo-estilos/demo-estilos';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ReactiveFormsModule, TelemetriaComponent, DemoEstilos],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  title: string = 'Panel de Control de Angular Servicio';
  private productService = inject(ProductService);
  public productsList = signal<Product[]>([]);
  public isLoading = signal<boolean>(false);
  public productForm = new FormGroup({
    name: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.minLength(3)],
    }),
    price: new FormControl(null, {
      validators: [Validators.required, Validators.min(1)],
    }),
  });

  public mostrarSensor = signal<boolean>(true);

  ngOnInit(): void {
    console.log(' ngOnInit ejecutado');
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.productsList.set(products);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error fetching products:', error);
        this.isLoading.set(false);
      },
    });
  }

  public onSubmit(): void {
    // Equivalente a: if (!ModelState.IsValid) return;
    if (this.productForm.invalid) {
      this.productForm.markAllAsTouched(); // Fuerza a que se muestren los errores en pantalla
      return;
    }

    // Extraemos los valores de forma segura y fuertemente tipada
    const rawValues = this.productForm.getRawValue();

    const newProduct = {
      name: rawValues.name,
      price: rawValues.price ?? 0,
    };

    this.productService.createProduct(newProduct).subscribe({
      next: (createdProduct) => {
        // Actualizamos nuestra Signal local agregando el nuevo producto al inicio de la lista
        this.productsList.update((currentProducts) => [createdProduct, ...currentProducts]);
        // Reseteamos el formulario de forma limpia
        this.productForm.reset();
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error creating product:', error);
        this.isLoading.set(false);
      },
    });
  }

  public onDelete(productId: number): void {
    this.isLoading.set(true);
    this.productService.deleteProduct(productId).subscribe({
      next: () => {
        this.productsList.update((currentProducts) =>
          currentProducts.filter((product) => product.id !== productId),
        );
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error deleting product:', error);
        this.isLoading.set(false);
      },
    });
  }

  public onUpdate(product: Product): void {
    this.isLoading.set(true);

    const updatedPayload: Product = {
      ...product,
      name: `${product.name} (Actualizado)`,
    };

    this.productService.updateProduct(updatedPayload).subscribe({
      next: (updatedProduct) => {
        this.productsList.update((currentProducts) =>
          currentProducts.map((p) => (p.id === updatedProduct.id ? updatedProduct : p)),
        );
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error updating product:', error);
        this.isLoading.set(false);
      },
    });
  }

  public onIncreasePrice(product: Product): void {
    this.isLoading.set(true);

    const updatedPayload: Product = {
      ...product,
      price: product.price + 10,
    };

    this.productService.updateProduct(updatedPayload).subscribe({
      next: (response) => {
        // Inmutabilidad pura: Mapeamos la lista y reemplazamos únicamente el producto editado
        this.productsList.update((currentProducts) =>
          currentProducts.map((p) => (p.id === response.id ? response : p)),
        );
        this.isLoading.set(false);
      },
      error: () => {
        alert('No se pudo actualizar el precio en el servidor.');
        this.isLoading.set(false);
      },
    });
  }

  // 1. COMPUTED: Cuenta cuántos productos hay en total
  public totalDispensadores = computed(() => {
    console.log('📊 [Computed] Recalculando cantidad total...');
    return this.productsList().length;
  });

  // 2. COMPUTED: Suma el valor de todo el inventario
  public valorTotalInventario = computed(() => {
    console.log('💰 [Computed] Recalculando valor financiero total...');
    return this.productsList().reduce((acc, product) => acc + product.price, 0);
  });
}

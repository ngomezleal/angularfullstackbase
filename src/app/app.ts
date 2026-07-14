import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Product, ProductService } from './services/product-service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  title: string = 'Panel de Control de Angular Servicio';
  private productService = inject(ProductService);
  public productsList = signal<Product[]>([]);
  public isLoading = signal<boolean>(false);

  ngOnInit(): void {
    console.log(' ngOnInit ejecutado');
    this.productService.fetchProductsFromApi().subscribe({
      next: (products) => {
        this.productsList.set(products);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Error fetching products:', error);
        this.isLoading.set(false);
      }
    });
  }
}

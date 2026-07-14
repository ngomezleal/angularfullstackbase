import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  price: number;
  imageUrl?: string;
}

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private http = inject(HttpClient);
  private apiUrl = 'https://jsonplaceholder.typicode.com/users';

  constructor() {}

  public getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl).pipe(
      map((response) => {
        return response.map((user) => ({
          id: user.id,
          name: `Dispensador Mod ${user.name}`,
          price: Math.floor(user.id * 35.5),
        }) as Product);
      }),
      catchError((error) => {
        console.error('Error fetching products:', error);
        return of([]);
      })
    )
  }

  public createProduct(product: Omit<Product, 'id'>): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, product).pipe(
      map((response) => {
        return {
          ...response,
          name: `Dispensador Mod ${response.name}`,
        };
      }),
      catchError((error) => {
        console.error('Error creating product:', error);
        throw error;
      })
    );
  }

  public updateProduct(product: Product): Observable<Product> {
    return this.http.put<Product>(`${this.apiUrl}/${product.id}`, product).pipe(
      catchError((error) => {
        console.error('Error updating product: ${product.id}', error);
        throw error;
      })
    );
  }

  public deleteProduct(productId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${productId}`).pipe(
      catchError((error) => {
        console.error('Error deleting product: ${productId}', error);
        throw error;
      })
    );
  }

  // public fetchProductsFromApi(): void {
  //   this.loadingState.set(true);

  //   this.http.get<Product[]>(this.apiUrl).subscribe({
  //     next: (response) => {
  //       const mappedProducts = response.map((user) => ({
  //         id: user.id,
  //         name: `Dispensador Mod ${user.name}`,
  //         price: Math.floor(user.id * 35.5)
  //       }) as Product);

  //       this.productsState.set(mappedProducts);
  //       this.loadingState.set(false);
  //     }, error: (error) => {
  //       console.error('Error fetching products:', error);
  //       this.loadingState.set(false);
  //     }
  //   });
  // }
}

import { inject, Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  price: number;
  imageUrl: string;
}

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private http = inject(HttpClient);
  private apiUrl = 'https://jsonplaceholder.typicode.com/users';

  constructor() {}

  public fetchProductsFromApi(): Observable<Product[]> {
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
